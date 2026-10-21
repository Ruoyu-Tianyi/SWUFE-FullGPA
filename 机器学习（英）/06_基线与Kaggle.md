# 06 基线与 Kaggle（Kaggle and Model-Free Prediction）

[返回复习导航](00_复习导航.md)

本章对应课堂的规则预测（Rule-Based Prediction）与启发式挑战（Heuristic Challenge）。复习目标：能解释为什么先做基线，能根据分组统计写规则，能识别提交文件和评估方式中的错误。

## 1. 从业务判断到基线

基线（Baseline）是衡量后续方法是否值得使用的参照。分类问题可以始终预测训练集中的多数类；回归问题可以始终预测训练目标的均值。基线并不保证很准，但提供了“复杂模型究竟改善了多少”的比较起点。

无模型预测（Model-Free Prediction）在本课中指直接由人编写规则，而不调用学习算法拟合参数。例如，根据训练数据的分组存活率，写出“女性预测存活、男性预测未存活”。规则仍然利用了数据中的信息。

启发式（Heuristic）是依据经验或数据现象制定的简便规则，不意味着它在所有样本上都正确。

| 方法 | 规则从哪里来 | 例子 | 需要检查什么 |
|---|---|---|---|
| 常数基线 | 训练目标的总体分布 | 所有人预测不取消 | 类别是否不平衡 |
| 分组规则 | 训练数据的分组统计 | 按性别预测存活 | 小样本组是否可靠 |
| 条件组合规则 | 人工结合多个特征 | 长提前期且无押金则预测取消 | 条件优先级、覆盖范围 |
| 训练后的模型 | 算法从训练数据学习 | 决策树自动选择切分 | 是否过拟合、评估是否公平 |

## 2. Kaggle 的三个文件

| 文件 | 是否有目标值 | 用途 |
|---|---|---|
| `train.csv` | 通常有 | 探索数据、拟合规则或模型；也可划分本地验证/测试集 |
| `test.csv` | 通常没有 | 为每一行生成预测，提交到平台 |
| `sample_submission.csv` | 只有格式示例 | 检查列名、ID、目标格式和行数 |

**Kaggle 的 `test.csv` 不等于本地测试集（Local Test Set）。** 本地测试集通常从有标签的 `train.csv` 划出，因此我们能计算分数；Kaggle 测试文件的真实标签由平台保管，单靠该文件不能计算准确率。

Titanic 提交表需要 `PassengerId` 和 `Survived` 两列，其中 `Survived` 为整数 0 或 1。不要把 DataFrame 的索引额外导出成第三列。

## 3. 课堂 Titanic 的两条规则

课堂数据中，整体存活率约为 38.4%，所以多数类基线是全部预测 0。女性存活率约 74.2%，男性约 18.9%，由此得到第二条按性别预测的规则。

这些比例描述的是课堂给出的训练样本。它们不是业务规律的证明，也不保证未来数据保持同样比例。复习重点是**从统计结果到规则的推理方式**，无需死记某次排行榜分数。

准确率（Accuracy）的定义为：

$$
\operatorname{Accuracy}=\frac{\text{预测正确的样本数}}{\text{样本总数}}.
$$

两种规则必须在相同评估数据上比较。训练集准确率与另一规则的测试集准确率不能直接作为公平胜负依据。

## 4. 最小代码：先看分布，再写规则

以下为**自建教学数据**，并非完整 Titanic 数据。

```python
import pandas as pd

train = pd.DataFrame({
    "Sex": ["male"] * 6 + ["female"] * 4,
    "Survived": [0] * 6 + [1, 1, 1, 0],
})

print(train["Survived"].value_counts(normalize=True))
print(train.groupby("Sex")["Survived"].mean())

# 训练多数类为 0
pred_constant = pd.Series(0, index=train.index)
pred_gender = train["Sex"].eq("female").astype(int)

print(pred_constant.eq(train["Survived"]).mean())  # 0.7
print(pred_gender.eq(train["Survived"]).mean())    # 0.9
```

因为 `Survived` 是 0/1，组内均值正好等于组内正类比例。上述两个分数只是训练样本上的描述，尚不能证明性别规则在新数据上一定更好。

下面演示提交格式，运行后会在当前目录生成 `submission.csv`。

```python
test = pd.DataFrame({
    "PassengerId": [892, 893, 894],
    "Sex": ["male", "female", "male"],
})

submission = pd.DataFrame({
    "PassengerId": test["PassengerId"],
    "Survived": test["Sex"].eq("female").astype(int),
})

assert len(submission) == len(test)
assert submission["PassengerId"].equals(test["PassengerId"])
assert submission["Survived"].isin([0, 1]).all()
submission.to_csv("submission.csv", index=False)
```

这里假定 `Sex` 已检查且只有 `male`、`female`。实际数据若有缺失或其他取值，应事先指定合理的默认规则，不能让未知值无意中被当成男性。

