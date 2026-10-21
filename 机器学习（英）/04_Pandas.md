# 04｜Pandas：选择、汇总与业务口径

[返回复习导航](00_复习导航.md)

本章目标：能读懂索引、筛选与分组代码，并说明结果的统计单位和分母。Pandas 的标签（Label）会影响对齐和选择，不能一律按 NumPy 的位置运算理解。

## 1. Series 与 DataFrame

序列（Series）是一维带标签的数据；数据框（DataFrame）是二维表，可有多种列类型。

| 表达式 | 返回对象 | 典型形状 |
|---|---|---|
| `df["sales"]` | Series | `(n,)` |
| `df[["sales"]]` | DataFrame | `(n,1)` |
| `df[["branch","sales"]]` | DataFrame | `(n,2)` |
| `df.loc[label,"sales"]` | 通常是单个值 | 标签唯一时为标量 |

贯穿本章的自编小数据（每行是一笔交易，索引标签刻意不从 0 开始）：

```python
import pandas as pd

df = pd.DataFrame({
    "branch": ["A", "A", "B", "B"],
    "product": ["tea", "coffee", "tea", "coffee"],
    "quantity": [2, 1, 3, 2],
    "price": [5, 8, 5, 8],
}, index=[10, 20, 30, 40])
df["sales"] = df["quantity"] * df["price"]
```

这里一行是一笔只含一种产品的交易，`quantity` 为购买件数，`price` 为单价（元/件），`sales` 为交易金额（元）。建立派生列后，完整表为：

| 索引标签 | branch | product | quantity | price | sales |
|---|---|---|---:|---:|---:|
| 10 | A | tea | 2 | 5 | 10 |
| 20 | A | coffee | 1 | 8 | 8 |
| 30 | B | tea | 3 | 5 | 15 |
| 40 | B | coffee | 2 | 8 | 16 |

后面的索引、筛选与分组都对这四笔交易操作。标签 20 表示第二条记录的标识，不是“第 20 行”。读取实际文件时用 `pd.read_csv("filename.csv")`，再确认一行到底代表交易、客户还是酒店。

## 2. 先检查结构，再计算

| 操作 | 能知道什么 |
|---|---|
| `df.head()` / `df.tail()` | 开头/末尾记录 |
| `df.shape` | 行数、列数 |
| `df.index` / `df.columns` | 行标签、列标签 |
| `df.dtypes` | 各列的存储类型 |
| `df.info()` | 行列、非缺失数量、类型等；显示信息，返回 `None` |
| `df.describe()` | 默认主要给出数值列的描述统计 |
| `df.describe(include="all")` | 扩展到非数值列，有些统计量只适用于部分类型 |
| `df.isna().sum()` | 各列缺失数量 |

`describe()` 常见数值统计：`count`、`mean`、`std`、`min`、`25%`、`50%`、`75%`、`max`。其中 `count` 是非缺失数；`50%` 为中位数，不一定等于均值。Pandas `.std()` 默认为样本标准差（`ddof=1`）。

“类别特征存为字符串”是完整描述；只说 `object/string` 描述了存储，没描述业务含义。

## 3. `loc` 与 `iloc`

| 方法 | 依据 | 切片终点 |
|---|---|---|
| `loc[行标签, 列标签]` | 标签 | 通常包含终点标签 |
| `iloc[行位置, 列位置]` | 从 0 开始的位置 | 不包含终点位置 |

```python
print(df.loc[20, "sales"])              # 8，标签为 20 的行
print(df.iloc[1, 4])                     # 8，第 2 行第 5 列
print(df.loc[20:30, ["branch", "sales"]]) # 包含标签 20、30
print(df.iloc[1:3, [0, 4]])              # 包含位置 1、2
```

**什么时候用哪一个？** 已知交易标签 20，要查询其金额，用 `df.loc[20,"sales"]`，得到 8 元；只想抽查当前表第二行，用 `df.iloc[1]`。排序后第二行可能换成另一笔交易，而交易标签 20 仍表示原来的那笔。`df.iloc[1,4]` 的列位置 4 对应 `sales`，因为新增后它是第 5 列。

`df.loc[1]` 查找标签 1，本例不存在，不能代替 `df.iloc[1]`。以上标签切片示例使用有序且唯一的索引；复杂重复或无序索引可能有额外限制。

