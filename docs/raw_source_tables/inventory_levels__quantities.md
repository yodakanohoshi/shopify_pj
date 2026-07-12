# raw.inventory_levels__quantities

在庫数の name / quantity ペア。inventory_levels の inline list (`quantities`) を dlt が子テーブル化。
粒度: 1 行 = (在庫レベル × 数量種別)。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| dlt行ID | _dlt_id | varchar | 行一意 ID。**PK** |
| dlt親行ID | _dlt_parent_id | varchar | 親の `inventory_levels._dlt_id`。**FK** |
| 数量種別 | name | varchar | available/on_hand/committed/incoming |
| 数量 | quantity | varchar(数値) | 該当種別の在庫数 |

親子関係: `_dlt_parent_id` → [inventory_levels](inventory_levels.md)`._dlt_id`。
