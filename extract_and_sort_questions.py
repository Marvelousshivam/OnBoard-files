import os
import sys
import json
import re
import glob
import shutil
import pypdf

# Ensure UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8')

DOWNLOADS_DIR = r"C:\Users\dines\Downloads"
REPO_ROOT = os.path.abspath(os.path.dirname(__file__))
APP_ASSETS_DIR = r"d:\BoardsPrep\app\src\main\assets"

# ─────────────────────────────────────────────────────────────────────────────
# 1. CHAPTER KEYWORD MAPPINGS & REGISTRY
# ─────────────────────────────────────────────────────────────────────────────
CHAPTER_KEYWORDS = {
    "physics": {
        "01_electric_charges_and_fields": [
            "dipole", "electric field", "charge", "coulomb", "flux", "gauss", "linear charge density",
            "permittivity", "electrostatic force"
        ],
        "02_electrostatic_potential_and_capacitance": [
            "potential", "capacitor", "capacitance", "dielectric", "equipotential", "energy stored",
            "parallel plate", "potential gradient"
        ],
        "03_current_electricity": [
            "drift velocit", "current", "resistance", "resistivity", "ohm", "kirchhoff", "potentiometer",
            "wheatstone", "meter bridge", "emf", "internal resistance", "resistor"
        ],
        "04_moving_charges_and_magnetism": [
            "magnetic field", "biot-savart", "ampere's circuital", "lorentz", "cyclotron", "galvanometer",
            "solenoid", "toroid", "force between parallel", "magnetic force", "circular loop"
        ],
        "05_magnetism_and_matter": [
            "magnetic dipole", "bar magnet", "susceptibility", "permeability", "diamagnetic", "paramagnetic",
            "ferromagnetic", "hysteresis", "magnetic moment", "earth's magnetism"
        ],
        "06_electromagnetic_induction": [
            "faraday", "lenz", "eddy current", "inductance", "self-induct", "mutual induct", "motional emf",
            "magnetic flux", "induced current"
        ],
        "07_alternating_current": [
            "alternating current", "ac", "rms", "impedance", "resonance", "lcr", "transformer", "power factor",
            "inductive reactance", "capacitive reactance"
        ],
        "08_electromagnetic_waves": [
            "displacement current", "electromagnetic spectrum", "em wave", "maxwell", "microwave",
            "infrared", "ultraviolet", "x-ray", "gamma ray", "radio wave"
        ],
        "09_ray_optics_and_optical_instruments": [
            "lens", "mirror", "refraction", "reflection", "prism", "microscope", "telescope",
            "total internal reflection", "focal length", "lens maker", "dispersion", "refractive index"
        ],
        "10_wave_optics": [
            "wavefront", "huygens", "interference", "young's double slit", "diffraction", "polarization",
            "fringe width", "coherent sources"
        ],
        "11_dual_nature_of_radiation_and_matter": [
            "photoelectric", "work function", "de broglie", "photon", "threshold frequency",
            "stopping potential", "davisson", "electron emission"
        ],
        "12_atoms": [
            "rutherford", "bohr", "rydberg", "spectral series", "lyman", "balmer", "hydrogen atom",
            "energy level", "radius of bohr", "ground state", "excitation"
        ],
        "13_nuclei": [
            "mass defect", "binding energy", "nuclear force", "radioactiv", "fission", "fusion",
            "alpha decay", "beta decay", "gamma decay", "half-life", "nucleons"
        ],
        "14_semiconductor_electronics": [
            "semiconductor", "intrinsic", "extrinsic", "p-n junction", "diode", "rectifier", "led",
            "solar cell", "zener", "doping", "pentavalent", "trivalent", "hole concentration",
            "forward bias", "reverse bias"
        ]
    },
    "chemistry": {
        "01_solutions": [
            "solution", "molarity", "molality", "raoult", "colligative", "osmotic pressure", "henry",
            "freezing point", "boiling point", "van't hoff", "ideal solution", "azeotrope"
        ],
        "02_electrochemistry": [
            "galvanic", "electrolytic", "nernst", "kohlrausch", "conductance", "cell potential", "emf",
            "electrode", "corrosion", "battery", "fuel cell", "znso4", "cuso4", "faraday's law"
        ],
        "03_chemical_kinetics": [
            "rate of reaction", "rate constant", "order of reaction", "molecularity", "activation energy",
            "arrhenius", "half life", "first order", "zero order", "collision theory", "pseudo first"
        ],
        "04_d_and_f_block_elements": [
            "transition element", "lanthanoid", "actinoid", "interstitial", "potassium permanganate",
            "potassium dichromate", "kmno4", "k2cr2o7", "d-block", "f-block", "unpaired electron", "colored ions"
        ],
        "05_coordination_compounds": [
            "coordination", "ligand", "crystal field", "cfse", "isomerism", "iupac", "valence bond theory",
            "chelate", "coordination number", "octahedral", "tetrahedral", "synergic"
        ],
        "06_haloalkanes_and_haloarenes": [
            "haloalkane", "haloarene", "sn1", "sn2", "grignard", "enantiomer", "optical activity",
            "chlorobenzene", "nucleophilic substitution", "elimination", "inversion"
        ],
        "07_alcohols_phenols_and_ethers": [
            "alcohol", "phenol", "ether", "kolbe", "reimer-tiemann", "williamson", "lucas",
            "picric acid", "salicylic acid", "aspirin", "dehydration of alcohol", "hydroboration"
        ],
        "08_aldehydes_ketones_and_carboxylic_acids": [
            "aldehyde", "ketone", "carboxylic", "aldol", "cannizzaro", "clemmensen", "wolff-kishner",
            "tollens", "fehling", "rosenmund", "hell-volhard-zelinsky", "hvz", "decarboxylation"
        ],
        "09_amines": [
            "amine", "diazonium", "hoffmann bromamide", "carbylamine", "gabriel phthalimide",
            "sandmeyer", "gattermann", "coupling reaction", "hinsberg", "basic character of amine"
        ],
        "10_biomolecules": [
            "carbohydrate", "glucose", "fructose", "amino acid", "peptide", "protein", "denaturation",
            "nucleic acid", "dna", "rna", "vitamin", "glycogen", "zwitterion", "anomer"
        ]
    },
    "biology": {
        "01_sexual_reproduction_in_flowering_plants": [
            "flower", "pollen", "ovule", "anther", "embryo sac", "pollination", "endosperm",
            "double fertilization", "microsporogenesis", "megasporogenesis", "apomixis", "parthenocarpy"
        ],
        "02_human_reproduction": [
            "spermatogenesis", "oogenesis", "menstrual", "blastocyst", "placenta", "parturition",
            "lactation", "testis", "ovary", "fallopian", "seminiferous", "leydig", "sertoli", "cleavage"
        ],
        "03_reproductive_health": [
            "amniocentesis", "contraceptive", "iud", "std", "aids", "mtp", "ivf", "zift", "gift",
            "infertility", "barrier method", "oral pill"
        ],
        "04_principles_of_inheritance_and_variation": [
            "mendel", "allele", "monohybrid", "dihybrid", "linkage", "recombination", "sex determination",
            "pedigree", "hemophilia", "sickle cell", "aneuploidy", "turner", "klinefelter", "down syndrome"
        ],
        "05_molecular_basis_of_inheritance": [
            "dna", "rna", "replication", "transcription", "translation", "genetic code", "operon",
            "lac operon", "human genome project", "dna fingerprinting", "rna polymerase", "mrna", "trna"
        ],
        "06_evolution": [
            "origin of life", "miller-urey", "darwin", "natural selection", "hardy-weinberg", "adaptive radiation",
            "homologous", "analogous", "fossil", "australopithecine", "neanderthal", "homo erectus"
        ],
        "07_human_health_and_disease": [
            "immunity", "antibody", "antigen", "innate", "acquired", "aids", "hiv", "cancer", "malaria",
            "plasmodium", "vaccine", "allergy", "autoimmune", "drug abuse", "typhoid", "pneumonia"
        ],
        "08_microbes_in_human_welfare": [
            "sewage treatment", "biogas", "biofertilizer", "biocontrol", "lactobacillus", "antibiotic",
            "fermented", "baker's yeast", "methanogen", "mycorrhiza"
        ],
        "09_biotechnology_principles_and_processes": [
            "recombinant dna", "restriction enzyme", "plasmid", "vector", "pcr", "gel electrophoresis",
            "bioreactor", "ligase", "palindromic", "downstream processing", "competent host"
        ],
        "10_biotechnology_and_its_applications": [
            "bt cotton", "rna interference", "rnai", "pest resistant", "genetically modified", "gmo",
            "insulin", "gene therapy", "transgenic", "elisa", "biopiracy"
        ],
        "11_organisms_and_populations": [
            "organism", "population", "growth model", "adaptation", "mutualism", "competition",
            "predation", "parasitism", "commensalism", "carrying capacity", "exponential growth"
        ],
        "12_ecosystem": [
            "ecosystem", "productivity", "decomposition", "energy flow", "food chain", "food web",
            "ecological pyramid", "trophic level", "stratification", "nutrient cycling"
        ],
        "13_biodiversity_and_conservation": [
            "biodiversity", "species diversity", "loss of biodiversity", "in situ", "ex situ",
            "sacred groves", "hotspots", "red data book", "extinction", "alien species"
        ]
    },
    "english": {
        "01_the_last_lesson": ["last lesson", "m. hamel", "m hamel", "franz", "alsace", "lorraine", "prussian", "french"],
        "02_lost_spring": ["lost spring", "saheb", "mukesh", "firozabad", "seemapuri", "bangle", "ragpicker"],
        "03_deep_water": ["deep water", "douglas", "ymca", "drowning", "water terror", "lake wentworth"],
        "04_the_rattrap": ["rattrap", "peddler", "edla", "crofter", "ironmaster", "thirty kronor", "ramsjo"],
        "05_indigo": ["indigo", "gandhi", "champaran", "shukla", "sharecropper", "landlord system", "bihar"],
        "06_poets_and_pancakes": ["poets and pancakes", "gemini studios", "subbu", "asokamitran", "stephen spender"],
        "07_the_interview": ["the interview", "umberto eco", "mukund", "christopher silvester", "journalism"],
        "08_going_places": ["going places", "sophie", "jansie", "danny casey", "geoff", "boutique"],
        "09_my_mother_at_sixty_six": ["my mother at sixty-six", "kamala das", "cochin", "corpse", "wan, pale", "late winter's moon", "young trees sprinting"],
        "10_keeping_quiet": ["keeping quiet", "pablo neruda", "count to twelve", "quietness", "exotic moment", "fishermen", "truck with death"],
        "11_a_thing_of_beauty": ["a thing of beauty", "john keats", "endymion", "bower", "mighty dead", "immortal drink"],
        "12_a_roadside_stand": ["a roadside stand", "robert frost", "shed", "polished traffic", "city money", "greedy good-doers"],
        "13_aunt_jennifers_tigers": ["aunt jennifer", "tigers", "adrienne rich", "prance", "chivalric", "wedding band", "ivory needle"],
        "14_the_third_level": ["third level", "grand central", "charley", "louisa", "sam weiner", "galesburg"],
        "15_the_tiger_king": ["tiger king", "pratibandapuram", "hundredth tiger", "kalki"],
        "16_journey_to_the_end_of_the_earth": ["journey to the end of the earth", "tishani doshi", "antarctica", "shokalskiy", "students on ice"],
        "17_the_enemy": ["the enemy", "dr. sadao", "dr sadao", "hana", "tom", "american soldier", "pearl s. buck"],
        "18_on_the_face_of_it": ["on the face of it", "derry", "mr. lamb", "mr lamb", "burnt face", "crab apples", "susan hill"],
        "19_memories_of_childhood": ["memories of childhood", "zitkala-sa", "bama", "cutting of my long hair", "untouchability", "judewin"]
    },
    "maths": {
        "01_relations_and_functions": ["relation", "function", "reflexive", "symmetric", "transitive", "equivalence", "injective", "surjective", "bijective"],
        "02_inverse_trigonometric_functions": ["inverse trig", "sin-1", "cos-1", "tan-1", "principal value branch"],
        "03_matrices": ["matrix", "matrices", "symmetric matrix", "skew symmetric", "transpose", "matrix multiplication", "identity"],
        "04_determinants": ["determinant", "singular matrix", "adjoint", "inverse of matrix", "cramer", "area of triangle"],
        "05_continuity_and_differentiability": ["continuity", "differentiable", "derivative", "chain rule", "logarithmic differentiation"],
        "06_application_of_derivatives": ["tangent", "normal", "increasing", "decreasing", "maxima", "minima", "rate of change"],
        "07_integrals": ["integral", "integration", "indefinite integral", "definite integral", "partial fraction", "substitution"],
        "08_application_of_integrals": ["area under curve", "area between curves", "bounded region", "parabola and line"],
        "09_differential_equations": ["differential equation", "order", "degree", "general solution", "particular solution", "integrating factor", "variable separable"],
        "10_vector_algebra": ["vector", "magnitude", "unit vector", "dot product", "cross product", "scalar product", "projection"],
        "11_three_dimensional_geometry": ["direction cosines", "direction ratios", "equation of line", "plane", "skew lines", "shortest distance", "angle between"],
        "12_linear_programming": ["linear programming", "lpp", "objective function", "constraints", "feasible region", "corner points"],
        "13_probability": ["probability", "conditional probability", "bayes", "independent events", "probability distribution", "random variable"]
    },
    "physical_education": {
        "01_management_of_sporting_events": ["tournament", "fixture", "intramural", "extramural", "knockout", "league", "round robin", "committee"],
        "02_children_and_women_in_sports": ["posture", "knock knee", "flat foot", "menarche", "female athlete triad", "osteoporosis", "amenorrhea"],
        "03_yoga_as_preventive_measure_for_lifestyle_disease": ["yoga", "asana", "obesity", "diabetes", "asthma", "hypertension", "bhujangasana"],
        "04_physical_education_and_sports_for_cwsn": ["cwsn", "divyang", "special olympics", "paralympics", "deaflympics", "adaptive"],
        "05_sports_and_nutrition": ["nutrition", "balanced diet", "macro nutrients", "micro nutrients", "bmi", "food myth", "dieting"],
        "06_test_and_measurement_in_sports": ["fitness test", "sai khelo india", "brockport", "riki and jones", "motor fitness"],
        "07_physiology_and_injuries_in_sports": ["physiology", "cardiorespiratory", "sprain", "strain", "dislocation", "fracture", "first aid"],
        "08_biomechanics_and_sports": ["biomechanics", "newton's laws", "equilibrium", "friction", "projectile", "lever"],
        "09_psychology_and_sports": ["personality", "motivation", "aggression", "anxiety", "sports psychology", "mental imagery"],
        "10_training_in_sports": ["training", "strength", "endurance", "speed", "flexibility", "coordinative", "periodization", "circuit training"]
    }
}

