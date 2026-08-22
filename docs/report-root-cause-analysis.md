# IRDB 日本語論文の OpenAlex Topic 誤分類 — 原因特定と改善策

> 武田英明先生・長野伸一様宛　技術報告書
>
> 2026 年 8 月 22 日　笠間和喜（iGroup Japan）

---

## 要旨

OpenAlex が IRDB 由来の日本語論文に対して行う Topic 付与がなぜ大規模に誤動作しているか、その**根本原因**を特定しました。OpenAlex の公式分類モデル（mBERT）のソースコードと学習データを解析し、1,000 件のサンプルに対して公式モデルの再現実験を行った結果、以下が判明しました。

1. **公式モデルの前処理が日本語テキストを除去している** — 同じモデルで日本語を保持するだけで精度が倍増
2. **IRDB レコードは公式モデルの4入力のうち3つが欠損している** — 参考文献・雑誌名・テキスト（前処理により）
3. **我々の v5 パイプラインは、公式モデル（日本語保持版）と同等以上** — 教師なし手法としては良好

本報告書では原因分析の詳細と、改善に向けた4つの選択肢を提示します。

---

## 1. 現状の問題：「Military Technology」への大量誤分類

1,000 件の IRDB 日本語論文サンプルについて、OpenAlex API から現在の Topic 付与値を取得しました。

**primary_topic の頻度上位 5 件：**

| Topic | 件数 |
|---|---|
| Military Technology and Strategies | **255 件（25.5%）** |
| Japanese History and Culture | 11 件 |
| Linguistics and Cultural Studies | 10 件 |
| EFL/ESL Teaching and Learning | 10 件 |
| Mathematics and Applications | 8 件 |

1,000 件中 255 件 — 全体の 4 分の 1 が「軍事技術」に分類されています。これらには地震学、看護学、言語学、森林学、心理学など多様な分野の論文が含まれており、系統的な誤動作が発生しています。

---

## 2. 原因分析

### 2.1 OpenAlex の分類システムの構造