避免含糊的链式赋值：需要修改选中行的某列时，使用一次 `.loc[条件, 列名] = 值`，例如 `df.loc[df["branch"]=="A", "price"] = 6`。

## 4. 条件筛选（Filtering）

```python
mask = (df["branch"] == "B") & (df["quantity"] >= 2)
result = df.loc[mask, ["product", "sales"]]
tea_or_large = df[(df["product"] == "tea") | (df["sales"] >= 16)]
not_a = df[~(df["branch"] == "A")]
selected = df[df["product"].isin(["tea", "coffee"])]
```

**这段代码回答的问题是：B 店购买至少两件商品的交易，买了什么、花了多少？** `mask` 依次为 `[False,False,True,True]`；`.loc` 先选中标签 30、40，再只显示 `product` 和 `sales` 两列，结果是 tea/15 元与 coffee/16 元。这里仍是两条明细；再对结果的 `sales` 求和，得到这些符合条件交易的合计金额。本例 B 店两笔交易恰好都符合条件，所以也等于 B 店总收入；一般情况下不能把筛选后的收入当成全店收入。

逐元素逻辑使用 `&`、`|`、`~`，每个比较条件加括号；不能把整列用 Python 的 `and/or` 合并。`mask` 是一列布尔值，`True` 的行被保留。

## 5. 频数、去重与分母

| 写法 | 含义 |
|---|---|
| `df["branch"].value_counts()` | 各分店出现的行数 |
| `df["branch"].value_counts(normalize=True)` | 各分店占有效观测的比例 |
| `df["branch"].value_counts(dropna=False)` | 把缺失也计为一类 |
| `df["branch"].nunique()` | 不同非缺失值的数量 |
| `df["branch"].unique()` | 不同值本身 |
| `df["sales"].count()` | 金额非缺失的记录数 |
| `len(df)` | 所有记录数 |

`value_counts()` 默认排除缺失值；`normalize=True` 默认分母也是非缺失观测数量。`count()` 与行数只在该列无缺失时相同。

**课程作业中的关键口径：** Marriott 数据仅包含 2020 年等级发生变化的酒店，而案例给出的全球酒店数为 **7,737**。因此：

$$\text{全球酒店升级比例}=\frac{\text{升级酒店数}}{7737}$$

若除以该数据集行数，得到的是“发生等级变化的酒店中升级的比例”，回答的是另一个问题。这里使用的是作业的历史案例数字，不代表当前酒店总数。

## 6. 分组聚合（GroupBy）

分组操作遵循“拆分—计算—组合”（Split–Apply–Combine）。先定义每组是谁，再明确每个输出统计量的单位。

```python
totals = df.groupby("branch")["sales"].sum()   # A=18，B=31
means = df.groupby("branch")["sales"].mean()   # A=9，B=15.5
summary = df.groupby("branch").agg(
    total_sales=("sales", "sum"),
    avg_sales=("sales", "mean"),
    orders=("sales", "size"),
)
table = df.pivot_table(
    index="branch", columns="product", values="sales", aggfunc="sum"
)  # 行为门店，列为产品，值为销售额
```

**同一份数据，三个不同问题：** `sum()` 回答“每店总共收入多少”，A 为 `10+8=18` 元；`mean()` 回答“每笔交易平均多少钱”，A 为 `18/2=9` 元；`size()` 回答“有几笔交易”，A 为 2 笔。它们都按门店分组，但统计单位不同。

透视表 `table` 把门店放到行、产品放到列，得到：

| branch | coffee | tea |
|---|---:|---:|
| A | 8 | 10 |
| B | 16 | 15 |

这适合回答“B 店比 A 店多出的收入主要来自哪类产品”。注意列按结果中的名称读取，不能默认 coffee/tea 的顺序与原表首次出现顺序一致。

`groupby(...).size()` 计组内总行数；某列的 `.count()` 计其非缺失值数。`pivot_table()` 是作业中用于比较两个分类维度的工具；注意指定 `aggfunc`，其默认通常是均值。

`df.groupby("branch").max()` 会**独立计算各列最大值**，结果同一行内的不同字段未必来自同一笔交易。要找销售额最大的一整行，应先取得其索引：

```python
best_rows = df.loc[df.groupby("branch")["sales"].idxmax()]
```

