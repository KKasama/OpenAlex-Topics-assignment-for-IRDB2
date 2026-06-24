# v1 / v2 / v3 手法比較レポート（正解ラベル対照）

**正解ラベル件数:** 97 件  

---

## 1. サマリ

| 手法 | 対照件数 | Primary一致率 | Top-3 Hit率 | 平均スコア |
|---|---|---|---|---|
| v1（embedding） | 97 件 | **20.6%** | 34.0% | 0.8094 |
| v2（ensemble） | 97 件 | **22.7%** | 35.1% | 0.7491 |
| v4-Gemini+e5 | 97 件 | **22.7%** | 37.1% | 0.7428 |
| v5-e5-large（翻訳なし） | 97 件 | **25.8%** | 41.2% | 0.7469 |

---

## 2. 詳細結果（全件）

### v1（embedding）

| # | タイトル（抜粋） | 正解 Topic | 本手法 Topic | Primary一致 | Top-3 |
|---|---|---|---|---|---|
| 1 | 経済危機と在日ブラジル人--何が大量失業・帰国をもたらしたのか | Migration and Labor Dynamics | Evasion and Academic Success F | ❌ | ✅ |
| 2 | ミカンバエの防除に関する研究 1 : その防除に必要な二・三の基礎的調 | Insect behavior and control te | Insect behavior and control te | ✅ | ✅ |
| 3 | 6．地震の規模別度数の統計式log n=a-bMの係数bを求める一方法 | earthquake and tectonic studie | Blasting Impact and Analysis | ❌ | ❌ |
| 4 | Patentable Subject Matter After May | Intellectual Property Law | Legal Cases and Commentary | ❌ | ❌ |
| 5 | 学部生の社会科教育観の変容に関する一考察 : 社会科教員養成科目(教科 | Educator Training and Historic | Innovative Teaching Methodolog | ❌ | ❌ |
| 6 | 日本産フサカサゴ科オニカサゴ属魚類(Scorpaenidae: Sco | Fish Biology and Ecology Studi | Subterranean biodiversity and  | ❌ | ❌ |
| 7 | 日本付近のM6.0以上の地震および被害地震の表 : 1885年～198 | earthquake and tectonic studie | Earthquake and Disaster Impact | ❌ | ❌ |
| 8 | 分裂酵母菌の一新種 (Schizosaccharomyces Japo | Plant Pathogens and Fungal Dis | Fermentation and Sensory Analy | ❌ | ❌ |
| 9 | 21. 東伊豆沖海底火山群 : その2-および伊豆諸島近海海底火山 | Geological and Geophysical Stu | Ecology, Conservation, and Geo | ❌ | ❌ |
| 10 | 西津軽・男鹿間における歴史地震(1694～1810)の震度・津波調査 | earthquake and tectonic studie | Earthquake and Disaster Impact | ❌ | ❌ |
| 11 | 書評「T. Kaczynski, K. Mischaikow, and | Topological and Geometric Data | Algebraic structures and combi | ❌ | ✅ |
| 12 | 看護基礎教育における模擬患者参加型教育方法の実態に関する文献的考察 : | Simulation-Based Education in  | Simulation-Based Education in  | ✅ | ✅ |
| 13 | 運動に伴う改訂版ポジティブ感情尺度 (MCL-S.2) の信頼性と妥当 | Psychometric Methodologies and | Psychometric Methodologies and | ✅ | ✅ |
| 14 | 大型の凝集粒子（マリンスノー）生成の実験的研究 | Advanced Mathematical Modeling | High-Energy Particle Collision | ❌ | ❌ |
| 15 | 主観的厚生に関する相対所得仮説の検証―幸福感・健康感・信頼感― | Psychological Well-being and L | Health, psychology, and well-b | ❌ | ❌ |
| 16 | サイエンスカフェ参加者のセグメンテーションとターゲティング : 「科学 | Museums and Cultural Heritage | Multimedia Communication and T | ❌ | ❌ |
| 17 | 植民都市におけるホテルにみる文化構築の動態 : ベトナム・ダラットを事 | Vietnamese History and Culture | Architecture and Cultural Infl | ❌ | ❌ |
| 18 | Patient Health Questionnaire (PHQ-9 | Anxiety, Depression, Psychomet | COVID-19 and Mental Health | ❌ | ✅ |
| 19 | メダカOryzias latipesの放卵機序〔英文〕 | Animal Behavior and Reproducti | Pregnancy-related medical rese | ❌ | ❌ |
| 20 | 北海道東部のミズナラ造林地における土壌の炭素および窒素の蓄積様式 :  | Soil Carbon and Nitrogen Dynam | Nitrogen and Sulfur Effects on | ❌ | ❌ |
| 21 | 〈論文〉接触場面初対面会話における話題スキーマ : 日本の大学における | Language, Discourse, Communica | Language, Discourse, Communica | ✅ | ✅ |
| 22 | カムチベット語瓊波／沖倉 [Khyungpo/Khromtshang] | Phonetics and Phonology Resear | Speech and dialogue systems | ❌ | ❌ |
| 23 | 書評 : 都市政治論の視角とその可能性（Jonathan S. Dav | Urban Planning and Governance | Urban Planning and Governance | ✅ | ✅ |
| 24 | ＜文献紹介＞ シャンタル・ジャケ著『スピノザにおける活動力の表現』Ja | Free Will and Agency | Psychoanalysis, Philosophy, an | ❌ | ❌ |
| 25 | Economic Origins of Dictatorship an | Political Conflict and Governa | Educational Technology and Opt | ❌ | ❌ |
| 26 | ＜文献紹介＞ エティエンヌ・バンブネ著 『自然と人間性　メルロ= ポン | Phenomenology and Existential  | Posthumanist Ethics and Activi | ❌ | ❌ |
| 27 | 大学生の社会科観・授業構成力の変容に差が生じる理由 : 同一の教員養成 | Educator Training and Historic | Education Pedagogy and Practic | ❌ | ✅ |
| 28 | 雑誌『音楽界』に見る明治・大正期の音楽教育の実態に関する研究 : 唱歌 | Diverse Music Education Insigh | Music Education and Analysis | ❌ | ❌ |
| 29 | 教職課程後半期における教員志望学生の社会科観・授業構成力の形成過程 : | Teacher Professional Developme | Educational Curriculum and Lea | ❌ | ❌ |
| 30 | 死と「迷惑」―現代日本における死生観の実情― | Death, Funerary Practices, and | Death, Funerary Practices, and | ✅ | ✅ |
| 31 | 北海道における地殻，上部マントルの熱的構造：総合報告 | High-pressure geophysics and m | High-pressure geophysics and m | ✅ | ✅ |
| 32 | 「性の多様性を認める態度」を促進する要因 : セクシュアルマジョリティ | LGBTQ Health, Identity, and Po | LGBTQ Health, Identity, and Po | ✅ | ✅ |
| 33 | アメリカ災害社会科学の系譜と研究動向 : 災害研究センター（DRC）を | Disaster Management and Resili | Social impacts of COVID-19 | ❌ | ❌ |
| 34 | 17世紀に千島・日本海溝で発生した巨大地震 (特集:「巨大地震と火山活 | earthquake and tectonic studie | Earthquake and Disaster Impact | ❌ | ❌ |
| 35 | 縞葉枯病抵抗性で糖含有率が高い稲発酵粗飼料専用品種「つきすずか」の育成 | Plant Disease Resistance and G | Genetic and Environmental Crop | ❌ | ❌ |
| 36 | 第4回 Keio-Gachon NRI ジョイントシンポジウム(201 | Neuroscience and Neuropharmaco | Dielectric properties of ceram | ❌ | ❌ |
| 37 | 『明教新誌』解題 : 創刊から明治21年頃までを中心に | Japanese History and Culture | Medical History and Innovation | ❌ | ❌ |
| 38 | 戦後日本の行政学研究の定量的検討 : 『年報行政研究』（1962～20 | Computational and Text Analysi | Public Policy and Administrati | ❌ | ❌ |
| 39 | 防災科研Hi-net 地中地震計設置方位情報推定方法の改良 | Geophysics and Sensor Technolo | Landslides and related hazards | ❌ | ❌ |
| 40 | 令和元年（2019 年）東日本台風による斜面崩壊地の岩石・土層物性：特 | Landslides and related hazards | Geotechnical and Geomechanical | ❌ | ✅ |
| 41 | 新型コロナウイルス感染症（COVID-19）パンデミックが大学生のメン | COVID-19 and Mental Health | COVID-19 and Mental Health | ✅ | ✅ |
| 42 | Evolution, development and educatio | Developmental and Educational  | Child and Animal Learning Deve | ❌ | ❌ |
| 43 | 宮崎演習林における樹木群集のα，β，γ多様度と標高との関係に地形が及ぼ | Forest Ecology and Biodiversit | Urban and spatial planning | ❌ | ❌ |
| 44 | 1722-2010年にわたる菅平高原の草原面積変遷の定性・定量分析：国 | Urban and spatial planning | Urban and spatial planning | ✅ | ✅ |
| 45 | 新型コロナウイルス感染症の流行に伴う「自粛警察」についての一考察 :  | Crime, Deviance, and Social Co | Discourse Analysis and Cultura | ❌ | ❌ |
| 46 | 日本の造形美と「和」の精神 : 修学旅行での生きた芸術鑑賞のために(各 | Art Education and Development | Museums and Cultural Heritage | ❌ | ❌ |
| 47 | 沖縄県におけるウコンの植付時期が、出芽、生育および収量に及ぼす影響 | Flowering Plant Growth and Cul | Genetics and Plant Breeding | ❌ | ✅ |
| 48 | 余呉湖・湖沼堆積物解析から推定される後期完新世の湖沼 : 流域系水文環 | Marine and environmental studi | Aquatic Ecosystems and Phytopl | ❌ | ❌ |
| 49 | 九州産スギ在来品種および精英樹のMuPS(multiplex-PCR  | Genetic Mapping and Diversity  | Plant pathogens and resistance | ❌ | ❌ |
| 50 | ＜書評＞ Francois Recanati, Direct Refe | Philosophy and Historical Thou | Philosophy and Literary Analys | ❌ | ❌ |
| 51 | ＜書評＞ Michael Gardiner, The Dialogic | Russian Literature and Bakhtin | Russian Literature and Bakhtin | ✅ | ✅ |
| 52 | 日英語「話法」の比較 : 日本語における「話法」とは | Linguistic research and analys | Speech and dialogue systems | ❌ | ❌ |
| 53 | 縄文時代の急激な環境変動期における生態系復原と人間の適応 : 八戸・上 | Archaeology and ancient enviro | Soil and Environmental Studies | ❌ | ❌ |
| 54 | 地域運営組織の体制に関する一考察　ー地域の主要なアクターとなりえるかー | Public Administration and Poli | Urban and spatial planning | ❌ | ❌ |
| 55 | 日本におけるカロリー価格指数と栄養素価格指数の長期的推計 | Economics of Agriculture and F | Economics of Agriculture and F | ✅ | ✅ |
| 56 | 東北北部の縄文前期人口の変動と火山噴火 | Archaeology and ancient enviro | Archaeology and ancient enviro | ✅ | ✅ |
| 57 | 生態水文学研究所赤津研究林白坂南北谷小流域日流出量観測報告（Ⅲ）（自2 | Hydrology and Watershed Manage | Urban and spatial planning | ❌ | ❌ |
| 58 | スイスドイツ語圏における歴史教師のビリーフ研究に関する考察 ―日本での | Educator Training and Historic | Historical Education Studies W | ❌ | ❌ |
| 59 | 東京大学北海道演習林における2011～2020年の樹木フェノロジーデー | Forest ecology and management | Forest, Soil, and Plant Ecolog | ❌ | ❌ |
| 60 | 4ステップコーディングによる質的データ分析手法SCATの提案　―着手し | Qualitative Research Methods a | Computational and Text Analysi | ❌ | ✅ |
| 61 | 仮説的抽出法を用いた高速鉄道輸送が地域間に与える経済波及効果分析 ―中 | Regional Economic and Spatial  | Transport and Economic Policie | ❌ | ✅ |
| 62 | カムチベット語捧八［Phongpa］方言の方言系統 | Language, Linguistics, Cultura | Urban and spatial planning | ❌ | ❌ |
| 63 | 日本の社会科教育研究における「授業観」の方法論的考察 : 「理論と実践 | Educational theories and pract | Educational theories and pract | ✅ | ✅ |
| 64 | 協同的に説明的文章を読み解くことによって自己の更新を促し，書くことにお | Writing and Handwriting Educat | Innovative Teaching and Learni | ❌ | ❌ |
| 65 | 小学校の英語教育における絵本活用の在り方―ことばへの気づきに焦点をあて | EFL/ESL Teaching and Learning | English Language Learning and  | ❌ | ❌ |
| 66 | 大学における教育支援の公平性の確保 : 合理的配慮を必要とする学生への | Higher Education Research Stud | Disability Education and Emplo | ❌ | ❌ |
| 67 | カムチベット語尼西/開香 [Khrezhag] 方言の方言特徴と語彙 | Language, Linguistics, Cultura | Language, Linguistics, Cultura | ✅ | ✅ |
| 68 | マンション住民と地域とのコミュニティ形成促進に関する研究 | Place Attachment and Urban Stu | Korean Urban and Social Studie | ❌ | ❌ |
| 69 | 大阪湾周辺府県における海岸漂着物処理推進施策 | Coastal and Marine Management | Coastal Management and Develop | ❌ | ❌ |
| 70 | 中堅教諭の社会科指導における困り感の抽出 : X教諭を事例として | Educator Training and Historic | Education in Rural Contexts | ❌ | ❌ |
| 71 | 若者の性の問題化の構造――保健体育科教科書における性感染症の記述を例に | Gender, Sexuality, and Educati | Adolescent Sexual and Reproduc | ❌ | ❌ |
| 72 | 歴史教師のビリーフに関する研究方法論の考察 : ビリーフ調査の質問項目 | Educator Training and Historic | Teacher Education and Leadersh | ❌ | ❌ |
| 73 | 小中学校における英語絵本の読み聞かせの方法とその効果について | EFL/ESL Teaching and Learning | Second Language Learning and T | ❌ | ❌ |
| 74 | 炎症性腸疾患患者における国内の看護研究の動向と看護課題（研究ノート） | Nursing care and research | Viral-associated cancers and d | ❌ | ❌ |
| 75 | 生態水文学研究所赤津研究林白坂南北谷小流域日流出量観測報告（Ⅱ）（自2 | Hydrology and Watershed Manage | Urban and spatial planning | ❌ | ❌ |
| 76 | 小学校社会科教師における信念と教材開発過程の解明 | Educator Training and Historic | Educational Curriculum and Lea | ❌ | ❌ |
| 77 | アニメーション的な誤配としての多重見当識――非対人性愛的な「二次元」へ | Psychoanalysis, Philosophy, an | Cybernetics and Technology in  | ❌ | ❌ |
| 78 | 職業訓練の効果測定における脱落の影響 | Human Resource Development and | Psychological Treatments and A | ❌ | ❌ |
| 79 | 日韓の国際選挙支援 : アジア型援助モデルに関する議論の観点から | International Development and  | Asian Industrial and Economic  | ❌ | ✅ |
| 80 | 津波シミュレータTNSの開発 | Simulation and Modeling Applic | Electromagnetic Simulation and | ❌ | ❌ |
| 81 | 臨地実習における看護系大学生のレジリエンス： フォーカスグループインタ | Focus Groups and Qualitative M | Problem Solving Skills Develop | ❌ | ❌ |
| 82 | 看護師のレジリエンスの概念分析 | Healthcare Education and Workf | Nursing education and manageme | ❌ | ✅ |
| 83 | 生態水文学研究所穴の宮試験流域日流出量観測結果報告（自2017年1月至 | Hydrology and Watershed Manage | Urban and spatial planning | ❌ | ❌ |
| 84 | フィリピン人日本語学習者のデータを基にした非漢字圏学習者向け語彙テスト | EFL/ESL Teaching and Learning | EFL/ESL Teaching and Learning | ✅ | ✅ |
| 85 | 宮崎演習林・樫葉国有林の有剣ハチ類 | Hymenoptera taxonomy and phylo | Insect behavior and control te | ❌ | ❌ |
| 86 | 曖昧さへの態度と⼼理的な問題解決の関連 ーレジリエンス及びコーピング⽅ | Problem Solving Skills Develop | Student Stress and Coping | ❌ | ✅ |
| 87 | 産業部門間の連関性指標の概説と地域経済への応用例 | Regional Economic and Spatial  | Global Trade and Competitivene | ❌ | ✅ |
| 88 | 小学校英語活動における英語絵本の活用に関する研究 : 児童の発達段階に | EFL/ESL Teaching and Learning | Reading and Literacy Developme | ❌ | ❌ |
| 89 | 東日本大震災を踏まえた地震ハザード評価の改良に向けた検討 | Seismic Performance and Analys | Evaluation Methods in Various  | ❌ | ❌ |
| 90 | 小学校社会科の単元展開における教師の実践的思考の研究 : 教師にとって | Educational Assessment and Imp | Early Childhood Education and  | ❌ | ✅ |
| 91 | 1940年代仏領インドシナの公共事業政策 : ドクーの政策と都市・建築 | Architecture and Cultural Infl | Urban and spatial planning | ❌ | ❌ |
| 92 | 地域在住外国人に対する日本語ボランティアの養成シラバス | Second Language Learning and T | Tourism, Volunteerism, and Dev | ❌ | ❌ |
| 93 | 日本における新型コロナ感染症による死亡について | COVID-19 and healthcare impact | COVID-19 and healthcare impact | ✅ | ✅ |
| 94 | 日本における異文化間カウンセリング研究の動向と展望 : スコーピングレ | Counseling Practices and Super | Counseling Practices and Super | ✅ | ✅ |
| 95 | あいち医療通訳システム利用経験をもつ医療従事者の語りからみえる医療通訳 | Interpreting and Communication | Interpreting and Communication | ✅ | ✅ |
| 96 | Health Locus of Controlによる保健行動予測の試み | Health and Wellbeing Research | Health and Wellbeing Research | ✅ | ✅ |
| 97 | 論考 地域日本語教室の5つの機能と研修プログラム : 豊かな学びと人間 | French Language Learning Metho | Foreign Language Teaching Meth | ❌ | ❌ |

### v2（ensemble）

| # | タイトル（抜粋） | 正解 Topic | 本手法 Topic | Primary一致 | Top-3 |
|---|---|---|---|---|---|
| 1 | 経済危機と在日ブラジル人--何が大量失業・帰国をもたらしたのか | Migration and Labor Dynamics | Evasion and Academic Success F | ❌ | ✅ |
| 2 | ミカンバエの防除に関する研究 1 : その防除に必要な二・三の基礎的調 | Insect behavior and control te | Insect behavior and control te | ✅ | ✅ |
| 3 | 6．地震の規模別度数の統計式log n=a-bMの係数bを求める一方法 | earthquake and tectonic studie | Blasting Impact and Analysis | ❌ | ❌ |
| 4 | Patentable Subject Matter After May | Intellectual Property Law | Legal Cases and Commentary | ❌ | ❌ |
| 5 | 学部生の社会科教育観の変容に関する一考察 : 社会科教員養成科目(教科 | Educator Training and Historic | Innovative Teaching Methodolog | ❌ | ❌ |
| 6 | 日本産フサカサゴ科オニカサゴ属魚類(Scorpaenidae: Sco | Fish Biology and Ecology Studi | Subterranean biodiversity and  | ❌ | ❌ |
| 7 | 日本付近のM6.0以上の地震および被害地震の表 : 1885年～198 | earthquake and tectonic studie | Earthquake and Disaster Impact | ❌ | ❌ |
| 8 | 分裂酵母菌の一新種 (Schizosaccharomyces Japo | Plant Pathogens and Fungal Dis | Fermentation and Sensory Analy | ❌ | ❌ |
| 9 | 21. 東伊豆沖海底火山群 : その2-および伊豆諸島近海海底火山 | Geological and Geophysical Stu | Library Collection Development | ❌ | ❌ |
| 10 | 西津軽・男鹿間における歴史地震(1694～1810)の震度・津波調査 | earthquake and tectonic studie | Library Collection Development | ❌ | ❌ |
| 11 | 書評「T. Kaczynski, K. Mischaikow, and | Topological and Geometric Data | Topological and Geometric Data | ✅ | ✅ |
| 12 | 看護基礎教育における模擬患者参加型教育方法の実態に関する文献的考察 : | Simulation-Based Education in  | Surgical Simulation and Traini | ❌ | ✅ |
| 13 | 運動に伴う改訂版ポジティブ感情尺度 (MCL-S.2) の信頼性と妥当 | Psychometric Methodologies and | Psychometric Methodologies and | ✅ | ✅ |
| 14 | 大型の凝集粒子（マリンスノー）生成の実験的研究 | Advanced Mathematical Modeling | High-Energy Particle Collision | ❌ | ❌ |
| 15 | 主観的厚生に関する相対所得仮説の検証―幸福感・健康感・信頼感― | Psychological Well-being and L | Health, psychology, and well-b | ❌ | ❌ |
| 16 | サイエンスカフェ参加者のセグメンテーションとターゲティング : 「科学 | Museums and Cultural Heritage | Museums and Cultural Heritage | ✅ | ✅ |
| 17 | 植民都市におけるホテルにみる文化構築の動態 : ベトナム・ダラットを事 | Vietnamese History and Culture | Architecture and Cultural Infl | ❌ | ❌ |
| 18 | Patient Health Questionnaire (PHQ-9 | Anxiety, Depression, Psychomet | Anxiety, Depression, Psychomet | ✅ | ✅ |
| 19 | メダカOryzias latipesの放卵機序〔英文〕 | Animal Behavior and Reproducti | Pregnancy-related medical rese | ❌ | ❌ |
| 20 | 北海道東部のミズナラ造林地における土壌の炭素および窒素の蓄積様式 :  | Soil Carbon and Nitrogen Dynam | Nitrogen and Sulfur Effects on | ❌ | ❌ |
| 21 | 〈論文〉接触場面初対面会話における話題スキーマ : 日本の大学における | Language, Discourse, Communica | Language, Discourse, Communica | ✅ | ✅ |
| 22 | カムチベット語瓊波／沖倉 [Khyungpo/Khromtshang] | Phonetics and Phonology Resear | Speech and dialogue systems | ❌ | ❌ |
| 23 | 書評 : 都市政治論の視角とその可能性（Jonathan S. Dav | Urban Planning and Governance | Urban Planning and Governance | ✅ | ✅ |
| 24 | ＜文献紹介＞ シャンタル・ジャケ著『スピノザにおける活動力の表現』Ja | Free Will and Agency | Psychoanalysis, Philosophy, an | ❌ | ❌ |
| 25 | Economic Origins of Dictatorship an | Political Conflict and Governa | University Challenges and Refo | ❌ | ❌ |
| 26 | ＜文献紹介＞ エティエンヌ・バンブネ著 『自然と人間性　メルロ= ポン | Phenomenology and Existential  | Modern American Literature Stu | ❌ | ❌ |
| 27 | 大学生の社会科観・授業構成力の変容に差が生じる理由 : 同一の教員養成 | Educator Training and Historic | Teacher Professional Developme | ❌ | ❌ |
| 28 | 雑誌『音楽界』に見る明治・大正期の音楽教育の実態に関する研究 : 唱歌 | Diverse Music Education Insigh | Diverse Music Education Insigh | ✅ | ✅ |
| 29 | 教職課程後半期における教員志望学生の社会科観・授業構成力の形成過程 : | Teacher Professional Developme | Educational Curriculum and Lea | ❌ | ❌ |
| 30 | 死と「迷惑」―現代日本における死生観の実情― | Death, Funerary Practices, and | Death, Funerary Practices, and | ✅ | ✅ |
| 31 | 北海道における地殻，上部マントルの熱的構造：総合報告 | High-pressure geophysics and m | High-pressure geophysics and m | ✅ | ✅ |
| 32 | 「性の多様性を認める態度」を促進する要因 : セクシュアルマジョリティ | LGBTQ Health, Identity, and Po | African Sexualities and LGBTQ+ | ❌ | ✅ |
| 33 | アメリカ災害社会科学の系譜と研究動向 : 災害研究センター（DRC）を | Disaster Management and Resili | Social impacts of COVID-19 | ❌ | ❌ |
| 34 | 17世紀に千島・日本海溝で発生した巨大地震 (特集:「巨大地震と火山活 | earthquake and tectonic studie | Earthquake and Disaster Impact | ❌ | ❌ |
| 35 | 縞葉枯病抵抗性で糖含有率が高い稲発酵粗飼料専用品種「つきすずか」の育成 | Plant Disease Resistance and G | Genetic and Environmental Crop | ❌ | ❌ |
| 36 | 第4回 Keio-Gachon NRI ジョイントシンポジウム(201 | Neuroscience and Neuropharmaco | Dielectric properties of ceram | ❌ | ❌ |
| 37 | 『明教新誌』解題 : 創刊から明治21年頃までを中心に | Japanese History and Culture | Medical History and Innovation | ❌ | ❌ |
| 38 | 戦後日本の行政学研究の定量的検討 : 『年報行政研究』（1962～20 | Computational and Text Analysi | Public Policy and Administrati | ❌ | ❌ |
| 39 | 防災科研Hi-net 地中地震計設置方位情報推定方法の改良 | Geophysics and Sensor Technolo | Landslides and related hazards | ❌ | ❌ |
| 40 | 令和元年（2019 年）東日本台風による斜面崩壊地の岩石・土層物性：特 | Landslides and related hazards | Geotechnical and Geomechanical | ❌ | ✅ |
| 41 | 新型コロナウイルス感染症（COVID-19）パンデミックが大学生のメン | COVID-19 and Mental Health | COVID-19 and Mental Health | ✅ | ✅ |
| 42 | Evolution, development and educatio | Developmental and Educational  | Child and Animal Learning Deve | ❌ | ❌ |
| 43 | 宮崎演習林における樹木群集のα，β，γ多様度と標高との関係に地形が及ぼ | Forest Ecology and Biodiversit | Urban and spatial planning | ❌ | ❌ |
| 44 | 1722-2010年にわたる菅平高原の草原面積変遷の定性・定量分析：国 | Urban and spatial planning | Urban and spatial planning | ✅ | ✅ |
| 45 | 新型コロナウイルス感染症の流行に伴う「自粛警察」についての一考察 :  | Crime, Deviance, and Social Co | Discourse Analysis and Cultura | ❌ | ❌ |
| 46 | 日本の造形美と「和」の精神 : 修学旅行での生きた芸術鑑賞のために(各 | Art Education and Development | Museums and Cultural Heritage | ❌ | ❌ |
| 47 | 沖縄県におけるウコンの植付時期が、出芽、生育および収量に及ぼす影響 | Flowering Plant Growth and Cul | Genetics and Plant Breeding | ❌ | ✅ |
| 48 | 余呉湖・湖沼堆積物解析から推定される後期完新世の湖沼 : 流域系水文環 | Marine and environmental studi | Aquatic Ecosystems and Phytopl | ❌ | ❌ |
| 49 | 九州産スギ在来品種および精英樹のMuPS(multiplex-PCR  | Genetic Mapping and Diversity  | Plant pathogens and resistance | ❌ | ❌ |
| 50 | ＜書評＞ Francois Recanati, Direct Refe | Philosophy and Historical Thou | Philosophy and Literary Analys | ❌ | ❌ |
| 51 | ＜書評＞ Michael Gardiner, The Dialogic | Russian Literature and Bakhtin | Critical Theory and Philosophy | ❌ | ✅ |
| 52 | 日英語「話法」の比較 : 日本語における「話法」とは | Linguistic research and analys | Speech and dialogue systems | ❌ | ❌ |
| 53 | 縄文時代の急激な環境変動期における生態系復原と人間の適応 : 八戸・上 | Archaeology and ancient enviro | Soil and Environmental Studies | ❌ | ❌ |
| 54 | 地域運営組織の体制に関する一考察　ー地域の主要なアクターとなりえるかー | Public Administration and Poli | Urban and spatial planning | ❌ | ❌ |
| 55 | 日本におけるカロリー価格指数と栄養素価格指数の長期的推計 | Economics of Agriculture and F | Economics of Agriculture and F | ✅ | ✅ |
| 56 | 東北北部の縄文前期人口の変動と火山噴火 | Archaeology and ancient enviro | Archaeology and ancient enviro | ✅ | ✅ |
| 57 | 生態水文学研究所赤津研究林白坂南北谷小流域日流出量観測報告（Ⅲ）（自2 | Hydrology and Watershed Manage | Urban and spatial planning | ❌ | ❌ |
| 58 | スイスドイツ語圏における歴史教師のビリーフ研究に関する考察 ―日本での | Educator Training and Historic | Historical Education Studies W | ❌ | ❌ |
| 59 | 東京大学北海道演習林における2011～2020年の樹木フェノロジーデー | Forest ecology and management | Educational Technology and E-L | ❌ | ❌ |
| 60 | 4ステップコーディングによる質的データ分析手法SCATの提案　―着手し | Qualitative Research Methods a | Qualitative Research Methods a | ✅ | ✅ |
| 61 | 仮説的抽出法を用いた高速鉄道輸送が地域間に与える経済波及効果分析 ―中 | Regional Economic and Spatial  | Transport and Economic Policie | ❌ | ✅ |
| 62 | カムチベット語捧八［Phongpa］方言の方言系統 | Language, Linguistics, Cultura | Library Collection Development | ❌ | ❌ |
| 63 | 日本の社会科教育研究における「授業観」の方法論的考察 : 「理論と実践 | Educational theories and pract | Educational theories and pract | ✅ | ✅ |
| 64 | 協同的に説明的文章を読み解くことによって自己の更新を促し，書くことにお | Writing and Handwriting Educat | Innovative Teaching and Learni | ❌ | ❌ |
| 65 | 小学校の英語教育における絵本活用の在り方―ことばへの気づきに焦点をあて | EFL/ESL Teaching and Learning | English Language Learning and  | ❌ | ❌ |
| 66 | 大学における教育支援の公平性の確保 : 合理的配慮を必要とする学生への | Higher Education Research Stud | Disability Education and Emplo | ❌ | ❌ |
| 67 | カムチベット語尼西/開香 [Khrezhag] 方言の方言特徴と語彙 | Language, Linguistics, Cultura | Language, Linguistics, Cultura | ✅ | ✅ |
| 68 | マンション住民と地域とのコミュニティ形成促進に関する研究 | Place Attachment and Urban Stu | Korean Urban and Social Studie | ❌ | ❌ |
| 69 | 大阪湾周辺府県における海岸漂着物処理推進施策 | Coastal and Marine Management | Coastal Management and Develop | ❌ | ❌ |
| 70 | 中堅教諭の社会科指導における困り感の抽出 : X教諭を事例として | Educator Training and Historic | Education in Rural Contexts | ❌ | ❌ |
| 71 | 若者の性の問題化の構造――保健体育科教科書における性感染症の記述を例に | Gender, Sexuality, and Educati | Adolescent Sexual and Reproduc | ❌ | ❌ |
| 72 | 歴史教師のビリーフに関する研究方法論の考察 : ビリーフ調査の質問項目 | Educator Training and Historic | Teacher Education and Leadersh | ❌ | ❌ |
| 73 | 小中学校における英語絵本の読み聞かせの方法とその効果について | EFL/ESL Teaching and Learning | Second Language Learning and T | ❌ | ❌ |
| 74 | 炎症性腸疾患患者における国内の看護研究の動向と看護課題（研究ノート） | Nursing care and research | Viral-associated cancers and d | ❌ | ❌ |
| 75 | 生態水文学研究所赤津研究林白坂南北谷小流域日流出量観測報告（Ⅱ）（自2 | Hydrology and Watershed Manage | Urban and spatial planning | ❌ | ❌ |
| 76 | 小学校社会科教師における信念と教材開発過程の解明 | Educator Training and Historic | Educational Curriculum and Lea | ❌ | ❌ |
| 77 | アニメーション的な誤配としての多重見当識――非対人性愛的な「二次元」へ | Psychoanalysis, Philosophy, an | Cybernetics and Technology in  | ❌ | ❌ |
| 78 | 職業訓練の効果測定における脱落の影響 | Human Resource Development and | Athletic Training and Educatio | ❌ | ❌ |
| 79 | 日韓の国際選挙支援 : アジア型援助モデルに関する議論の観点から | International Development and  | Asian Industrial and Economic  | ❌ | ✅ |
| 80 | 津波シミュレータTNSの開発 | Simulation and Modeling Applic | Electromagnetic Simulation and | ❌ | ❌ |
| 81 | 臨地実習における看護系大学生のレジリエンス： フォーカスグループインタ | Focus Groups and Qualitative M | Problem Solving Skills Develop | ❌ | ❌ |
| 82 | 看護師のレジリエンスの概念分析 | Healthcare Education and Workf | Nursing education and manageme | ❌ | ✅ |
| 83 | 生態水文学研究所穴の宮試験流域日流出量観測結果報告（自2017年1月至 | Hydrology and Watershed Manage | Urban and spatial planning | ❌ | ❌ |
| 84 | フィリピン人日本語学習者のデータを基にした非漢字圏学習者向け語彙テスト | EFL/ESL Teaching and Learning | EFL/ESL Teaching and Learning | ✅ | ✅ |
| 85 | 宮崎演習林・樫葉国有林の有剣ハチ類 | Hymenoptera taxonomy and phylo | Species Distribution and Clima | ❌ | ❌ |
| 86 | 曖昧さへの態度と⼼理的な問題解決の関連 ーレジリエンス及びコーピング⽅ | Problem Solving Skills Develop | Student Stress and Coping | ❌ | ✅ |
| 87 | 産業部門間の連関性指標の概説と地域経済への応用例 | Regional Economic and Spatial  | Global Trade and Competitivene | ❌ | ✅ |
| 88 | 小学校英語活動における英語絵本の活用に関する研究 : 児童の発達段階に | EFL/ESL Teaching and Learning | Reading and Literacy Developme | ❌ | ❌ |
| 89 | 東日本大震災を踏まえた地震ハザード評価の改良に向けた検討 | Seismic Performance and Analys | Evaluation Methods in Various  | ❌ | ❌ |
| 90 | 小学校社会科の単元展開における教師の実践的思考の研究 : 教師にとって | Educational Assessment and Imp | Early Childhood Education and  | ❌ | ✅ |
| 91 | 1940年代仏領インドシナの公共事業政策 : ドクーの政策と都市・建築 | Architecture and Cultural Infl | Urban and spatial planning | ❌ | ❌ |
| 92 | 地域在住外国人に対する日本語ボランティアの養成シラバス | Second Language Learning and T | Tourism, Volunteerism, and Dev | ❌ | ❌ |
| 93 | 日本における新型コロナ感染症による死亡について | COVID-19 and healthcare impact | COVID-19 and healthcare impact | ✅ | ✅ |
| 94 | 日本における異文化間カウンセリング研究の動向と展望 : スコーピングレ | Counseling Practices and Super | Counseling Practices and Super | ✅ | ✅ |
| 95 | あいち医療通訳システム利用経験をもつ医療従事者の語りからみえる医療通訳 | Interpreting and Communication | Interpreting and Communication | ✅ | ✅ |
| 96 | Health Locus of Controlによる保健行動予測の試み | Health and Wellbeing Research | Health and Wellbeing Research | ✅ | ✅ |
| 97 | 論考 地域日本語教室の5つの機能と研修プログラム : 豊かな学びと人間 | French Language Learning Metho | Foreign Language Teaching Meth | ❌ | ❌ |

### v4-Gemini+e5

| # | タイトル（抜粋） | 正解 Topic | 本手法 Topic | Primary一致 | Top-3 |
|---|---|---|---|---|---|
| 1 | 経済危機と在日ブラジル人--何が大量失業・帰国をもたらしたのか | Migration and Labor Dynamics | Evasion and Academic Success F | ❌ | ✅ |
| 2 | ミカンバエの防除に関する研究 1 : その防除に必要な二・三の基礎的調 | Insect behavior and control te | Insect behavior and control te | ✅ | ✅ |
| 3 | 6．地震の規模別度数の統計式log n=a-bMの係数bを求める一方法 | earthquake and tectonic studie | Blasting Impact and Analysis | ❌ | ❌ |
| 4 | Patentable Subject Matter After May | Intellectual Property Law | Legal Cases and Commentary | ❌ | ❌ |
| 5 | 学部生の社会科教育観の変容に関する一考察 : 社会科教員養成科目(教科 | Educator Training and Historic | Innovative Teaching Methodolog | ❌ | ❌ |
| 6 | 日本産フサカサゴ科オニカサゴ属魚類(Scorpaenidae: Sco | Fish Biology and Ecology Studi | Subterranean biodiversity and  | ❌ | ❌ |
| 7 | 日本付近のM6.0以上の地震および被害地震の表 : 1885年～198 | earthquake and tectonic studie | Radioactive contamination and  | ❌ | ❌ |
| 8 | 分裂酵母菌の一新種 (Schizosaccharomyces Japo | Plant Pathogens and Fungal Dis | Fermentation and Sensory Analy | ❌ | ❌ |
| 9 | 21. 東伊豆沖海底火山群 : その2-および伊豆諸島近海海底火山 | Geological and Geophysical Stu | Radioactive contamination and  | ❌ | ❌ |
| 10 | 西津軽・男鹿間における歴史地震(1694～1810)の震度・津波調査 | earthquake and tectonic studie | Geotechnical and Geomechanical | ❌ | ✅ |
| 11 | 書評「T. Kaczynski, K. Mischaikow, and | Topological and Geometric Data | Topological and Geometric Data | ✅ | ✅ |
| 12 | 看護基礎教育における模擬患者参加型教育方法の実態に関する文献的考察 : | Simulation-Based Education in  | Surgical Simulation and Traini | ❌ | ✅ |
| 13 | 運動に伴う改訂版ポジティブ感情尺度 (MCL-S.2) の信頼性と妥当 | Psychometric Methodologies and | Psychometric Methodologies and | ✅ | ✅ |
| 14 | 大型の凝集粒子（マリンスノー）生成の実験的研究 | Advanced Mathematical Modeling | High-Energy Particle Collision | ❌ | ❌ |
| 15 | 主観的厚生に関する相対所得仮説の検証―幸福感・健康感・信頼感― | Psychological Well-being and L | Health, psychology, and well-b | ❌ | ❌ |
| 16 | サイエンスカフェ参加者のセグメンテーションとターゲティング : 「科学 | Museums and Cultural Heritage | Museums and Cultural Heritage | ✅ | ✅ |
| 17 | 植民都市におけるホテルにみる文化構築の動態 : ベトナム・ダラットを事 | Vietnamese History and Culture | Architecture and Cultural Infl | ❌ | ❌ |
| 18 | Patient Health Questionnaire (PHQ-9 | Anxiety, Depression, Psychomet | Anxiety, Depression, Psychomet | ✅ | ✅ |
| 19 | メダカOryzias latipesの放卵機序〔英文〕 | Animal Behavior and Reproducti | Insect behavior and control te | ❌ | ❌ |
| 20 | 北海道東部のミズナラ造林地における土壌の炭素および窒素の蓄積様式 :  | Soil Carbon and Nitrogen Dynam | Nitrogen and Sulfur Effects on | ❌ | ❌ |
| 21 | 〈論文〉接触場面初対面会話における話題スキーマ : 日本の大学における | Language, Discourse, Communica | Language, Discourse, Communica | ✅ | ✅ |
| 22 | カムチベット語瓊波／沖倉 [Khyungpo/Khromtshang] | Phonetics and Phonology Resear | Speech and dialogue systems | ❌ | ❌ |
| 23 | 書評 : 都市政治論の視角とその可能性（Jonathan S. Dav | Urban Planning and Governance | Urban Planning and Governance | ✅ | ✅ |
| 24 | ＜文献紹介＞ シャンタル・ジャケ著『スピノザにおける活動力の表現』Ja | Free Will and Agency | Psychoanalysis, Philosophy, an | ❌ | ❌ |
| 25 | Economic Origins of Dictatorship an | Political Conflict and Governa | Corruption and Economic Develo | ❌ | ❌ |
| 26 | ＜文献紹介＞ エティエンヌ・バンブネ著 『自然と人間性　メルロ= ポン | Phenomenology and Existential  | Modern American Literature Stu | ❌ | ❌ |
| 27 | 大学生の社会科観・授業構成力の変容に差が生じる理由 : 同一の教員養成 | Educator Training and Historic | Teacher Professional Developme | ❌ | ❌ |
| 28 | 雑誌『音楽界』に見る明治・大正期の音楽教育の実態に関する研究 : 唱歌 | Diverse Music Education Insigh | Diverse Music Education Insigh | ✅ | ✅ |
| 29 | 教職課程後半期における教員志望学生の社会科観・授業構成力の形成過程 : | Teacher Professional Developme | Flow Experience in Various Fie | ❌ | ❌ |
| 30 | 死と「迷惑」―現代日本における死生観の実情― | Death, Funerary Practices, and | Death, Funerary Practices, and | ✅ | ✅ |
| 31 | 北海道における地殻，上部マントルの熱的構造：総合報告 | High-pressure geophysics and m | High-pressure geophysics and m | ✅ | ✅ |
| 32 | 「性の多様性を認める態度」を促進する要因 : セクシュアルマジョリティ | LGBTQ Health, Identity, and Po | African Sexualities and LGBTQ+ | ❌ | ✅ |
| 33 | アメリカ災害社会科学の系譜と研究動向 : 災害研究センター（DRC）を | Disaster Management and Resili | Social impacts of COVID-19 | ❌ | ❌ |
| 34 | 17世紀に千島・日本海溝で発生した巨大地震 (特集:「巨大地震と火山活 | earthquake and tectonic studie | Geotechnical and Geomechanical | ❌ | ❌ |
| 35 | 縞葉枯病抵抗性で糖含有率が高い稲発酵粗飼料専用品種「つきすずか」の育成 | Plant Disease Resistance and G | Genetic and Environmental Crop | ❌ | ❌ |
| 36 | 第4回 Keio-Gachon NRI ジョイントシンポジウム(201 | Neuroscience and Neuropharmaco | Dielectric properties of ceram | ❌ | ❌ |
| 37 | 『明教新誌』解題 : 創刊から明治21年頃までを中心に | Japanese History and Culture | Medical History and Innovation | ❌ | ❌ |
| 38 | 戦後日本の行政学研究の定量的検討 : 『年報行政研究』（1962～20 | Computational and Text Analysi | Public Policy and Administrati | ❌ | ❌ |
| 39 | 防災科研Hi-net 地中地震計設置方位情報推定方法の改良 | Geophysics and Sensor Technolo | Landslides and related hazards | ❌ | ❌ |
| 40 | 令和元年（2019 年）東日本台風による斜面崩壊地の岩石・土層物性：特 | Landslides and related hazards | Geotechnical and Geomechanical | ❌ | ✅ |
| 41 | 新型コロナウイルス感染症（COVID-19）パンデミックが大学生のメン | COVID-19 and Mental Health | COVID-19 and Mental Health | ✅ | ✅ |
| 42 | Evolution, development and educatio | Developmental and Educational  | Child and Animal Learning Deve | ❌ | ❌ |
| 43 | 宮崎演習林における樹木群集のα，β，γ多様度と標高との関係に地形が及ぼ | Forest Ecology and Biodiversit | Urban and spatial planning | ❌ | ❌ |
| 44 | 1722-2010年にわたる菅平高原の草原面積変遷の定性・定量分析：国 | Urban and spatial planning | Urban and spatial planning | ✅ | ✅ |
| 45 | 新型コロナウイルス感染症の流行に伴う「自粛警察」についての一考察 :  | Crime, Deviance, and Social Co | Discourse Analysis and Cultura | ❌ | ❌ |
| 46 | 日本の造形美と「和」の精神 : 修学旅行での生きた芸術鑑賞のために(各 | Art Education and Development | Cultural and Artistic Studies | ❌ | ❌ |
| 47 | 沖縄県におけるウコンの植付時期が、出芽、生育および収量に及ぼす影響 | Flowering Plant Growth and Cul | Genetics and Plant Breeding | ❌ | ✅ |
| 48 | 余呉湖・湖沼堆積物解析から推定される後期完新世の湖沼 : 流域系水文環 | Marine and environmental studi | Aquatic Ecosystems and Phytopl | ❌ | ❌ |
| 49 | 九州産スギ在来品種および精英樹のMuPS(multiplex-PCR  | Genetic Mapping and Diversity  | Plant pathogens and resistance | ❌ | ❌ |
| 50 | ＜書評＞ Francois Recanati, Direct Refe | Philosophy and Historical Thou | Philosophy and Literary Analys | ❌ | ❌ |
| 51 | ＜書評＞ Michael Gardiner, The Dialogic | Russian Literature and Bakhtin | Critical Theory and Philosophy | ❌ | ✅ |
| 52 | 日英語「話法」の比較 : 日本語における「話法」とは | Linguistic research and analys | Speech and dialogue systems | ❌ | ❌ |
| 53 | 縄文時代の急激な環境変動期における生態系復原と人間の適応 : 八戸・上 | Archaeology and ancient enviro | Soil and Environmental Studies | ❌ | ❌ |
| 54 | 地域運営組織の体制に関する一考察　ー地域の主要なアクターとなりえるかー | Public Administration and Poli | Urban and spatial planning | ❌ | ❌ |
| 55 | 日本におけるカロリー価格指数と栄養素価格指数の長期的推計 | Economics of Agriculture and F | Economics of Agriculture and F | ✅ | ✅ |
| 56 | 東北北部の縄文前期人口の変動と火山噴火 | Archaeology and ancient enviro | Archaeology and ancient enviro | ✅ | ✅ |
| 57 | 生態水文学研究所赤津研究林白坂南北谷小流域日流出量観測報告（Ⅲ）（自2 | Hydrology and Watershed Manage | Soil and Water Nutrient Dynami | ❌ | ❌ |
| 58 | スイスドイツ語圏における歴史教師のビリーフ研究に関する考察 ―日本での | Educator Training and Historic | Historical Education Studies W | ❌ | ❌ |
| 59 | 東京大学北海道演習林における2011～2020年の樹木フェノロジーデー | Forest ecology and management | Lymphadenopathy Diagnosis and  | ❌ | ✅ |
| 60 | 4ステップコーディングによる質的データ分析手法SCATの提案　―着手し | Qualitative Research Methods a | Qualitative Research Methods a | ✅ | ✅ |
| 61 | 仮説的抽出法を用いた高速鉄道輸送が地域間に与える経済波及効果分析 ―中 | Regional Economic and Spatial  | Transport and Economic Policie | ❌ | ✅ |
| 62 | カムチベット語捧八［Phongpa］方言の方言系統 | Language, Linguistics, Cultura | Discourse Analysis and Cultura | ❌ | ❌ |
| 63 | 日本の社会科教育研究における「授業観」の方法論的考察 : 「理論と実践 | Educational theories and pract | Educational theories and pract | ✅ | ✅ |
| 64 | 協同的に説明的文章を読み解くことによって自己の更新を促し，書くことにお | Writing and Handwriting Educat | Innovative Teaching and Learni | ❌ | ❌ |
| 65 | 小学校の英語教育における絵本活用の在り方―ことばへの気づきに焦点をあて | EFL/ESL Teaching and Learning | English Language Learning and  | ❌ | ❌ |
| 66 | 大学における教育支援の公平性の確保 : 合理的配慮を必要とする学生への | Higher Education Research Stud | Disability Education and Emplo | ❌ | ❌ |
| 67 | カムチベット語尼西/開香 [Khrezhag] 方言の方言特徴と語彙 | Language, Linguistics, Cultura | Language, Linguistics, Cultura | ✅ | ✅ |
| 68 | マンション住民と地域とのコミュニティ形成促進に関する研究 | Place Attachment and Urban Stu | Korean Urban and Social Studie | ❌ | ❌ |
| 69 | 大阪湾周辺府県における海岸漂着物処理推進施策 | Coastal and Marine Management | Coastal Management and Develop | ❌ | ❌ |
| 70 | 中堅教諭の社会科指導における困り感の抽出 : X教諭を事例として | Educator Training and Historic | Education in Rural Contexts | ❌ | ❌ |
| 71 | 若者の性の問題化の構造――保健体育科教科書における性感染症の記述を例に | Gender, Sexuality, and Educati | Adolescent Sexual and Reproduc | ❌ | ❌ |
| 72 | 歴史教師のビリーフに関する研究方法論の考察 : ビリーフ調査の質問項目 | Educator Training and Historic | Teacher Education and Leadersh | ❌ | ❌ |
| 73 | 小中学校における英語絵本の読み聞かせの方法とその効果について | EFL/ESL Teaching and Learning | Second Language Learning and T | ❌ | ❌ |
| 74 | 炎症性腸疾患患者における国内の看護研究の動向と看護課題（研究ノート） | Nursing care and research | Viral-associated cancers and d | ❌ | ❌ |
| 75 | 生態水文学研究所赤津研究林白坂南北谷小流域日流出量観測報告（Ⅱ）（自2 | Hydrology and Watershed Manage | Soil and Water Nutrient Dynami | ❌ | ❌ |
| 76 | 小学校社会科教師における信念と教材開発過程の解明 | Educator Training and Historic | Educational Curriculum and Lea | ❌ | ❌ |
| 77 | アニメーション的な誤配としての多重見当識――非対人性愛的な「二次元」へ | Psychoanalysis, Philosophy, an | Sexuality, Behavior, and Techn | ❌ | ❌ |
| 78 | 職業訓練の効果測定における脱落の影響 | Human Resource Development and | Athletic Training and Educatio | ❌ | ❌ |
| 79 | 日韓の国際選挙支援 : アジア型援助モデルに関する議論の観点から | International Development and  | Asian Industrial and Economic  | ❌ | ✅ |
| 80 | 津波シミュレータTNSの開発 | Simulation and Modeling Applic | Electromagnetic Simulation and | ❌ | ❌ |
| 81 | 臨地実習における看護系大学生のレジリエンス： フォーカスグループインタ | Focus Groups and Qualitative M | Problem Solving Skills Develop | ❌ | ❌ |
| 82 | 看護師のレジリエンスの概念分析 | Healthcare Education and Workf | Nursing education and manageme | ❌ | ✅ |
| 83 | 生態水文学研究所穴の宮試験流域日流出量観測結果報告（自2017年1月至 | Hydrology and Watershed Manage | Freshwater macroinvertebrate d | ❌ | ❌ |
| 84 | フィリピン人日本語学習者のデータを基にした非漢字圏学習者向け語彙テスト | EFL/ESL Teaching and Learning | EFL/ESL Teaching and Learning | ✅ | ✅ |
| 85 | 宮崎演習林・樫葉国有林の有剣ハチ類 | Hymenoptera taxonomy and phylo | Species Distribution and Clima | ❌ | ❌ |
| 86 | 曖昧さへの態度と⼼理的な問題解決の関連 ーレジリエンス及びコーピング⽅ | Problem Solving Skills Develop | Student Stress and Coping | ❌ | ✅ |
| 87 | 産業部門間の連関性指標の概説と地域経済への応用例 | Regional Economic and Spatial  | Global Trade and Competitivene | ❌ | ✅ |
| 88 | 小学校英語活動における英語絵本の活用に関する研究 : 児童の発達段階に | EFL/ESL Teaching and Learning | Reading and Literacy Developme | ❌ | ❌ |
| 89 | 東日本大震災を踏まえた地震ハザード評価の改良に向けた検討 | Seismic Performance and Analys | Evaluation Methods in Various  | ❌ | ❌ |
| 90 | 小学校社会科の単元展開における教師の実践的思考の研究 : 教師にとって | Educational Assessment and Imp | Early Childhood Education and  | ❌ | ✅ |
| 91 | 1940年代仏領インドシナの公共事業政策 : ドクーの政策と都市・建築 | Architecture and Cultural Infl | International Development and  | ❌ | ❌ |
| 92 | 地域在住外国人に対する日本語ボランティアの養成シラバス | Second Language Learning and T | Tourism, Volunteerism, and Dev | ❌ | ❌ |
| 93 | 日本における新型コロナ感染症による死亡について | COVID-19 and healthcare impact | COVID-19 and healthcare impact | ✅ | ✅ |
| 94 | 日本における異文化間カウンセリング研究の動向と展望 : スコーピングレ | Counseling Practices and Super | Counseling Practices and Super | ✅ | ✅ |
| 95 | あいち医療通訳システム利用経験をもつ医療従事者の語りからみえる医療通訳 | Interpreting and Communication | Interpreting and Communication | ✅ | ✅ |
| 96 | Health Locus of Controlによる保健行動予測の試み | Health and Wellbeing Research | Health and Wellbeing Research | ✅ | ✅ |
| 97 | 論考 地域日本語教室の5つの機能と研修プログラム : 豊かな学びと人間 | French Language Learning Metho | Foreign Language Teaching Meth | ❌ | ❌ |

### v5-e5-large（翻訳なし）

| # | タイトル（抜粋） | 正解 Topic | 本手法 Topic | Primary一致 | Top-3 |
|---|---|---|---|---|---|
| 1 | 経済危機と在日ブラジル人--何が大量失業・帰国をもたらしたのか | Migration and Labor Dynamics | Employment and Welfare Studies | ❌ | ❌ |
| 2 | ミカンバエの防除に関する研究 1 : その防除に必要な二・三の基礎的調 | Insect behavior and control te | Insect behavior and control te | ✅ | ✅ |
| 3 | 6．地震の規模別度数の統計式log n=a-bMの係数bを求める一方法 | earthquake and tectonic studie | Statistical Methods and Bayesi | ❌ | ❌ |
| 4 | Patentable Subject Matter After May | Intellectual Property Law | Legal Cases and Commentary | ❌ | ❌ |
| 5 | 学部生の社会科教育観の変容に関する一考察 : 社会科教員養成科目(教科 | Educator Training and Historic | Evaluation of Teaching Practic | ❌ | ❌ |
| 6 | 日本産フサカサゴ科オニカサゴ属魚類(Scorpaenidae: Sco | Fish Biology and Ecology Studi | Fish biology, ecology, and beh | ❌ | ❌ |
| 7 | 日本付近のM6.0以上の地震および被害地震の表 : 1885年～198 | earthquake and tectonic studie | Earthquake Detection and Analy | ❌ | ✅ |
| 8 | 分裂酵母菌の一新種 (Schizosaccharomyces Japo | Plant Pathogens and Fungal Dis | Fermentation and Sensory Analy | ❌ | ❌ |
| 9 | 21. 東伊豆沖海底火山群 : その2-および伊豆諸島近海海底火山 | Geological and Geophysical Stu | Cold Fusion and Nuclear Reacti | ❌ | ❌ |
| 10 | 西津軽・男鹿間における歴史地震(1694～1810)の震度・津波調査 | earthquake and tectonic studie | earthquake and tectonic studie | ✅ | ✅ |
| 11 | 書評「T. Kaczynski, K. Mischaikow, and | Topological and Geometric Data | Topological and Geometric Data | ✅ | ✅ |
| 12 | 看護基礎教育における模擬患者参加型教育方法の実態に関する文献的考察 : | Simulation-Based Education in  | Empathy and Medical Education | ❌ | ✅ |
| 13 | 運動に伴う改訂版ポジティブ感情尺度 (MCL-S.2) の信頼性と妥当 | Psychometric Methodologies and | Psychometric Methodologies and | ✅ | ✅ |
| 14 | 大型の凝集粒子（マリンスノー）生成の実験的研究 | Advanced Mathematical Modeling | High-Energy Particle Collision | ❌ | ❌ |
| 15 | 主観的厚生に関する相対所得仮説の検証―幸福感・健康感・信頼感― | Psychological Well-being and L | Health, psychology, and well-b | ❌ | ✅ |
| 16 | サイエンスカフェ参加者のセグメンテーションとターゲティング : 「科学 | Museums and Cultural Heritage | Multidisciplinary Science and  | ❌ | ❌ |
| 17 | 植民都市におけるホテルにみる文化構築の動態 : ベトナム・ダラットを事 | Vietnamese History and Culture | Memory, Trauma, and Commemorat | ❌ | ❌ |
| 18 | Patient Health Questionnaire (PHQ-9 | Anxiety, Depression, Psychomet | Anxiety, Depression, Psychomet | ✅ | ✅ |
| 19 | メダカOryzias latipesの放卵機序〔英文〕 | Animal Behavior and Reproducti | Marine Invertebrate Physiology | ❌ | ❌ |
| 20 | 北海道東部のミズナラ造林地における土壌の炭素および窒素の蓄積様式 :  | Soil Carbon and Nitrogen Dynam | Environmental and biological s | ❌ | ❌ |
| 21 | 〈論文〉接触場面初対面会話における話題スキーマ : 日本の大学における | Language, Discourse, Communica | Language, Discourse, Communica | ✅ | ✅ |
| 22 | カムチベット語瓊波／沖倉 [Khyungpo/Khromtshang] | Phonetics and Phonology Resear | Linguistic Studies and Languag | ❌ | ❌ |
| 23 | 書評 : 都市政治論の視角とその可能性（Jonathan S. Dav | Urban Planning and Governance | Urban Planning and Landscape D | ❌ | ✅ |
| 24 | ＜文献紹介＞ シャンタル・ジャケ著『スピノザにおける活動力の表現』Ja | Free Will and Agency | Education, Healthcare and Soci | ❌ | ❌ |
| 25 | Economic Origins of Dictatorship an | Political Conflict and Governa | Corruption and Economic Develo | ❌ | ❌ |
| 26 | ＜文献紹介＞ エティエンヌ・バンブネ著 『自然と人間性　メルロ= ポン | Phenomenology and Existential  | Phenomenology and Existential  | ✅ | ✅ |
| 27 | 大学生の社会科観・授業構成力の変容に差が生じる理由 : 同一の教員養成 | Educator Training and Historic | Higher Education Practises and | ❌ | ✅ |
| 28 | 雑誌『音楽界』に見る明治・大正期の音楽教育の実態に関する研究 : 唱歌 | Diverse Music Education Insigh | Diverse Music Education Insigh | ✅ | ✅ |
| 29 | 教職課程後半期における教員志望学生の社会科観・授業構成力の形成過程 : | Teacher Professional Developme | Evaluation of Teaching Practic | ❌ | ❌ |
| 30 | 死と「迷惑」―現代日本における死生観の実情― | Death, Funerary Practices, and | Death, Funerary Practices, and | ✅ | ✅ |
| 31 | 北海道における地殻，上部マントルの熱的構造：総合報告 | High-pressure geophysics and m | High-pressure geophysics and m | ✅ | ✅ |
| 32 | 「性の多様性を認める態度」を促進する要因 : セクシュアルマジョリティ | LGBTQ Health, Identity, and Po | African Sexualities and LGBTQ+ | ❌ | ✅ |
| 33 | アメリカ災害社会科学の系譜と研究動向 : 災害研究センター（DRC）を | Disaster Management and Resili | Earthquake and Disaster Impact | ❌ | ❌ |
| 34 | 17世紀に千島・日本海溝で発生した巨大地震 (特集:「巨大地震と火山活 | earthquake and tectonic studie | earthquake and tectonic studie | ✅ | ✅ |
| 35 | 縞葉枯病抵抗性で糖含有率が高い稲発酵粗飼料専用品種「つきすずか」の育成 | Plant Disease Resistance and G | Shallot Cultivation and Analys | ❌ | ❌ |
| 36 | 第4回 Keio-Gachon NRI ジョイントシンポジウム(201 | Neuroscience and Neuropharmaco | Coagulation, Bradykinin, Polyp | ❌ | ❌ |
| 37 | 『明教新誌』解題 : 創刊から明治21年頃までを中心に | Japanese History and Culture | Religion, Theology, History, J | ❌ | ❌ |
| 38 | 戦後日本の行政学研究の定量的検討 : 『年報行政研究』（1962～20 | Computational and Text Analysi | Public Policy and Administrati | ❌ | ❌ |
| 39 | 防災科研Hi-net 地中地震計設置方位情報推定方法の改良 | Geophysics and Sensor Technolo | Seismology and Earthquake Stud | ❌ | ❌ |
| 40 | 令和元年（2019 年）東日本台風による斜面崩壊地の岩石・土層物性：特 | Landslides and related hazards | Geotechnical and Geomechanical | ❌ | ❌ |
| 41 | 新型コロナウイルス感染症（COVID-19）パンデミックが大学生のメン | COVID-19 and Mental Health | COVID-19 and Mental Health | ✅ | ✅ |
| 42 | Evolution, development and educatio | Developmental and Educational  | Child and Animal Learning Deve | ❌ | ✅ |
| 43 | 宮崎演習林における樹木群集のα，β，γ多様度と標高との関係に地形が及ぼ | Forest Ecology and Biodiversit | Forest, Soil, and Plant Ecolog | ❌ | ❌ |
| 44 | 1722-2010年にわたる菅平高原の草原面積変遷の定性・定量分析：国 | Urban and spatial planning | Wildlife Ecology and Conservat | ❌ | ❌ |
| 45 | 新型コロナウイルス感染症の流行に伴う「自粛警察」についての一考察 :  | Crime, Deviance, and Social Co | Discourse Analysis and Cultura | ❌ | ❌ |
| 46 | 日本の造形美と「和」の精神 : 修学旅行での生きた芸術鑑賞のために(各 | Art Education and Development | Museums and Cultural Heritage | ❌ | ❌ |
| 47 | 沖縄県におけるウコンの植付時期が、出芽、生育および収量に及ぼす影響 | Flowering Plant Growth and Cul | Medicinal Plant Pharmacodynami | ❌ | ❌ |
| 48 | 余呉湖・湖沼堆積物解析から推定される後期完新世の湖沼 : 流域系水文環 | Marine and environmental studi | Freshwater macroinvertebrate d | ❌ | ❌ |
| 49 | 九州産スギ在来品種および精英樹のMuPS(multiplex-PCR  | Genetic Mapping and Diversity  | Research in Cotton Cultivation | ❌ | ✅ |
| 50 | ＜書評＞ Francois Recanati, Direct Refe | Philosophy and Historical Thou | Historical and Modern Theater  | ❌ | ❌ |
| 51 | ＜書評＞ Michael Gardiner, The Dialogic | Russian Literature and Bakhtin | Critical Theory and Philosophy | ❌ | ✅ |
| 52 | 日英語「話法」の比較 : 日本語における「話法」とは | Linguistic research and analys | Language, Discourse, Communica | ❌ | ✅ |
| 53 | 縄文時代の急激な環境変動期における生態系復原と人間の適応 : 八戸・上 | Archaeology and ancient enviro | Archaeology and ancient enviro | ✅ | ✅ |
| 54 | 地域運営組織の体制に関する一考察　ー地域の主要なアクターとなりえるかー | Public Administration and Poli | Korean Urban and Social Studie | ❌ | ❌ |
| 55 | 日本におけるカロリー価格指数と栄養素価格指数の長期的推計 | Economics of Agriculture and F | Economics of Agriculture and F | ✅ | ✅ |
| 56 | 東北北部の縄文前期人口の変動と火山噴火 | Archaeology and ancient enviro | Archaeology and ancient enviro | ✅ | ✅ |
| 57 | 生態水文学研究所赤津研究林白坂南北谷小流域日流出量観測報告（Ⅲ）（自2 | Hydrology and Watershed Manage | Environmental and biological s | ❌ | ❌ |
| 58 | スイスドイツ語圏における歴史教師のビリーフ研究に関する考察 ―日本での | Educator Training and Historic | Sociology and Education Studie | ❌ | ❌ |
| 59 | 東京大学北海道演習林における2011～2020年の樹木フェノロジーデー | Forest ecology and management | Forest ecology and management | ✅ | ✅ |
| 60 | 4ステップコーディングによる質的データ分析手法SCATの提案　―着手し | Qualitative Research Methods a | Qualitative Research Methods a | ✅ | ✅ |
| 61 | 仮説的抽出法を用いた高速鉄道輸送が地域間に与える経済波及効果分析 ―中 | Regional Economic and Spatial  | Belt and Road Initiative | ❌ | ❌ |
| 62 | カムチベット語捧八［Phongpa］方言の方言系統 | Language, Linguistics, Cultura | semigroups and automata theory | ❌ | ❌ |
| 63 | 日本の社会科教育研究における「授業観」の方法論的考察 : 「理論と実践 | Educational theories and pract | Innovative Teaching Methodolog | ❌ | ✅ |
| 64 | 協同的に説明的文章を読み解くことによって自己の更新を促し，書くことにお | Writing and Handwriting Educat | Literature, Culture, and Aesth | ❌ | ❌ |
| 65 | 小学校の英語教育における絵本活用の在り方―ことばへの気づきに焦点をあて | EFL/ESL Teaching and Learning | Linguistics and Language Analy | ❌ | ❌ |
| 66 | 大学における教育支援の公平性の確保 : 合理的配慮を必要とする学生への | Higher Education Research Stud | Behavioral and Psychological S | ❌ | ❌ |
| 67 | カムチベット語尼西/開香 [Khrezhag] 方言の方言特徴と語彙 | Language, Linguistics, Cultura | Language, Linguistics, Cultura | ✅ | ✅ |
| 68 | マンション住民と地域とのコミュニティ形成促進に関する研究 | Place Attachment and Urban Stu | Collaborative and Sustainable  | ❌ | ❌ |
| 69 | 大阪湾周辺府県における海岸漂着物処理推進施策 | Coastal and Marine Management | Coastal and Marine Management | ✅ | ✅ |
| 70 | 中堅教諭の社会科指導における困り感の抽出 : X教諭を事例として | Educator Training and Historic | Educator Training and Historic | ✅ | ✅ |
| 71 | 若者の性の問題化の構造――保健体育科教科書における性感染症の記述を例に | Gender, Sexuality, and Educati | Adolescent Sexual and Reproduc | ❌ | ❌ |
| 72 | 歴史教師のビリーフに関する研究方法論の考察 : ビリーフ調査の質問項目 | Educator Training and Historic | History and Theory of Mathemat | ❌ | ✅ |
| 73 | 小中学校における英語絵本の読み聞かせの方法とその効果について | EFL/ESL Teaching and Learning | Subtitles and Audiovisual Medi | ❌ | ❌ |
| 74 | 炎症性腸疾患患者における国内の看護研究の動向と看護課題（研究ノート） | Nursing care and research | Nursing care and research | ✅ | ✅ |
| 75 | 生態水文学研究所赤津研究林白坂南北谷小流域日流出量観測報告（Ⅱ）（自2 | Hydrology and Watershed Manage | Soil and Water Nutrient Dynami | ❌ | ❌ |
| 76 | 小学校社会科教師における信念と教材開発過程の解明 | Educator Training and Historic | Psychology of Development and  | ❌ | ❌ |
| 77 | アニメーション的な誤配としての多重見当識――非対人性愛的な「二次元」へ | Psychoanalysis, Philosophy, an | Sound Studies and Aurality | ❌ | ❌ |
| 78 | 職業訓練の効果測定における脱落の影響 | Human Resource Development and | Survey Sampling and Estimation | ❌ | ❌ |
| 79 | 日韓の国際選挙支援 : アジア型援助モデルに関する議論の観点から | International Development and  | Asian Industrial and Economic  | ❌ | ✅ |
| 80 | 津波シミュレータTNSの開発 | Simulation and Modeling Applic | Electromagnetic Simulation and | ❌ | ❌ |
| 81 | 臨地実習における看護系大学生のレジリエンス： フォーカスグループインタ | Focus Groups and Qualitative M | Health and Wellbeing Research | ❌ | ❌ |
| 82 | 看護師のレジリエンスの概念分析 | Healthcare Education and Workf | Healthcare Education and Workf | ✅ | ✅ |
| 83 | 生態水文学研究所穴の宮試験流域日流出量観測結果報告（自2017年1月至 | Hydrology and Watershed Manage | Fish biology, ecology, and beh | ❌ | ❌ |
| 84 | フィリピン人日本語学習者のデータを基にした非漢字圏学習者向け語彙テスト | EFL/ESL Teaching and Learning | Psychometric Methodologies and | ❌ | ❌ |
| 85 | 宮崎演習林・樫葉国有林の有剣ハチ類 | Hymenoptera taxonomy and phylo | Species Distribution and Clima | ❌ | ❌ |
| 86 | 曖昧さへの態度と⼼理的な問題解決の関連 ーレジリエンス及びコーピング⽅ | Problem Solving Skills Develop | Student Stress and Coping | ❌ | ❌ |
| 87 | 産業部門間の連関性指標の概説と地域経済への応用例 | Regional Economic and Spatial  | Regional resilience and develo | ❌ | ✅ |
| 88 | 小学校英語活動における英語絵本の活用に関する研究 : 児童の発達段階に | EFL/ESL Teaching and Learning | Early Childhood Education and  | ❌ | ❌ |
| 89 | 東日本大震災を踏まえた地震ハザード評価の改良に向けた検討 | Seismic Performance and Analys | Earthquake and Disaster Impact | ❌ | ✅ |
| 90 | 小学校社会科の単元展開における教師の実践的思考の研究 : 教師にとって | Educational Assessment and Imp | Evaluation of Teaching Practic | ❌ | ❌ |
| 91 | 1940年代仏領インドシナの公共事業政策 : ドクーの政策と都市・建築 | Architecture and Cultural Infl | Urban Planning and Landscape D | ❌ | ❌ |
| 92 | 地域在住外国人に対する日本語ボランティアの養成シラバス | Second Language Learning and T | International Student and Expa | ❌ | ❌ |
| 93 | 日本における新型コロナ感染症による死亡について | COVID-19 and healthcare impact | COVID-19 Clinical Research Stu | ❌ | ❌ |
| 94 | 日本における異文化間カウンセリング研究の動向と展望 : スコーピングレ | Counseling Practices and Super | Counseling Practices and Super | ✅ | ✅ |
| 95 | あいち医療通訳システム利用経験をもつ医療従事者の語りからみえる医療通訳 | Interpreting and Communication | Interpreting and Communication | ✅ | ✅ |
| 96 | Health Locus of Controlによる保健行動予測の試み | Health and Wellbeing Research | Health and Wellbeing Research | ✅ | ✅ |
| 97 | 論考 地域日本語教室の5つの機能と研修プログラム : 豊かな学びと人間 | French Language Learning Metho | Indigenous and Place-Based Edu | ❌ | ❌ |

---

## 3. 考察

- **Primary一致率**: 正解 Topic と primary_topic が完全一致した割合
- **Top-3 Hit率**: 正解 Topic が topics[] の上位 3 件に含まれた割合
- 正解ラベルは Claude が候補 20 件の中から選択したもの（上位候補外の正解は含まない）

*本レポートは `scripts/compare_methods.py` により自動生成されました。*