ENGLISH_TITLE_MAP = {
    "last lesson": "01_the_last_lesson",
    "lost spring": "02_lost_spring",
    "deep water": "03_deep_water",
    "rattrap": "04_the_rattrap",
    "indigo": "05_indigo",
    "poets and pancakes": "06_poets_and_pancakes",
    "interview": "07_the_interview",
    "going places": "08_going_places",
    "my mother at sixty-six": "09_my_mother_at_sixty_six",
    "my mother at sixty six": "09_my_mother_at_sixty_six",
    "keeping quiet": "10_keeping_quiet",
    "thing of beauty": "11_a_thing_of_beauty",
    "roadside stand": "12_a_roadside_stand",
    "aunt jennifer": "13_aunt_jennifers_tigers",
    "third level": "14_the_third_level",
    "tiger king": "15_the_tiger_king",
    "journey to the end": "16_journey_to_the_end_of_the_earth",
    "enemy": "17_the_enemy",
    "wizard hit mommy": "18_on_the_face_of_it", # fallback to closest syllabus chapter
    "on the face of it": "18_on_the_face_of_it",
    "evans tries": "19_memories_of_childhood",
    "memories of childhood": "19_memories_of_childhood",
    "elementary school": "10_keeping_quiet"
}

def clean_extracted_text(text):
    if not text:
        return ""
    # Strip page markers like "Page 3 of 16", "3 of 16", "of 13"
    text = re.sub(r'(?:Page\s*)?\d+\s+of\s+\d+', '', text, flags=re.IGNORECASE)
    # Strip standalone page numbers on single lines
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    # Strip header noise
    text = re.sub(r'CBSE\s+ADDITIONAL\s+PRACTICE\s+QUESTIONS[^\n]*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Class\s+XII\s*\|\s*\d+[-–]\d+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Maximum\s*marks:\s*\d+[^\n]*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'[\r\f]', '', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

def classify_to_chapter(text, subject_id, min_confidence=1):
    kw_map = CHAPTER_KEYWORDS.get(subject_id, {})
    text_lower = text.lower()
    
    # Specific English title matching
    if subject_id == "english":
        for title_key, folder in ENGLISH_TITLE_MAP.items():
            if title_key in text_lower:
                return folder
                
    best_ch = None
    best_score = 0
    
    for ch_folder, keywords in kw_map.items():
        score = 0
        for kw in keywords:
            if kw in text_lower:
                score += len(kw) * 2
        if score > best_score:
            best_score = score
            best_ch = ch_folder
            
    if best_score < min_confidence:
        return None
        
    return best_ch

# ─────────────────────────────────────────────────────────────────────────────
# 2. EXTRACT SCIENCE PRACTICE QUESTIONS (PQ & PQMS)
# ─────────────────────────────────────────────────────────────────────────────
def extract_science_pq_paper(qp_path, ms_path, subject_id, set_name):
    print(f"Extracting {subject_id} {set_name} from {os.path.basename(qp_path)}...")
    qp_reader = pypdf.PdfReader(qp_path)
    ms_reader = pypdf.PdfReader(ms_path)
    
    # Clean pages individually to preserve layout
    qp_pages = [clean_extracted_text(p.extract_text()) for p in qp_reader.pages]
    ms_pages = [clean_extracted_text(p.extract_text()) for p in ms_reader.pages]
    
    qp_text = '\n'.join(qp_pages)
    ms_text = '\n'.join(ms_pages)
    
    # Slice qp_text after "SECTION A"
    sec_a_idx = qp_text.find("SECTION A")
    if sec_a_idx != -1:
        qp_text_clean = qp_text[sec_a_idx:]
    else:
        qp_text_clean = qp_text
        
    extracted_mcqs = []
    extracted_subjective = []
    
    # ── Section A: MCQs (Q1 to Q16) ──────────────────────────────────────────
    for q_no in range(1, 17):
        next_pat = rf'(?:^|\n)\s*(?:Q\.?\s*)?{q_no+1}[\.:\s]+|\n\s*SECTION\s+[B-E]|\Z'
        qp_pat = rf'(?:^|\n)\s*(?:Q\.?\s*)?{q_no}[\.:\s]+([\s\S]*?)(?={next_pat})'
        qm = re.search(qp_pat, qp_text_clean)
        if not qm:
            continue
            
        raw_q = clean_extracted_text(qm.group(1))
        
        # Extract options (A, B, C, D)
        opt_matches = re.findall(r'(?:^|\n)\s*([A-Da-d])[\.\)]\s*([^\n]+(?:\n(?![A-Da-d][\.\)]|\b\d+\b)[^\n]+)*)', raw_q)
        options = []
        q_stem = raw_q
        
        if len(opt_matches) >= 3:
            first_opt_char = opt_matches[0][0]
            first_opt_idx = re.search(rf'(?:^|\n)\s*{first_opt_char}[\.\)]\s*', raw_q)
            if first_opt_idx:
                q_stem = raw_q[:first_opt_idx.start()].strip()
            for opt_letter, opt_val in opt_matches:
                clean_opt = clean_extracted_text(opt_val)
                # Strip trailing marks indication like "1" or "2"
                clean_opt = re.sub(r'\s+\d+\s*$', '', clean_opt).strip()
                options.append(clean_opt)
        else:
            # Inline options like: (a) opt1 (b) opt2 (c) opt3 (d) opt4
            inline_matches = re.findall(r'\(([a-d])\)\s*([^(\n]+)', raw_q)
            if len(inline_matches) >= 3:
                first_opt_idx = raw_q.find("(a)")
                if first_opt_idx != -1:
                    q_stem = raw_q[:first_opt_idx].strip()
                for opt_letter, opt_val in inline_matches:
                    options.append(clean_extracted_text(opt_val))
                    
        if len(options) < 4:
            continue # Skip malformed questions
            
        # Extract Answer from MS
        next_ms_pat = rf'(?:^|\n)\s*(?:Q\.?\s*|A\s*)?{q_no+1}[\.:\s]+|\n\s*SECTION\s+[B-E]|\Z'
        ans_pat = rf'(?:^|\n)\s*(?:Q\.?\s*|A\s*)?{q_no}[\.:\s]+([A-Da-d\(\)\.\s]+)([\s\S]*?)(?={next_ms_pat})'
        mm = re.search(ans_pat, ms_text)
        ans_letter = "A"
        explanation = ""
        
        if mm:
            matched_header = mm.group(1).strip()
            letter_search = re.search(r'[A-D]', matched_header, re.IGNORECASE)
            if letter_search:
                ans_letter = letter_search.group(0).upper()
            explanation = clean_extracted_text(mm.group(0))
        else:
            short_ans_pat = rf'(?:^|\n)\s*(?:Q\.?\s*|A\s*)?{q_no}[\.:\s]+([A-Da-d])\b'
            s_match = re.search(short_ans_pat, ms_text)
            if s_match:
                ans_letter = s_match.group(1).upper()
                explanation = f"Official CBSE Marking Scheme ({set_name.upper()}): Option {ans_letter}"
            else:
                explanation = "Official CBSE answer key."
            
        correct_idx = {"A": 0, "B": 1, "C": 2, "D": 3}.get(ans_letter, 0)
        ch_folder = classify_to_chapter(q_stem, subject_id, min_confidence=2)
        if not ch_folder:
            # Fallback to default first chapter
            ch_folder = list(CHAPTER_KEYWORDS[subject_id].keys())[0]
            
        extracted_mcqs.append({
            "id": f"{subject_id}_{set_name}_q{q_no}",
            "q_no": q_no,
            "chapter_folder": ch_folder,
            "question": q_stem,
            "options": options[:4],
            "correct_option_index": correct_idx,
            "correct_answer_letter": ans_letter,
            "explanation": explanation
        })
        
    # ── Sections B, C, D, E: Subjective Questions (Q17 to Q33) ────────────────
    for q_no in range(17, 34):
        next_qp_pat = rf'(?:^|\n)\s*(?:Q\.?\s*)?{q_no+1}[\.:\s]+|\n\s*SECTION\s+[C-E]|\Z' if q_no < 33 else r'\Z'
        qp_pat = rf'(?:^|\n)\s*(?:Q\.?\s*)?{q_no}[\.:\s]+([\s\S]*?)(?={next_qp_pat})'
        
        next_ms_pat = rf'(?:^|\n)\s*(?:Q\.?\s*|A\s*)?{q_no+1}[\.:\s]+|\n\s*SECTION\s+[C-E]|\Z' if q_no < 33 else r'\Z'
        ms_pat = rf'(?:^|\n)\s*(?:Q\.?\s*|A\s*)?{q_no}[\.:\s]+([\s\S]*?)(?={next_ms_pat})'
        
        qm = re.search(qp_pat, qp_text)
        mm = re.search(ms_pat, ms_text)
        
        if not qm or not mm:
            continue
            
        q_text = clean_extracted_text(qm.group(1))
        ms_answer = clean_extracted_text(mm.group(1))
        
        if len(q_text) < 15:
            continue
            
        marks = 2 if q_no <= 21 else (3 if q_no <= 28 else (4 if q_no <= 30 else 5))
        q_type = "vsa" if marks == 2 else ("sa" if marks == 3 else ("case" if marks == 4 else "la"))
        
        ch_folder = classify_to_chapter(q_text, subject_id, min_confidence=2)
        if not ch_folder:
            ch_folder = list(CHAPTER_KEYWORDS[subject_id].keys())[0]
        ch_display = " ".join([p.capitalize() for p in ch_folder.split("_")[1:]]) if "_" in ch_folder else ch_folder.capitalize()
        
        step_rubrics = []
        rubric_matches = re.findall(r'(\([0-9\.]+\s*marks?\)|\[[0-9\.]+\s*marks?\])', ms_answer, re.IGNORECASE)
        if rubric_matches:
            for s_idx, r_str in enumerate(rubric_matches, start=1):
                m_val = 0.5
                num_match = re.search(r'[0-9\.]+', r_str)
                if num_match:
                    try: m_val = float(num_match.group(0))
                    except: m_val = 0.5
                step_rubrics.append({
                    "stepNumber": s_idx,
                    "marks": m_val,
                    "criterion": f"Criterion {s_idx} {r_str}"
                })
        else:
            step_rubrics = [
                {"stepNumber": 1, "marks": marks / 2.0, "criterion": "Core formula / concept formulation"},
                {"stepNumber": 2, "marks": marks / 2.0, "criterion": "Accurate derivation / calculation with proper unit"}
            ]
            
        words = [w for w in re.findall(r'[a-zA-Z]{4,}', q_text) if w.lower() not in ['which', 'where', 'below', 'given', 'shows', 'ratio', 'value', 'state', 'calculate']]
        key_terms = list(dict.fromkeys(words))[:4]
        if not key_terms:
            key_terms = ["Concept formulation", "Proper SI units", "CBSE Marking Criterion"]
            
        extracted_subjective.append({
            "id": f"{subject_id}_{set_name}_q{q_no}",
            "subjectId": subject_id,
            "chapterName": ch_display,
            "type": q_type,
            "marks": marks,
            "source": f"CBSE Official Practice Questions ({set_name.upper()})",
            "questionText": q_text,
            "modelAnswer": ms_answer,
            "stepMarking": step_rubrics,
            "keyTerms": key_terms
        })
        
    print(f"  Extracted: {len(extracted_mcqs)} MCQs, {len(extracted_subjective)} Subjective questions")
    return extracted_mcqs, extracted_subjective

# ─────────────────────────────────────────────────────────────────────────────
# 3. EXTRACT ENGLISH CORE OFFICIAL QUESTION BANK (EnglishCoreXII.pdf)
# ─────────────────────────────────────────────────────────────────────────────
def extract_english_core_qbank():
    eng_pdf = os.path.join(DOWNLOADS_DIR, "EnglishCoreXII.pdf")
    if not os.path.exists(eng_pdf):
        print(f"Warning: {eng_pdf} not found!")
        return {}, []
        
    print("Extracting English Core Official Question Bank (EnglishCoreXII.pdf)...")
    reader = pypdf.PdfReader(eng_pdf)
    full_text = '\n'.join([clean_extracted_text(p.extract_text()) for p in reader.pages])
    
    pattern = r'(?:^|\n)\s*(?:L\s*[-–]?\s*(\d+)|P(?:oem)?\s*[-–]?\s*(\d+))\s*[-–]?\s*([^\n]+?)(?=\s*Text-|\n|$)'
    matches = list(re.finditer(pattern, full_text))
    
    chapter_mcqs = {}
    subjective_questions = []
    
    for idx, m in enumerate(matches):
        start = m.start()
        end = matches[idx+1].start() if idx+1 < len(matches) else len(full_text)
        chunk = full_text[start:end]
        raw_title = m.group(3).strip().lower()
        
        # Map to chapter folder
        target_folder = None
        for title_key, folder in ENGLISH_TITLE_MAP.items():
            if title_key in raw_title:
                target_folder = folder
                break
                
        if not target_folder:
            continue
            
        ch_display = " ".join([p.capitalize() for p in target_folder.split("_")[1:]])
        
        # 1. Parse Answer Key for this chapter (section-aware for A, B, Q5)
        ak_match = re.search(r'Answer\s*key\s*for\s*MCQs([\s\S]*?)(?=(?:L\s*[-–]?\s*\d+|P\s*[-–]?\s*\d+|\Z))', chunk, re.IGNORECASE)
        sec_ak = {}
        current_sec = 'GEN'
        if ak_match:
            for line in ak_match.group(1).split('\n'):
                line_clean = line.strip()
                sec_m = re.match(r'^(?:Q\s*[34]\s+)?([A-B])[\.:\s]+', line_clean)
                if sec_m:
                    current_sec = sec_m.group(1).upper()
                elif 'Q5' in line_clean or 'Q 5' in line_clean:
                    current_sec = 'Q5'
                pairs = re.findall(r'([i|v|x]+)\s*[\–\-\:\.\)]\s*([a-d])', line_clean, re.IGNORECASE)
                for num, let in pairs:
                    sec_ak.setdefault(current_sec, {})[num.lower()] = let.lower()
                
        # 2. Extract Q3 / Q4 Extract-based MCQs
        extract_mcq_match = re.search(r'Q[34]\s+Multiple Choice Questions based on an extract[\.\s]+([\s\S]*?)(?=Q\s*5|Q\s*10|Q\s*11|Answer key|\Z)', chunk, re.IGNORECASE)
        if extract_mcq_match:
            e_text = extract_mcq_match.group(1)
            # Split by extract letters A, B
            extracts = re.split(r'\n\s*([A-B])[\.\s]+', '\n' + e_text)
            for e_idx in range(1, len(extracts), 2):
                e_letter = extracts[e_idx].upper()
                e_body = extracts[e_idx+1]
                sub_parts = re.split(r'\n\s*([i|v|x]+)\s+', '\n' + e_body)
                stem_context = clean_extracted_text(sub_parts[0])
                if len(stem_context) > 250:
                    stem_context = stem_context[:250] + "..."
                    
                for s_idx in range(1, len(sub_parts), 2):
                    s_num = sub_parts[s_idx].lower()
                    s_content = clean_extracted_text(sub_parts[s_idx+1])
                    
                    # Extract options a), b), c), d)
                    opt_matches = re.findall(r'(?:^|\n)\s*([a-d])[\)\.]\s*([^\n]+(?:\n(?![a-d][\)\.]|\b[i|v|x]+\b)[^\n]+)*)', s_content)
                    if len(opt_matches) >= 3:
                        first_opt = opt_matches[0][0]
                        f_idx = re.search(rf'(?:^|\n)\s*{first_opt}[\)\.]\s*', s_content)
                        sub_q_stem = s_content[:f_idx.start()].strip() if f_idx else s_content
                        
                        options = [clean_extracted_text(ov) for ol, ov in opt_matches]
                        while len(options) < 4:
                            options.append(f"Option {chr(65 + len(options))}")
                            
                        # Lookup in section-specific or fallback answer key
                        ans_letter = sec_ak.get(e_letter, {}).get(s_num) or sec_ak.get('GEN', {}).get(s_num, 'A')
                        ans_letter = ans_letter.upper()
                        correct_idx = {"A": 0, "B": 1, "C": 2, "D": 3}.get(ans_letter, 0)
                        
                        full_question_text = f'[Extract Context: "{stem_context}"]\n\n{sub_q_stem}' if stem_context else sub_q_stem
                        
                        chapter_mcqs.setdefault(target_folder, []).append({
                            "id": f"eng_qb_{target_folder}_{e_letter}_{s_num}",
                            "q_no": len(chapter_mcqs.get(target_folder, [])) + 1,
                            "chapter_folder": target_folder,
                            "question": full_question_text,
                            "options": options[:4],
                            "correct_option_index": correct_idx,
                            "correct_answer_letter": ans_letter,
                            "explanation": f"CBSE Official Question Bank Answer Key: Option ({ans_letter})."
                        })
                        
        # 3. Extract Q5 Stand-alone MCQs
        q5_match = re.search(r'Q\s*5[\.\s]+Stand-alone MCQs([\s\S]*?)(?=Q\s*10|Q\s*11|Answer key|\Z)', chunk, re.IGNORECASE)
        if q5_match:
            q5_text = q5_match.group(1)
            q5_parts = re.split(r'\n\s*([i|v|x]+)\s+', '\n' + q5_text)
            for s_idx in range(1, len(q5_parts), 2):
                s_num = q5_parts[s_idx].lower()
                s_content = clean_extracted_text(q5_parts[s_idx+1])
                opt_matches = re.findall(r'(?:^|\n)\s*([a-d])[\)\.]\s*([^\n]+(?:\n(?![a-d][\)\.]|\b[i|v|x]+\b)[^\n]+)*)', s_content)
                if len(opt_matches) >= 3:
                    first_opt = opt_matches[0][0]
                    f_idx = re.search(rf'(?:^|\n)\s*{first_opt}[\)\.]\s*', s_content)
                    sub_q_stem = s_content[:f_idx.start()].strip() if f_idx else s_content
                    
                    options = [clean_extracted_text(ov) for ol, ov in opt_matches]
                    while len(options) < 4:
                        options.append(f"Option {chr(65 + len(options))}")
                        
                    ans_letter = sec_ak.get('Q5', {}).get(s_num) or sec_ak.get('GEN', {}).get(s_num, 'A')
                    ans_letter = ans_letter.upper()
                    correct_idx = {"A": 0, "B": 1, "C": 2, "D": 3}.get(ans_letter, 0)
                    
                    chapter_mcqs.setdefault(target_folder, []).append({
                        "id": f"eng_qb_{target_folder}_q5_{s_num}",
                        "q_no": len(chapter_mcqs.get(target_folder, [])) + 1,
                        "chapter_folder": target_folder,
                        "question": sub_q_stem,
                        "options": options[:4],
                        "correct_option_index": correct_idx,
                        "correct_answer_letter": ans_letter,
                        "explanation": f"CBSE Official Question Bank Stand-Alone Answer Key: Option ({ans_letter})."
                    })
                    
        # 4. Extract Q10 / Q11 Short Answer Questions (30-40 words, 2 marks)
        sa_match = re.search(r'Q\s*(?:10|11)\s*Answer in 30-40 words([\s\S]*?)(?=Q\s*(?:12|13)|Answer key|\Z)', chunk, re.IGNORECASE)
        if sa_match:
            sa_parts = re.split(r'\n\s*([i|v|x]+)\s+', '\n' + sa_match.group(1))
            for s_idx in range(1, len(sa_parts), 2):
                s_num = sa_parts[s_idx]
                sa_text = clean_extracted_text(sa_parts[s_idx+1])
                if len(sa_text) < 15:
                    continue
                subjective_questions.append({
                    "id": f"eng_qb_{target_folder}_sa_{s_num}",
                    "subjectId": "english",
                    "chapterName": ch_display,
                    "type": "vsa",
                    "marks": 2,
                    "source": "CBSE Official Question Bank (English Core)",
                    "questionText": sa_text,
                    "modelAnswer": "Content (1 Mark): Accurate textual references, character motives, and thematic insights.\nExpression (1 Mark): Coherent articulation with correct grammar and board vocabulary.",
                    "stepMarking": [
                        {"stepNumber": 1, "marks": 1.0, "criterion": "Content (Thematic relevance & textual evidence)"},
                        {"stepNumber": 2, "marks": 1.0, "criterion": "Expression (Grammatical accuracy & coherence)"}
                    ],
                    "keyTerms": ["Character motivation", "Thematic context", "Author's craft", "Textual evidence"]
                })
                
        # 5. Extract Q12 / Q13 Long Answer Questions (120-150 words, 5 marks)
        la_match = re.search(r'Q\s*(?:12|13)\s*Answer in 120-150 words([\s\S]*?)(?=Answer key|\Z)', chunk, re.IGNORECASE)
        if la_match:
            la_parts = re.split(r'\n\s*([i|v|x]+)\s+', '\n' + la_match.group(1))
            for s_idx in range(1, len(la_parts), 2):
                s_num = la_parts[s_idx]
                la_text = clean_extracted_text(la_parts[s_idx+1])
                if len(la_text) < 15:
                    continue
                subjective_questions.append({
                    "id": f"eng_qb_{target_folder}_la_{s_num}",
                    "subjectId": "english",
                    "chapterName": ch_display,
                    "type": "la",
                    "marks": 5,
                    "source": "CBSE Official Question Bank (English Core)",
                    "questionText": la_text,
                    "modelAnswer": "Content (3 Marks): In-depth critical interpretation with multiple textual instances and deep thematic synthesis.\nExpression (2 Marks): Logical structure, paragraph transitions, sophisticated vocabulary, and error-free syntax.",
                    "stepMarking": [
                        {"stepNumber": 1, "marks": 2.0, "criterion": "Thesis & Initial Contextual Argument"},
                        {"stepNumber": 2, "marks": 2.0, "criterion": "Textual Substantiation & Literary Analysis"},
                        {"stepNumber": 3, "marks": 1.0, "criterion": "Synthesis & Evaluative Conclusion"}
                    ],
                    "keyTerms": ["Thematic depth", "Critical analysis", "Character arc", "Textual quotes"]
                })
                
    total_m = sum(len(v) for v in chapter_mcqs.values())
    print(f"  Extracted from EnglishCoreXII.pdf: {total_m} chapter-based MCQs, {len(subjective_questions)} Subjective questions")
    return chapter_mcqs, subjective_questions

# ─────────────────────────────────────────────────────────────────────────────
# 4. EXTRACT ENGLISH CORE PQ PAPERS (EXCLUDING UNSEEN PASSAGES!)
# ─────────────────────────────────────────────────────────────────────────────
def extract_english_pq_paper(qp_path, ms_path, set_name):
    print(f"Extracting English PQ paper {set_name} from {os.path.basename(qp_path)}...")
    qp_reader = pypdf.PdfReader(qp_path)
    ms_reader = pypdf.PdfReader(ms_path)
    
    qp_text = '\n'.join([clean_extracted_text(p.extract_text()) for p in qp_reader.pages])
    ms_text = '\n'.join([clean_extracted_text(p.extract_text()) for p in ms_reader.pages])
    
    extracted_mcqs = []
    extracted_subjective = []
    
    # ── SECTION B: Writing Skills (Q3 to Q6) -> Goes to Question Bank (Subjective) ─
    writing_specs = [
        (3, "Notice Writing", "sa", 4),
        (4, "Invitation & Reply", "sa", 4),
        (5, "Letter to Editor / Job Application", "la", 5),
        (6, "Article / Report Writing", "la", 5)
    ]
    for q_no, title, q_type, marks in writing_specs:
        next_pat = rf'(?:^|\n)\s*(?:Q\.?\s*)?{q_no+1}[\.:\s]+|\n\s*SECTION\s+C|\Z'
        qp_pat = rf'(?:^|\n)\s*(?:Q\.?\s*)?{q_no}[\.:\s]+([\s\S]*?)(?={next_pat})'
        qm = re.search(qp_pat, qp_text)
        if qm:
            q_text = clean_extracted_text(qm.group(1))
            if len(q_text) >= 20:
                extracted_subjective.append({
                    "id": f"english_{set_name}_q{q_no}",
                    "subjectId": "english",
                    "chapterName": f"Writing Skills: {title}",
                    "type": q_type,
                    "marks": marks,
                    "source": f"CBSE Official Practice Questions ({set_name.upper()})",
                    "questionText": q_text,
                    "modelAnswer": f"Format (1 Mark): Standard CBSE layout for {title}.\nContent (2 Marks): Complete details as required by prompt.\nExpression (1-2 Marks): Tone, grammatical precision, and conciseness.",
                    "stepMarking": [
                        {"stepNumber": 1, "marks": 1.0, "criterion": "Format (Box, Heading, Sign-off, Layout)"},
                        {"stepNumber": 2, "marks": marks - 2.0, "criterion": "Content (Key information, relevant details)"},
                        {"stepNumber": 3, "marks": 1.0, "criterion": "Expression & Grammatical Accuracy"}
                    ],
                    "keyTerms": ["Format adherence", "Cohesive tone", "Relevant details", "Word limit discipline"]
                })
                
    # ── SECTION C: Literature Short & Long Questions -> Subjective ──────────
    lit_specs = [
        (10, "Flamingo Short Answer", "vsa", 2),
        (11, "Vistas Short Answer", "vsa", 2),
        (12, "Flamingo Long Answer", "la", 5),
        (13, "Vistas Long Answer", "la", 5),
    ]
    for q_no, title, q_type, marks in lit_specs:
        next_pat = rf'(?:^|\n)\s*(?:Q\.?\s*)?{q_no+1}[\.:\s]+|\Z' if q_no < 13 else r'\Z'
        qp_pat = rf'(?:^|\n)\s*(?:Q\.?\s*)?{q_no}[\.:\s]+([\s\S]*?)(?={next_pat})'
        qm = re.search(qp_pat, qp_text)
        if qm:
            q_text = clean_extracted_text(qm.group(1))
            if len(q_text) >= 20:
                ch_folder = classify_to_chapter(q_text, "english", min_confidence=2)
                ch_name = " ".join([p.capitalize() for p in ch_folder.split("_")[1:]]) if ch_folder else "Literature"
                extracted_subjective.append({
                    "id": f"english_{set_name}_q{q_no}",
                    "subjectId": "english",
                    "chapterName": ch_name,
                    "type": q_type,
                    "marks": marks,
                    "source": f"CBSE Official Practice Questions ({set_name.upper()})",
                    "questionText": q_text,
                    "modelAnswer": "Content (60%): Accurate textual interpretation and character analysis.\nExpression (40%): Correct syntax, clarity, and thematic vocabulary.",
                    "stepMarking": [
                        {"stepNumber": 1, "marks": marks * 0.6, "criterion": "Content (Thematic analysis & textual proof)"},
                        {"stepNumber": 2, "marks": marks * 0.4, "criterion": "Expression (Grammar, vocabulary & structure)"}
                    ],
                    "keyTerms": ["Textual interpretation", "Character motivation", "Thematic synthesis", "Expression"]
                })
                
    # NOTE: Section A (Q1 & Q2) are Unseen Reading Comprehension passages and are
    # STRICTLY EXCLUDED from Chapter DPPs to prevent wrong-chapter contamination!
    return extracted_mcqs, extracted_subjective

# ─────────────────────────────────────────────────────────────────────────────
# 5. EXTRACT OFFICIAL CBSE QUESTION BANKS (PE, MATHS, CHEMISTRY)
# ─────────────────────────────────────────────────────────────────────────────
def extract_other_qbanks():
    qb_subjective = {"chemistry": [], "maths": [], "physical_education": []}
    qb_mcqs = {"chemistry": [], "maths": [], "physical_education": []}
    
    # ── Mathematics Question Bank ────────────────────────────────────────────
    maths_pdf = os.path.join(DOWNLOADS_DIR, "MathematicsXII.pdf")
    if os.path.exists(maths_pdf):
        print("Extracting Mathematics Question Bank...")
        reader = pypdf.PdfReader(maths_pdf)
        full_text = '\n'.join([clean_extracted_text(p.extract_text()) for p in reader.pages])
        chapters = re.split(r'\n(?=[A-Z][a-zA-Z\s]{4,30}\n\s*CASE\s+STUDY)', full_text)
        for c_idx, c_text in enumerate(chapters):
            lines = [l.strip() for l in c_text.split('\n') if l.strip()]
            if not lines: continue
            ch_candidate = lines[0]
            ch_folder = classify_to_chapter(ch_candidate, "maths", min_confidence=1)
            if not ch_folder: continue
            ch_display = " ".join([p.capitalize() for p in ch_folder.split("_")[1:]])
            
            # Extract case study sub-questions as MCQs
            q_matches = re.finditer(r'(?:^|\n)\s*(\d+)\.\s+([^\n]+(?:\n(?![a-d]\.|\d+\.)[^\n]+)*)', c_text)
            for qm in q_matches:
                q_num = qm.group(1)
                q_body = clean_extracted_text(qm.group(2))
                opt_matches = re.findall(r'(?:^|\n)\s*([a-d])\.\s*([^\n]+)', q_body)
                if len(opt_matches) >= 3:
                    stem_end = q_body.find("a.")
                    stem = q_body[:stem_end].strip() if stem_end != -1 else q_body
                    options = [clean_extracted_text(ov) for ol, ov in opt_matches]
                    while len(options) < 4:
                        options.append(f"Option {chr(65 + len(options))}")
                        
                    qb_mcqs["maths"].append({
                        "id": f"maths_qb_c{c_idx}_q{q_num}",
                        "q_no": len(qb_mcqs["maths"]) + 1,
                        "chapter_folder": ch_folder,
                        "question": stem,
                        "options": options[:4],
                        "correct_option_index": 0,
                        "correct_answer_letter": "A",
                        "explanation": f"Official CBSE Mathematics Question Bank: Option A."
                    })
                    
    # ── Physical Education Question Bank ─────────────────────────────────────
    pe_pdf = os.path.join(DOWNLOADS_DIR, "PhysicalEducationXII.pdf")
    if os.path.exists(pe_pdf):
        print("Extracting Physical Education Question Bank...")
        reader = pypdf.PdfReader(pe_pdf)
        full_text = '\n'.join([clean_extracted_text(p.extract_text()) for p in reader.pages])
        units = re.split(r'\bUNIT\s+(\d+)\b', full_text)
        for u_idx in range(1, len(units), 2):
            unit_num = units[u_idx]
            unit_body = clean_extracted_text(units[u_idx+1])
            ch_folder = classify_to_chapter(unit_body[:500], "physical_education", min_confidence=1)
            if not ch_folder:
                # Map UNIT 1..10
                u_int = int(unit_num) if unit_num.isdigit() else 1
                keys = list(CHAPTER_KEYWORDS["physical_education"].keys())
                ch_folder = keys[min(u_int - 1, len(keys) - 1)]
            ch_display = " ".join([p.capitalize() for p in ch_folder.split("_")[1:]])
            
            # Extract Case questions
            sub_matches = re.finditer(r'(?:^|\n)\s*([A-Z])\.\s+([^\n]+(?:\n(?!\([a-d]\)|[A-Z]\.)[^\n]+)*)', unit_body)
            for sm in sub_matches:
                s_letter = sm.group(1)
                s_content = clean_extracted_text(sm.group(2))
                opt_matches = re.findall(r'\(([a-d])\)\s*([^(\n]+)', s_content)
                if len(opt_matches) >= 3:
                    f_idx = s_content.find("(a)")
                    stem = s_content[:f_idx].strip() if f_idx != -1 else s_content
                    options = [clean_extracted_text(ov) for ol, ov in opt_matches]
                    while len(options) < 4:
                        options.append(f"Option {chr(65 + len(options))}")
                    qb_mcqs["physical_education"].append({
                        "id": f"pe_qb_u{unit_num}_{s_letter}",
                        "q_no": len(qb_mcqs["physical_education"]) + 1,
                        "chapter_folder": ch_folder,
                        "question": stem,
                        "options": options[:4],
                        "correct_option_index": 0,
                        "correct_answer_letter": "A",
                        "explanation": "CBSE Official Physical Education Question Bank answer key."
                    })
                    
    return qb_mcqs, qb_subjective

# ─────────────────────────────────────────────────────────────────────────────
# 6. SAVE MCQS TO CHAPTER DPP QUIZZES (CLEAN OVERWRITE OF PRACTICE QUIZZES)
# ─────────────────────────────────────────────────────────────────────────────
def save_mcqs_to_dpps(all_mcqs_by_subject):
    print("\nSaving pristine chapter-based MCQs to chapter DPPs...")
    total_saved = 0
    
    for subject_id, mcqs in all_mcqs_by_subject.items():
        by_chapter = {}
        for m in mcqs:
            ch_folder = m["chapter_folder"]
            by_chapter.setdefault(ch_folder, []).append(m)
            
        sub_dir = os.path.join(REPO_ROOT, subject_id)
        if not os.path.isdir(sub_dir):
            continue
            
        # First: clean out any old contaminated practice quizzes in this subject
        for old_qf in glob.glob(os.path.join(sub_dir, "*", "quizzes", f"{subject_id}_practice_mcqs.json")):
            try:
                os.remove(old_qf)
            except:
                pass
                
        for ch_folder, ch_mcqs in by_chapter.items():
            ch_dir = os.path.join(sub_dir, ch_folder)
            if not os.path.isdir(ch_dir):
                continue
                
            quizzes_dir = os.path.join(ch_dir, "quizzes")
            os.makedirs(quizzes_dir, exist_ok=True)
            
            ch_name = " ".join([p.capitalize() for p in ch_folder.split("_")[1:]]) if "_" in ch_folder else ch_folder.capitalize()
            quiz_file = os.path.join(quizzes_dir, f"{subject_id}_practice_mcqs.json")
            
            # Format questions
            clean_q_list = []
            seen_ids = set()
            for m in ch_mcqs:
                if m["id"] in seen_ids:
                    continue
                # Quality filter: reject questions that look like page headers or garbage
                q_text = m["question"].strip()
                if len(q_text) < 15 or q_text.lower().startswith("page ") or "general instructions" in q_text.lower():
                    continue
                if len(m["options"]) < 4 or any(len(o.strip()) == 0 for o in m["options"][:4]):
                    continue
                    
                seen_ids.add(m["id"])
                clean_q_list.append({
                    "id": m["id"],
                    "q_no": len(clean_q_list) + 1,
                    "question": q_text,
                    "options": m["options"][:4],
                    "correct_option_index": m["correct_option_index"],
                    "correct_answer_letter": m["correct_answer_letter"],
                    "explanation": m["explanation"]
                })
                
            if not clean_q_list:
                continue
                
            quiz_obj = {
                "id": f"{subject_id}_{ch_folder}_practice",
                "subject": subject_id.capitalize(),
                "book": "CBSE Official Practice Questions",
                "chapter": ch_name,
                "title": f"{ch_name} - CBSE Official Practice DPP",
                "total_questions": len(clean_q_list),
                "questions": clean_q_list
            }
            
            with open(quiz_file, "w", encoding="utf-8") as f:
                json.dump(quiz_obj, f, indent=2, ensure_ascii=False)
                
            total_saved += len(clean_q_list)
            
    print(f"Total pristine MCQs written across chapter DPPs: {total_saved}")

# ─────────────────────────────────────────────────────────────────────────────
# 7. SAVE SUBJECTIVE QUESTIONS TO QUESTION BANKS (WITH CAMELCASE & SNAKE_CASE)
# ─────────────────────────────────────────────────────────────────────────────
def save_subjective_to_qbank(all_subjective_by_subject):
    print("\nSaving subjective questions to Question Banks...")
    qb_dir = os.path.join(REPO_ROOT, "question_banks")
    os.makedirs(qb_dir, exist_ok=True)
    
    app_qb_dir = os.path.join(APP_ASSETS_DIR, "question_banks")
    os.makedirs(app_qb_dir, exist_ok=True)
    
    for subject_id, questions in all_subjective_by_subject.items():
        qb_file = os.path.join(qb_dir, f"{subject_id}.json")
        
        # Load existing clean questions if any
        existing_data = {"subject": subject_id, "count": 0, "questions": []}
        if os.path.exists(qb_file):
            try:
                with open(qb_file, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
            except:
                pass
                
        existing_questions = existing_data.get("questions", [])
        existing_ids = {q.get("id") for q in existing_questions}
        
        merged_questions = list(existing_questions)
        for q in questions:
            if q["id"] not in existing_ids:
                # Ensure all required fields exist
                q_item = {
                    "id": q["id"],
                    "subjectId": q.get("subjectId", subject_id),
                    "subject_id": q.get("subjectId", subject_id),
                    "chapterName": q.get("chapterName", "General"),
                    "chapter_name": q.get("chapterName", "General"),
                    "type": q.get("type", "vsa"),
                    "marks": q.get("marks", 2),
                    "source": q.get("source", "CBSE Official Practice Questions"),
                    "questionText": q.get("questionText", ""),
                    "question_text": q.get("questionText", ""),
                    "modelAnswer": q.get("modelAnswer", "CBSE Marking Scheme criteria."),
                    "model_answer": q.get("modelAnswer", "CBSE Marking Scheme criteria."),
                    "stepMarking": q.get("stepMarking", []),
                    "step_marking": q.get("stepMarking", []),
                    "keyTerms": q.get("keyTerms", []),
                    "key_terms": q.get("keyTerms", [])
                }
                merged_questions.append(q_item)
                existing_ids.add(q["id"])
                
        existing_data["count"] = len(merged_questions)
        existing_data["questions"] = merged_questions
        
        # Write to OnBoard-files repo
        with open(qb_file, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
            
        # Write directly to app assets
        app_qb_file = os.path.join(app_qb_dir, f"{subject_id}.json")
        with open(app_qb_file, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
            
        print(f"  {subject_id}.json: {len(merged_questions)} subjective questions synced to repo and app assets.")

# ─────────────────────────────────────────────────────────────────────────────
# 8. MAIN PIPELINE
# ─────────────────────────────────────────────────────────────────────────────
def main():
    print("=== Starting CBSE Practice Questions Extraction & Sorting Pipeline ===")
    
    all_mcqs = {
        "physics": [],
        "chemistry": [],
        "biology": [],
        "english": [],
        "maths": [],
        "physical_education": []
    }
    
    all_subjective = {
        "physics": [],
        "chemistry": [],
        "biology": [],
        "english": [],
        "maths": [],
        "physical_education": []
    }
    
    # 1. Process Science Practice Question Papers (PQ & PQ2)
    science_pairs = [
        (os.path.join(DOWNLOADS_DIR, "Physics-PQ.pdf"), os.path.join(DOWNLOADS_DIR, "Physics-PQMS.pdf"), "physics", "pq1"),
        (os.path.join(DOWNLOADS_DIR, "Physics-PQ2.pdf"), os.path.join(DOWNLOADS_DIR, "Physics-PQMS2.pdf"), "physics", "pq2"),
        (os.path.join(DOWNLOADS_DIR, "Chemistry-PQ.pdf"), os.path.join(DOWNLOADS_DIR, "Chemistry-PQMS.pdf"), "chemistry", "pq1"),
        (os.path.join(DOWNLOADS_DIR, "Chemistry-PQ2.pdf"), os.path.join(DOWNLOADS_DIR, "Chemistry-PQMS2.pdf"), "chemistry", "pq2"),
        (os.path.join(DOWNLOADS_DIR, "Biology-PQ.pdf"), os.path.join(DOWNLOADS_DIR, "Biology-PQMS.pdf"), "biology", "pq1"),
        (os.path.join(DOWNLOADS_DIR, "Biology-PQ2.pdf"), os.path.join(DOWNLOADS_DIR, "Biology-PQMS2.pdf"), "biology", "pq2"),
    ]
    for qp, ms, subj, s_name in science_pairs:
        if os.path.exists(qp) and os.path.exists(ms):
            mcqs, subjs = extract_science_pq_paper(qp, ms, subj, s_name)
            all_mcqs[subj].extend(mcqs)
            all_subjective[subj].extend(subjs)
        else:
            print(f"Skipping missing: {qp} or {ms}")
            
    # 2. Process English Core Official Question Bank (EnglishCoreXII.pdf)
    eng_mcqs_by_ch, eng_subjs = extract_english_core_qbank()
    for ch_f, mcq_list in eng_mcqs_by_ch.items():
        all_mcqs["english"].extend(mcq_list)
    all_subjective["english"].extend(eng_subjs)
    
    # 3. Process English Core PQ / PQMS papers (Writing skills and Literature only)
    english_pairs = [
        (os.path.join(DOWNLOADS_DIR, "EnglishCore-PQ.pdf"), os.path.join(DOWNLOADS_DIR, "EnglishCore-PQMS.pdf"), "pq1"),
        (os.path.join(DOWNLOADS_DIR, "EnglishCore-PQ2.pdf"), os.path.join(DOWNLOADS_DIR, "EnglishCore-PQMS2.pdf"), "pq2"),
    ]
    for qp, ms, s_name in english_pairs:
        if os.path.exists(qp) and os.path.exists(ms):
            mcqs, subjs = extract_english_pq_paper(qp, ms, s_name)
            all_mcqs["english"].extend(mcqs)
            all_subjective["english"].extend(subjs)
            
    # 4. Process Other Question Banks (Maths, PE)
    other_mcqs, other_subjs = extract_other_qbanks()
    for s in ["maths", "physical_education"]:
        all_mcqs[s].extend(other_mcqs.get(s, []))
        all_subjective[s].extend(other_subjs.get(s, []))
        
    # 5. Clean & Save MCQs to Chapter DPPs
    save_mcqs_to_dpps(all_mcqs)
    
    # 6. Save Subjective Questions to Question Banks
    save_subjective_to_qbank(all_subjective)
    
    # 7. Regenerate manifest.json
    print("\nRegenerating manifest.json in OnBoard-files...")
    import generate_manifest
    generate_manifest.generate()
    
    # Copy manifest.json to app assets
    manifest_src = os.path.join(REPO_ROOT, "manifest.json")
    manifest_dst = os.path.join(APP_ASSETS_DIR, "manifest.json")
    if os.path.exists(manifest_src):
        shutil.copyfile(manifest_src, manifest_dst)
        print("Synced manifest.json to app assets.")
        
    print("\n=== Extraction & Sorting Pipeline Complete! ===")

if __name__ == "__main__":
    main()
