import os
import json
from datetime import datetime, timezone

REPO_ROOT = os.path.abspath(os.path.dirname(__file__))
RAW_BASE_URL = "https://raw.githubusercontent.com/Marvelousshivam/OnBoard-files/main"

SUBJECT_METADATA = {
    "english": {
        "name": "English Core",
        "code": "301",
        "stream": "General",
        "total_theory_marks": 80,
        "total_practical_marks": 20,
        "icon_name": "menu_book"
    },
    "physics": {
        "name": "Physics",
        "code": "042",
        "stream": "Science",
        "total_theory_marks": 70,
        "total_practical_marks": 30,
        "icon_name": "bolt"
    },
    "chemistry": {
        "name": "Chemistry",
        "code": "043",
        "stream": "Science",
        "total_theory_marks": 70,
        "total_practical_marks": 30,
        "icon_name": "science"
    },
    "maths": {
        "name": "Mathematics",
        "code": "041",
        "stream": "PCM",
        "total_theory_marks": 80,
        "total_practical_marks": 20,
        "icon_name": "functions"
    },
    "biology": {
        "name": "Biology",
        "code": "044",
        "stream": "PCB",
        "total_theory_marks": 70,
        "total_practical_marks": 30,
        "icon_name": "biotech"
    },
    "physical_education": {
        "name": "Physical Education",
        "code": "048",
        "stream": "General",
        "total_theory_marks": 70,
        "total_practical_marks": 30,
        "icon_name": "fitness_center"
    }
}

def clean_title(filename):
    name = os.path.splitext(filename)[0]
    name = name.replace("_", " ").replace("-", " ")
    parts = name.split()
    capitalized = " ".join([p.capitalize() for p in parts])
    return capitalized