OpenAlex の公式 Topic 分類器（[GitHub リポジトリ](https://github.com/ourresearch/openalex-topic-classification)、[Hugging Face](https://huggingface.co/OpenAlex/bert-base-multilingual-cased-finetuned-openalex-topic-classification-title-abstract)）は以下の構成です。

| 要素 | 内容 |
|---|---|
| モデル | `bert-base-multilingual-cased`（0.2B パラメータ）をファインチューニング |
| 学習データ | CWTS の引用ネットワーククラスタリングによるラベル（7,100 万件、[Zenodo CC0](https://zenodo.org/records/10560276)）|
| 分類数 | 4,516 Topics（4 Domain → 27 Field → 254 Subfield → 4,516 Topic の階層構造）|
| **入力特徴量** | **① タイトル ② 要旨 ③ 雑誌名（source） ④ 引用文献（citations）** |
| ライセンス | Apache 2.0 |

重要なのは、**テキスト（①②）だけでなく、雑誌名（③）と引用ネットワーク（④）が入力に含まれる**点です。公式モデルのテキストのみ版の学習時精度は **48.46%**（[Hugging Face Model Card](https://huggingface.co/OpenAlex/bert-base-multilingual-cased-finetuned-openalex-topic-classification-title-abstract)）であり、残りの精度は③④が稼いでいます。

### 2.2 IRDB レコードにおける入力欠損

OpenAlex API から取得した 1,000 件の IRDB レコードの特性：

| 入力特徴量 | 状態 | 影響 |
|---|---|---|
| ① タイトル | 存在するが大半が日本語 → **前処理で除去される**（後述） | ❌ 無効化 |
| ② 要旨 | 全体の約 40% が空または短文 → 残りも日本語なら除去 | ❌ 大部分が無効化 |
| ③ 雑誌名（source） | **88.5% が "Institutional Repositories DataBase (IRDB)"** という汎用名 | ❌ 分野識別力なし |
| ④ 引用文献（references） | **79.3% が 0 件** | ❌ 欠損 |

つまり、**4 つの入力のうち最大で 3 つが無効**という状態でモデルが推論を行っています。

### 2.3 根本原因：日本語テキスト除去の前処理

公式の本番コード（`predictor.py`）に、以下の前処理が実装されています。

```python
# predictor.py より抜粋
groups_to_skip = ['HIRAGANA', 'CJK', 'KATAKANA', 'ARABIC', 'HANGUL', ...]

def check_for_non_latin_characters(text):
    groups, latin_chars = group_non_latin_characters(str(text))
    if name_to_keep_ind(groups) == 1:  # スキップ対象の文字がなければ通す
        return 1
    elif latin_chars > 20:  # Latin 文字が 20 文字超なら通す
        return 1
    else:
        return 0  # それ以外は除去
```

この処理は：

1. テキスト中にひらがな・カタカナ・漢字が含まれるか検査する
2. **Latin 文字が 20 文字以下**の場合、テキスト全体を空文字列にする
3. 通過したテキストからも**非 Latin 文字（日本語部分）を個別に除去**する

我々の 1,000 件サンプルに適用した結果：

- タイトルが完全に除去された論文：**324 件（32.4%）**
- タイトル＋要旨がともに空になった論文：**196 件（19.6%）**

196 件はモデルへの入力が文字通り空文字列であり、モデルはバイアス項だけで分類を行います。その結果、学習データ中の頻度が高い Topic（"Military Technology and Strategies" 等）にデフォルトで分類される構造です。

**テキスト入力が保持された残りの 676 件についても**、日本語部分が除去されるため、例えば：

| 原文タイトル | 前処理後（モデルが受け取る入力） |
|---|---|
| Patient Health Questionnaire (PHQ-9, PHQ-15) **日本語版** および Generalized Anxiety Disorder-7 | Patient Health Questionnaire (PHQ-9, PHQ-15) Generalized Anxiety Disorder-7 |
| ＜**書評**＞ Francois Recanati, Direct Reference | ＜＞ Francois Recanati, Direct Reference |

「書評」「日本語版」といった分類に重要な情報が失われています。

---

## 3. 検証実験

### 3.1 実験設計

公式モデルを 2 つの前処理モードで 1,000 件に適用し、既存手法と比較しました。

| 手法 | 説明 |
|---|---|
| **OpenAlex 現行** | OpenAlex API から取得した、本番環境で付与済みの Topic |
| **公式 mBERT（openalex 前処理）** | 公式モデルを本番と同じ前処理で再実行（検証用） |
| **公式 mBERT（日本語保持）** | 同じモデルだが、日本語テキスト除去をスキップ |
| **v2 ensemble** | 我々の e5-base + BM25 アンサンブル |
| **v5 e5-large** | 我々の multilingual-e5-large + BM25（最終版） |

評価は Anthropic Claude が生成した正解ラベル 97 件（v1 の上位 20 候補から選定）との照合です。

> **正解ラベルのバイアスに関する注記：** 本正解ラベルは v1 の埋め込み検索候補から選定されているため、埋め込みベース手法に有利なバイアスが内在します。人手評価の独立した検証が引き続き重要です。

### 3.2 結果

| 手法 | Primary 一致 | Top-3 Hit | Subfield | Field | Domain |
|---|---|---|---|---|---|
| **OpenAlex 現行** | **5.2%** | 7.2% | 9.3% | 17.5% | 38.1% |
| 公式 mBERT（openalex 前処理） | **12.4%** | 15.5% | 14.4% | 23.7% | 41.2% |
| **公式 mBERT（日本語保持）** | **26.8%** | 38.1% | 34.0% | 51.5% | 73.2% |
| v2 ensemble | **22.7%** | 35.1% | 27.8% | 53.6% | 78.4% |
| **v5 e5-large** | **25.8%** | 41.2% | 37.1% | 58.8% | 78.4% |

### 3.3 結果の解釈

**① OpenAlex 現行と公式 mBERT（openalex 前処理）の乖離（5.2% vs 12.4%）**

同じ前処理なのに結果が異なるのは、本番環境では③雑誌名と④引用文献も入力されるためです。しかし IRDB レコードではこの 2 つが実質的に無効であるため、本番環境でも低精度に留まっています。

**② 日本語テキスト除去の影響（12.4% → 26.8%、同一モデル）**

日本語テキストを除去する前処理を外すだけで、Primary 一致率が **12.4% → 26.8%（2.2 倍）**、Domain 一致率が **41.2% → 73.2%** に改善しました。mBERT は `bert-base-multilingual-cased` をベースとしており、日本語を含む 104 言語で事前学習されています。日本語テキストを入力すること自体はモデルの設計に沿っています。

**③ v5 と公式 mBERT（日本語保持）の比較**

| 指標 | 公式 mBERT（日本語保持） | v5 e5-large |
|---|---|---|
| Primary 一致 | **26.8%** | 25.8% |
| Top-3 Hit | 38.1% | **41.2%** |
| Field 一致 | 51.5% | **58.8%** |
| Domain 一致 | 73.2% | **78.4%** |

Primary 一致では公式モデルがわずかに上回り、Top-3 以降および上位階層（Field / Domain）では v5 が上回っています。v5 は**教師なし手法**（学習データを使わず、Topic 記述文との類似度で検索）であり、教師あり分類モデルの公式 mBERT と互角以上であることは注目に値します。

### 3.4 具体例

| 論文タイトル | 正解 | OpenAlex 現行 | 公式 mBERT（日本語保持） | v5 e5-large |
|---|---|---|---|---|
| 経済危機と在日ブラジル人 | Migration and Labor Dynamics | Military Technology ❌ | Migration and Labor Dynamics ✅ | Employment and Welfare Studies △ |
| 6. 地震の規模別度数の統計式… | earthquake and tectonic studies | Military Technology ❌ | earthquake and tectonic studies ✅ | Statistical Methods… ❌ |
| 看護基礎教育における模擬患者参加型教育… | Simulation-Based Education in Healthcare | Military Technology ❌ | Simulation-Based Education ✅ | Empathy and Medical Education △ |
| 西津軽・男鹿間における歴史地震… | earthquake and tectonic studies | Military Technology ❌ | Earthquake and Tsunami Effects △ | earthquake and tectonic studies ✅ |
| 運動に伴う改訂版ポジティブ感情尺度… | Psychometric Methodologies | Health and Wellbeing ❌ | Sport Psychology ❌ | Psychometric Methodologies ✅ |
| 死と「迷惑」― 現代日本における死生観… | Death, Funerary Practices | Military Technology ❌ | Japanese History and Culture △ | Death, Funerary Practices ✅ |

公式 mBERT（日本語保持）と v5 は**相補的**に機能しており、一方が正解する論文で他方が外すケースが見られます。

---

## 4. 改善策の選択肢

以下に 4 つの改善策を、実現容易度と期待される効果の順に提示します。

### 選択肢 A：OpenAlex への前処理修正提案（最小コスト・最大インパクト）

| 項目 | 内容 |
|---|---|
| 概要 | OpenAlex の `predictor.py` における非 Latin 文字除去処理の修正を提案 |
| 具体策 | `check_for_non_latin_characters` で HIRAGANA / CJK / KATAKANA を除去対象から外す（または Latin 文字数の閾値を撤廃） |
| 根拠 | 同一モデルで Primary 一致率が 2.2 倍に改善（12.4% → 26.8%）。mBERT は多言語モデルであり日本語入力は設計内 |
| 影響範囲 | IRDB だけでなく、OpenAlex 上の全ての日本語・中国語・韓国語・アラビア語等の論文に波及 |
| 必要な作業 | OpenAlex CTO（Casey 氏）への技術提案書の作成・送付 |

**この選択肢が最も費用対効果が高いと考えます。**

### 選択肢 B：公式 mBERT + v5 のアンサンブル（中程度のコスト）

| 項目 | 内容 |
|---|---|
| 概要 | 公式 mBERT（日本語保持）と v5 e5-large の出力を統合 |
| 根拠 | 両手法は相補的に機能し、一方が正解する論文で他方が外すケースが多い |
| 期待効果 | Primary 一致率 30% 超、Domain 一致率 80% 超の可能性 |
| 必要な作業 | アンサンブルロジックの実装、重みの最適化 |

### 選択肢 C：教師あり分類への転換（高コスト・高効果）

| 項目 | 内容 |
|---|---|
| 概要 | v5 の e5-large 埋め込みを固定し、4,516 クラスの分類ヘッド（線形プローブ）を CWTS ラベルで学習 |
| 根拠 | v5 は教師なし手法の天井に近い。CWTS のラベル付きデータ（7,100 万件、CC0）が利用可能 |
| 期待効果 | テキストのみモデルの天井（公式 mBERT の学習精度 48.46%）に近づく可能性 |
| 必要な作業 | CWTS データのダウンロード（3 GB）、GPU 環境での学習（数時間〜1 日）|

### 選択肢 D：IRDB / JPCOAR メタデータの活用（中コスト・補完的）

| 項目 | 内容 |
|---|---|
| 概要 | OpenAlex が取得していないメタデータ（紀要名、NDC 分類、英語タイトル/英語抄録、著者所属）を IRDB の OAI-PMH / JPCOAR スキーマから直接取得 |
| 根拠 | 現在 source が "IRDB" の一語に潰れている問題を解消。紀要名は分野特異性が高い（例：「看護学部紀要」→ Health Sciences）。英語抄録が存在すれば機械翻訳コスト不要 |
| 必要な作業 | JPCOAR ハーベスティング、メタデータの整備・マッチング |

---

## 5. 人手評価への影響

現在準備中の人手評価（200 件、長野様による評価）について、今回の知見を踏まえた提案です。

1. **比較対象の追加**：v1（OpenAlex 現行）vs v5 の 2 手法比較に加え、**公式 mBERT（日本語保持）** を 3 手法目として追加することをご検討ください。手法間の相補性を検証できます。
2. **階層別評価の導入**：Primary Topic の完全一致に加え、**Field / Domain レベルの正誤**を評価項目に追加することで、手法の「大外し」と「惜しい外し」を区別できます。
3. **正解ラベルの独立性**：現行の自動正解ラベル（Claude が v1 候補から選定）にはバイアスがあるため、人手評価の結果が最も信頼性の高い評価軸となります。

---

## 6. 今後の進め方（提案）

| ステップ | 内容 | 時期 |
|---|---|---|
| ① | 本報告の共有・ご意見聴取 | 2026 年 8 月下旬 |
| ② | 選択肢 A の OpenAlex 提案書作成 | 2026 年 9 月上旬 |
| ③ | 人手評価の実施（3 手法比較・階層別） | 2026 年 9 月 |
| ④ | 選択肢 B または C の実装・検証 | 評価結果に基づき判断 |
| ⑤ | 全 249 万件への適用可否の協議 | ③④の結果を踏まえて |

---

## 付録：実験環境・再現手順

| 項目 | 内容 |
|---|---|
| 公式モデル | `OpenAlex/bert-base-multilingual-cased-finetuned-openalex-topic-classification-title-abstract`（HuggingFace, Apache-2.0）|
| CWTS ラベルデータ | [Zenodo 10560276](https://zenodo.org/records/10560276)（CC0） |
| クラスタ→Topic 対応表 | `data/cluster_to_topic.json`（本プロジェクトで構築、4,511/4,521 対応）|
| 実行環境 | Mac mini M4, Python 3.14, PyTorch 2.12 (MPS), transformers 5.10 |
| 処理時間 | 1,000 件あたり約 50 秒（batch_size=32, MPS）|
| 再現コマンド | `python scripts/assign_topics_official.py --input data/works-1k.jsonl --output <出力> --preprocess {openalex\|keep-ja}` |
| 比較コマンド | `python scripts/compare_all_methods.py --gold data/gold-labels-100.jsonl --meta index-e5-large/topics_meta.json --methods ...` |

すべてのスクリプト・データ・結果は本リポジトリに含まれています。

---

笠間和喜
iGroup Japan
kazuki@igroupjapan.com
