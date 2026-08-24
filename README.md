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

## 手法比較（1,000件 IRDB 日本語論文）

| 手法 | 平均信頼度 | 高信頼（≥0.8） | 低信頼（<0.2） |
|---|---|---|---|
| OpenAlex 現行（API取得値） | 0.349 | 156 件（16%） | 447 件（45%） |
| v2-clean（埋め込み+BM25、翻訳なし） | 0.747 | 542 件（54%） | 0 件 |
| v3-Gemini-clean（Gemini翻訳+階層+BM25） | 0.759 | 600 件（60%） | 0 件 |
| **v3-OPUS-clean（OPUS-MT翻訳+階層+BM25）** | **0.777** | **663 件（66%）** | **0 件** |

### 主な知見

- OpenAlex の公式分類器は非ラテン文字（日本語等）を前処理で除去するため、日本語論文の 45% がスコア 0.2 未満
- 当方の手法ではいずれも低信頼スコアが 0 件（多言語埋め込みモデルが日本語を直接処理可能なため）
- 日英翻訳（OPUS-MT）+ 階層的分類 + BM25 アンサンブルの組み合わせが最高性能を達成
- OPUS-MT は API 不要・無料のローカル実行モデルであり、運用コスト面でも有利

### v3 パイプライン（推奨）

```
日本語論文（タイトル + 要旨）
      │
      ├─ テキストクリーニング（リポジトリ定型文の除去）
      │
      ├─ OPUS-MT 翻訳（日本語→英語）
      │
      ├─【A】multilingual-e5-base（埋め込み）─→ 階層的ドメインフィルタ → top-k Topics
      │
      └─【B】BM25（キーワードマッチング）────→ top-k Topics
                        │
                        ▼
            final_score = 0.75 × emb_score + 0.25 × bm25_score
                        │
                        ▼
              primary_topic + topics[3件]
```

## 前バージョンとの比較

| 項目 | v1（埋め込みのみ） | v2（アンサンブル） | v3（翻訳+階層+アンサンブル） |
|---|---|---|---|
| 手法 | multilingual-e5-base | e5-base + BM25 | OPUS-MT翻訳 + e5-base + 階層 + BM25 |
| スコア | コサイン類似度 | 重み付き融合スコア | 重み付き融合スコア |
| 翻訳 | なし | なし | OPUS-MT / Gemini |
| 平均信頼度 | — | 0.747 | **0.777** |
| 高信頼（≥0.8） | — | 542件 | **663件** |

## ライセンス

MIT License — © 2026 Kazuki Kasama, iGroup Japan
