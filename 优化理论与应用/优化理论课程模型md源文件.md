# 《优化理论》课程问题与解答整理

> 本 Markdown 按照课程单元整理了所有课件中的问题描述、数学建模（目标函数 + 约束条件）以及 Python + Gurobi 编程答案。所用 Python 库仅限 `gurobipy`、NumPy、pandas、matplotlib、folium 以及课件/作业中提到的其他常见库。

---

## 目录

- [Unit 3：Portfolio Optimization（投资组合优化）](#unit-3-portfolio-optimization)
- [Unit 4：Facility Location（设施选址）](#unit-4-facility-location)
- [Unit 5：Traveling Salesman Problem（旅行商问题）](#unit-5-traveling-salesman-problem)
- [Unit 6：Heuristics（启发式算法）](#unit-6-heuristics)
- [Unit 7：Game Theory（博弈论）](#unit-7-game-theory)

---

## Unit 3：Portfolio Optimization

### 问题 3.1：Markowitz 均值-方差模型（课件基础模型）

#### 问题描述

给定 $n$ 支股票，希望在预算 $B$ 内决定每支股票的投资金额 $x_i$，使得投资组合的方差最小，同时期望收益不低于目标 $\beta$，且不允许卖空。

#### 数学建模

**参数：**

- $i$：股票，$i = 1, 2, \dots, n$
- $\mu_i$：股票 $i$ 的期望收益
- $\sigma_{ij}$：股票 $i$ 与 $j$ 的协方差（$\Sigma$ 为协方差矩阵）
- $B$：投资预算
- $\beta$：目标期望收益

**决策变量：**

- $x_i \geq 0$：投资股票 $i$ 的金额

**目标函数：**
$$
\min \quad \sum_{i=1}^{n}\sum_{j=1}^{n} \sigma_{ij} x_i x_j \; = \; \mathbf{x}^{\top} \Sigma \mathbf{x}
$$

**约束条件：**
$$
\begin{aligned}
\sum_{i=1}^{n} x_i &\leq B \quad \text{（预算约束）} \\
\sum_{i=1}^{n} \mu_i x_i &\geq \beta \quad \text{（收益目标）} \\
x_i &\geq 0, \quad \forall i \quad \text{（无卖空）}
\end{aligned}
$$

> 这是一个**二次优化问题（Quadratic Programming, QP）**，目标函数为二次，约束为线性，可用 Gurobi 求解。

---

#### Python 答案（Gurobi）

```python
import pandas as pd
import gurobipy as gp

# ===== 数据读取（实际作业使用 data_portfolio.csv）=====
data = pd.read_csv('data_portfolio.csv')    # 读取CSV文件，数据行为各期收益，列为各股票
stocks = data.columns.values               # 提取列名（股票代码列表）

ret_mean = data.mean()    # 对每列求均值 → 各股票的期望收益率
mu = dict(ret_mean)       # 转成字典，键=股票名，值=期望收益
Sigma = data.cov().values # 计算各列的协方差矩阵（即各股票收益的协方差）

budget = 1000
beta = 5
# ===== 模型建立 =====
m = gp.Model('markowitz')

x = m.addVars(stocks, lb=0, name='x')

# 目标：min x^T Sigma x
m.setObjective(
    gp.quicksum(Sigma[i, j] * x[stocks[i]] * x[stocks[j]]
                for i in range(len(stocks)) for j in range(len(stocks))),
    gp.GRB.MINIMIZE
)
# 约束1：预算
m.addConstr(gp.quicksum(x[s] for s in stocks) <= budget, name='budget')
# 约束2：收益目标
m.addConstr(gp.quicksum(mu[s] * x[s] for s in stocks) >= beta, name='return')
# 求解
m.optimize()

# 输出结果
if m.status == gp.GRB.OPTIMAL:
    print(f"最优目标值（最小方差）= {m.ObjVal:.6f}")
    print("\n各股票投资金额：")
    for s in stocks:
        if x[s].X > 1e-3:
            print(f"  {s}: {x[s].X:.4f}")
    print(f"\n总投资: {sum(x[s].X for s in stocks):.4f}")
    print(f"总期望收益: {sum(mu[s] * x[s].X for s in stocks):.4f}")
```

---

### 问题 3.2：Portfolio Optimization II — 最大化达到目标收益的概率（课件 Page 14）

#### 问题描述

在同样的投资决策框架下，不再最小化方差，而是最大化投资组合收益不低于目标 $\beta$ 的概率。在正态分布假设下，可转化为一个可求解的优化问题。

#### 问题推导（课件）

假设股票收益 $\tilde{\mathbf{r}}$ 服从多元正态分布，则：
$$
\mathbb{P}[\tilde{\mathbf{r}}^{\top} \mathbf{x} \geq \beta]
= \Phi\!\left( \frac{\boldsymbol{\mu}^{\top} \mathbf{x} - \beta}{\sqrt{\mathbf{x}^{\top} \Sigma \mathbf{x}}} \right)
$$

最大化该概率等价于最大化括号内的值（Sharpe ratio 形式）。进一步做变量替换：令 $y = \boldsymbol{\mu}^{\top} \mathbf{x} - \beta$，$\bar{\mathbf{x}} = \mathbf{x} / y$，$z = 1/y$，则得到：

#### 数学建模（转化后的二次优化问题）

**决策变量：**
- $\bar{x}_i$：辅助变量（与 $x_i$ 成正比）
- $z \geq 0$：辅助变量

**目标函数：**
$$
\min \quad \bar{\mathbf{x}}^{\top} \Sigma \bar{\mathbf{x}}
$$

**约束条件：**
$$
\begin{aligned}
\sum_{i=1}^{n} \bar{x}_i &\leq B \cdot z \quad \text{（预算约束）} \\
\sum_{i=1}^{n} \mu_i \bar{x}_i - \beta \cdot z &= 1 \quad \text{（归一化约束）} \\
\bar{x}_i &\geq 0, \quad z \geq 0
\end{aligned}
$$

**还原实际投资金额：**
$$
x_i = \frac{\bar{x}_i}{z}
$$

---

#### Python 答案（Gurobi）

```python
# -*- coding: utf-8 -*-
import pandas as pd
from gurobipy import *
# ===== 数据读取 =====
data1 = pd.read_csv('data_portfolio.csv') # 读取CSV文件，数据行为各期收益，列为各股票
stocks = data1.columns.values             # 提取列名（股票代码列表）

ret_mean = data1.mean()                   # 对每列求均值 → 各股票的期望收益率
ret_mean = dict(ret_mean)                 # 转成字典，键=股票名，值=期望收益
ret_cov = data1.cov()                     # 计算各列的协方差矩阵（即各股票收益的协方差）

budget = 1000
exp_ret = 5
# ===== 模型建立 =====
m = Model('portfolio_max_prob')

x = m.addVars(stocks, name='bar')
z = m.addVar(name='z', lb=0)
# 目标函数：min x̄^T Σ x̄
m.setObjective(
    quicksum(ret_cov.loc[i, j] * x[i] * x[j]
             for i in stocks for j in stocks),
    sense=GRB.MINIMIZE
)
# 约束1：预算约束
m.addConstr(
    quicksum(x[i] for i in stocks) <= budget * z,
    name='budget_con'
)
# 约束2：归一化约束
m.addConstr(
    quicksum(ret_mean[i] * x[i] for i in stocks) - exp_ret * z == 1,
    name='norm_con'
)

m.write('model.lp')
m.optimize()
# ===== 结果输出 =====
if m.status == GRB.OPTIMAL:
    z_val = z.X
    if abs(z_val) < 1e-6:
        print("Warning: z 接近 0，模型可能无意义或 β 设置过高")
    else:
        print(f"\n最优目标值 (x̄^T Σ x̄) = {m.ObjVal:.6f}")
        print(f"辅助变量 z = {z_val:.6f}")
        print("\n--- 实际投资金额 x = x̄ / z ---")
        
        total_invested = 0
        actual_x = {}
        for s in stocks:
            val = x[s].X / z_val
            actual_x[s] = val
            total_invested += val
            if abs(val) > 1e-3:
                print(f"{s}: x̄ = {x[s].X:.4f},  x = {val:.4f}")
        
        print(f"\n总投资金额: {total_invested:.4f} (应 <= {budget})")
```

> **数据说明：** `data_portfolio.csv` 包含 5 支股票（JPM, AMZN, AAPL, DOC, GOOG）的历史收益率数据，共 40 期。

---

### 问题 3.3：Assignment 0 — 广告优化（LP）

#### 问题描述

某百货商店经理需要决定广告投放方案。有三种媒体可选：电视（TV）、报纸（Newspaper）、广播（Radio）。各类广告成本、受众人数及性别/年龄分布如下：

| 媒体 | 成本 | Senior Male | Senior Female | Young Male | Young Female |
|------|------|-------------|---------------|------------|--------------|
| TV   | $15,000 | 5,000 | 5,000 | 5,000 | 10,000 |
| Newspaper | $4,000 | 4,000 | 3,000 | 2,000 | 1,000 |
| Radio | $6,000 | 1,500 | 1,500 | 4,500 | 7,500 |

广告政策：
(a) 广播广告数量至少是报纸的两倍；
(b) 总触达客户至少 100,000 人；
(c) 触达年轻人至少是老年人的两倍；
(d) 女性受众至少占 60%；
(e) 报纸广告最多 7 个。

求最小化总成本的最优广告投放组合。

#### 数学建模

**决策变量：**
- $x_1$：电视广告数量
- $x_2$：报纸广告数量
- $x_3$：广播广告数量

**目标函数：**
$$
\min \quad 15000 x_1 + 4000 x_2 + 6000 x_3
$$

**约束条件：**
$$
\begin{aligned}
x_3 &\geq 2 x_2 \quad \text{（广播 >= 2×报纸）} \\
25000 x_1 + 10000 x_2 + 15000 x_3 &\geq 100000 \quad \text{（总触达）} \\
(5+10)000 x_1 + (2+1)000 x_2 + (4.5+7.5)000 x_3 &\geq 2 \times [(5+5)000 x_1 + (4+3)000 x_2 + (1.5+1.5)000 x_3] \quad \text{（年轻人 >= 2×老年人）} \\
(5+10)000 x_1 + (3+1)000 x_2 + (1.5+7.5)000 x_3 &\geq 0.6 \times \text{总触达} \quad \text{（女性 >= 60%）} \\
x_2 &\leq 7 \quad \text{（报纸上限）} \\
x_1, x_2, x_3 &\geq 0 \text{ 且为整数}
\end{aligned}
$$

> 以上为根据题意推导的标准 LP 模型，可用 Gurobi 直接求解。

---

#### Python 答案（Gurobi）

```python
import gurobipy as gp

# ===== 模型建立 =====
m = gp.Model('advertising')

x1 = m.addVar(vtype=gp.GRB.INTEGER, lb=0, name='TV')
x2 = m.addVar(vtype=gp.GRB.INTEGER, lb=0, name='Newspaper')
x3 = m.addVar(vtype=gp.GRB.INTEGER, lb=0, name='Radio')

# 目标：最小化总成本
m.setObjective(15000*x1 + 4000*x2 + 6000*x3, gp.GRB.MINIMIZE)

# 约束a：广播 >= 2×报纸
m.addConstr(x3 >= 2*x2, name='radio_vs_newspaper')

# 约束b：总触达 >= 100,000
m.addConstr(25000*x1 + 10000*x2 + 15000*x3 >= 100000, name='reach')

# 约束c：年轻人 >= 2×老年人
# Young = 15000x1 + 3000x2 + 12000x3, Senior = 10000x1 + 7000x2 + 3000x3
m.addConstr(15000*x1 + 3000*x2 + 12000*x3 >= 2*(10000*x1 + 7000*x2 + 3000*x3), name='young_vs_senior')

# 约束d：女性 >= 60% 总触达
# Female = 15000x1 + 4000x2 + 9000x3, Total = 25000x1 + 10000x2 + 15000*x3
m.addConstr(15000*x1 + 4000*x2 + 9000*x3 >= 0.6*(25000*x1 + 10000*x2 + 15000*x3), name='female_ratio')

# 约束e：报纸上限
m.addConstr(x2 <= 7, name='newspaper_limit')

# 求解
m.optimize()

# 输出结果
if m.status == gp.GRB.OPTIMAL:
    print(f"最优总成本: ${m.ObjVal:,.0f}")
    print(f"TV 广告数: {x1.X:.0f}")
    print(f"Newspaper 广告数: {x2.X:.0f}")
    print(f"Radio 广告数: {x3.X:.0f}")
    
    total_reach = 25000*x1.X + 10000*x2.X + 15000*x3.X
    young_reach = 15000*x1.X + 3000*x2.X + 12000*x3.X
    senior_reach = 10000*x1.X + 7000*x2.X + 3000*x3.X
    female_reach = 15000*x1.X + 4000*x2.X + 9000*x3.X
    
    print(f"\n总触达: {total_reach:,.0f}")
    print(f"年轻人触达: {young_reach:,.0f} (老年人: {senior_reach:,.0f})")
    print(f"女性触达: {female_reach:,.0f} (占比: {female_reach/total_reach:.2%})")
```

---

---

### 问题 3.4：Assignment 0 — 货币兑换（可选）

#### 问题描述

有 $N$ 种货币，1 单位货币 $i$ 可兑换 $r_{ij}$ 单位货币 $j$（$r_{ij} > 0$）。每天货币 $i$ 的兑换总额上限为 $u_i$。初始持有 $B$ 单位货币 1，希望通过一系列交易最大化最终持有的货币 $N$ 的数量。假设不存在套利循环（即对任意货币循环 $i_1 \to i_2 \to \dots \to i_k \to i_1$，有 $r_{i_1 i_2} r_{i_2 i_3} \dots r_{i_k i_1} \leq 1$）。

#### 数学建模（LP）

**决策变量：**
- $x_{ij} \geq 0$：从货币 $i$ 兑换到货币 $j$ 的数量

**目标函数：**
$$
\max \quad \sum_{i=1}^{N-1} r_{iN} x_{iN} - \sum_{j=1}^{N-1} x_{Nj}
$$
（即流入货币 $N$ 的净数量）

更标准的写法是引入每个货币 $k$ 的**净持有量** $y_k$：

$$
\begin{aligned}
\max \quad & y_N \\
\text{s.t.} \quad & y_1 = B - \sum_{j \neq 1} x_{1j} + \sum_{i \neq 1} r_{i1} x_{i1} \\
& y_k = \sum_{i \neq k} r_{ik} x_{ik} - \sum_{j \neq k} x_{kj}, \quad k = 2, \dots, N \\
& \sum_{j \neq i} x_{ij} \leq u_i, \quad \forall i \\
& x_{ij} \geq 0, \quad y_k \geq 0
\end{aligned}
$$

> 以下使用 Gurobi 求解。

---

#### Python 答案（Gurobi）

```python
import numpy as np
import gurobipy as gp

# ===== 数据（课件概念题，实际考试/作业替换为题目给定数据）=====
N = 4   # 4 种货币
B = 100   # 初始持有 100 单位货币 1
u_limit = [80, 60, 70, 50]   # 每种货币兑换上限

# 汇率矩阵：r[i][j] 表示 1 单位 i 可换 j 的数量
r = np.array([
    [1.0, 0.85, 1.12, 0.74],   # 货币 1
    [1.17, 1.0, 1.31, 0.87],   # 货币 2
    [0.89, 0.76, 1.0, 0.66],   # 货币 3
    [1.35, 1.15, 1.51, 1.0]    # 货币 4
])

# ===== 模型建立 =====
m = gp.Model('currency_exchange')

x = m.addVars(N, N, lb=0, name='x')   # x[i,j] = 从 i 换到 j 的数量
y = m.addVars(N, lb=0, name='y')     # y[k] = 货币 k 的净持有量

# 目标：最大化货币 N 的净持有量
m.setObjective(y[N-1], gp.GRB.MAXIMIZE)

# 约束1：货币 1 的净持有量 = 初始 - 换出 + 换入
m.addConstr(
    y[0] == B - gp.quicksum(x[0, j] for j in range(N) if j != 0)
          + gp.quicksum(r[i, 0] * x[i, 0] for i in range(N) if i != 0),
    name='balance_1'
)

# 约束2：其他货币的净持有量
for k in range(1, N):
    m.addConstr(
        y[k] == gp.quicksum(r[i, k] * x[i, k] for i in range(N) if i != k)
              - gp.quicksum(x[k, j] for j in range(N) if j != k),
        name=f'balance_{k}'
    )

# 约束3：每种货币兑换上限
for i in range(N):
    m.addConstr(
        gp.quicksum(x[i, j] for j in range(N) if j != i) <= u_limit[i],
        name=f'limit_{i}'
    )

# 求解
m.optimize()

# 输出结果
if m.status == gp.GRB.OPTIMAL:
    print(f"最优目标值（货币 {N} 净持有量）= {m.ObjVal:.4f}")
    print("
各货币净持有量：")
    for k in range(N):
        if y[k].X > 1e-3:
            print(f"  货币 {k+1}: {y[k].X:.4f}")
    print("
兑换操作：")
    for i in range(N):
        for j in range(N):
            if i != j and x[i, j].X > 1e-3:
                print(f"  {x[i,j].X:.4f} 单位货币 {i+1} → 货币 {j+1}")
```

---


---

## Unit 4：Facility Location

### 问题 4.1：p-Median 问题（课件）

#### 问题描述

给定 $n$ 个客户（集合 $\mathcal{I}$）和 $m$ 个候选设施点（集合 $\mathcal{J}$），需要从中选出 $p$ 个设施点开设，并将每个客户分配到一个已开设的设施点，使得总服务距离/成本最小。

#### 数学建模

**参数：**

- $c_{ij}$：客户 $i$ 由设施 $j$ 服务的距离/成本
- $p$：需开设的设施数量

**决策变量：**

- $x_j \in \{0, 1\}$：设施 $j$ 是否开设（1 = 开设）
- $y_{ij} \in \{0, 1\}$：客户 $i$ 是否分配给设施 $j$

**目标函数：**
$$
\min \quad \sum_{i \in \mathcal{I}} \sum_{j \in \mathcal{J}} c_{ij} y_{ij}
$$

**约束条件：**
$$
\begin{aligned}
\sum_{j \in \mathcal{J}} y_{ij} &= 1, \quad \forall i \in \mathcal{I} \quad \text{（每个客户必须被服务）} \\
\sum_{j \in \mathcal{J}} x_j &= p \quad \text{（恰好开设 $p$ 个设施）} \\
y_{ij} &\leq x_j, \quad \forall i \in \mathcal{I}, j \in \mathcal{J} \quad \text{（只能分配给已开设的设施）} \\
x_j &\in \{0, 1\}, \quad y_{ij} \in \{0, 1\}
\end{aligned}
$$

---

#### Python 答案（Gurobi）

```python
import numpy as np
import gurobipy as gp

# ===== 数据（课件概念题，实际考试/作业替换为题目给定数据）=====
n = 10   # 客户数
m = 8    # 候选设施数
p = 3    # 开设设施数

np.random.seed(42)
loc_cust = np.random.randint(0, 100, (n, 2))   # 客户坐标
loc_fac = np.random.randint(0, 100, (m, 2))    # 设施坐标

# 计算欧氏距离
c = {(i, j): np.linalg.norm(loc_cust[i] - loc_fac[j])
     for i in range(n) for j in range(m)}

I = range(n)
J = range(m)

# ===== 模型建立 =====
model = gp.Model('pmedian')

x = model.addVars(J, vtype=gp.GRB.BINARY, name='x')
y = model.addVars(I, J, vtype=gp.GRB.BINARY, name='y')

model.setObjective(gp.quicksum(c[i, j] * y[i, j] for i in I for j in J), gp.GRB.MINIMIZE)

model.addConstrs((gp.quicksum(y[i, j] for j in J) == 1 for i in I), name='assign')
model.addConstr(gp.quicksum(x[j] for j in J) == p, name='p_facilities')
model.addConstrs((y[i, j] <= x[j] for i in I for j in J), name='link')

model.optimize()

# 输出结果
if model.status == gp.GRB.OPTIMAL:
    print(f"最优总距离 = {model.ObjVal:.2f}")
    opened = [j for j in J if x[j].X > 0.9]
    print(f"开设设施: {opened}")
    for i in I:
        assigned = [j for j in J if y[i, j].X > 0.9]
        print(f"  客户 {i} → 设施 {assigned[0]}, 距离={c[i, assigned[0]]:.2f}")
```

---

### 问题 4.2：p-Center 问题（课件）

#### 问题描述

与 p-Median 类似，但目标改为最小化**最远的**客户到设施的距离，体现公平性。常用于消防站、急救中心等公共设施的选址。

#### 数学建模

引入辅助变量 $w$ 表示最大服务距离。

**目标函数：**
$$
\min \quad w
$$

**约束条件：**
$$
\begin{aligned}
\sum_{j \in \mathcal{J}} y_{ij} &= 1, \quad \forall i \in \mathcal{I} \\
\sum_{j \in \mathcal{J}} x_j &= p \\
y_{ij} &\leq x_j, \quad \forall i, j \\
\sum_{j \in \mathcal{J}} c_{ij} y_{ij} &\leq w, \quad \forall i \in \mathcal{I} \quad \text{（每个客户的服务距离不超过 $w$）} \\
x_j &\in \{0, 1\}, \quad y_{ij} \in \{0, 1\}
\end{aligned}
$$

> 注：该模型通过引入 $w$ 将 min-max 问题线性化，可用 Gurobi 求解。

---

#### Python 答案（Gurobi）

```python
import numpy as np
import gurobipy as gp

# ===== 数据（课件概念题，实际考试/作业替换为题目给定数据）=====
n = 10   # 客户数
m = 8    # 候选设施数
p = 3    # 开设设施数

np.random.seed(42)
loc_cust = np.random.randint(0, 100, (n, 2))
loc_fac = np.random.randint(0, 100, (m, 2))

c = {(i, j): np.linalg.norm(loc_cust[i] - loc_fac[j])
     for i in range(n) for j in range(m)}

I = range(n)
J = range(m)

# ===== 模型建立 =====
model = gp.Model('pcenter')

x = model.addVars(J, vtype=gp.GRB.BINARY, name='x')
y = model.addVars(I, J, vtype=gp.GRB.BINARY, name='y')
w = model.addVar(lb=0, name='w')   # 最大服务距离

model.setObjective(w, gp.GRB.MINIMIZE)

model.addConstrs((gp.quicksum(y[i, j] for j in J) == 1 for i in I), name='assign')
model.addConstr(gp.quicksum(x[j] for j in J) == p, name='p_facilities')
model.addConstrs((y[i, j] <= x[j] for i in I for j in J), name='link')
model.addConstrs((gp.quicksum(c[i, j] * y[i, j] for j in J) <= w for i in I), name='max_dist')

model.optimize()

# 输出结果
if model.status == gp.GRB.OPTIMAL:
    print(f"最优最大距离 = {w.X:.2f}")
    opened = [j for j in J if x[j].X > 0.9]
    print(f"开设设施: {opened}")
    for i in I:
        assigned = [j for j in J if y[i, j].X > 0.9]
        dist = c[i, assigned[0]]
        print(f"  客户 {i} → 设施 {assigned[0]}, 距离={dist:.2f}")
```

---

---

### 问题 4.3：Fixed-Charge Facility Location（课件）

#### 问题描述

每个候选设施点 $j$ 开设需要支付固定成本 $f_j$，且有容量限制 $v_j$。客户 $i$ 的需求为 $d_i$，由设施 $j$ 服务每单位需求的可变成本为 $c_{ij}$。决定开设哪些设施以及如何分配客户需求，使总成本（固定成本 + 可变成本）最小。

#### 数学建模

**参数：**
- $d_i$：客户 $i$ 的需求
- $f_j$：开设设施 $j$ 的固定成本
- $v_j$：设施 $j$ 的容量
- $c_{ij}$：单位服务成本

**决策变量：**
- $x_j \in \{0, 1\}$：设施 $j$ 是否开设
- $y_{ij} \in [0, 1]$：客户 $i$ 由设施 $j$ 服务的**需求比例**

**目标函数：**
$$
\min \quad \sum_{j \in \mathcal{J}} f_j x_j + \sum_{i \in \mathcal{I}} \sum_{j \in \mathcal{J}} c_{ij} d_i y_{ij}
$$

**约束条件：**
$$
\begin{aligned}
\sum_{j \in \mathcal{J}} y_{ij} &= 1, \quad \forall i \in \mathcal{I} \quad \text{（需求完全满足）} \\
\sum_{i \in \mathcal{I}} d_i y_{ij} &\leq v_j x_j, \quad \forall j \in \mathcal{J} \quad \text{（容量约束）} \\
x_j &\in \{0, 1\}, \quad y_{ij} \in [0, 1]
\end{aligned}
$$

> 以下使用 Gurobi 求解。

---

#### Python 答案（Gurobi）

```python
import numpy as np
import gurobipy as gp

# ===== 数据（课件概念题，实际考试/作业替换为题目给定数据）=====
n = 8   # 客户数
m = 5   # 候选设施数

np.random.seed(42)
d = np.random.randint(10, 50, n)                 # 客户需求
f = np.random.randint(100, 200, m)               # 固定开设成本
v = np.random.randint(80, 150, m)                # 设施容量
c = np.random.randint(1, 10, (n, m))             # 单位服务成本

I = range(n)
J = range(m)

# ===== 模型建立 =====
model = gp.Model('fixed_charge')

x = model.addVars(J, vtype=gp.GRB.BINARY, name='x')
y = model.addVars(I, J, lb=0, ub=1, name='y')

model.setObjective(
    gp.quicksum(f[j] * x[j] for j in J) +
    gp.quicksum(c[i, j] * d[i] * y[i, j] for i in I for j in J),
    gp.GRB.MINIMIZE
)

model.addConstrs((gp.quicksum(y[i, j] for j in J) == 1 for i in I), name='demand')
model.addConstrs((gp.quicksum(d[i] * y[i, j] for i in I) <= v[j] * x[j] for j in J), name='capacity')

model.optimize()

# 输出结果
if model.status == gp.GRB.OPTIMAL:
    print(f"最优总成本 = {model.ObjVal:.2f}")
    opened = [j for j in J if x[j].X > 0.9]
    print(f"开设设施: {opened}")
    for j in opened:
        served = [i for i in I if y[i, j].X > 0.01]
        print(f"  设施 {j} 服务客户: {served}")
```

---

### 问题 4.4：作业 — 门店关闭选址（Grocery Store Chain）

#### 问题描述

某杂货连锁店在一个城市有 10 家门店，要求任意两家门店之间的距离不能小于 2 英里。下图将距离小于 2 英里的门店用圆圈标出。已知各门店月收益（单位：千美元），需要决定保留哪些门店，使得保留门店的总收益最大。

**门店收益：**

| 门店 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|------|---|---|---|---|---|---|---|---|---|----|
| 收益 | 127 | 83 | 165 | 96 | 112 | 88 | 135 | 141 | 117 | 94 |

**互斥圆圈（距离 < 2 英里）：**

- Circle 1：门店 {1, 2, 4}
- Circle 2：门店 {3, 4, 5}
- Circle 3：门店 {4, 5, 6, 7}
- Circle 4：门店 {5, 6, 9}
- Circle 5：门店 {6, 7, 8}
- Circle 6：门店 {8, 9, 10}
- Circle 7：门店 {5, 9}

#### 数学建模

**决策变量：**
- $x_i \in \{0, 1\}$：门店 $i$ 是否保留（1 = 保留）

**目标函数：**
$$
\max \quad \sum_{i=1}^{10} r_i x_i
$$
其中 $r_i$ 为门店 $i$ 的收益。

**约束条件：**
$$
\begin{aligned}
x_1 + x_2 + x_4 &\leq 1 \quad \text{（Circle 1）} \\
x_3 + x_4 + x_5 &\leq 1 \quad \text{（Circle 2）} \\
x_4 + x_5 + x_6 + x_7 &\leq 1 \quad \text{（Circle 3）} \\
x_5 + x_6 + x_9 &\leq 1 \quad \text{（Circle 4）} \\
x_6 + x_7 + x_8 &\leq 1 \quad \text{（Circle 5）} \\
x_8 + x_9 + x_{10} &\leq 1 \quad \text{（Circle 6）} \\
x_5 + x_9 &\leq 1 \quad \text{（Circle 7）} \\
x_i &\in \{0, 1\}, \quad i = 1, \dots, 10
\end{aligned}
$$

#### Python 答案（Gurobi）

```python
import gurobipy as gp

# ===== 数据 =====
revenue = {
    1: 127, 2: 83, 3: 165, 4: 96, 5: 112,
    6: 88, 7: 135, 8: 141, 9: 117, 10: 94
}
circles = [
    [1, 2, 4],       # 圆圈1
    [3, 4, 5],       # 圆圈2
    [4, 5, 6, 7],    # 圆圈3
    [5, 6, 9],       # 圆圈4
    [6, 7, 8],       # 圆圈5
    [8, 9, 10],      # 圆圈6
    [5, 9]           # 圆圈7
]
I = list(range(1, 11))   # [1, 2, 3, ..., 10]

# ===== 模型建立 =====
m = gp.Model('store_selection')

x = m.addVars(I, vtype=gp.GRB.BINARY, name='x')

m.setObjective(x.prod(revenue), gp.GRB.MAXIMIZE)

m.addConstrs(
    (gp.quicksum(x[i] for i in circles[k]) <= 1 for k in range(7)),
    name='conflict'
)

# ===== 求解 =====
m.optimize()

print('=== 求解结果 ===')
keep = [i for i in I if x[i].X > 0.9]
close = [i for i in I if x[i].X < 0.1]
print(f'保留的门店：{keep}')
print(f'关闭的门店：{close}')
print(f'总收入：${m.objVal * 1000:,.0f}')
```

**求解结果：**
- 保留门店：1, 3, 7, 9
- 关闭门店：2, 4, 5, 6, 8, 10
- 最大总收益：$544,000

---

### 问题 4.5：Exercise — p-Median 中国城市设施选址

#### 问题描述

使用 `cn.csv` 数据（中国 2577 个城市，包含经纬度、人口、行政级别等），从中选择行政级别为 `admin` 或 `primary` 的城市作为候选设施点，建立 p-Median 模型，选择 $p = 20\%$ 的城市作为设施点，最小化所有城市到最近设施点的总距离。结果用 folium 地图可视化。

#### Python 答案（Gurobi + folium）

```python
import numpy as np
import pandas as pd
import gurobipy as gp
import folium

# ===== 数据读取与预处理 =====
data = pd.read_csv('cn.csv')                                # 读取CSV文件，每行一个城市，含经纬度、行政级别等字段
data = data[(data['capital'] == 'admin') | (data['capital'] == 'primary')]   # 筛选：只保留省会城市/直辖市

n = data.shape[0]                                          # 获取筛选后的行数（城市数量）
cities = data['city'].values                               # 提取'city'列 → 城市名称数组
loc_x_vals = data['lat'].values   # 纬度                   # 提取'lat'列 → 纬度数组（后续计算距离用）
loc_y_vals = data['lng'].values   # 经度                 # 提取'lng'列 → 经度数组（后续计算距离用）
loc_x = dict(zip(cities, loc_x_vals))
loc_y = dict(zip(cities, loc_y_vals))

I = cities   # 客户集合
J = cities   # 候选设施集合
p = round(n * 0.2)   # 开设设施数量（20%）

# 计算欧氏距离（基于经纬度）
c = {(i, j): ((loc_x[i] - loc_x[j])**2 + (loc_y[i] - loc_y[j])**2)**0.5
     for i in I for j in J}

# ===== 模型建立 =====
m = gp.Model('pmedian')

x = m.addVars(I, vtype=gp.GRB.BINARY, name='x')       # 设施点是否开设
y = m.addVars(I, J, vtype=gp.GRB.BINARY, name='y')   # 客户分配给哪个设施

m.setObjective(y.prod(c), gp.GRB.MINIMIZE)

m.addConstrs((y.sum(i, '*') == 1 for i in I), name='cover')   # 每个客户被覆盖
m.addConstr(x.sum() == p, name='p_location')                  # 恰好开设 p 个
m.addConstrs((y[i, j] <= x[j] for i in I for j in J), name='capacity')  # 只能去开设的设施

# ===== 求解 =====
m.params.TimeLimit = 30
m.optimize()

print('The solution time is', m.runtime)
print('The MIP gap is', m.mipgap)

# ===== 可视化 =====
if m.status != gp.GRB.INFEASIBLE:
    pmedian_map = folium.Map(location=[34.32, 106.55], zoom_start=4)
    
    cities_selected = [j for j in J if x[j].x > 0.9]
    for i in I:
        if i in cities_selected:
            folium.Marker(location=(loc_x[i], loc_y[i]),
                          icon=folium.Icon(color='red'), popup=i).add_to(pmedian_map)
        else:
            folium.Marker(location=(loc_x[i], loc_y[i]), popup=i).add_to(pmedian_map)
    
    # 绘制分配关系
    assignments = [(i, j) for i in I for j in J if y[i, j].x > 0.9]
    for (i, j) in assignments:
        folium.PolyLine(
            [(loc_x[i], loc_y[i]), (loc_x[j], loc_y[j])]
        ).add_to(pmedian_map)
    
    pmedian_map.save('pmedian_map.html')
```

> **数据说明：** `cn.csv` 包含中国 2577 个城市的经纬度信息。筛选后约有 70 个 admin/primary 城市作为候选设施点，选择其中约 14 个（20%）作为设施点。

---


---

## Unit 5：Traveling Salesman Problem

### 问题 5.1：TSP 基础模型（课件）

#### 问题描述

给定 $n$ 个城市（节点集合 $\mathcal{N} = \{0, 1, \dots, n-1\}$），以及每对城市之间的距离 $c_{ij}$，寻找一条最短的回路，使得每个城市恰好被访问一次并返回起点。

#### 数学建模（MTZ 消圈约束）

**参数：**
- $c_{ij}$：城市 $i$ 到 $j$ 的距离
- $\mathcal{A} = \{(i, j) \mid i, j \in \mathcal{N}, i \neq j\}$：弧集合

**决策变量：**
- $x_{ij} \in \{0, 1\}$：是否从城市 $i$ 直接走到城市 $j$
- $u_i \in [1, n-1]$：城市 $i$ 的访问顺序（MTZ 辅助变量，$i = 1, \dots, n-1$）

**目标函数：**
$$
\min \quad \sum_{(i, j) \in \mathcal{A}} c_{ij} x_{ij}
$$

**约束条件：**
$$
\begin{aligned}
\sum_{j:(j,i) \in \mathcal{A}} x_{ji} &= 1, \quad \forall i \in \mathcal{N} \quad \text{（每个城市恰好进入一次）} \\
\sum_{j:(i,j) \in \mathcal{A}} x_{ij} &= 1, \quad \forall i \in \mathcal{N} \quad \text{（每个城市恰好离开一次）} \\
u_j &\geq u_i + 1 - n(1 - x_{ij}), \quad \forall i, j \in \{1, \dots, n-1\}, i \neq j \quad \text{（MTZ 消圈）} \\
x_{ij} &\in \{0, 1\}, \quad 1 \leq u_i \leq n-1
\end{aligned}
$$

> **注意：** 仅使用 $x_{ij}$ 和流守恒约束会导致**子环（subtour）**问题。MTZ 约束通过引入顺序变量 $u_i$ 消除子环，确保解是一条完整的哈密顿回路。

---

#### Python 答案（Gurobi）

```python
import numpy as np
import matplotlib.pyplot as plt
import gurobipy as gp

# ===== 数据（课件概念题，实际考试/作业替换为题目给定数据）=====
# 以下为随机示例数据，实际作业中应替换为题目提供的坐标或 CSV
n = 20
N = list(range(n))
A = [(i, j) for i in N for j in N if i != j]

np.random.seed(0)
loc_x = np.random.randint(0, 100, n)
loc_y = np.random.randint(0, 100, n)

# 计算欧氏距离
d = {(i, j): ((loc_x[i] - loc_x[j])**2 + (loc_y[i] - loc_y[j])**2)**0.5
     for (i, j) in A}

# ===== 模型建立 =====
m = gp.Model('tsp')

x = m.addVars(A, vtype=gp.GRB.BINARY, name='x')

m.setObjective(x.prod(d), gp.GRB.MINIMIZE)

# 流守恒约束
m.addConstrs((x.sum('*', i) == 1 for i in range(n)), name='inflow')
m.addConstrs((x.sum(i, '*') == 1 for i in range(n)), name='outflow')

# MTZ 消圈约束
u = m.addVars(N, lb=1, ub=n-1, name='u')
m.addConstrs(
    ((x[i, j] == 1) >> (u[j] >= u[i] + 1)
     for i in range(1, n) for j in range(1, n) if i != j),
    name='mtz'
)

# ===== 求解 =====
m.params.timelimit = 30
m.optimize()

# ===== 可视化 =====
if m.status != gp.GRB.INFEASIBLE:
    selected = [(i, j) for (i, j) in A if x[i, j].x > 0.9]
    plt.scatter(loc_x, loc_y, c='r', marker='o')
    for (i, j) in selected:
        plt.plot((loc_x[i], loc_x[j]), (loc_y[i], loc_y[j]), c='b')
    plt.savefig('tour.png', dpi=300)
    plt.show()
```

---

### 问题 5.2：CVRP（带容量约束的车辆路径问题，课件）

#### 问题描述

在 TSP 基础上，引入车辆容量限制。有 $m$ 辆同质车辆，每辆容量为 $Q$。客户 $i$ 的需求为 $q_i$。从仓库（节点 0）出发，需要规划车辆路径，在满足容量限制的前提下服务所有客户，总行驶成本最小。

#### 数学建模

**参数：**
- $q_i$：客户 $i$ 的需求
- $Q$：车辆容量
- $m$：可用车辆数
- $c_{ij}$：弧 $(i, j)$ 的行驶成本

**决策变量：**
- $x_{ij} \in \{0, 1\}$：弧 $(i, j)$ 是否被某辆车使用
- $u_i \in [q_i, Q]$：车辆到达客户 $i$ 后的剩余装载量（用于消圈+容量）

**目标函数：**
$$
\min \quad \sum_{(i, j) \in \mathcal{A}} c_{ij} x_{ij}
$$

**约束条件：**
$$
\begin{aligned}
\sum_{j \in \mathcal{N}} x_{ij} = \sum_{j \in \mathcal{N}} x_{ji} &= 1, \quad \forall i \in \mathcal{N}_C \quad \text{（每个客户恰好被访问一次）} \\
\sum_{j \in \mathcal{N}} x_{0j} &\leq m \quad \text{（从仓库出发的车辆数不超过 $m$）} \\
u_j - u_i + Q(1 - x_{ij}) &\geq q_j, \quad \forall i, j \in \mathcal{N}_C, i \neq j \quad \text{（容量+消圈）} \\
q_i \leq u_i &\leq Q, \quad \forall i \in \mathcal{N}_C \\
x_{ij} &\in \{0, 1\}
\end{aligned}
$$

> 注：$u_i$ 同时承担了 MTZ 消圈和车辆容量限制两个功能。

---

#### Python 答案（Gurobi）

```python
import numpy as np
import gurobipy as gp

# ===== 数据（课件概念题，实际考试/作业替换为题目给定数据）=====
# 以下为随机示例数据，实际作业中应替换为题目提供的坐标、需求、容量等
n = 15          # 客户数
Q = 50          # 车辆容量
m_vehicles = 3  # 可用车辆数

np.random.seed(42)
loc = np.random.randint(0, 100, (n+1, 2))   # 节点 0 是仓库
q = np.random.randint(5, 20, n)             # 客户需求

c = {(i, j): np.linalg.norm(loc[i] - loc[j]) for i in range(n+1) for j in range(n+1) if i != j}

N = list(range(n+1))
A = [(i, j) for i in N for j in N if i != j]
Nc = list(range(1, n+1))   # 客户节点

# ===== 模型建立 =====
model = gp.Model('cvrp')

x = model.addVars(A, vtype=gp.GRB.BINARY, name='x')
u = model.addVars(Nc, lb=0, ub=Q, name='u')

model.setObjective(gp.quicksum(c[i, j] * x[i, j] for i, j in A), gp.GRB.MINIMIZE)

# 流守恒
model.addConstrs((gp.quicksum(x[i, j] for j in N if j != i) == 1 for i in Nc), name='outflow')
model.addConstrs((gp.quicksum(x[j, i] for j in N if j != i) == 1 for i in Nc), name='inflow')

# 从仓库出发的车辆数
model.addConstr(gp.quicksum(x[0, j] for j in Nc) <= m_vehicles, name='vehicles')

# 容量 + MTZ 消圈
model.addConstrs(
    (u[j] - u[i] + Q * (1 - x[i, j]) >= q[j-1]
     for i in Nc for j in Nc if i != j),
    name='capacity_mtz'
)

# 初始装载量
model.addConstrs((u[i] >= q[i-1] for i in Nc), name='u_lb')

model.params.TimeLimit = 30
model.optimize()

# 输出结果
if model.status != gp.GRB.INFEASIBLE:
    print(f"最优总距离 = {model.ObjVal:.2f}")
    routes = [(i, j) for i, j in A if x[i, j].X > 0.9]
    print(f"使用弧数: {len(routes)}")
    # 按路径分组输出
    from collections import defaultdict
    out_edges = defaultdict(list)
    for i, j in routes:
        out_edges[i].append(j)
    print("
各路径：")
    for start in out_edges[0]:
        route = [0, start]
        cur = start
        while cur != 0:
            cur = out_edges[cur][0]
            route.append(cur)
        print(f"  {' → '.join(map(str, route))}")
```

---

---

### 问题 5.3：Orienteering Problem（定向问题，作业）

#### 问题描述

TSP 的变种：给定 $n$ 个节点，每个节点有得分 $s_i$，从节点 0（仓库）出发并返回节点 0。每段弧 $(i, j)$ 有旅行时间 $c_{ij}$，总旅行时间不能超过预算 $T$。不需要访问所有节点，目标是选择一部分节点访问并确定访问顺序，使得**收集的总得分最大**。

#### 数学建模

**参数：**
- $s_i$：节点 $i$ 的得分
- $c_{ij}$：从节点 $i$ 到 $j$ 的旅行时间
- $T$：时间预算
- $n$：节点总数

**决策变量：**
- $x_{ij} \in \{0, 1\}$：是否从节点 $i$ 直接走到节点 $j$
- $y_i \in \{0, 1\}$：是否访问节点 $i$
- $u_i \in [0, n-1]$：节点 $i$ 的访问顺序（MTZ 辅助变量）

**目标函数：**
$$
\max \quad \sum_{i=0}^{n-1} s_i y_i
$$

**约束条件：**
$$
\begin{aligned}
y_0 &= 1 \quad \text{（必须从节点 0 出发）} \\
\sum_{j} x_{ji} = \sum_{j} x_{ij} &= y_i, \quad \forall i \in \mathcal{N} \quad \text{（流守恒）} \\
\sum_{i,j} c_{ij} x_{ij} &\leq T \quad \text{（时间预算）} \\
(x_{ij} = 1) \Rightarrow (u_j &\geq u_i + 1), \quad \forall i, j \in \{1,\dots,n-1\}, i \neq j \quad \text{（MTZ 消圈）} \\
u_i &\leq (n-1) y_i, \quad \forall i \in \{1,\dots,n-1\} \quad \text{（$u$ 与 $y$ 关联，未访问节点 $u=0$）} \\
u_i &\geq y_i, \quad \forall i \in \{1,\dots,n-1\} \\
x_{ij} &\in \{0, 1\}, \quad y_i \in \{0, 1\}
\end{aligned}
$$

> **关键点：** 与 TSP 不同，这里不需要访问所有节点。$y_i$ 控制节点是否被访问，流守恒约束中流入=流出=$y_i$ 确保只有被访问的节点才需要有边进出。

---

#### Python 答案（Gurobi）

```python
import numpy as np
import matplotlib.pyplot as plt
import gurobipy as gp

# ===== 数据导入（实际作业从 op_random_instance.py 读取）=====
# 方式1：直接导入（若在同一目录）
exec(open('op_random_instance.py').read())                # 执行该文件，把n/loc_x/loc_y/s/c/T等变量读入当前环境

# 方式2：手动复制数据（若无法导入文件）
# n = 20
# np.random.seed(0)
# loc_x = np.random.randint(0, 100, n)
# loc_y = np.random.randint(0, 100, n)
# s = np.random.randint(1, 10, n)
# c = {(i, j): ((loc_x[i] - loc_x[j])**2 + (loc_y[i] - loc_y[j])**2)**0.5
#      for i in range(n) for j in range(n)}
# T = 300

N = list(range(n))
A = [(i, j) for i in N for j in N if i != j]

# ===== 模型建立 =====
m = gp.Model('op')

x = m.addVars(A, vtype=gp.GRB.BINARY, name='x')   # 弧是否被使用
y = m.addVars(N, vtype=gp.GRB.BINARY, name='y')    # 节点是否被访问
u = m.addVars(N, lb=0, ub=n-1, name='u')           # MTZ 顺序变量

# 目标：最大化总得分
m.setObjective(gp.quicksum(s[i] * y[i] for i in N), gp.GRB.MAXIMIZE)

# 约束1：必须经过起点（节点 0）
m.addConstr(y[0] == 1, name='visit_depot')

# 约束2：流守恒（入=出=y_i）
m.addConstrs((x.sum('*', i) == y[i] for i in N), name='inflow')
m.addConstrs((x.sum(i, '*') == y[i] for i in N), name='outflow')

# 约束3：时间预算
m.addConstr(gp.quicksum(c[i, j] * x[i, j] for i, j in A) <= T, name='time_budget')

# 约束4：MTZ 消圈（仅非仓库节点）
m.addConstrs(
    ((x[i, j] == 1) >> (u[j] >= u[i] + 1)
     for i in range(1, n) for j in range(1, n) if i != j),
    name='mtz'
)

# 约束5：u 与 y 挂钩（未访问节点 u=0，访问节点 u>=1）
m.addConstrs((u[i] <= (n - 1) * y[i] for i in range(1, n)), name='u_link_y')
m.addConstrs((u[i] >= y[i] for i in range(1, n)), name='u_lb')

# ===== 求解 =====
m.params.timelimit = 30
m.optimize()

# ===== 结果输出与可视化 =====
if m.status == gp.GRB.OPTIMAL or m.status == gp.GRB.TIME_LIMIT:
    visited = [i for i in N if y[i].x > 0.9]
    selected = [(i, j) for i, j in A if x[i, j].x > 0.9]
    total_score = sum(s[i] for i in visited)
    total_time = sum(c[i, j] for i, j in selected)

    print(f"Visited nodes: {visited}")
    print(f"Total collected score: {total_score}")
    print(f"Total travel time: {total_time:.2f} / {T}")

    # 绘图
    plt.figure(figsize=(8, 8))
    plt.scatter(loc_x, loc_y, c='lightgray', s=100, zorder=1, label='Unvisited')
    plt.scatter(loc_x[visited], loc_y[visited], c='red', s=200, zorder=3, label='Visited')
    for i in N:
        color = 'red' if i in visited else 'gray'
        plt.annotate(f'{i}\n(s={s[i]})', (loc_x[i], loc_y[i]),
                     textcoords="offset points", xytext=(0, 10),
                     ha='center', fontsize=8, color=color)
    for (i, j) in selected:
        plt.plot((loc_x[i], loc_x[j]), (loc_y[i], loc_y[j]),
                 c='blue', linewidth=2, zorder=2)
    plt.title(f'Orienteering Problem\nScore: {total_score}, Time: {total_time:.2f}/{T}')
    plt.legend()
    plt.savefig('op_tour.png', dpi=300)
    plt.show()
```


---


---

## Unit 6：Heuristics（启发式算法）

### 问题 6.1：TSP 的构造启发式（课件）

#### 问题描述

对于大规模 TSP（如 100,000 个节点），精确算法（如 Gurobi 分支定界）无法在合理时间内求得最优解。启发式算法可以在多项式时间内构造出"足够好"的解。

课件中介绍了以下几种 TSP 构造启发式：

| 方法 | 思路 |
|------|------|
| **贪婪算法（Greedy）** | 迭代选择当前最短的可用边，直到形成哈密顿回路 |
| **最近邻（Nearest Neighbor）** | 从任意节点出发，每次走到最近的未访问节点，最后返回起点 |
| **最便宜插入（Cheapest Insertion）** | 从一个子环开始，每次选择一个未访问节点，插入到子环中使得新增距离最小 |
| **随机插入（Random Insertion）** | 与 cheapest insertion 类似，但随机选择待插入节点 |

#### 伪代码逻辑

**最近邻（Nearest Neighbor）：**
```python
# 伪代码
solution = [0]  # 从节点 0 出发
unvisited = set(range(1, n))
while unvisited:
    current = solution[-1]
    next_node = argmin_{j in unvisited} d[current][j]
    solution.append(next_node)
    unvisited.remove(next_node)
# 最后回到起点
solution.append(0)
```

**2-opt 改进（局部搜索）：**
```python
# 伪代码
improved = True
while improved:
    improved = False
    for i in range(1, len(solution) - 2):
        for j in range(i + 1, len(solution)):
            # 尝试交换边 (i-1, i) 和 (j-1, j) 为 (i-1, j-1) 和 (i, j)
            old_dist = d[solution[i-1]][solution[i]] + d[solution[j-1]][solution[j]]
            new_dist = d[solution[i-1]][solution[j-1]] + d[solution[i]][solution[j]]
            if new_dist < old_dist:
                # 翻转 i 到 j-1 之间的路径
                solution[i:j] = reversed(solution[i:j])
                improved = True
```

**3-opt：** 与 2-opt 类似，但一次交换三条边，搜索空间更大，解质量通常更好但计算更慢。

> **关键洞察：** 解的质量主要取决于**改进启发式（improvement heuristic）**，而非构造启发式。先快速构造一个可行解，再用局部搜索不断改进，是求解大规模 COP 的常见策略。

---

### 问题 6.2：模拟退火（Simulated Annealing，课件）

#### 问题描述

局部搜索（如 2-opt）容易陷入**局部最优**。模拟退火通过引入随机性，允许以一定概率接受"更差"的解，从而逃离局部最优。

#### 核心思想

- **类比物理退火：** 高温时系统状态随机跳变，低温时趋于稳定。
- **接受概率：** 设当前解为 $S$，邻域解为 $S'$，目标函数差为 $\Delta E = f(S') - f(S)$（对于最小化问题）：

$$
P(\text{接受 } S') = \begin{cases} 1, & \text{if } \Delta E < 0 \text{（更优）} \\ e^{-\Delta E / (k T)}, & \text{if } \Delta E \geq 0 \text{（更差，以概率接受）} \end{cases}
$$

- **温度 $T$：** 随时间逐渐降低（冷却 schedule），初始温度高时接受差解的概率大，后期温度低时趋于贪心。

#### 伪代码

```python
# 伪代码
T = T0                    # 初始温度
S = initial_solution()    # 初始解（可用 NN 或 CI 构造）
best = S

while T > T_min:
    for _ in range(iterations_per_T):
        S_new = neighbor(S)   # 邻域操作（如 2-opt）
        delta = f(S_new) - f(S)
        if delta < 0 or random.random() < exp(-delta / T):
            S = S_new
            if f(S) < f(best):
                best = S
    T = alpha * T   # 降温，alpha ∈ (0, 1)，如 0.95

return best
```

> 注：课件未要求提交编程作业，上述为算法原理总结。

---

## Unit 7：Game Theory（博弈论）

### 问题 7.1：矩阵博弈与最优纯策略（课件）

#### 问题描述

二人有限零和博弈：局中人甲和乙各有有限个策略，同一局势下两人损益之和为零。给定甲的赢得矩阵 $A = (a_{ij})_{m \times n}$，求双方最优策略。

**前提假设：** 双方都是理性的，都从各自最不利情形中选择最有利情形。

#### 数学建模（纯策略）

**判断纯策略解是否存在：**

若满足：
$$
\max_i \min_j a_{ij} = \min_j \max_i a_{ij} = V
$$

则称博弈存在**鞍点（saddle point）**，对应的策略为**最优纯策略**，$V$ 为博弈的值。

**求解步骤：**
1. 对矩阵 $A$ 的每一行求最小值（甲的最不利情形）
2. 在这些行最小值中取最大者：$\underline{V} = \max_i \min_j a_{ij}$（甲的 max-min）
3. 对矩阵 $A$ 的每一列求最大值（乙的最不利情形）
4. 在这些列最大值中取最小者：$\overline{V} = \min_j \max_i a_{ij}$（乙的 min-max）
5. 若 $\underline{V} = \overline{V}$，则存在纯策略解

#### 示例：乒乓球团体赛

甲队赢得矩阵：
$$
A = \begin{bmatrix} 1 & 1 & 1 \\ 1 & -1 & -3 \\ 3 & -1 & 3 \end{bmatrix}
$$

- 行最小值：$\min(1,1,1)=1$，$\min(1,-1,-3)=-3$，$\min(3,-1,3)=-1$ → 行最小值列：$[1, -3, -1]$
- $\max_i \min_j a_{ij} = \max(1, -3, -1) = 1$（策略 $\alpha_1$）
- 列最大值：$\max(1,1,3)=3$，$\max(1,-1,-1)=1$，$\max(1,-3,3)=3$ → 列最大值行：$[3, 1, 3]$
- $\min_j \max_i a_{ij} = \min(3, 1, 3) = 1$（策略 $\beta_2$）

因 $\max_i \min_j a_{ij} = \min_j \max_i a_{ij} = 1$，存在鞍点 $(\alpha_1, \beta_2)$，博弈值 $V = 1$。

---

### 问题 7.2：矩阵博弈的混合策略（课件）

#### 问题描述

当纯策略解不存在（即 $\max_i \min_j a_{ij} \neq \min_j \max_i a_{ij}$）时，双方以一定概率随机选择策略，称为**混合策略**。求最优混合策略等价于求解一个线性规划问题。

#### 数学建模（LP 方法）

设甲有 $m$ 个策略，乙有 $n$ 个策略。甲选择策略 $i$ 的概率为 $x_i$，乙选择策略 $j$ 的概率为 $y_j$。

**甲的视角（最大化最不利情形下的期望收益）：**

**决策变量：**
- $x_i \geq 0$：甲选择策略 $i$ 的概率
- $v$：甲在最不利情形下的期望收益（博弈值）

**目标函数：**
$$
\max \quad v
$$

**约束条件：**
$$
\begin{aligned}
\sum_{i=1}^{m} a_{ij} x_i &\geq v, \quad j = 1, \dots, n \quad \text{（无论乙选什么，甲至少得 $v$）} \\
\sum_{i=1}^{m} x_i &= 1 \\
x_i &\geq 0
\end{aligned}
$$

**标准化（令 $x_i' = x_i / v$，适用于 $v > 0$）：**

若 $v > 0$，令 $x_i' = x_i / v$，则转化为：
$$
\min \quad \sum_{i=1}^{m} x_i' \quad \text{s.t.} \quad \sum_{i=1}^{m} a_{ij} x_i' \geq 1, \; \sum x_i' = 1/v, \; x_i' \geq 0
$$

更标准的 LP 写法（无需 $v > 0$ 假设）：
$$
\begin{aligned}
\max \quad & v \\
\text{s.t.} \quad & \sum_{i=1}^{m} a_{ij} x_i - v \geq 0, \quad j = 1, \dots, n \\
& \sum_{i=1}^{m} x_i = 1 \\
& x_i \geq 0
\end{aligned}
$$

**乙的对偶问题（最小化最不利情形下的期望损失）：**

$$
\begin{aligned}
\min \quad & w \\
\text{s.t.} \quad & \sum_{j=1}^{n} a_{ij} y_j - w \leq 0, \quad i = 1, \dots, m \\
& \sum_{j=1}^{n} y_j = 1 \\
& y_j \geq 0
\end{aligned}
$$

> **对偶关系：** 根据强对偶定理，$v^* = w^*$，即双方最优混合策略下的博弈值相同。

#### 示例：$2 \times 2$ 矩阵博弈

赢得矩阵：
$$
A = \begin{bmatrix} 5 & 9 \\ 8 & 6 \end{bmatrix}
$$

- $\max_i \min_j a_{ij} = \max(5, 6) = 6$（甲选 $\alpha_2$）
- $\min_j \max_i a_{ij} = \min(8, 9) = 8$（乙选 $\beta_1$）
- $6 \neq 8$，无纯策略解，需求混合策略。

**甲的 LP：**
$$
\begin{aligned}
\max \quad & v \\
\text{s.t.} \quad & 5x_1 + 8x_2 \geq v \\
& 9x_1 + 6x_2 \geq v \\
& x_1 + x_2 = 1 \\
& x_1, x_2 \geq 0
\end{aligned}
$$

通过求解（或等式联立），得最优混合策略：$x_1^* = 1/3, x_2^* = 2/3$，博弈值 $v = 7$。

---

#### Python 答案（Gurobi）

```python
import numpy as np
import gurobipy as gp

# ===== 赢得矩阵（甲的视角）=====
A = np.array([
    [5, 9],
    [8, 6]
])

m, n = A.shape

# ===== 甲的 LP：max v =====
model_a = gp.Model('game_a')

x = model_a.addVars(m, lb=0, name='x')
v = model_a.addVar(lb=-gp.GRB.INFINITY, name='v')

model_a.setObjective(v, gp.GRB.MAXIMIZE)

# 无论乙选什么策略，甲至少得 v
for j in range(n):
    model_a.addConstr(gp.quicksum(A[i, j] * x[i] for i in range(m)) >= v, name=f'strategy_{j}')

model_a.addConstr(gp.quicksum(x[i] for i in range(m)) == 1, name='prob')

model_a.optimize()

print("=== 甲（行玩家）最优混合策略 ===")
if model_a.status == gp.GRB.OPTIMAL:
    print(f"博弈值 v = {v.X:.4f}")
    for i in range(m):
        print(f"  x_{i+1} = {x[i].X:.4f}")

# ===== 乙的 LP：min w（对偶问题）=====
model_b = gp.Model('game_b')

y = model_b.addVars(n, lb=0, name='y')
w = model_b.addVar(lb=-gp.GRB.INFINITY, name='w')

model_b.setObjective(w, gp.GRB.MINIMIZE)

for i in range(m):
    model_b.addConstr(gp.quicksum(A[i, j] * y[j] for j in range(n)) <= w, name=f'strategy_{i}')

model_b.addConstr(gp.quicksum(y[j] for j in range(n)) == 1, name='prob')

model_b.optimize()

print("
=== 乙（列玩家）最优混合策略 ===")
if model_b.status == gp.GRB.OPTIMAL:
    print(f"博弈值 w = {w.X:.4f}")
    for j in range(n):
        print(f"  y_{j+1} = {y[j].X:.4f}")

print(f"
验证：v = w = {v.X:.4f}（强对偶定理成立）")
```

> 运行结果：甲选策略 1 的概率 $1/3$，策略 2 的概率 $2/3$；博弈值 $v = w = 7$。乙的混合策略可通过对偶问题求得。

---

### 问题 7.3：其他博弈类型（课件）

#### 囚徒困境（Prisoner's Dilemma）

两个囚徒被隔离审讯，各自选择"坦白"或"抵赖"。

|  | 囚徒2：坦白 | 囚徒2：抵赖 |
|--|------------|------------|
| **囚徒1：坦白** | (-5, -5) | (0, -8) |
| **囚徒1：抵赖** | (-8, 0) | (-1, -1) |

**分析：** 无论对方如何选择，"坦白"都是各自的严格占优策略（dominant strategy）。但双方都坦白 (-5, -5) 比双方都抵赖 (-1, -1) 更差。这揭示了**个人最优 ≠ 集体最优**。

> **纳什均衡：** （坦白，坦白）是唯一的纳什均衡——在对方策略不变的情况下，任何一方单方面改变策略都不会获得更好结果。

#### 智猪博弈（Boxed Pigs）

猪圈中有大猪和小猪，按踏板食槽会掉出饲料，但按踏板消耗体力（等值 2 份饲料）。

扣除体力后收益矩阵：

|  | 小猪：踩 | 小猪：等待 |
|--|----------|------------|
| **大猪：踩** | (5, 1) | (4, 4) |
| **大猪：等待** | (9, -1) | (0, 0) |

**分析：** 小猪严格占优策略是"等待"；大猪知道小猪会等待，因此被迫选择"踩"。

> **启示：** 竞争中"弱者"（小猪）可以通过搭便车（free-riding）策略生存，而"强者"（大猪）不得不承担更多成本。

---

## 附录：常见问题与技巧汇总

### 1. Gurobi 建模技巧

| 技巧 | 代码示例 |
|------|----------|
| 快速求和 | `gp.quicksum(x[i] for i in range(n))` |
| 变量.prod() | `x.prod(d)` 等价于 `gp.quicksum(x[i,j]*d[i,j] for ...)` |
| 指示约束 | `((x[i,j] == 1) >> (u[j] >= u[i] + 1))` |
| 时间限制 | `m.params.TimeLimit = 30`（秒） |
| 获取解值 | `x[i].X` 或 `x[i].x`（注意大小写） |
| 判断最优 | `m.status == gp.GRB.OPTIMAL` |

### 2. 消圈约束对比

| 问题 | 消圈方法 | 辅助变量 |
|------|----------|----------|
| TSP | MTZ 约束 | $u_i \in [1, n-1]$，顺序变量 |
| CVRP | 容量-MTZ 联合约束 | $u_i \in [q_i, Q]$，剩余装载量 |
| OP | MTZ + $u$ 与 $y$ 关联 | $u_i \in [0, n-1]$，未访问则 $u_i = 0$ |

### 3. 模型类型速查

| 单元 | 问题 | 模型类型 |
|------|------|----------|
| 3 | Markowitz | 二次规划（QP） |
| 3 | Portfolio II | 二次规划（QP）+ 变量替换 |
| 3 | 广告优化 | 线性规划（LP）/ 整数线性规划（ILP） |
| 4 | p-Median | 整数线性规划（ILP） |
| 4 | p-Center | 整数线性规划（ILP）+ 辅助变量线性化 |
| 4 | Fixed-Charge | 混合整数线性规划（MILP） |
| 4 | 门店关闭 | 整数线性规划（ILP） |
| 5 | TSP | 整数线性规划（ILP）+ MTZ |
| 5 | CVRP | 整数线性规划（ILP）+ 容量-MTZ |
| 5 | OP | 整数线性规划（ILP）+ MTZ + 部分访问 |
| 7 | 混合策略 | 线性规划（LP） |

---

### 4. CSV读取与数据处理速查（开卷考试用）

> 以下为本课程中常见数据来源及对应的 pandas 读取/处理代码。考试时若题目提供 CSV 或 `.py` 数据文件，直接套用即可。

#### 4.1 读取 CSV 文件

```python
import pandas as pd

data = pd.read_csv('文件名.csv')       # 读取CSV，返回一个DataFrame（数据表）
```

- `pd.read_csv('xxx.csv')` 是最常用的读取方式，括号内填入文件路径（同目录下直接写文件名）。
- 返回的 `data` 是一个 **DataFrame**，可以想象成 Excel 表格：行是记录，列是字段。

#### 4.2 提取列名（如股票代码、城市名）

```python
stocks = data.columns.values            # 提取所有列名 → NumPy数组，如 ['JPM','AMZN','AAPL','DOC','GOOG']
cities = data['city'].values            # 提取'city'列的所有值 → NumPy数组，如 ['Shanghai','Beijing',...]
```

- `data.columns.values`：获取表头列名列表，常用于获取变量名列表。
- `data['列名'].values`：获取某一列的所有值，转为 NumPy 数组。`列名`必须是 CSV 文件中实际存在的字段名。

#### 4.3 提取行数 / 筛选行

```python
n = data.shape[0]                       # 获取总行数（如2577个城市 → n=2577）
data = data[(data['capital'] == 'admin') | (data['capital'] == 'primary')]   # 筛选：只保留满足条件的行
```

- `data.shape[0]`：返回 DataFrame 的行数，常用于确定 $n$ 的取值。
- `data[条件]`：按条件筛选行。`|` 是"或"，多个条件用 `&`（与）连接。`==` 表示等于，可用于字符串或数字比较。

#### 4.4 计算统计量（均值、协方差）

```python
mu = data.mean()                        # 对每列求均值 → 各列的平均值，如各股票的期望收益率
Sigma = data.cov().values               # 计算各列的协方差矩阵 → values转为NumPy数组供Gurobi使用
```

- `data.mean()`：对**每一列**计算算术平均值，返回 Series（可转为字典 `dict(data.mean())`）。
- `data.cov()`：对**每一列**计算协方差矩阵，返回 DataFrame。加 `.values` 转为 NumPy 数组，因为 Gurobi 的 `quicksum` 需要数字索引。

#### 4.5 转成字典（方便 Gurobi 用变量名索引）

```python
mu = dict(data.mean())                  # 转成字典：键=列名，值=均值，如 {'JPM': 0.005, 'AMZN': 0.032, ...}
```

- 转成字典后，Gurobi 的 `addVars` 可以用股票名（如 `'JPM'`）作为变量索引，代码可读性更好。
- 如果不需要字典，直接用 `data.mean().values` 得到数组，再用 `0,1,2...` 索引也可以。

#### 4.6 读取 `.py` 数据文件（如 `op_random_instance.py`）

```python
exec(open('op_random_instance.py').read())   # 执行该文件，把n/loc_x/loc_y/s/c/T等变量读入当前环境
```

- 有的作业不提供 CSV，而是提供一个 `.py` 文件，里面只有变量定义（如 `n=20`, `loc_x=...`, `s=...`）。
- `exec(open(...).read())` 会把该文件的所有变量直接导入当前程序，之后就可以直接用 `n`, `loc_x`, `s` 等变量了。
- 如果无法导入（如考试环境限制），直接把 `.py` 文件的内容复制到代码中即可。

#### 4.7 常见 CSV 结构对照

| 题目 | CSV 文件 | 行代表 | 列代表 | 关键字段 |
|------|----------|--------|--------|----------|
| 3.1/3.2 Markowitz | `data_portfolio.csv` | 各期历史收益 | 各股票（JPM, AMZN, AAPL, DOC, GOOG）| 无额外字段，整表就是收益率矩阵 |
| 4.5 p-Median | `cn.csv` | 各城市 | 城市名、纬度、经度、行政级别 | `city`, `lat`, `lng`, `capital` |
| 5.3 OP | `op_random_instance.py`（非CSV） | 无 | 直接定义变量 | `n`, `loc_x`, `loc_y`, `s`, `c`, `T` |

> **考试策略：** 拿到题目后，先确认数据来源是 **CSV 文件**、**直接给出的数值** 还是 **`.py` 数据文件**。如果是 CSV，先 `pd.read_csv()` 读入，再根据题目要求提取列名、列数据、筛选行、计算统计量。后续建模代码基本不变。

---

> 本 Markdown 由课程课件和作业代码整理而成，涵盖从基础的 LP/QP 到复杂的组合优化（TSP、CVRP、OP）以及启发式算法的完整内容。所有代码均使用 `gurobipy` 求解器，可配合 Gurobi 许可证直接运行。