def generate():
    manifest = {
        "version": 2,
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "base_raw_url": RAW_BASE_URL,
        "subjects": []
    }

    # Discover subjects
    for sub_id in ["english", "physics", "chemistry", "maths", "biology", "physical_education"]:
        sub_dir = os.path.join(REPO_ROOT, sub_id)
        if not os.path.isdir(sub_dir):
            continue

        meta = SUBJECT_METADATA.get(sub_id, {
            "name": sub_id.capitalize(),
            "code": "000",
            "stream": "General",
            "total_theory_marks": 70,
            "total_practical_marks": 30,
            "icon_name": "menu_book"
        })

        subject_obj = {
            "id": sub_id,
            "name": meta["name"],
            "code": meta["code"],
            "stream": meta["stream"],
            "total_theory_marks": meta["total_theory_marks"],
            "total_practical_marks": meta["total_practical_marks"],
            "icon_name": meta["icon_name"],
            "chapters": []
        }

        # Scan chapter folders inside subject
        chapter_folders = sorted([d for d in os.listdir(sub_dir) if os.path.isdir(os.path.join(sub_dir, d)) and d != "writing_section"])

        for ch_folder in chapter_folders:
            ch_dir = os.path.join(sub_dir, ch_folder)
            
            # Read chapter.json if present
            chapter_meta = {}
            ch_meta_file = os.path.join(ch_dir, "chapter.json")
            if os.path.exists(ch_meta_file):
                try:
                    with open(ch_meta_file, "r", encoding="utf-8") as f:
                        chapter_meta = json.load(f)
                except Exception as e:
                    print(f"Error reading {ch_meta_file}: {e}")

            # Defaults
            ch_number = 1
            if "_" in ch_folder and ch_folder.split("_")[0].isdigit():
                ch_number = int(ch_folder.split("_")[0])
            
            ch_name = chapter_meta.get("name", clean_title(ch_folder.split("_", 1)[-1] if "_" in ch_folder else ch_folder))
            ch_id = chapter_meta.get("id", f"{sub_id}_{ch_folder}")
            weightage = chapter_meta.get("weightage_marks", 5)
            key_topics = chapter_meta.get("key_topics", [])
            videos = chapter_meta.get("videos", [])

            # NCERT PDFs
            ncert_dir = os.path.join(ch_dir, "ncert")
            ncert_url = ""
            if os.path.isdir(ncert_dir):
                ncert_files = [f for f in os.listdir(ncert_dir) if f.lower().endswith(".pdf")]
                if ncert_files:
                    ncert_url = f"{RAW_BASE_URL}/{sub_id}/{ch_folder}/ncert/{ncert_files[0]}"

            # Notes PDFs
            notes_list = []
            notes_dir = os.path.join(ch_dir, "notes")
            if os.path.isdir(notes_dir):
                for f in sorted(os.listdir(notes_dir)):
                    if f.lower().endswith(".pdf"):
                        notes_list.append({
                            "title": clean_title(f),
                            "filename": f,
                            "url": f"{RAW_BASE_URL}/{sub_id}/{ch_folder}/notes/{f}"
                        })

            # DPP PDFs
            dpp_list = []
            dpp_dir = os.path.join(ch_dir, "dpp")
            if os.path.isdir(dpp_dir):
                for f in sorted(os.listdir(dpp_dir)):
                    if f.lower().endswith(".pdf"):
                        dpp_list.append({
                            "title": clean_title(f),
                            "filename": f,
                            "url": f"{RAW_BASE_URL}/{sub_id}/{ch_folder}/dpp/{f}"
                        })

            # Quizzes JSON
            quizzes_list = []
            quizzes_dir = os.path.join(ch_dir, "quizzes")
            if os.path.isdir(quizzes_dir):
                for f in sorted(os.listdir(quizzes_dir)):
                    if f.lower().endswith(".json"):
                        quiz_path = os.path.join(quizzes_dir, f)
                        q_title = clean_title(f)
                        total_q = 10
                        try:
                            with open(quiz_path, "r", encoding="utf-8") as qf:
                                q_data = json.load(qf)
                                if "title" in q_data and q_data["title"]:
                                    q_title = q_data["title"]
                                if "total_questions" in q_data and q_data["total_questions"] > 0:
                                    total_q = q_data["total_questions"]
                                elif "questions" in q_data:
                                    total_q = len(q_data["questions"])
                        except Exception:
                            pass
                            
                        quizzes_list.append({
                            "id": os.path.splitext(f)[0],
                            "title": q_title,
                            "filename": f,
                            "url": f"{RAW_BASE_URL}/{sub_id}/{ch_folder}/quizzes/{f}",
                            "total_questions": total_q
                        })

            chapter_obj = {
                "id": ch_id,
                "subject_id": sub_id,
                "number": ch_number,
                "name": ch_name,
                "folder": f"{sub_id}/{ch_folder}",
                "weightage_marks": weightage,
                "key_topics": key_topics,
                "ncert_pdf_url": ncert_url,
                "notes": notes_list,
                "dpps": dpp_list,
                "quizzes": quizzes_list,
                "videos": videos
            }
            subject_obj["chapters"].append(chapter_obj)

        # English special writing section
        if sub_id == "english":
            writing_notes = []
            writing_dir = os.path.join(sub_dir, "writing_section", "notes")
            if os.path.isdir(writing_dir):
                for f in sorted(os.listdir(writing_dir)):
                    if f.lower().endswith(".pdf"):
                        writing_notes.append({
                            "title": clean_title(f),
                            "filename": f,
                            "url": f"{RAW_BASE_URL}/english/writing_section/notes/{f}"
                        })
            subject_obj["writing_section_notes"] = writing_notes

        manifest["subjects"].append(subject_obj)

    # Write manifest.json
    out_path = os.path.join(REPO_ROOT, "manifest.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    total_chapters = sum(len(s["chapters"]) for s in manifest["subjects"])
    total_notes = sum(sum(len(c["notes"]) for c in s["chapters"]) for s in manifest["subjects"])
    total_dpps = sum(sum(len(c["dpps"]) for c in s["chapters"]) for s in manifest["subjects"])
    total_quizzes = sum(sum(len(c["quizzes"]) for c in s["chapters"]) for s in manifest["subjects"])
    total_videos = sum(sum(len(c["videos"]) for c in s["chapters"]) for s in manifest["subjects"])

    print(f"Generated manifest.json successfully!")
    print(f"  Subjects: {len(manifest['subjects'])}")
    print(f"  Chapters: {total_chapters}")
    print(f"  Notes PDFs: {total_notes}")
    print(f"  DPP PDFs: {total_dpps}")
    print(f"  Quizzes JSONs: {total_quizzes}")
    print(f"  Videos: {total_videos}")

if __name__ == "__main__":
    generate()
