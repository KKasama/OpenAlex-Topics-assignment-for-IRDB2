# 全手法比較レポート（正解ラベル対照・階層別）

**正解ラベル件数:** 97 件  

---

## 1. サマリ

| 手法 | n | Primary一致 | Top-3 Hit | Subfield一致 | Field一致 | Domain一致 | Avg Score |
|---|---|---|---|---|---|---|---|
| OpenAlex現行 | 97 | **5.2%** | 7.2% | 9.3% | 17.5% | 38.1% | 0.1636 |
| 公式mBERT(openalex前処理) | 97 | **12.4%** | 15.5% | 14.4% | 23.7% | 41.2% | 0.1547 |
| 公式mBERT(日本語保持) | 97 | **26.8%** | 38.1% | 34.0% | 51.5% | 73.2% | 0.3102 |
| v2 ensemble | 97 | **22.7%** | 35.1% | 27.8% | 53.6% | 78.4% | 0.6613 |
| v5 e5-large | 97 | **25.8%** | 41.2% | 37.1% | 58.8% | 78.4% | 0.7469 |

---

## 2. 詳細（Primary Topic 比較 — 先頭 30 件）

| # | 正解 Topic | 手法 | 付与 Topic | P | T3 | SF | F | D |
|---|---|---|---|---|---|---|---|---|
| 1 | Migration and Labor Dynamics | OpenAlex現行 | Military Technology and Strategies | ❌ | ❌ | ❌ | ❌ | ❌ |
| 1 | Migration and Labor Dynamics | 公式mBERT(openalex前処理) | Educational Robotics and Engineerin | ❌ | ❌ | ❌ | ❌ | ❌ |
| 1 | Migration and Labor Dynamics | 公式mBERT(日本語保持) | Migration and Labor Dynamics | ✅ | ✅ | ✅ | ✅ | ✅ |
| 1 | Migration and Labor Dynamics | v2 ensemble | Evasion and Academic Success Factor | ❌ | ✅ | ❌ | ✅ | ✅ |
| 1 | Migration and Labor Dynamics | v5 e5-large | Employment and Welfare Studies | ❌ | ❌ | ❌ | ❌ | ❌ |
| 2 | Insect behavior and control techniq | OpenAlex現行 | Insect behavior and control techniq | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2 | Insect behavior and control techniq | 公式mBERT(openalex前処理) | Insect behavior and control techniq | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2 | Insect behavior and control techniq | 公式mBERT(日本語保持) | Insect behavior and control techniq | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2 | Insect behavior and control techniq | v2 ensemble | Insect behavior and control techniq | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2 | Insect behavior and control techniq | v5 e5-large | Insect behavior and control techniq | ✅ | ✅ | ✅ | ✅ | ✅ |
| 3 | earthquake and tectonic studies | OpenAlex現行 | Military Technology and Strategies | ❌ | ❌ | ❌ | ❌ | ✅ |
| 3 | earthquake and tectonic studies | 公式mBERT(openalex前処理) | Educational Robotics and Engineerin | ❌ | ❌ | ❌ | ❌ | ✅ |
| 3 | earthquake and tectonic studies | 公式mBERT(日本語保持) | earthquake and tectonic studies | ✅ | ✅ | ✅ | ✅ | ✅ |
| 3 | earthquake and tectonic studies | v2 ensemble | Blasting Impact and Analysis | ❌ | ❌ | ❌ | ❌ | ✅ |
| 3 | earthquake and tectonic studies | v5 e5-large | Statistical Methods and Bayesian In | ❌ | ❌ | ❌ | ❌ | ✅ |
| 4 | Intellectual Property Law | OpenAlex現行 | Intellectual Property and Patents | ❌ | ❌ | ❌ | ❌ | ✅ |
| 4 | Intellectual Property Law | 公式mBERT(openalex前処理) | Legal Cases and Commentary | ❌ | ❌ | ❌ | ❌ | ❌ |
| 4 | Intellectual Property Law | 公式mBERT(日本語保持) | Intellectual Property and Patents | ❌ | ❌ | ❌ | ❌ | ✅ |
| 4 | Intellectual Property Law | v2 ensemble | Legal Cases and Commentary | ❌ | ❌ | ❌ | ❌ | ❌ |
| 4 | Intellectual Property Law | v5 e5-large | Legal Cases and Commentary | ❌ | ❌ | ❌ | ❌ | ❌ |
| 5 | Educator Training and Historical Pe | OpenAlex現行 | Educational Research and Pedagogy | ❌ | ❌ | ❌ | ❌ | ❌ |
| 5 | Educator Training and Historical Pe | 公式mBERT(openalex前処理) | Education, Safety, and Science Stud | ❌ | ❌ | ❌ | ✅ | ✅ |
| 5 | Educator Training and Historical Pe | 公式mBERT(日本語保持) | Educational Robotics and Engineerin | ❌ | ❌ | ❌ | ❌ | ❌ |
| 5 | Educator Training and Historical Pe | v2 ensemble | Innovative Teaching Methodologies i | ❌ | ❌ | ❌ | ✅ | ✅ |
| 5 | Educator Training and Historical Pe | v5 e5-large | Evaluation of Teaching Practices | ❌ | ❌ | ❌ | ✅ | ✅ |
| 6 | Fish Biology and Ecology Studies | OpenAlex現行 | Agriculture and Biological Studies | ❌ | ❌ | ❌ | ✅ | ✅ |
| 6 | Fish Biology and Ecology Studies | 公式mBERT(openalex前処理) | Ichthyology and Marine Biology | ❌ | ❌ | ❌ | ❌ | ❌ |
| 6 | Fish Biology and Ecology Studies | 公式mBERT(日本語保持) | Ichthyology and Marine Biology | ❌ | ❌ | ❌ | ❌ | ❌ |
| 6 | Fish Biology and Ecology Studies | v2 ensemble | Subterranean biodiversity and taxon | ❌ | ❌ | ❌ | ❌ | ❌ |
| 6 | Fish Biology and Ecology Studies | v5 e5-large | Fish biology, ecology, and behavior | ❌ | ❌ | ❌ | ❌ | ❌ |
| 7 | earthquake and tectonic studies | OpenAlex現行 | Military Technology and Strategies | ❌ | ❌ | ❌ | ❌ | ✅ |
| 7 | earthquake and tectonic studies | 公式mBERT(openalex前処理) | Academic Publishing and Open Access | ❌ | ❌ | ❌ | ❌ | ❌ |
| 7 | earthquake and tectonic studies | 公式mBERT(日本語保持) | Earthquake and Disaster Impact Stud | ❌ | ✅ | ❌ | ❌ | ❌ |
| 7 | earthquake and tectonic studies | v2 ensemble | Earthquake and Disaster Impact Stud | ❌ | ❌ | ❌ | ❌ | ❌ |
| 7 | earthquake and tectonic studies | v5 e5-large | Earthquake Detection and Analysis | ❌ | ✅ | ✅ | ✅ | ✅ |
| 8 | Plant Pathogens and Fungal Diseases | OpenAlex現行 | Fungal Biology and Applications | ❌ | ❌ | ❌ | ❌ | ❌ |
| 8 | Plant Pathogens and Fungal Diseases | 公式mBERT(openalex前処理) | Yeasts and Rust Fungi Studies | ❌ | ❌ | ❌ | ✅ | ✅ |
| 8 | Plant Pathogens and Fungal Diseases | 公式mBERT(日本語保持) | Yeasts and Rust Fungi Studies | ❌ | ❌ | ❌ | ✅ | ✅ |
| 8 | Plant Pathogens and Fungal Diseases | v2 ensemble | Fermentation and Sensory Analysis | ❌ | ❌ | ❌ | ❌ | ✅ |
| 8 | Plant Pathogens and Fungal Diseases | v5 e5-large | Fermentation and Sensory Analysis | ❌ | ❌ | ❌ | ❌ | ✅ |
| 9 | Geological and Geophysical Studies | OpenAlex現行 | Military Technology and Strategies | ❌ | ❌ | ❌ | ❌ | ✅ |
| 9 | Geological and Geophysical Studies | 公式mBERT(openalex前処理) | Academic Publishing and Open Access | ❌ | ❌ | ❌ | ❌ | ❌ |
| 9 | Geological and Geophysical Studies | 公式mBERT(日本語保持) | Geotourism and Geoheritage Conserva | ❌ | ❌ | ✅ | ✅ | ✅ |
| 9 | Geological and Geophysical Studies | v2 ensemble | Library Collection Development and  | ❌ | ❌ | ❌ | ❌ | ✅ |
| 9 | Geological and Geophysical Studies | v5 e5-large | Cold Fusion and Nuclear Reactions | ❌ | ❌ | ❌ | ✅ | ✅ |
| 10 | earthquake and tectonic studies | OpenAlex現行 | Military Technology and Strategies | ❌ | ❌ | ❌ | ❌ | ✅ |
| 10 | earthquake and tectonic studies | 公式mBERT(openalex前処理) | Academic Publishing and Open Access | ❌ | ❌ | ❌ | ❌ | ❌ |
| 10 | earthquake and tectonic studies | 公式mBERT(日本語保持) | Earthquake and Tsunami Effects | ❌ | ✅ | ❌ | ❌ | ✅ |
| 10 | earthquake and tectonic studies | v2 ensemble | Library Collection Development and  | ❌ | ❌ | ❌ | ❌ | ✅ |
| 10 | earthquake and tectonic studies | v5 e5-large | earthquake and tectonic studies | ✅ | ✅ | ✅ | ✅ | ✅ |
| 11 | Topological and Geometric Data Anal | OpenAlex現行 | Topological and Geometric Data Anal | ✅ | ✅ | ✅ | ✅ | ✅ |
| 11 | Topological and Geometric Data Anal | 公式mBERT(openalex前処理) | Topological and Geometric Data Anal | ✅ | ✅ | ✅ | ✅ | ✅ |
| 11 | Topological and Geometric Data Anal | 公式mBERT(日本語保持) | Topological and Geometric Data Anal | ✅ | ✅ | ✅ | ✅ | ✅ |
| 11 | Topological and Geometric Data Anal | v2 ensemble | Topological and Geometric Data Anal | ✅ | ✅ | ✅ | ✅ | ✅ |
| 11 | Topological and Geometric Data Anal | v5 e5-large | Topological and Geometric Data Anal | ✅ | ✅ | ✅ | ✅ | ✅ |
| 12 | Simulation-Based Education in Healt | OpenAlex現行 | Military Technology and Strategies | ❌ | ❌ | ❌ | ❌ | ❌ |
| 12 | Simulation-Based Education in Healt | 公式mBERT(openalex前処理) | Simulation-Based Education in Healt | ✅ | ✅ | ✅ | ✅ | ✅ |
| 12 | Simulation-Based Education in Healt | 公式mBERT(日本語保持) | Simulation-Based Education in Healt | ✅ | ✅ | ✅ | ✅ | ✅ |
| 12 | Simulation-Based Education in Healt | v2 ensemble | Surgical Simulation and Training | ❌ | ✅ | ❌ | ✅ | ✅ |
| 12 | Simulation-Based Education in Healt | v5 e5-large | Empathy and Medical Education | ❌ | ✅ | ❌ | ✅ | ✅ |
| 13 | Psychometric Methodologies and Test | OpenAlex現行 | Health and Wellbeing Research | ❌ | ❌ | ❌ | ❌ | ❌ |
| 13 | Psychometric Methodologies and Test | 公式mBERT(openalex前処理) | Sport Psychology and Performance | ❌ | ❌ | ❌ | ❌ | ✅ |
| 13 | Psychometric Methodologies and Test | 公式mBERT(日本語保持) | Sport Psychology and Performance | ❌ | ❌ | ❌ | ❌ | ✅ |
| 13 | Psychometric Methodologies and Test | v2 ensemble | Psychometric Methodologies and Test | ✅ | ✅ | ✅ | ✅ | ✅ |
| 13 | Psychometric Methodologies and Test | v5 e5-large | Psychometric Methodologies and Test | ✅ | ✅ | ✅ | ✅ | ✅ |
| 14 | Advanced Mathematical Modeling in E | OpenAlex現行 | Military Technology and Strategies | ❌ | ❌ | ❌ | ❌ | ✅ |
| 14 | Advanced Mathematical Modeling in E | 公式mBERT(openalex前処理) | Educational Robotics and Engineerin | ❌ | ❌ | ❌ | ✅ | ✅ |
| 14 | Advanced Mathematical Modeling in E | 公式mBERT(日本語保持) | Advanced Physical and Chemical Mole | ❌ | ❌ | ❌ | ❌ | ✅ |
| 14 | Advanced Mathematical Modeling in E | v2 ensemble | High-Energy Particle Collisions Res | ❌ | ❌ | ❌ | ❌ | ✅ |
| 14 | Advanced Mathematical Modeling in E | v5 e5-large | High-Energy Particle Collisions Res | ❌ | ❌ | ❌ | ❌ | ✅ |
| 15 | Psychological Well-being and Life S | OpenAlex現行 | Military Technology and Strategies | ❌ | ❌ | ❌ | ❌ | ❌ |
| 15 | Psychological Well-being and Life S | 公式mBERT(openalex前処理) | Educational Robotics and Engineerin | ❌ | ❌ | ❌ | ❌ | ❌ |
| 15 | Psychological Well-being and Life S | 公式mBERT(日本語保持) | Psychological Well-being and Life S | ✅ | ✅ | ✅ | ✅ | ✅ |
| 15 | Psychological Well-being and Life S | v2 ensemble | Health, psychology, and well-being | ❌ | ❌ | ❌ | ❌ | ❌ |
| 15 | Psychological Well-being and Life S | v5 e5-large | Health, psychology, and well-being | ❌ | ✅ | ❌ | ❌ | ❌ |
| 16 | Museums and Cultural Heritage | OpenAlex現行 | Climate Change Communication and Pe | ❌ | ❌ | ❌ | ❌ | ✅ |
| 16 | Museums and Cultural Heritage | 公式mBERT(openalex前処理) | Climate Change Communication and Pe | ❌ | ❌ | ❌ | ❌ | ✅ |
| 16 | Museums and Cultural Heritage | 公式mBERT(日本語保持) | Climate Change Communication and Pe | ❌ | ❌ | ❌ | ❌ | ✅ |
| 16 | Museums and Cultural Heritage | v2 ensemble | Museums and Cultural Heritage | ✅ | ✅ | ✅ | ✅ | ✅ |
| 16 | Museums and Cultural Heritage | v5 e5-large | Multidisciplinary Science and Engin | ❌ | ❌ | ❌ | ❌ | ✅ |
| 17 | Vietnamese History and Culture Stud | OpenAlex現行 | Military Technology and Strategies | ❌ | ❌ | ❌ | ❌ | ❌ |
| 17 | Vietnamese History and Culture Stud | 公式mBERT(openalex前処理) | Educational Robotics and Engineerin | ❌ | ❌ | ❌ | ❌ | ❌ |
| 17 | Vietnamese History and Culture Stud | 公式mBERT(日本語保持) | Financial Crisis of the 21st Centur | ❌ | ❌ | ❌ | ❌ | ✅ |
| 17 | Vietnamese History and Culture Stud | v2 ensemble | Architecture and Cultural Influence | ❌ | ❌ | ❌ | ❌ | ✅ |
| 17 | Vietnamese History and Culture Stud | v5 e5-large | Memory, Trauma, and Commemoration | ❌ | ❌ | ❌ | ❌ | ✅ |
| 18 | Anxiety, Depression, Psychometrics, | OpenAlex現行 | Healthcare and Venom Research | ❌ | ❌ | ❌ | ❌ | ❌ |
| 18 | Anxiety, Depression, Psychometrics, | 公式mBERT(openalex前処理) | Anxiety, Depression, Psychometrics, | ✅ | ✅ | ✅ | ✅ | ✅ |
| 18 | Anxiety, Depression, Psychometrics, | 公式mBERT(日本語保持) | Anxiety, Depression, Psychometrics, | ✅ | ✅ | ✅ | ✅ | ✅ |
| 18 | Anxiety, Depression, Psychometrics, | v2 ensemble | Anxiety, Depression, Psychometrics, | ✅ | ✅ | ✅ | ✅ | ✅ |
| 18 | Anxiety, Depression, Psychometrics, | v5 e5-large | Anxiety, Depression, Psychometrics, | ✅ | ✅ | ✅ | ✅ | ✅ |
| 19 | Animal Behavior and Reproduction | OpenAlex現行 | Military Technology and Strategies | ❌ | ❌ | ❌ | ❌ | ❌ |
| 19 | Animal Behavior and Reproduction | 公式mBERT(openalex前処理) | Educational Robotics and Engineerin | ❌ | ❌ | ❌ | ❌ | ❌ |
| 19 | Animal Behavior and Reproduction | 公式mBERT(日本語保持) | Reproductive biology and impacts on | ❌ | ❌ | ❌ | ❌ | ✅ |
| 19 | Animal Behavior and Reproduction | v2 ensemble | Pregnancy-related medical research | ❌ | ❌ | ❌ | ❌ | ❌ |
| 19 | Animal Behavior and Reproduction | v5 e5-large | Marine Invertebrate Physiology and  | ❌ | ❌ | ❌ | ❌ | ❌ |
| 20 | Soil Carbon and Nitrogen Dynamics | OpenAlex現行 | Military Technology and Strategies | ❌ | ❌ | ❌ | ❌ | ❌ |
| 20 | Soil Carbon and Nitrogen Dynamics | 公式mBERT(openalex前処理) | Educational Robotics and Engineerin | ❌ | ❌ | ❌ | ❌ | ❌ |
| 20 | Soil Carbon and Nitrogen Dynamics | 公式mBERT(日本語保持) | Soil Carbon and Nitrogen Dynamics | ✅ | ✅ | ✅ | ✅ | ✅ |
| 20 | Soil Carbon and Nitrogen Dynamics | v2 ensemble | Nitrogen and Sulfur Effects on Bras | ❌ | ❌ | ❌ | ❌ | ✅ |
| 20 | Soil Carbon and Nitrogen Dynamics | v5 e5-large | Environmental and biological studie | ❌ | ❌ | ❌ | ❌ | ❌ |
| 21 | Language, Discourse, Communication  | OpenAlex現行 | Military Technology and Strategies | ❌ | ❌ | ❌ | ❌ | ❌ |
| 21 | Language, Discourse, Communication  | 公式mBERT(openalex前処理) | Pharmacy and Medical Practices | ❌ | ❌ | ❌ | ❌ | ❌ |
| 21 | Language, Discourse, Communication  | 公式mBERT(日本語保持) | Educational Robotics and Engineerin | ❌ | ✅ | ❌ | ❌ | ❌ |
| 21 | Language, Discourse, Communication  | v2 ensemble | Language, Discourse, Communication  | ✅ | ✅ | ✅ | ✅ | ✅ |
| 21 | Language, Discourse, Communication  | v5 e5-large | Language, Discourse, Communication  | ✅ | ✅ | ✅ | ✅ | ✅ |
| 22 | Phonetics and Phonology Research | OpenAlex現行 | Military Technology and Strategies | ❌ | ❌ | ❌ | ❌ | ❌ |
| 22 | Phonetics and Phonology Research | 公式mBERT(openalex前処理) | Educational Robotics and Engineerin | ❌ | ❌ | ❌ | ❌ | ❌ |
| 22 | Phonetics and Phonology Research | 公式mBERT(日本語保持) | Phonetics and Phonology Research | ✅ | ✅ | ✅ | ✅ | ✅ |
| 22 | Phonetics and Phonology Research | v2 ensemble | Speech and dialogue systems | ❌ | ❌ | ❌ | ❌ | ❌ |
| 22 | Phonetics and Phonology Research | v5 e5-large | Linguistic Studies and Language Acq | ❌ | ❌ | ❌ | ❌ | ❌ |
| 23 | Urban Planning and Governance | OpenAlex現行 | Political and Economic history of U | ❌ | ❌ | ❌ | ✅ | ✅ |
| 23 | Urban Planning and Governance | 公式mBERT(openalex前処理) | Urban Planning and Governance | ✅ | ✅ | ✅ | ✅ | ✅ |
| 23 | Urban Planning and Governance | 公式mBERT(日本語保持) | Urban Planning and Governance | ✅ | ✅ | ✅ | ✅ | ✅ |
| 23 | Urban Planning and Governance | v2 ensemble | Urban Planning and Governance | ✅ | ✅ | ✅ | ✅ | ✅ |
| 23 | Urban Planning and Governance | v5 e5-large | Urban Planning and Landscape Design | ❌ | ✅ | ❌ | ❌ | ❌ |
| 24 | Free Will and Agency | OpenAlex現行 | Seventeenth-Century Political and P | ❌ | ❌ | ❌ | ❌ | ❌ |
| 24 | Free Will and Agency | 公式mBERT(openalex前処理) | Seventeenth-Century Political and P | ❌ | ❌ | ❌ | ❌ | ❌ |
| 24 | Free Will and Agency | 公式mBERT(日本語保持) | Seventeenth-Century Political and P | ❌ | ❌ | ❌ | ❌ | ❌ |
| 24 | Free Will and Agency | v2 ensemble | Psychoanalysis, Philosophy, and Pol | ❌ | ❌ | ❌ | ❌ | ❌ |
| 24 | Free Will and Agency | v5 e5-large | Education, Healthcare and Sociology | ❌ | ❌ | ❌ | ❌ | ❌ |
| 25 | Political Conflict and Governance | OpenAlex現行 | Historical Geopolitical and Social  | ❌ | ❌ | ❌ | ✅ | ✅ |
| 25 | Political Conflict and Governance | 公式mBERT(openalex前処理) | Cambodian History and Society | ❌ | ✅ | ✅ | ✅ | ✅ |
| 25 | Political Conflict and Governance | 公式mBERT(日本語保持) | Japanese History and Culture | ❌ | ✅ | ❌ | ✅ | ✅ |
| 25 | Political Conflict and Governance | v2 ensemble | University Challenges and Reforms | ❌ | ❌ | ❌ | ✅ | ✅ |
| 25 | Political Conflict and Governance | v5 e5-large | Corruption and Economic Development | ❌ | ❌ | ✅ | ✅ | ✅ |
| 26 | Phenomenology and Existential Philo | OpenAlex現行 | Philosophical and Theoretical Analy | ❌ | ❌ | ❌ | ❌ | ✅ |
| 26 | Phenomenology and Existential Philo | 公式mBERT(openalex前処理) | Philosophical and Theoretical Analy | ❌ | ✅ | ❌ | ❌ | ✅ |
| 26 | Phenomenology and Existential Philo | 公式mBERT(日本語保持) | Phenomenology and Existential Philo | ✅ | ✅ | ✅ | ✅ | ✅ |
| 26 | Phenomenology and Existential Philo | v2 ensemble | Modern American Literature Studies | ❌ | ❌ | ❌ | ❌ | ✅ |
| 26 | Phenomenology and Existential Philo | v5 e5-large | Phenomenology and Existential Philo | ✅ | ✅ | ✅ | ✅ | ✅ |
| 27 | Educator Training and Historical Pe | OpenAlex現行 | Military Technology and Strategies | ❌ | ❌ | ❌ | ❌ | ❌ |
| 27 | Educator Training and Historical Pe | 公式mBERT(openalex前処理) | Educator Training and Historical Pe | ✅ | ✅ | ✅ | ✅ | ✅ |
| 27 | Educator Training and Historical Pe | 公式mBERT(日本語保持) | Educational Robotics and Engineerin | ❌ | ❌ | ❌ | ❌ | ❌ |
| 27 | Educator Training and Historical Pe | v2 ensemble | Teacher Professional Development an | ❌ | ❌ | ❌ | ✅ | ✅ |
| 27 | Educator Training and Historical Pe | v5 e5-large | Higher Education Practises and Enga | ❌ | ✅ | ❌ | ✅ | ✅ |
| 28 | Diverse Music Education Insights | OpenAlex現行 | Military Technology and Strategies | ❌ | ❌ | ❌ | ❌ | ❌ |
| 28 | Diverse Music Education Insights | 公式mBERT(openalex前処理) | Diverse Music Education Insights | ✅ | ✅ | ✅ | ✅ | ✅ |
| 28 | Diverse Music Education Insights | 公式mBERT(日本語保持) | Japanese History and Culture | ❌ | ✅ | ❌ | ❌ | ✅ |
| 28 | Diverse Music Education Insights | v2 ensemble | Diverse Music Education Insights | ✅ | ✅ | ✅ | ✅ | ✅ |
| 28 | Diverse Music Education Insights | v5 e5-large | Diverse Music Education Insights | ✅ | ✅ | ✅ | ✅ | ✅ |
| 29 | Teacher Professional Development an | OpenAlex現行 | Military Technology and Strategies | ❌ | ❌ | ❌ | ❌ | ❌ |
| 29 | Teacher Professional Development an | 公式mBERT(openalex前処理) | Educational Robotics and Engineerin | ❌ | ❌ | ❌ | ❌ | ❌ |
| 29 | Teacher Professional Development an | 公式mBERT(日本語保持) | Educational Robotics and Engineerin | ❌ | ❌ | ❌ | ❌ | ❌ |
| 29 | Teacher Professional Development an | v2 ensemble | Educational Curriculum and Learning | ❌ | ❌ | ✅ | ✅ | ✅ |
| 29 | Teacher Professional Development an | v5 e5-large | Evaluation of Teaching Practices | ❌ | ❌ | ✅ | ✅ | ✅ |
| 30 | Death, Funerary Practices, and Mour | OpenAlex現行 | Military Technology and Strategies | ❌ | ❌ | ❌ | ❌ | ❌ |
| 30 | Death, Funerary Practices, and Mour | 公式mBERT(openalex前処理) | Educational Robotics and Engineerin | ❌ | ❌ | ❌ | ❌ | ❌ |
| 30 | Death, Funerary Practices, and Mour | 公式mBERT(日本語保持) | Japanese History and Culture | ❌ | ❌ | ❌ | ✅ | ✅ |
| 30 | Death, Funerary Practices, and Mour | v2 ensemble | Death, Funerary Practices, and Mour | ✅ | ✅ | ✅ | ✅ | ✅ |
| 30 | Death, Funerary Practices, and Mour | v5 e5-large | Death, Funerary Practices, and Mour | ✅ | ✅ | ✅ | ✅ | ✅ |

---

*作成：笠間和喜（iGroup Japan）/ 2026-08-22*