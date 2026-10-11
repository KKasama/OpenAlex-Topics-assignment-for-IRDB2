# OpenAlex Topics Assignment for IRDB（IRDB2）

IRDB（機関リポジトリデータベース）に登録された**日本語論文**に、OpenAlex の Topic（約4,500）を付け直すためのツールです。タイトルと抄録から、多言語の埋め込み（multilingual-e5）と BM25 を組み合わせて Topic を推定し、OpenAlex の Work スキーマに沿った JSONL で出力します。

> このリポジトリは前版 [OpenAlex-Topics-assignment-for-IRDB](https://github.com/KKasama/OpenAlex-Topics-assignment-for-IRDB)（v1・埋め込みのみ・アーカイブ済み）の後継です。

## 背景

OpenAlex の Topic は、タイトル・抄録・被引用・ジャーナル名から、深層学習の分類器が自動で付けています。しかし、この分類器は前処理で非ラテン文字を取り除くため、日本語の論文では Topic が外れやすくなります。1,000件の IRDB 日本語論文で調べたところ、現行の OpenAlex の Topic は、約45%が信頼度0.2未満でした（詳細は `docs/report-root-cause-analysis.md`）。

本ツールは、多言語モデルで日本語のまま Topic を推定することで、この問題を補います。**現在の推奨は v5（multilingual-e5-large + BM25、翻訳なし）** です。翻訳を使う v3・v4 も試しましたが、翻訳なしの v5 が最良でした（後述）。

## 方式

バージョンごとに、次のように段階的に拡張しています。

| | v1 | v2 | v3 | v4 | v5（推奨） |
|---|---|---|---|---|---|
| 埋め込み | e5-base | e5-base | e5-base | e5-base / SciBERT | **e5-large** |
| BM25 | なし | あり | あり | あり（重み0.10） | あり（重み0.10） |
| 翻訳 | なし | なし | OPUS-MT または Gemini | Gemini（改良版）/ FuguMT | **なし** |
| 階層（ドメイン）絞り込み | なし | なし | あり | なし（精度を下げたため廃止） | なし |
| 実行 | （前版リポジトリ） | `assign_topics.py` | `assign_topics_v3.py` | `assign_topics_v4.py` | `assign_topics_v4.py --translator none --emb-model e5-large` |

v5 は専用のスクリプトではなく、`assign_topics_v4.py` を翻訳なし・e5-large で実行したものです（`docs/blog-openalex-topics-ja.md` の記述と、スクリプトの選択肢から読み取れる範囲）。

### v2：埋め込み＋BM25

```
論文テキスト（タイトル + 抄録）
 │
 ├─【A】multilingual-e5-base（埋め込み）─→ 上位 top-k Topic ＋ コサイン類似度
 │
 └─【B】BM25（キーワード照合）──────────→ 上位 top-k Topic ＋ 正規化スコア
          │
          ▼
 final_score = w_emb × emb_score + w_bm25 × bm25_score   （既定: 0.75 / 0.25）
          │
          ▼
 primary_topic ＋ topics[3件]
```

BM25 は、Topic の keywords・display_name・description に対して計算します。埋め込みモデルが苦手な専門用語や略語を補います。CJK 文字は文字バイグラムで扱います。

### v3：翻訳＋階層＋アンサンブル

```
日本語論文（タイトル + 抄録）
 │
 ├─ テキストクリーニング（リポジトリの定型文などを除去）
 ├─ 日本語 → 英語の翻訳（OPUS-MT または Gemini）
 │
 ├─【A】multilingual-e5-base ─→ 上位50件 ─→ 優勢なドメインに絞り込み
 └─【B】BM25（翻訳後の英語テキスト）
          │
          ▼
 final_score = 0.75 × emb_score + 0.25 × bm25_score
```

翻訳の選択肢と、実験での評価は次のとおりです。

- `--translator opus`: Helsinki-NLP/opus-mt-ja-en。ローカル実行で無料（初回に約300 MBをダウンロード）。ただし、学術的な日本語の翻訳品質が低く、正解ラベルとの Primary 一致率は **3.1%** まで下がりました。**推奨しません。**
- `--translator gemini`: Gemini API。環境変数 `GEMINI_API_KEY` が必要です。全約249万件を処理する場合の費用は約77,000円・約12日間と見積もられており、実運用には課題があります。

### v4：翻訳の改良と SciBERT の評価

`assign_topics_v4.py` は、翻訳器（`none` / `fugumt` / `gemini`）と埋め込みモデル（`e5` / `e5-large` / `scibert`）を組み合わせて比較するスクリプトです。v3 の問題（抄録に混ざるリポジトリの定型文、英語タイトルと日本語抄録の一括翻訳）を直し、タイトルと抄録を別々に翻訳して結合します。階層絞り込みは精度を下げたため外しました。既定の重みは embedding 0.90、BM25 0.10 です。

- 改良した Gemini 翻訳＋e5-base は、Primary 一致率は v2 と同じ22.7%、Top-3 は37.1%でした。
- SciBERT は英語のみで学習されているため、Primary 一致率が5〜7%に下がりました。

### v5：multilingual-e5-large＋BM25（推奨）

翻訳なしのまま、埋め込みモデルを e5-large（560Mパラメータ、1,024次元）に替えたものです。Primary 一致率25.8%、Top-3 は41.2%で、v2 より Primary +3.1 ポイント、Top-3 +6.1 ポイント改善しました。翻訳が不要で、無料・ローカルで実行できます。結果は `docs/comparison-v5-e5-large.md` にあります。

## セットアップ

Python 3.9 以上を想定しています。モデルの重みに数GBのディスク容量が必要です。

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 使い方

### 1. Topic インデックスを作る（初回のみ）

OpenAlex の Topics API から Topic を取得し、埋め込みを FAISS インデックスにします。**インデックスと、付与時の埋め込みモデルは同じものにしてください。**

```bash
# v2・v3 用（e5-base）
python scripts/build_index.py \
  --index-dir ./index-base \
  --model intfloat/multilingual-e5-base \
  --mailto your@example.org

# v5 用（e5-large）
python scripts/build_index.py \
  --index-dir ./index-large \
  --model intfloat/multilingual-e5-large \
  --mailto your@example.org
```

### 2. データを取得する（OpenAlex API を使う場合）

```bash
python scripts/fetch_openalex_works.py \
  --source S7407056385 \
  --output data/works-irdb-ja.jsonl \
  --mailto your@example.org
```

### 3. Topic を付与する

v5（推奨。e5-large、翻訳なし、重み 0.90 / 0.10）:

```bash
python scripts/assign_topics_v4.py \
  --translator none --emb-model e5-large \
  --index-dir ./index-large \
  --input data/works-irdb-ja.jsonl \
  --output data/topics-irdb-ja-v5.jsonl
```

v2（コードの既定の重みは 0.75 / 0.25）:

```bash
python scripts/assign_topics.py \
  --index-dir ./index-base \
  --input data/works-irdb-ja.jsonl \
  --output data/topics-irdb-ja-ensemble.jsonl \
  --minimal --top-n 3
```

重みを変えるときは `--w-emb 0.6 --w-bm25 0.4` のように指定します（合計は1.0）。日本語以外の論文は既定で処理せず（`skipped`）、`--no-japanese-only` で処理できます。

v3（翻訳あり。Gemini が既定。OPUS-MT は品質が低いため非推奨）:

```bash
export GEMINI_API_KEY="..."
python scripts/assign_topics_v3.py \
  --index-dir ./index-base \
  --input data/works-irdb-ja.jsonl \
  --output data/topics-irdb-ja-v3.jsonl \
  --translator gemini --top-n 3
```

### 4. 品質を確認する

```bash
# 信頼度スコアの分析
python scripts/deep_analysis.py \
  --topics-out data/topics-irdb-ja-ensemble.jsonl \
  --works-in data/works-irdb-ja.jsonl \
  --meta index-base/topics_meta.json \
  --out-md docs/deep-analysis-ensemble.md

# 現行の OpenAlex との比較表
python scripts/build_comparison.py \
  --input data/topics-irdb-ja-ensemble.jsonl \
  --works-in data/works-irdb-ja.jsonl \
  --sample 10 \
  --mailto your@example.org \
  --out-md docs/comparison-ensemble.md
```

## 入力形式

1行1件の JSONL（JSON 配列も可）です。CSV（OpenAlex Works の CSV）にも対応しています（`src/io_adapters.py`）。

```json
{"id": "oai:example:0001", "title": "…", "abstract": "…", "language": "ja", "ndc_codes": ["913"]}
```

- 識別子は `id`、`work_id`、`openalex_id`、`url` のうち、最初に見つかったものを `work_id` として使います。
- `abstract` は省略できます。リポジトリの定型文（「UTokyo Repository は…」など）や、文字が空白で区切られて壊れた抄録は、自動で捨てます。
- `ndc_codes`（日本十進分類）の対応表は `src/ndc_mapping.py` にあります。

## 出力形式

OpenAlex の Work スキーマに沿った JSONL です。

```json
{
  "work_id": "https://openalex.org/W...",
  "primary_topic": {"id": "https://openalex.org/T10318", "display_name": "Urban and spatial planning", "score": 0.8231},
  "topics": [
    {"id": "...", "display_name": "Urban and spatial planning", "score": 0.8231},
    {"id": "...", "display_name": "Urban Planning and Landscape", "score": 0.8102},
    {"id": "...", "display_name": "Ecology and Conservation", "score": 0.7891}
  ],
  "method": "ensemble",
  "emb_score": 0.8105,
  "bm25_score": 0.4320
}
```

`method` の値は次のとおりです。

| 値 | 意味 |
|---|---|
| `ensemble` | v2。BM25 が有効に働いた |
| `embedding_only` | v2。BM25 のスコアが 0 |
| `skipped` | v2。日本語以外のため処理しない（出力には書かれない） |
| `v3_ensemble` / `v3_hierarchical` | v3。それぞれ BM25 が有効 / 無効 |
| `v4_ensemble` / `v4_embedding` | v4。それぞれ BM25 が有効 / 無効 |

v3 の出力には、確認用に `translated_title`（翻訳後のテキスト）が付きます。

## 評価結果

### 正解ラベルとの一致率（97件）

主な評価は、1,000件のサンプルから作った97件の正解ラベルとの一致率です（`docs/comparison-all-methods.md`、`docs/blog-openalex-topics-ja.md`）。

| 手法 | Primary 一致 | Top-3 に含む | Subfield 一致 | Field 一致 | Domain 一致 |
|---|---|---|---|---|---|
| OpenAlex 現行 | 5.2% | 7.2% | 9.3% | 17.5% | 38.1% |
| 公式 mBERT（日本語保持） | 26.8% | 38.1% | 34.0% | 51.5% | 73.2% |
| v1（e5-base） | 20.6% | 34.0% | — | — | — |
| v2（e5-base＋BM25） | 22.7% | 35.1% | 27.8% | 53.6% | 78.4% |
| v3（OPUS-MT 翻訳） | 3.1% | — | — | — | — |
| v4（Gemini 翻訳＋e5-base） | 22.7% | 37.1% | — | — | — |
| v4（SciBERT） | 5〜7% | — | — | — | — |
| **v5（e5-large＋BM25）** | **25.8%** | **41.2%** | 37.1% | 58.8% | 78.4% |

「公式 mBERT（日本語保持）」は、OpenAlex の公式モデルを、前処理で日本語を落とさずに使った場合です。Primary 一致率は v5 とほぼ同じ水準で、現行の OpenAlex（5.2%）との差の多くは、日本語を除去する前処理によるものだと読み取れます。

### 信頼度スコア（1,000件の IRDB 日本語論文）

各手法が出すスコアの平均です。**正解との一致率ではありません。**

| 手法 | 平均信頼度 | 高信頼（0.8以上） | 低信頼（0.2未満） |
|---|---|---|---|
| OpenAlex 現行（API取得値） | 0.349 | 156件（16%） | 447件（45%） |
| v2（埋め込み＋BM25、翻訳なし） | 0.747 | 542件（54%） | 0件 |
| v3-Gemini（Gemini翻訳＋階層＋BM25） | 0.759 | 600件（60%） | 0件 |
| v3-OPUS（OPUS-MT翻訳＋階層＋BM25） | 0.777 | 663件（66%） | 0件 |

v3-OPUS は信頼度が最も高いものの、正解ラベルでは Primary 一致率が3.1%でした。**信頼度が高いことは、当たっていることを意味しません。** 手法の優劣は、必ず一致率で判断してください。

### 読み方の注意

- 正解ラベルは、1,000件のサンプルから Claude API を使って作った97件です。埋め込み検索の上位20件の Topic 候補を提示し、最も適切なものを選ばせる方式のため、**候補を出す埋め込み検索に近い手法が有利になる可能性**があります。人手の評価（`docs/human-eval-design-log.md`、200件・Top-3形式）で確認する必要があります。
- Primary Topic が完全に一致する割合は、最良の手法でも25〜27%程度です。一方、Field・Domain の単位では一致率が大きく上がります（Domain で78%）。細かい Topic の一致より、大きな分野の振り分けに向いています。
- 正解ラベルが97件と少ないため、手法間の小さな差は誤差の範囲に入ることがあります。
- 重みは、コードの既定値（v2：0.75 / 0.25）と、ブログ記事の記述（0.90 / 0.10）が異なります。実験では BM25 の重みを0.10〜0.25で比べても精度への影響は軽微でした。

## ディレクトリ構成

```
src/        埋め込み・BM25・アンサンブル・翻訳・NDC対応・入出力などの本体
scripts/    インデックス構築、データ取得、Topic付与（v2〜v4）、比較・分析
docs/       比較レポート、原因分析（report-root-cause-analysis.md）、評価設計
data/       入出力データ（Git 管理しない場合は .gitignore 推奨）
```

## Japanese_Data_HUB との連携

[Japanese_Data_HUB](https://github.com/KKasama/Japanese_Data_HUB) は、このツールを別プログラムとして呼び出します。ハブからこのツールへ渡す入力は `export-topics-input`、結果の取り込みは `import-topics` で行います。

```bash
# ハブ側：入力 JSONL を書き出す
python3 -m jhub export-topics-input --out topics_input.jsonl

# このツール側：Topic を付与する（v5）
python scripts/assign_topics_v4.py --translator none --emb-model e5-large \
  --index-dir ./index-large --input topics_input.jsonl --output topics_output.jsonl

# ハブ側：結果を取り込む（別表に保存し、API では auto_topics として返す）
python3 -m jhub import-topics topics_output.jsonl --topics-version v5
```

Topic は、ハブの元データとは別の表に保存し、自動推定の結果であることと、バージョン・付与日時を明示して提供します。

## ライセンス

MIT License — © 2026 Kazuki Kasama, iGroup Japan
