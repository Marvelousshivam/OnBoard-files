# OnBOARD CBSE 2027 Official Curriculum Library

Extensible, future-proof repository of Class 12 CBSE curriculum assets for **OnBOARD**, organized by **Subject → Chapter**.

---

## Directory Structure

```
OnBoard-files/
├── manifest.json                 # Auto-generated master curriculum manifest for the app
├── generate_manifest.py          # Script to scan and generate manifest.json
├── .github/workflows/            # GitHub Action to auto-regenerate manifest.json on push
├── english/
│   ├── 01_the_last_lesson/
│   │   ├── chapter.json          # Chapter info and YouTube video lecture links
│   │   ├── ncert/                # Official NCERT PDF
│   │   ├── notes/                # Handwritten and revision notes PDFs
│   │   ├── dpp/                  # Printable daily practice problem PDFs
│   │   └── quizzes/              # Interactive MCQ quiz JSON files
│   ├── 02_lost_spring/
│   │   └── ...
│   └── writing_section/
│       └── notes/                # Formats, notices, letters, articles & reports
├── physics/
│   ├── 01_electric_charges_and_fields/
│   └── ... (01 to 14)
├── chemistry/
│   ├── 01_solutions/
│   └── ... (01 to 10)
├── maths/
│   ├── 01_relations_and_functions/
│   └── ... (01 to 13)
├── biology/
│   ├── 01_sexual_reproduction_in_flowering_plants/
│   └── ... (01 to 13)
└── physical_education/
    ├── 01_management_of_sporting_events/
    └── ... (01 to 10)
```

---

## How to Add Content in the Future

### 1. Adding Revision Notes
Drop any PDF into the chapter's `notes/` directory (e.g. `english/01_the_last_lesson/notes/topper_notes.pdf`). It will automatically appear in the app under **NCERT & Notes → Chapter Revision Notes**.

### 2. Adding DPP Practice Sheets
Drop any PDF into the chapter's `dpp/` directory (e.g. `english/01_the_last_lesson/dpp/dpp_02.pdf`). It will automatically appear in the app under **DPP & Quizzes**.

### 3. Adding Interactive Quizzes
Drop a quiz `.json` file into the chapter's `quizzes/` directory (e.g. `english/01_the_last_lesson/quizzes/exam_prep_quiz.json`). The app will dynamically load it into the timed test engine.

### 4. Adding or Updating Video Lectures
Open `chapter.json` in the chapter folder and add or modify items under `"videos"`:
```json
{
  "videos": [
    {
      "id": "eng_ch01_1",
      "title": "The Last Lesson — Line-by-Line Explanation",
      "youtube_url": "https://www.youtube.com/watch?v=G9EEwMHSo7Y",
      "duration": "19 mins",
      "author": "Dear Sir"
    }
  ]
}
```

### 5. Regenerating the Manifest
- **Automatic**: When pushing to GitHub, GitHub Actions runs `generate_manifest.py` and auto-updates `manifest.json`.
- **Manual**: Run `python generate_manifest.py` locally before committing.
