# v1（埋め込みのみ）vs v2（アンサンブル）比較レポート
## 1,000 件サンプルによる手法比較

**作成日：** 2026 年 6 月 10 日  
**対象：** IRDB 日本語論文 1,000 件サンプル（`data/works-1k.jsonl`）  
**v1 出力：** `topics-1k-multi.jsonl`（埋め込みのみ、multilingual-e5-base）  
**v2 出力：** `topics-1k-ensemble.jsonl`（埋め込み × BM25 アンサンブル）

---

## 1. サマリ

| 指標 | v1（埋め込みのみ） | v2（アンサンブル） |
|---|---|---|
| 手法 | multilingual-e5-base | e5-base + BM25（重み 0.75 / 0.25） |
| primary_topic が v1 と同じ | — | **629 件（62.9%）** |
| primary_topic が変わった | — | **371 件（37.1%）** |
| BM25 有効（keyword overlap あり） | — | 610 件（61.0%） |
| 埋め込みスコア平均 | **0.8119** | 0.8083 |
| BM25スコア平均（有効のみ） | — | **0.9396** |

---

## 2. BM25 の影響分析

### 重要な発見

**変更された 371 件のすべてにおいて、BM25 スコアが有効（> 0）でした。**

すなわち、v1 と v2 で primary_topic が変わった原因は **100% BM25 によるもの**です。BM25 がキーワード一致を検出した論文では、埋め込みスコアだけでは選ばれなかった Topic に融合スコアが押し上げられています。

### スコア比較

| グループ | v1 埋め込みスコア平均 | v2 埋め込みスコア平均 |
|---|---|---|
| 全体（1,000 件） | 0.8119 | 0.8083 |
| 変更あり（371 件） | 0.8135 | 0.8037 |
| 変更なし（629 件） | 0.8110 | （同上） |

変更が生じた論文では v2 の埋め込みスコアが v1 より低く、BM25 が上乗せされることで異なる Topic が選ばれています。

---

## 3. 変更例（10 件）

| v1（埋め込みのみ） | v2（アンサンブル） | 考察 |
|---|---|---|
| Syntax, Semantics, Linguistic Variation | Linguistics, Language Diversity, and Identity | 言語学内での移動 |
| Diabetic Foot Ulcer Assessment | Sleep and related disorders | ⚠️ v1 の方が適切の可能性 |
| Bladed Disk Vibration Dynamics | Control and Stability of Dynamical Systems | より汎用的な分野へ |
| Student Assessment and Feedback | Writing and Handwriting Education | 日本語教育文脈でより具体的 |
| Nitric Oxide and Endothelin Effects | Cardiovascular Disease and Adiposity | より広い分野へ |
| Geometric Analysis and Curvature Flows | Mathematical Inequalities and Applications | 数学内での移動 |
| Geriatric Care and Nursing Homes | Dental Research and COVID-19 | ⚠️ v1 の方が適切の可能性 |
| Diverse Scientific and Economic Studies | Market Dynamics and Volatility | より具体的な分野へ |
| Peacebuilding and International Security | Peace and Human Rights Education | 教育文脈へ（IRDB 的に妥当） |
| Music Education and Analysis | Diverse Music Education Insights | 音楽教育内での移動 |

> ⚠️ マークの 2 件は v1 の方が適切に見えます。BM25 が意図しないキーワードに引っ張られた可能性があります。

---

## 4. 考察

### BM25 が有効に機能するケース
- 論文タイトルに英語技術用語・略語が含まれる場合
- Topic の keywords に対応する語が論文中に明示されている場合

### BM25 が逆効果になりうるケース
- 要旨が空または短い論文（キーワード一致が表層的になる）
- 日本語論文で BM25 の英語コーパスとの一致が偶発的に生じる場合

### 現時点の結論

BM25 の追加は primary_topic の **37%** に影響を与えており、一部は改善、一部は後退の可能性があります。変更の質を判断するには**人手による正解ラベルとの照合**が必要です。

---

## 5. 次のステップ（提案）

1. **人手評価**：変更のあった 371 件から 20〜30 件を抽出し、v1・v2 の topic を人手で採点
2. **BM25 重みの調整**：現在 0.25 → 0.1〜0.2 に下げて BM25 の影響を抑制する実験
3. **BM25 有効件数の絞り込み**：BM25 スコアが高い（例 ≥ 0.5）場合のみ採用するしきい値の導入

---

*本レポートは `scripts/assign_topics.py`（v2）の出力をもとに Python で集計しました。*