本例索引唯一且每组均有有效金额，得到 A 的 tea 交易和 B 的 coffee 交易。并列最大值时 `idxmax()` 取首次出现的位置；题目若要求所有并列记录，需要另外处理。

## 7. 派生列、排序、删除与输出

```python
df["sales"] = df["quantity"] * df["price"]   # 向量化派生列
df["large"] = df["sales"] >= 15             # 布尔列
df["branch_lower"] = df["branch"].apply(str.lower)
ranked = df.sort_values("sales", ascending=False)
reset = ranked.reset_index(drop=True)          # 丢弃原索引标签
small = df.drop(columns=["large", "branch_lower"])
row_removed = df.drop(index=[20])              # 按标签删行
# small.to_csv("result.csv", index=False)      # 需要导出时执行
```

`sort_values()`、`drop()` 等通常返回新对象，默认不原地改变 `df`；赋给变量，或明确使用支持的 `inplace=True`。不要写 `df = df.sort_values(..., inplace=True)`，因为原地操作通常返回 `None`。

排序不会自动把标签改成 `0,1,...`；可用 `ignore_index=True` 或 `reset_index(drop=True)`。`reset_index()` 不带 `drop=True` 时通常将原索引保存为一列。

数值字符串的转换与合并属于常用辅助语法：`pd.to_numeric(s, errors="coerce")` 把无法解析的值转为缺失；`s.astype(float)` 要求值能被相应转换。`pd.concat([a,b], axis=0)` 按行拼接，`axis=1` 按列拼接并按行标签对齐。

## 8. 标签对齐（Alignment）

Pandas 的 Series 运算通常先按标签配对，而非按显示位置配对：

```python
a = pd.Series([10, 20], index=["x", "y"])
b = pd.Series([1, 2], index=["y", "x"])
print(a + b)    # x=12，y=21
```

例如把 `a` 看成两个门店原收入，`b` 看成补录收入：门店 x 的原收入 10 必须加上标签 x 的 2，得到 12；不能因为 1 显示在 `b` 的第一行，就把它加给 x。标签对齐解决的是“同一对象相加”，不是“显示在同一位置的数相加”。

给 DataFrame 赋一列 Series 也会按行标签对齐；缺少对应标签时可能产生缺失值。例如本章 `df` 的索引是 `10,20,30,40`，直接赋入默认索引 `0,1,2,3` 的 Series 就不会按行号自动匹配。若只想按位置赋值，必须先明确长度和顺序，再使用数组等无标签值。

## 9. 纸笔例题与解答

**题目。** 用本章交易表，计算 B 店销售额比 A 店高多少百分比；再求 B 店占全部销售额的比例。这两题分母分别是什么？

**解答。** A 店 18，B 店 31。相对 A 的增幅为 $(31-18)/18\approx72.22\%$；B 的销售额占比为 $31/(18+31)\approx63.27\%$。第一题分母是比较基准 A，第二题分母是总销售额。不能用 B/A 的 172.22% 直接声称“高 172.22%”。

## 10. 易错点与自测

常见错误：按位置理解 `loc`；筛选时遗漏括号；把 `count` 当所有行数；把逐列最大值当真实的一行；对无标签对应的 Series 赋值；只报告数字却不解释单位和分母。

1. 本章 `df.iloc[1:3]` 选中哪些行标签？
2. `df["sales"]` 与 `df[["sales"]]` 的维度有何不同？
3. 10 笔交易中金额缺失 2 笔，`len(df)` 与金额的 `.count()` 各是多少？
4. `groupby("branch")["sales"].mean()` 是每店总销售额吗？
5. 两个 Series 的标签相同但顺序相反，相加时按什么配对？

**简答：** 1. 20、30。2. 一维 Series、二维 DataFrame。3. 10 与 8。4. 不是，是每店每笔有效交易的平均金额。5. 按标签配对。

## 课程来源

- [Pandas 课程页](https://bana409.harrywang.me/docs/lectures/pandas)
- [教师教程：Pandas](https://www.harrywang.me/blog/data-science-intro#pandas)
- [Assignment 1：Exploratory Data Analysis](https://bana409.harrywang.me/docs/assignments/assignment-1-exploratory-data-analysis)

四行交易表、纸笔例题与自测为复习自编；Marriott 分母来自课程作业案例。
