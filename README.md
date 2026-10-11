# OpenAlex Topics Assignment for IRDB（IRDB2）

IRDB（機関リポジトリデータベース）に登録された**日本語論文**に、OpenAlex の Topic（約4,500）を付け直すためのツールです。タイトルと抄録から、多言語の埋め込み（multilingual-e5）と BM25 を組み合わせて Topic を推定し、OpenAlex の Work スキーマに沿った JSONL で出力します。

> このリポジトリは前版 [OpenAlex-Topics-assignment-for-IRDB](https://github.com/KKasama/OpenAlex-Topics-assignment-for-IRDB)（v1・埋め込みのみ・アーカイブ済み）の後継です。

## 背景

OpenAlex の Topic は、タイトル・抄録・被引用・ジャーナル名から、深層学習の分類器が自動で付けています。しかし、この分類器は前処理で非ラテン文字を取り除くため、日本語の論文では Topic が外れやすくなります。1,000件の IRDB 日本語論文で調べたところ、現行の OpenAlex の Topic は、約45%が信頼度0.2未満でした（詳細は `docs/report-root-cause-analysis.md`）。

本ツールは、日本語のまま、または英訳してから多言語モデルで Topic を推定することで、この問題を補います。

## 方式

バージョンごとに、次のように段階的に拡張しています。

| | v1 | v2（アンサンブル） | v3（翻訳＋階層＋アンサンブル） | v4 / v5（比較実験） |
|---|---|---|---|---|
| 埋め込み | multilingual-e5 | multilingual-e5-base | multilingual-e5-base | e5-base / e5-large / SciBERT |
| BM25 | なし | あり | あり | あり（重み0.10） |
| 翻訳 | なし | なし | OPUS-MT または Gemini | なし / FuguMT / Gemini |
| 階層（ドメイン）絞り込み | なし | なし | あり | なし（精度を下げたため廃止） |
| スクリプト | （前版リポジトリ） | `assign_topics.py` | `assign_topics_v3.py` | `assign_topics_v4.py` |

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

翻訳の選択肢は次のとおりです。

- `--translator opus`: Helsinki-NLP/opus-mt-ja-en。ローカル実行で無料。初回に約300 MBのモデルをダウンロードします。
- `--translator gemini`: Gemini API。環境変数 `GEMINI_API_KEY` が必要です。

### v4 / v5：翻訳器と埋め込みモデルの比較

`assign_topics_v4.py` は、翻訳器（`none` / `fugumt` / `gemini`）と埋め込みモデル（`e5` / `e5-large` / `scibert`）の組み合わせを比較するためのスクリプトです。タイトルと抄録を別々に翻訳して結合し、階層絞り込みは行いません。既定の重みは embedding 0.90、BM25 0.10 です。結果は `docs/comparison-v4-full.md` と `docs/comparison-v5-e5-large.md` にあります。

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
python scripts/build_index.py \
  --index-dir ./index-base \
  --model intfloat/multilingual-e5-base \
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

v2（既定の重み 0.75 / 0.25）:

```bash
python scripts/assign_topics.py \
  --index-dir ./index-base \
  --input data/works-irdb-ja.jsonl \
  --output data/topics-irdb-ja-ensemble.jsonl \
  --minimal --top-n 3
```

重みを変えるときは `--w-emb 0.6 --w-bm25 0.4` のように指定します（合計は1.0）。日本語以外の論文は既定で処理せず（`skipped`）、`--no-japanese-only` で処理できます。

v3（OPUS-MT で翻訳）:

```bash
python scripts/assign_topics_v3.py \
  --index-dir ./index-base \
  --input data/works-irdb-ja.jsonl \
  --output data/topics-irdb-ja-v3.jsonl \
  --translator opus --top-n 3
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

### 信頼度スコア（1,000件の IRDB 日本語論文）

信頼度は、各手法が出すスコアの平均です。**正解との一致率ではありません。**

| 手法 | 平均信頼度 | 高信頼（0.8以上） | 低信頼（0.2未満） |
|---|---|---|---|
| OpenAlex 現行（API取得値） | 0.349 | 156件（16%） | 447件（45%） |
| v2（埋め込み＋BM25、翻訳なし） | 0.747 | 542件（54%） | 0件 |
| v3-Gemini（Gemini翻訳＋階層＋BM25） | 0.759 | 600件（60%） | 0件 |
| v3-OPUS（OPUS-MT翻訳＋階層＋BM25） | 0.777 | 663件（66%） | 0件 |

### 正解ラベルとの一致率（97件）

`docs/comparison-all-methods.md` の、正解ラベル97件に対する一致率です。

| 手法 | Primary 一致 | Top-3 に含む | Subfield 一致 | Field 一致 | Domain 一致 |
|---|---|---|---|---|---|
| OpenAlex 現行 | 5.2% | 7.2% | 9.3% | 17.5% | 38.1% |
| 公式 mBERT（日本語保持） | 26.8% | 38.1% | 34.0% | 51.5% | 73.2% |
| v2 ensemble | 22.7% | 35.1% | 27.8% | 53.6% | 78.4% |
| v5 e5-large | 25.8% | 41.2% | 37.1% | 58.8% | 78.4% |

### 読み方の注意

- 信頼度は、モデル自身のスコアです。分類が当たっているかどうかは、正解ラベルとの一致率で見てください。
- 正解ラベルとの比較では、Primary Topic が完全に一致する割合は、最良の手法でも25〜27%程度です。一方、Field・Domain の単位で見ると一致率は大きく上がります（Domain で78%）。細かい Topic の一致より、大きな分野の振り分けに向いています。
- 正解ラベルは97件と少なく、手法間の差は誤差の範囲に入ることがあります。
- 人手による評価の設計は `docs/human-eval-design-log.md` にあります。

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

# このツール側：Topic を付与する
python scripts/assign_topics.py --index-dir ./index-base \
  --input topics_input.jsonl --output topics_output.jsonl --minimal --top-n 3

# ハブ側：結果を取り込む（別表に保存し、API では auto_topics として返す）
python3 -m jhub import-topics topics_output.jsonl --topics-version v2
```

Topic は、ハブの元データとは別の表に保存し、自動推定の結果であることと、バージョン・付与日時を明示して提供します。

## ライセンス

MIT License — © 2026 Kazuki Kasama, iGroup Japan
