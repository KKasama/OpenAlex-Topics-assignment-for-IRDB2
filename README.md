# OpenAlex Topics Assignment for IRDB — Ensemble (v2)

IRDB（機関リポジトリDB）日本語論文への OpenAlex Topic 再付与プロジェクト、アンサンブル版。

前バージョン（[OpenAlex-Topics-assignment-for-IRDB](https://github.com/KKasama/OpenAlex-Topics-assignment-for-IRDB)）の埋め込みベース単体から、**埋め込み + BM25 アンサンブル**に拡張しています。

## アンサンブル構成

```
論文テキスト（タイトル + 要旨）
      │
      ├─【A】multilingual-e5-base（埋め込み）─→ 上位 top-k Topics + コサイン類似度
      │
      └─【B】BM25（キーワードマッチング）────→ 上位 top-k Topics + 正規化スコア
                        │
                        ▼
            final_score = w_emb × emb_score + w_bm25 × bm25_score
            （デフォルト: w_emb=0.75, w_bm25=0.25）
                        │
                        ▼
              primary_topic + topics[3件]
```

### BM25 の役割
- OpenAlex Topic の `keywords` / `display_name` / `description` に対して BM25 スコアを計算
- 英語技術用語・略語など、埋め込みモデルが苦手な固有表現に補完的に機能
- CJK 文字バイグラムにより言語横断的な部分一致も考慮

## 出力フォーマット（OpenAlex Work スキーマ準拠）

```json
{
  "work_id": "https://openalex.org/W...",
  "primary_topic": {
    "id": "https://openalex.org/T10318",
    "display_name": "Urban and spatial planning",
    "score": 0.8231
  },
  "topics": [
    { "id": "...", "display_name": "Urban and spatial planning",   "score": 0.8231 },
    { "id": "...", "display_name": "Urban Planning and Landscape", "score": 0.8102 },
    { "id": "...", "display_name": "Ecology and Conservation",     "score": 0.7891 }
  ],
  "method": "ensemble",
  "emb_score": 0.8105,
  "bm25_score": 0.4320
}
```

`method` は `"ensemble"`（BM25 が有効に機能）または `"embedding_only"`（BM25 スコアが 0）。

## セットアップ

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 使い方

### 1. インデックス構築（初回のみ）

```bash
# index-base/ を既存プロジェクトからコピー、または再ビルド
python scripts/build_index.py --index-dir ./index-base --model intfloat/multilingual-e5-base
```

### 2. データ取得（OpenAlex API）

```bash
python scripts/fetch_openalex_works.py \
  --source S7407056385 \
  --output data/works-irdb-ja.jsonl \
  --mailto your@example.org
```

### 3. Topic 付与（アンサンブル）

```bash
# デフォルト重み: emb=0.75, bm25=0.25
python scripts/assign_topics.py \
  --index-dir ./index-base \
  --input  data/works-irdb-ja.jsonl \
  --output data/topics-irdb-ja-ensemble.jsonl \
  --minimal --top-n 3

# 重みを調整する場合
python scripts/assign_topics.py \
  --index-dir ./index-base \
  --input  data/works-irdb-ja.jsonl \
  --output data/topics-irdb-ja-ensemble.jsonl \
  --minimal --top-n 3 --w-emb 0.6 --w-bm25 0.4
```

### 4. 品質評価・比較

```bash
# 信頼度スコア深掘り分析
python scripts/deep_analysis.py \
  --topics-out data/topics-irdb-ja-ensemble.jsonl \
  --works-in   data/works-irdb-ja.jsonl \
  --meta       index-base/topics_meta.json \
  --out-md     docs/deep-analysis-ensemble.md

# 既存 OpenAlex との比較表
python scripts/build_comparison.py \
  --input    data/topics-irdb-ja-ensemble.jsonl \
  --works-in data/works-irdb-ja.jsonl \
  --sample   10 \
  --mailto   your@example.org \
  --out-md   docs/comparison-ensemble.md
```

## 前バージョンとの比較

| 項目 | v1（埋め込みのみ） | v2（アンサンブル） |
|---|---|---|
| 手法 | multilingual-e5-base | e5-base + BM25 |
| スコア | コサイン類似度 | 重み付き融合スコア |
| method フィールド | `embedding` | `ensemble` / `embedding_only` |
| 追加フィールド | なし | `emb_score`, `bm25_score` |
| 処理速度 | ベースライン | ほぼ同等（BM25 は高速） |

## ライセンス

MIT License — © 2026 Kazuki Kasama, iGroup Japan