若要练习课堂的 `.apply()`，等价写法为：

```python
def survival_by_gender(sex):
    return int(sex == "female")  # 已确认仅有两类

prediction = test["Sex"].apply(survival_by_gender)
```

## 5. 启发式挑战的完整思路

以酒店取消（Cancellation）为例，先明确正类 `Canceled = 1`，再执行以下步骤：

1. 看总体取消比例，建立全部不取消的常数基线。
2. 按渠道、押金类型等分组，看取消率以及每组样本数。
3. 对提前预订天数等数值变量尝试有业务意义的区间。
4. 把发现写成少量可解释的条件，明确条件冲突时的优先级。
5. 在保留的验证数据上比较规则，并记录改动理由。
6. 为所有待预测订单输出结果，检查 ID 与提交格式。

例如，`lead_time > 100` 与 `deposit_type == "No Deposit"` 是两个条件，组合时要用括号：

```python
bookings = pd.DataFrame({
    "booking_id": ["B01", "B02", "B03"],
    "lead_time": [30, 120, 150],  # 预订到入住的天数
    "deposit_type": ["No Deposit", "No Deposit", "Non Refund"],
})
risky = (bookings["lead_time"] > 100) & (
    bookings["deposit_type"] == "No Deposit"
)
rule_prediction = risky.astype(int)
print(rule_prediction.tolist())  # [0, 1, 0]，1 表示预测取消
```

上面三行是自建订单：B01 没超过 100 天，输出 0；B02 同时满足两个条件，输出 1；B03 虽提前 150 天，但押金类型不匹配，仍输出 0。`&` 要求两项都成立，`.astype(int)` 再把布尔值转成提交需要的 0/1。此处只有预测，没有真实取消标签，所以不能直接计算这三行的准确率。

阈值 100 只是示意，不是课程指定的最优阈值。样本很少的组出现 100% 取消率，并不能说明该规则值得推广。

## 6. 手算例题：高准确率是否足够

**自建例题。** 验证集有 100 个订单，其中 80 个未取消、20 个取消。规则 A 全部预测未取消；规则 B 正确找出 12 个取消订单，同时把 6 个未取消订单误报为取消。

规则 A 的正确数为 80，准确率为 80%。规则 B 的正确数为：

$$12+(80-6)=86,\qquad \operatorname{Accuracy}_B=86\%.$$

规则 B 在这个验证集上准确率更高。若误报和漏报损失不同，还应比较业务成本；第 09 章会计算这一点。规则 A 的 80% 也说明了类别不平衡（Class Imbalance）可能让“不做区分”的预测看起来很好。

## 7. 常见失分点

- 删除 Kaggle 测试数据的缺失行：会造成部分 ID 没有预测。应采用适当填充等方式保留待预测行。
- 独热编码后只比较列数：即使列数相同，列名或顺序也可能不同。
- 用测试数据决定均值、阈值或类别映射：标准流程应从训练数据学习这些内容，再应用到后续数据。
- 不断根据公共排行榜调规则：也可能对公共测试部分过拟合，排行榜分数并非永远可信的独立检验。
- 看到模型训练准确率更高就认为优于规则：应比较同一验证集或同一交叉验证设置下的结果。
- 认为规则简单就没有过拟合：大量试阈值、试组合也可能拟合验证集噪声。

## 8. 纸笔自测

1. `train.csv` 中 90% 的标签为 0。全部预测 0 是否说明模型已能识别正类？
2. Kaggle 的 `test.csv` 没有目标列，为什么仍称为测试数据？我们能直接计算准确率吗？
3. 导出提交文件时 `index=False` 的作用是什么？
4. 两条规则分别在不同验证划分上得到 0.81 和 0.82，能直接断定第二条更好吗？
5. 某训练组只有 2 个样本且全为正类，把未来所有该组样本预测为正类有什么风险？

### 自测答案

1. 不能。它在相同类比例的样本上可得到 90% 准确率，但正类召回率为 0。
2. 平台用隐藏标签评估提交结果；本地没有真实标签，不能直接计算准确率。
3. 不把 DataFrame 行索引写入 CSV，避免多出不需要的列。
4. 不能。样本难度和随机划分不同，应在同一评估设置下比较。
5. 组内比例非常不稳定，可能只是偶然现象；需要更多证据和独立验证。

## 9. 来源与复习边界

- [课程：Kaggle and Model-Free Prediction](https://bana409.harrywang.me/docs/lectures/kaggle-and-model-free-prediction)
- [课程：Rule-Based Prediction](https://bana409.harrywang.me/docs/lectures/kaggle-and-model-free-prediction/rule-based-prediction)
- [课程：Heuristic Challenge](https://bana409.harrywang.me/docs/lectures/kaggle-and-model-free-prediction/heuristic-challenge)

排行榜反复调试与验证集可比性属于帮助理解泛化的整理说明。考试具体题目与各章权重尚未公布。
