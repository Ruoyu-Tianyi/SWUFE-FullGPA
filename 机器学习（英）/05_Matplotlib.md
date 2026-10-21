# 05｜Matplotlib：选图、读图与解释

[返回复习导航](00_复习导航.md)

本章目标：根据问题选图，能解释图中元素与分布，并读懂 Matplotlib 和 Pandas 绘图代码。复习时优先练习“这张图回答什么问题”，再记必要 API。

## 1. 图形对象、绘图区与坐标轴

| 名称 | 含义 | 对应代码 |
|---|---|---|
| 图形对象（Figure） | 最外层容器，包含一个或多个绘图区 | `fig` |
| 绘图区（Axes） | 一块具体绘图区域，内含曲线、坐标轴、标题等 | `ax` |
| 坐标轴（Axis） | 控制 x/y 等坐标维度的刻度与标签 | x-axis、y-axis |
| 标题（Title） | 说明图展示的问题或发现 | `ax.set_title(...)` |
| 轴标签（Axis Label） | 说明变量与单位 | `ax.set_xlabel(...)` |
| 刻度/刻度标签（Tick / Tick Label） | 具体坐标位置及其文字 | `ax.set_xticks(...)` |
| 图例（Legend） | 说明颜色、线条等编码含义 | `ax.legend()` |
| 标记（Marker） | 表示单个数据点的符号 | `marker="o"` |

注意：`Axes` 在这里是一个绘图区对象的名称，不是“多个 Figure”。一张 Figure 可以有多个 Axes，而每个 Axes 可以有 x 与 y 坐标轴。

## 2. 最小绘图模板

```python
import matplotlib.pyplot as plt

weeks = [1, 2, 3, 4]
sales = [100, 120, 115, 140]
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(weeks, sales, marker="o", color="blue", label="Store A")
ax.set_title("Weekly sales increase from 100 to 140")
ax.set_xlabel("Week")
ax.set_ylabel("Sales (units)")
ax.set_xticks(weeks)
ax.legend()
fig.tight_layout()  # 减少标签遮挡
plt.show()
```

`figsize=(宽,高)` 的默认单位是英寸，不是像素。`label=` 定义图例文字，通常还需要调用 `legend()` 才显示。线型可用 `linestyle="dashed"`，点形可用 `marker="s"`。

正文用中文解释即可；代码中的英文图标签便于跨环境显示。无需把绘图样式、颜色列表都抄到 cheatsheet。

## 3. 一张图里放多个子图

默认 `squeeze=True` 时：

| 创建方式 | 返回的第二个对象 | 访问方式 |
|---|---|---|
| `plt.subplots()` | 单个 Axes | `ax.plot(...)` |
| `plt.subplots(1,2)` | 一维 Axes 数组 | `axes[0]`、`axes[1]` |
| `plt.subplots(2,1)` | 一维 Axes 数组 | `axes[0]`、`axes[1]` |
| `plt.subplots(2,3)` | 二维 Axes 数组 | `axes[行,列]` |

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].plot([1, 2, 3], [4, 6, 5])
axes[0].set_title("Trend")
axes[1].bar(["A", "B"], [15, 20])
axes[1].set_title("Comparison")
fig.tight_layout()
plt.show()
```

如果创建的是 `plt.subplots(2,3)`，右下角用 `axes[1,2]`，因为索引从 0 开始。

## 4. 不同问题选什么图

| 图形 | 适合回答的问题 | 典型 API | 读图重点 |
|---|---|---|---|
| 折线图（Line Plot） | 有序变量或时间上的变化趋势 | `ax.plot(x,y)` | 顺序、趋势、波动、拐点 |
| 柱状图（Bar Plot） | 比较离散类别的数量或统计量 | `ax.bar(x,height)` | 类别间差异、单位、基准 |
| 直方图（Histogram） | 一个数值变量如何分布 | `ax.hist(x,bins=...)` | 中心、离散、偏态、多峰 |
| 箱线图（Box Plot） | 比较分布位置、离散程度与异常点 | `ax.boxplot(x)` | 中位数、四分位距、须、异常点 |
| 散点图（Scatter Plot） | 两个数值变量有什么关系 | `ax.scatter(x,y)` | 方向、强弱、非线性、群组 |
| 散点矩阵（Scatter Matrix） | 同时检查多组变量关系 | `pd.plotting.scatter_matrix(...)` | 非对角线成对关系、对角线单变量分布 |

折线连接意味着相邻点有顺序意义。若数据只是任意排列的国家或客户，连线很容易让人误以为存在时间或连续变化；比较类别通常用柱状图更直接。

类别频数可以先 `value_counts()`，再画柱状图。即使某个库允许给直方图传入类别，也应理解直方图的核心用途是将数值划分区间。

## 5. 柱状图与直方图的区别

柱状图的一根柱通常对应一个类别；直方图的一根柱对应一个数值区间（Bin）。直方图的箱数或箱宽会影响看到的分布形状。

```python
import pandas as pd

