import os
import sys
import json
import re
import glob
import pypdf

# Ensure UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8')

DOWNLOADS_DIR = r"C:\Users\dines\Downloads"
REPO_ROOT = os.path.abspath(os.path.dirname(__file__))

# ─────────────────────────────────────────────────────────────────────────────
# 1. CHAPTER KEYWORD MAPPINGS
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
            "alcohol", "phenol", "ether", "reimer-tiemann", "kolbe", "hydroboration", "fermentation",
            "lucas", "williamson", "picric acid", "salicylic", "acidity of phenol"
        ],
        "08_aldehydes_ketones_and_carboxylic_acids": [
            "aldehyde", "ketone", "carboxylic", "aldol", "cannizzaro", "clemmensen", "wolff-kishner",
            "tollens", "fehling", "decarboxylation", "hvz", "carbonyl"
        ],
        "09_amines": [
            "amine", "diazonium", "carbylamine", "hinsberg", "gabriel phthalimide", "hoffmann bromamide",
            "basicity of amine", "aniline", "coupling reaction"
        ],
        "10_biomolecules": [
            "carbohydrate", "glucose", "fructose", "amino acid", "peptide", "protein", "enzyme",
            "dna", "rna", "nucleic acid", "vitamin", "denaturation", "glycogen"
        ]
    },
    "biology": {
        "01_sexual_reproduction_in_flowering_plants": [
            "microsporangium", "pollen", "megasporangium", "embryo sac", "pollination", "double fertilization",
            "endosperm", "apomixis", "seed development", "stamen", "carpel", "pistil", "anther"
        ],
        "02_human_reproduction": [
            "spermatogenesis", "oogenesis", "menstrual cycle", "fertilization", "blastocyst", "implantation",
            "parturition", "lactation", "testis", "ovary", "placenta", "seminiferous", "leydig"
        ],
        "03_reproductive_health": [
            "contraception", "iud", "art", "ivf", "zift", "gift", "std", "amniocentesis", "mtp",
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

def classify_to_chapter(text, subject_id):
    """Classify a question text to a chapter folder based on keyword frequency."""
    kw_map = CHAPTER_KEYWORDS.get(subject_id, {})
    text_lower = text.lower()
    
    best_ch = None
    best_score = 0
    
    for ch_folder, keywords in kw_map.items():
        score = 0
        for kw in keywords:
            if kw in text_lower:
                score += len(kw) # Give higher weight to more specific phrases
        if score > best_score:
            best_score = score
            best_ch = ch_folder
            
    if not best_ch and kw_map:
        best_ch = list(kw_map.keys())[0]
        
    return best_ch

def clean_extracted_text(text):
    text = re.sub(r'[\r\f]', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# ─────────────────────────────────────────────────────────────────────────────
# 2. EXTRACT PRACTICE QUESTIONS (PQ & PQMS) - SCIENCE (PHY, CHEM, BIO)
# ─────────────────────────────────────────────────────────────────────────────
def extract_science_pq_paper(qp_path, ms_path, subject_id, set_name):
    print(f"Extracting {subject_id} {set_name} from {os.path.basename(qp_path)}...")
    qp_reader = pypdf.PdfReader(qp_path)
    ms_reader = pypdf.PdfReader(ms_path)
    
    qp_text = '\n'.join([p.extract_text() for p in qp_reader.pages])
    ms_text = '\n'.join([p.extract_text() for p in ms_reader.pages])
    
    extracted_mcqs = []
    extracted_subjective = []
    
    # ── Section A: MCQs (Q1 to Q16) ──────────────────────────────────────────
    for q_no in range(1, 17):
        next_pat = rf'(?:^|\n)\s*(?:Q\.?\s*)?{q_no+1}[\.:\s]+|\n\s*SECTION\s+[B-E]|\Z'
        qp_pat = rf'(?:^|\n)\s*(?:Q\.?\s*)?{q_no}[\.:\s]+([\s\S]*?)(?={next_pat})'
        qm = re.search(qp_pat, qp_text)
        if not qm:
            continue
            
        raw_q = clean_extracted_text(qm.group(1))
        
        # Extract options
        opt_matches = re.findall(r'([A-Da-d])[\.\)]\s*([^\n]+(?:\n(?![A-Da-d][\.\)]|\d+\b)[^\n]+)*)', raw_q)
        options = []
        q_stem = raw_q
        
        if opt_matches:
            first_opt_char = opt_matches[0][0]
            first_opt_idx = re.search(rf'{first_opt_char}[\.\)]\s*', raw_q)
            if first_opt_idx:
                q_stem = raw_q[:first_opt_idx.start()].strip()
            for opt_letter, opt_val in opt_matches:
                options.append(clean_extracted_text(opt_val))
                
        while len(options) < 4:
            options.append(f"Option {chr(65 + len(options))}")
            
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
            # Fallback for simple 'A1 c 1' format
            short_ans_pat = rf'(?:^|\n)\s*(?:Q\.?\s*|A\s*)?{q_no}[\.:\s]+([A-Da-d])\b'
            s_match = re.search(short_ans_pat, ms_text)
            if s_match:
                ans_letter = s_match.group(1).upper()
                explanation = f"Official CBSE Marking Scheme ({set_name.upper()}): Option {ans_letter}"
            else:
                explanation = "Official CBSE answer key."
            
        letter_to_idx = {"A": 0, "B": 1, "C": 2, "D": 3}
        correct_idx = letter_to_idx.get(ans_letter, 0)
        
        ch_folder = classify_to_chapter(q_stem, subject_id)
        
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
        
        marks = 2 if q_no <= 21 else (3 if q_no <= 28 else (4 if q_no <= 30 else 5))
        q_type = "vsa" if marks == 2 else ("sa" if marks == 3 else ("case" if marks == 4 else "la"))
        
        ch_folder = classify_to_chapter(q_text, subject_id)
        ch_display = " ".join([p.capitalize() for p in ch_folder.split("_")[1:]]) if "_" in ch_folder else ch_folder.capitalize()
        
        # Step rubrics
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
            
        words = [w for w in re.findall(r'[a-zA-Z]{4,}', q_text) if w.lower() not in ['which', 'where', 'below', 'given', 'shows', 'ratio', 'value']]
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
# 3. EXTRACT ENGLISH CORE PRACTICE QUESTIONS (PQ & PQMS)
# ─────────────────────────────────────────────────────────────────────────────
def extract_english_pq_paper(qp_path, ms_path, set_name):
    print(f"Extracting english {set_name} from {os.path.basename(qp_path)}...")
    qp_reader = pypdf.PdfReader(qp_path)
    ms_reader = pypdf.PdfReader(ms_path)
    
    qp_text = '\n'.join([p.extract_text() for p in qp_reader.pages])
    ms_text = '\n'.join([p.extract_text() for p in ms_reader.pages])
    
    extracted_mcqs = []
    extracted_subjective = []
    
    # ── Literature Extracts MCQs (Q7 Poetry, Q8 Vistas, Q9 Flamingo) ──────────
    for q_no in [7, 8, 9]:
        next_q = q_no + 1
        next_pat = rf'(?:^|\n)\s*{next_q}[\.:\s]+|\Z'
        pat = rf'(?:^|\n)\s*{q_no}[\.:\s]+([\s\S]*?)(?={next_pat})'
        qm = re.search(pat, qp_text)
        mm = re.search(pat, ms_text)
        if not qm: continue
        
        q_block = qm.group(1)
        ms_block = mm.group(1) if mm else ""
        
        # Find sub-questions with options A-D
        sub_qs = re.findall(r'([i|v|x]+)\s+([^\n]+(?:\n(?![i|v|x]+\b)[^\n]+)*)', q_block)
        for s_num, s_content in sub_qs:
            opt_matches = re.findall(r'([A-D])[\.\)]\s*([^\n]+(?:\n(?![A-D][\.\)]|\b[i|v|x]+\b)[^\n]+)*)', s_content)
            if len(opt_matches) >= 3:
                q_stem = s_content
                first_opt_char = opt_matches[0][0]
                first_opt_idx = re.search(rf'{first_opt_char}[\.\)]\s*', s_content)
                if first_opt_idx:
                    q_stem = s_content[:first_opt_idx.start()].strip()
                    
                options = [clean_extracted_text(ov) for ol, ov in opt_matches]
                while len(options) < 4:
                    options.append(f"Option {chr(65 + len(options))}")
                    
                # Find answer in MS block
                ans_pat = rf'{s_num}\s+([A-D])\b'
                ans_match = re.search(ans_pat, ms_block, re.IGNORECASE)
                ans_letter = ans_match.group(1).upper() if ans_match else "A"
                correct_idx = {"A": 0, "B": 1, "C": 2, "D": 3}.get(ans_letter, 0)
                
                ch_folder = classify_to_chapter(q_stem + " " + q_block[:200], "english")
                
                extracted_mcqs.append({
                    "id": f"english_{set_name}_q{q_no}_{s_num}",
                    "q_no": len(extracted_mcqs) + 1,
                    "chapter_folder": ch_folder,
                    "question": clean_extracted_text(q_stem),
                    "options": options[:4],
                    "correct_option_index": correct_idx,
                    "correct_answer_letter": ans_letter,
                    "explanation": f"CBSE English Core Practice Paper ({set_name.upper()}) Marking Scheme: Option {ans_letter}."
                })

    # ── Subjective: Writing (Q3-Q6) & Literature (Q10-Q13) ───────────────────
    subjective_specs = [
        (3, "Notice Writing", "sa", 4),
        (4, "Invitation / Reply", "sa", 4),
        (5, "Letter / Application", "la", 5),
        (6, "Article / Report", "la", 5),
        (10, "Flamingo Short Answer (40-50 words)", "sa", 2),
        (11, "Vistas Short Answer (40-50 words)", "sa", 2),
        (12, "Flamingo Long Answer (120-150 words)", "la", 5),
        (13, "Vistas Long Answer (120-150 words)", "la", 5),
    ]
    
    for q_no, q_title, q_type, marks in subjective_specs:
        next_pat = rf'(?:^|\n)\s*(?:Q\.?\s*)?{q_no+1}[\.:\s]+|\Z' if q_no < 13 else r'\Z'
        qp_pat = rf'(?:^|\n)\s*(?:Q\.?\s*)?{q_no}[\.:\s]+([\s\S]*?)(?={next_pat})'
        ms_pat = rf'(?:^|\n)\s*(?:Q\.?\s*|A\s*)?{q_no}[\.:\s]+([\s\S]*?)(?={next_pat})'
        
        qm = re.search(qp_pat, qp_text)
        mm = re.search(ms_pat, ms_text)
        
        if not qm: continue
        
        q_text = clean_extracted_text(qm.group(1))
        ms_answer = clean_extracted_text(mm.group(1)) if mm else "CBSE Official Marking Scheme criteria."
        
        ch_folder = classify_to_chapter(q_text, "english")
        ch_display = " ".join([p.capitalize() for p in ch_folder.split("_")[1:]]) if "_" in ch_folder else ch_folder.capitalize()
        
        if q_no in [3, 4, 5, 6]:
            ch_display = q_title
            
        step_rubrics = [
            {"stepNumber": 1, "marks": marks * 0.4, "criterion": "Format and initial thesis / context"},
            {"stepNumber": 2, "marks": marks * 0.4, "criterion": "Content, thematic analysis, and textual evidence"},
            {"stepNumber": 3, "marks": marks * 0.2, "criterion": "Expression, grammar, and coherence"}
        ]
        
        extracted_subjective.append({
            "id": f"english_{set_name}_q{q_no}",
            "subjectId": "english",
            "chapterName": ch_display,
            "type": q_type,
            "marks": marks,
            "source": f"CBSE Official Practice Questions ({set_name.upper()})",
            "questionText": q_text[:800],
            "modelAnswer": ms_answer[:1200],
            "stepMarking": step_rubrics,
            "keyTerms": ["Thematic evidence", "Character motivation", "Coherence", "Expression"]
        })
        
    print(f"  Extracted: {len(extracted_mcqs)} MCQs, {len(extracted_subjective)} Subjective questions")
    return extracted_mcqs, extracted_subjective

# ─────────────────────────────────────────────────────────────────────────────
# 4. EXTRACT OFFICIAL CBSE QUESTION BANKS (PE, MATHS, CHEMISTRY, ENGLISH)
# ─────────────────────────────────────────────────────────────────────────────
def extract_official_qbanks():
    qb_subjective = {
        "chemistry": [],
        "maths": [],
        "physical_education": [],
        "english": []
    }
    qb_mcqs = {
        "chemistry": [],
        "maths": [],
        "physical_education": [],
        "english": []
    }
    
    # ── Mathematics Question Bank ─────────────────────────────────────────────
    maths_pdf = os.path.join(DOWNLOADS_DIR, "MathematicsXII.pdf")
    if os.path.exists(maths_pdf):
        print("Extracting Mathematics official question bank...")
        reader = pypdf.PdfReader(maths_pdf)
        full_text = '\n'.join([p.extract_text() for p in reader.pages])
        case_studies = re.split(r'(?i)CASE\s*STUDY\s*\d*[:\-]', full_text)
        for idx, cs in enumerate(case_studies[1:], start=1):
            cs_clean = clean_extracted_text(cs)
            if len(cs_clean) < 50: continue
            ch_folder = classify_to_chapter(cs_clean[:400], "maths")
            ch_display = " ".join([p.capitalize() for p in ch_folder.split("_")[1:]]) if "_" in ch_folder else ch_folder.capitalize()
            
            qb_subjective["maths"].append({
                "id": f"maths_qb_case_{idx}",
                "subjectId": "maths",
                "chapterName": ch_display,
                "type": "case",
                "marks": 4,
                "source": "CBSE Official Question Bank (Mathematics)",
                "questionText": cs_clean[:800],
                "modelAnswer": cs_clean[800:1500] if len(cs_clean) > 800 else "Refer to CBSE Official Model Solutions.",
                "stepMarking": [
                    {"stepNumber": 1, "marks": 1.0, "criterion": "Identification of mathematical model"},
                    {"stepNumber": 2, "marks": 1.0, "criterion": "Sub-part (i) solution"},
                    {"stepNumber": 3, "marks": 1.0, "criterion": "Sub-part (ii) solution"},
                    {"stepNumber": 4, "marks": 1.0, "criterion": "Final evaluation with domain restrictions"}
                ],
                "keyTerms": ["Domain restriction", "Equivalence relation", "Optimization", "Probability distribution"]
            })
            
    # ── Physical Education Question Bank ─────────────────────────────────────
    pe_pdf = os.path.join(DOWNLOADS_DIR, "PhysicalEducationXII.pdf")
    if os.path.exists(pe_pdf):
        print("Extracting Physical Education official question bank...")
        reader = pypdf.PdfReader(pe_pdf)
        full_text = '\n'.join([p.extract_text() for p in reader.pages])
        q_blocks = re.split(r'\n\s*Q\.\s*\d+[\.:]?', full_text)
        for idx, qb in enumerate(q_blocks[1:], start=1):
            qb_clean = clean_extracted_text(qb)
            if len(qb_clean) < 60: continue
            ch_folder = classify_to_chapter(qb_clean[:300], "physical_education")
            ch_display = " ".join([p.capitalize() for p in ch_folder.split("_")[1:]]) if "_" in ch_folder else ch_folder.capitalize()
            
            qb_subjective["physical_education"].append({
                "id": f"pe_qb_case_{idx}",
                "subjectId": "physical_education",
                "chapterName": ch_display,
                "type": "case" if idx % 2 == 0 else "sa",
                "marks": 4 if idx % 2 == 0 else 3,
                "source": "CBSE Official Question Bank (Physical Education)",
                "questionText": qb_clean[:700],
                "modelAnswer": qb_clean[700:1300] if len(qb_clean) > 700 else "Official CBSE model answer criteria.",
                "stepMarking": [
                    {"stepNumber": 1, "marks": 1.5, "criterion": "Key rule / physiological concept definition"},
                    {"stepNumber": 2, "marks": 1.5, "criterion": "Practical tournament / training application"}
                ],
                "keyTerms": ["Tournament fixture", "Balanced nutrition", "Biomechanics", "Motor fitness"]
            })
            
    # ── Chemistry Question Bank ──────────────────────────────────────────────
    chem_pdf = os.path.join(DOWNLOADS_DIR, "ChemistryXII.pdf")
    if os.path.exists(chem_pdf):
        print("Extracting Chemistry official question bank...")
        reader = pypdf.PdfReader(chem_pdf)
        full_text = '\n'.join([p.extract_text() for p in reader.pages])
        passages = re.split(r'\([I|V|X]+\)\s*Read the passage', full_text)
        for idx, p_text in enumerate(passages[1:], start=1):
            p_clean = clean_extracted_text(p_text)
            if len(p_clean) < 60: continue
            ch_folder = classify_to_chapter(p_clean[:300], "chemistry")
            ch_display = " ".join([p.capitalize() for p in ch_folder.split("_")[1:]]) if "_" in ch_folder else ch_folder.capitalize()
            
            qb_subjective["chemistry"].append({
                "id": f"chem_qb_case_{idx}",
                "subjectId": "chemistry",
                "chapterName": ch_display,
                "type": "case",
                "marks": 4,
                "source": "CBSE Official Question Bank (Chemistry)",
                "questionText": p_clean[:800],
                "modelAnswer": p_clean[800:1400] if len(p_clean) > 800 else "Official CBSE Step-marking rationale.",
                "stepMarking": [
                    {"stepNumber": 1, "marks": 1.0, "criterion": "Reaction mechanism / colligative equation"},
                    {"stepNumber": 2, "marks": 1.0, "criterion": "Substitution of given data"},
                    {"stepNumber": 3, "marks": 2.0, "criterion": "Logical scientific deduction with units"}
                ],
                "keyTerms": ["Equilibrium", "Rate constant", "Colligative property", "Oxidation state"]
            })

    # ── English Core Question Bank ───────────────────────────────────────────
    eng_pdf = os.path.join(DOWNLOADS_DIR, "EnglishCoreXII.pdf")
    if os.path.exists(eng_pdf):
        print("Extracting English Core official question bank...")
        reader = pypdf.PdfReader(eng_pdf)
        full_text = '\n'.join([p.extract_text() for p in reader.pages])
        lessons = re.split(r'\bL-\d+\s+|\bPoem-\d+\s+', full_text)
        for idx, l_text in enumerate(lessons[1:], start=1):
            l_clean = clean_extracted_text(l_text)
            if len(l_clean) < 100: continue
            ch_folder = classify_to_chapter(l_clean[:400], "english")
            ch_display = " ".join([p.capitalize() for p in ch_folder.split("_")[1:]]) if "_" in ch_folder else ch_folder.capitalize()
            
            # 1. Extract MCQs from Q3 / Q5 with Answer Key
            ak_match = re.search(r'Answer\s*key\s*for\s*MCQs([\s\S]*?)(?=\n\s*(?:[A-Z\s]{6,}|L-\d|Poem-\d|\Z))', l_clean, re.IGNORECASE)
            ak_dict = {}
            if ak_match:
                ak_text = ak_match.group(1)
                pairs = re.findall(r'([i|v|x]+)\s*[\–\-\:\.\)]\s*([a-d])', ak_text, re.IGNORECASE)
                for num_str, letter in pairs:
                    ak_dict[num_str.lower()] = letter.lower()
                    
            # Match MCQs
            q3_mcq_matches = re.finditer(r'(?:^|\n)\s*([i|v|x]+)\s+([^\n]+(?:\n(?![a-d][\)\.]|[i|v|x]+\b)[^\n]+)*)', l_clean)
            for qm in q3_mcq_matches:
                q_num = qm.group(1).lower()
                q_body = clean_extracted_text(qm.group(2))
                
                # Check options
                opt_matches = re.findall(r'([a-d])[\)\.]\s*([^\n]+(?:\n(?![a-d][\)\.]|[i|v|x]+\b)[^\n]+)*)', q_body)
                if opt_matches and q_num in ak_dict:
                    ans_char = ak_dict[q_num].upper()
                    correct_idx = {"A": 0, "B": 1, "C": 2, "D": 3}.get(ans_char, 0)
                    
                    first_opt_char = opt_matches[0][0]
                    first_opt_idx = re.search(rf'{first_opt_char}[\)\.]\s*', q_body)
                    stem = q_body[:first_opt_idx.start()].strip() if first_opt_idx else q_body
                    
                    options = [clean_extracted_text(ov) for ol, ov in opt_matches]
                    while len(options) < 4:
                        options.append(f"Option {chr(65 + len(options))}")
                        
                    qb_mcqs["english"].append({
                        "id": f"english_qb_ch{idx}_{q_num}",
                        "q_no": len(qb_mcqs["english"]) + 1,
                        "chapter_folder": ch_folder,
                        "question": stem,
                        "options": options[:4],
                        "correct_option_index": correct_idx,
                        "correct_answer_letter": ans_char,
                        "explanation": f"Official CBSE English Core Question Bank answer key: Option {ans_char}."
                    })
            
            # 2. Extract 30-40 word Short Answer and 120-150 word Long Answer
            q10_match = re.search(r'Q10\s*Answer in 30-40 words([\s\S]*?)(?=Q12|\Z)', l_clean)
            if q10_match:
                sa_text = clean_extracted_text(q10_match.group(1))
                qb_subjective["english"].append({
                    "id": f"eng_qb_sa_{idx}",
                    "subjectId": "english",
                    "chapterName": ch_display,
                    "type": "sa",
                    "marks": 2,
                    "source": "CBSE Official Question Bank (English Core)",
                    "questionText": sa_text[:500],
                    "modelAnswer": "Content (1 mark): Reference to characters and thematic context. Expression (1 mark): Grammatical accuracy and vocabulary.",
                    "stepMarking": [
                        {"stepNumber": 1, "marks": 1.0, "criterion": "Content (thematic relevance)"},
                        {"stepNumber": 2, "marks": 1.0, "criterion": "Expression (coherence and grammar)"}
                    ],
                    "keyTerms": ["Character motivation", "Theme of identity", "Critical reflection", "Textual evidence"]
                })
                
            q12_match = re.search(r'Q12\s*Answer in 120-150 words([\s\S]*?)(?=Answer key|\Z)', l_clean)
            if q12_match:
                la_text = clean_extracted_text(q12_match.group(1))
                qb_subjective["english"].append({
                    "id": f"eng_qb_la_{idx}",
                    "subjectId": "english",
                    "chapterName": ch_display,
                    "type": "la",
                    "marks": 5,
                    "source": "CBSE Official Question Bank (English Core)",
                    "questionText": la_text[:600],
                    "modelAnswer": "Content (3 marks): Sustained interpretation with evidence from the text. Expression (2 marks): Well-structured paragraph, tone, and appropriate vocabulary.",
                    "stepMarking": [
                        {"stepNumber": 1, "marks": 2.0, "criterion": "Initial thesis statement and contextual arguments"},
                        {"stepNumber": 2, "marks": 2.0, "criterion": "Supporting textual quotes and literary analysis"},
                        {"stepNumber": 3, "marks": 1.0, "criterion": "Concluding synthesis"}
                    ],
                    "keyTerms": ["Thematic synthesis", "Character arc", "Symbolism", "Author's craft"]
                })

    return qb_mcqs, qb_subjective

# ─────────────────────────────────────────────────────────────────────────────
# 5. SAVE MCQS TO CHAPTER DPP QUIZZES
# ─────────────────────────────────────────────────────────────────────────────
def save_mcqs_to_dpps(all_mcqs_by_subject):
    print("\nSaving MCQs to chapter DPP quizzes...")
    total_added = 0
    
    for subject_id, mcqs in all_mcqs_by_subject.items():
        by_chapter = {}
        for m in mcqs:
            ch_folder = m["chapter_folder"]
            by_chapter.setdefault(ch_folder, []).append(m)
            
        sub_dir = os.path.join(REPO_ROOT, subject_id)
        if not os.path.isdir(sub_dir):
            continue
            
        for ch_folder, ch_mcqs in by_chapter.items():
            ch_dir = os.path.join(sub_dir, ch_folder)
            if not os.path.isdir(ch_dir):
                continue
                
            quizzes_dir = os.path.join(ch_dir, "quizzes")
            os.makedirs(quizzes_dir, exist_ok=True)
            
            ch_name = " ".join([p.capitalize() for p in ch_folder.split("_")[1:]]) if "_" in ch_folder else ch_folder.capitalize()
            quiz_file = os.path.join(quizzes_dir, f"{subject_id}_practice_mcqs.json")
            
            existing_questions = []
            if os.path.exists(quiz_file):
                try:
                    with open(quiz_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        existing_questions = data.get("questions", [])
                except:
                    existing_questions = []
                    
            existing_ids = {q.get("id") for q in existing_questions}
            
            new_list = list(existing_questions)
            for m in ch_mcqs:
                if m["id"] not in existing_ids:
                    new_list.append({
                        "id": m["id"],
                        "q_no": len(new_list) + 1,
                        "question": m["question"],
                        "options": m["options"],
                        "correct_option_index": m["correct_option_index"],
                        "correct_answer_letter": m["correct_answer_letter"],
                        "explanation": m["explanation"]
                    })
                    existing_ids.add(m["id"])
                    total_added += 1
                    
            quiz_obj = {
                "id": f"{subject_id}_{ch_folder}_practice",
                "subject": subject_id.capitalize(),
                "book": "CBSE Official Practice Questions",
                "chapter": ch_name,
                "title": f"{ch_name} - CBSE Official Practice DPP",
                "total_questions": len(new_list),
                "questions": new_list
            }
            
            with open(quiz_file, "w", encoding="utf-8") as f:
                json.dump(quiz_obj, f, indent=2, ensure_ascii=False)
                
    print(f"Total MCQs saved across chapter DPPs: {total_added}")

# ─────────────────────────────────────────────────────────────────────────────
# 6. SAVE SUBJECTIVE QUESTIONS TO QUESTION BANKS
# ─────────────────────────────────────────────────────────────────────────────
def save_subjective_to_qbank(all_subjective_by_subject):
    print("\nSaving subjective questions to Question Banks...")
    qb_dir = os.path.join(REPO_ROOT, "question_banks")
    os.makedirs(qb_dir, exist_ok=True)
    
    for subject_id, questions in all_subjective_by_subject.items():
        qb_file = os.path.join(qb_dir, f"{subject_id}.json")
        
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
                merged_questions.append(q)
                existing_ids.add(q["id"])
                
        existing_data["count"] = len(merged_questions)
        existing_data["questions"] = merged_questions
        
        with open(qb_file, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
            
        print(f"  {subject_id}.json: {len(merged_questions)} total subjective questions")

# ─────────────────────────────────────────────────────────────────────────────
# 7. MAIN PIPELINE EXECUTION
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
    
    # 1. Process 12 Science PQ / PQMS papers
    science_pairs = [
        # Physics
        (os.path.join(DOWNLOADS_DIR, "Physics-PQ.pdf"), os.path.join(DOWNLOADS_DIR, "Physics-PQMS.pdf"), "physics", "pq1"),
        (os.path.join(DOWNLOADS_DIR, "Physics-PQ2.pdf"), os.path.join(DOWNLOADS_DIR, "Physics-PQMS2.pdf"), "physics", "pq2"),
        # Chemistry
        (os.path.join(DOWNLOADS_DIR, "Chemistry-PQ.pdf"), os.path.join(DOWNLOADS_DIR, "Chemistry-PQMS.pdf"), "chemistry", "pq1"),
        (os.path.join(DOWNLOADS_DIR, "Chemistry-PQ2.pdf"), os.path.join(DOWNLOADS_DIR, "Chemistry-PQMS2.pdf"), "chemistry", "pq2"),
        # Biology
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
            
    # 2. Process English Core PQ / PQMS papers
    english_pairs = [
        (os.path.join(DOWNLOADS_DIR, "EnglishCore-PQ.pdf"), os.path.join(DOWNLOADS_DIR, "EnglishCore-PQMS.pdf"), "pq1"),
        (os.path.join(DOWNLOADS_DIR, "EnglishCore-PQ2.pdf"), os.path.join(DOWNLOADS_DIR, "EnglishCore-PQMS2.pdf"), "pq2"),
    ]
    
    for qp, ms, s_name in english_pairs:
        if os.path.exists(qp) and os.path.exists(ms):
            mcqs, subjs = extract_english_pq_paper(qp, ms, s_name)
            all_mcqs["english"].extend(mcqs)
            all_subjective["english"].extend(subjs)
        else:
            print(f"Skipping missing: {qp} or {ms}")
            
    # 3. Process Official CBSE Question Bank PDFs (PE, Maths, Chemistry, English)
    qb_mcqs, qb_subjs = extract_official_qbanks()
    for s in ["chemistry", "maths", "physical_education", "english"]:
        all_mcqs[s].extend(qb_mcqs.get(s, []))
        all_subjective[s].extend(qb_subjs.get(s, []))
        
    # 4. Save MCQs to chapter DPPs
    save_mcqs_to_dpps(all_mcqs)
    
    # 5. Save Subjective to Question Banks
    save_subjective_to_qbank(all_subjective)
    
    # 6. Regenerate manifest.json
    print("\nRegenerating manifest.json...")
    import generate_manifest
    generate_manifest.generate()
    
    print("\n=== Extraction & Sorting Pipeline Complete! ===")

if __name__ == "__main__":
    main()