df = pd.DataFrame({
    "store": ["A", "A", "B", "B", "B"],
    "sales": [10, 12, 8, 15, 20],
    "customers": [5, 6, 4, 7, 10],
})
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
df.groupby("store")["sales"].sum().plot.bar(ax=axes[0])
axes[0].set_title("Total sales by store")
axes[0].set_ylabel("Sales")
df["sales"].plot.hist(bins=[0, 10, 15, 25], ax=axes[1])
axes[1].set_title("Distribution of transaction sales")
axes[1].set_xlabel("Sales per transaction")
fig.tight_layout()
plt.show()
```

**这两幅图分别回答什么？** 假设上表一行是一笔交易，`sales` 是金额（元）。左图先按门店合计，柱高为 A=22、B=43 元，比较的是门店总收入；右图不分门店，将五笔金额 `[10,12,8,15,20]` 放入金额区间，比较的是交易金额分布。

右图显式指定区间边界 `[0,10,15,25]`，三根柱分别计 `[0,10)`、`[10,15)`、`[15,25]`，频数是 `1、2、2` 笔。柱高为 2 表示该区间有两笔交易，不表示收入为 2 元。`ax=axes[1]` 只决定画在右侧绘图区，不会筛选第二家门店。

Pandas 绘图默认基于 Matplotlib；传入 `ax=` 可以把图画在指定绘图区。默认频数直方图的柱高是落入区间的观测数；若改为密度（Density）图，应按面积解释，不能仍当作原始频数。

分布的基本读法：均值容易受极端值影响；右偏（Right-skewed）意味着较长尾部向右；少量分箱可能隐藏细节，过多分箱可能突出随机噪声。

## 6. 箱线图：必须记对的公式

设第一四分位数为 $Q_1$，中位数为 $Q_2$，第三四分位数为 $Q_3$：

$$IQR=Q_3-Q_1$$

$$\text{下围栏}=Q_1-1.5IQR,\qquad\text{上围栏}=Q_3+1.5IQR$$

- 箱体：从 $Q_1$ 到 $Q_3$，表示中间约 50% 的数据范围。
- 箱内横线：中位数（Median），不是均值（Mean）。
- 须（Whiskers）：默认延伸到围栏内最远的**实际观测值**，不一定正好等于围栏。
- 围栏外的点：按这一规则标记为异常点（Outliers / Fliers），不等于数据错误，也不意味着必须删除。

教师教程把异常值阈值写成了“中位数 ± 1.5IQR”；这里按 Matplotlib 默认定义使用上面的 $Q_1/Q_3$ 围栏。不同软件或手算规则的四分位数定义可能不同，计算题应先看题目指定的约定。

```python
import numpy as np

values = np.array([1, 2, 3, 4, 5, 6, 7, 8, 20])
q1, median, q3 = np.percentile(values, [25, 50, 75])
iqr = q3 - q1
lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
outliers = values[(values < lower) | (values > upper)]
print(q1, median, q3, lower, upper, outliers)
# 3.0 5.0 7.0 -3.0 13.0 [20]
```

不要把“作图时把异常点单独画出来”理解为“已经从原数据中删除”。对比不同分组时，箱体位置反映分布位置，箱体高度反映中间数据的离散程度；样本量不同仍需谨慎解释。

## 7. 散点图与相关性

```python
fig, ax = plt.subplots()
df.plot.scatter(x="customers", y="sales", ax=ax)
ax.set_title("Sales and customer count")
plt.show()

# 多个数值特征的成对关系
pd.plotting.scatter_matrix(df[["customers", "sales"]], figsize=(6, 6))
plt.show()
```

相关系数（Correlation Coefficient）$r$ 的范围为 $[-1,1]$。正相关表示一个变量较大时另一个往往也较大；负相关相反；$|r|$ 接近 1 表示较强的线性关系。

**$r=0$ 表示没有线性相关，不表示完全没有关系，也不保证独立（Independence）。** 例如对称的 U 形关系可能线性相关很弱。散点图还能揭示分群、曲线、异常点，单个相关系数可能看不到这些结构。

相关性（Correlation）不能证明因果关系（Causation）。销售额与顾客数量相关不代表只增加顾客数量便必然按同样幅度提升利润；还需考虑客单价、成本及其他变量。

## 8. 纸笔例题与解答

**题目。** 对数组 `[1,2,3,4,5,6,7,8,20]`，使用 NumPy 默认百分位计算方式，已得 $Q_1=3$、$Q_2=5$、$Q_3=7$。求四分位距、上下围栏、上下须端点及异常值。

**解答。** $IQR=4$，围栏为 $3-6=-3$ 和 $7+6=13$。围栏内最小观测为 1，最大为 8，所以须端点为 1、8。20 超过上围栏，是异常点。须端点不是 −3、13；中位数为 5，不能把它当均值。

## 9. 易错点与自测

常见错误：把 `Axes` 与 `Axis` 混淆；子图索引维度写错；把任意行号当时间；把直方图区间当类别；把箱内线当均值；把围栏当须端点；由相关性直接推出因果。

1. 比较四家门店总收入，优先选哪种图？
2. 检查客户收入分布是否右偏，优先选哪种图？
3. `plt.subplots(2,2)` 返回的 `axes`，右下角如何索引？
4. $Q_1=10$、$Q_3=18$ 时，上围栏是多少？值 29 是否越界？
5. 两个变量相关系数为 0，是否可以断定彼此独立？

**简答：** 1. 柱状图。2. 直方图，也可辅以箱线图。3. `axes[1,1]`。4. $18+1.5(18-10)=30$；29 没有越界。5. 不能，可能存在非线性关系。

## 课程来源

- [Matplotlib 课程页](https://bana409.harrywang.me/docs/lectures/matplotlib)
- [教师教程：Matplotlib 与 Pandas Charting](https://www.harrywang.me/blog/data-science-intro#matplotlib)
- [Matplotlib 官方 boxplot 文档](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.boxplot.html)（核对默认围栏和须）
- [Assignment 1：图表需服务于商业问题](https://bana409.harrywang.me/docs/assignments/assignment-1-exploratory-data-analysis)

本章小数据、纸笔例题与自测为复习自编。
