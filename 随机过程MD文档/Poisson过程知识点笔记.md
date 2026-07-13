# 随机过程 · Poisson 过程 知识点笔记

> 整理自课件《2 Poisson 过程(1)》与《3 TLHPoisson 过程(2)》
> 涵盖：齐次 Poisson 过程、非齐次 Poisson 过程、复合 Poisson 过程、条件（混合）Poisson 过程

---

## 一、齐次 Poisson 过程（Homogeneous Poisson Process）

### 1.1 背景与概念

**(1) Poisson 分布的推广**

- 普通 Poisson 分布：$N \sim P(\lambda)$
- 推广到时间维度：$N(t) \sim P(\lambda t)$

**(2) 研究对象**

一段时间内随机事件 $A$ 发生的次数 $\rightarrow$ **计数过程**（Counting Process）

**例**：
- $(0,t]$ 内进入某商场的人数 $N(t)$
- $(0,t]$ 内某地区出生的婴儿数 $N(t)$
- $(0,t]$ 内某地区死亡的人数 $N(t)$
- $(0,t]$ 内某篮球运动员的得分数 $N(t)$

**(3) 计数过程定义**

随机过程 $\{N(t), t \geq 0\}$ 为一个**计数过程**，当且仅当：

$$
\begin{cases}
N(t) \text{ 为非负整数，且单调不减} \\
N(t) - N(s) \text{ 表示 } (s,t] \text{ 内事件发生次数（或 } N(t) \text{ 右连续）}
\end{cases}
$$

**(4) 齐次 Poisson 过程定义**

计数过程 $\{N(t), t \geq 0\}$ 称为**参数为 $\lambda$ 的齐次 Poisson 过程**，当且仅当：

$$
\begin{cases}
N(0) = 0 \\
\{N(t), t \geq 0\} \text{ 是独立增量过程} \\
P\{N(t+h) - N(t) = 1\} = \lambda h + o(h), \quad P\{N(t+h) - N(t) \geq 2\} = o(h)
\end{cases}
$$

> **核心思想**：独立增量 + 平稳增量（强度 $\lambda$ 为常数）$\rightarrow$ Poisson 过程

### 1.2 三种等价定义

计数过程 $\{N(t), t \geq 0\}$ 为参数 $\lambda$ 的 Poisson 过程，以下三种定义等价：

**定义 1（增量定义）**：
$$
\begin{cases}
N(0) = 0 \\
\text{独立增量} \\
P\{N(t+h) - N(t) = 1\} = \lambda h + o(h), \; P\{N(t+h) - N(t) \geq 2\} = o(h)
\end{cases}
$$

**定义 2（分布定义）**：
$$
\begin{cases}
N(0) = 0 \\
\text{独立增量} \\
P\{N(t+s) - N(s) = k\} = \dfrac{(\lambda t)^k}{k!} e^{-\lambda t}, \quad \forall s,t \geq 0
\end{cases}
$$

**定义 3（间隔时间定义）**：
$$
\begin{cases}
\{N(t), t \geq 0\} \text{ 为计数过程} \\
\text{事件发生间隔 } \{X_i, i \geq 1\} \text{ 为 iid 随机变量} \\
X_i \sim Exp(\lambda)
\end{cases}
$$

---

## 二、齐次 Poisson 过程的六大性质

### 性质 1：任意时间段内发生次数的分布

**定理 1**：设 $\{N(t), t \geq 0\}$ 为参数 $\lambda$ 的 Poisson 过程，则 $\forall s,t \geq 0$：

$$
P\{N(t+s) - N(s) = k\} = \frac{(\lambda t)^k}{k!} e^{-\lambda t}
$$

即 $N(t+s) - N(s) \triangleq N(t) \sim P(\lambda t)$

> **考点**：平稳增量性——任意长度为 $t$ 的时间段内事件发生次数服从参数 $\lambda t$ 的 Poisson 分布，与起点 $s$ 无关。

### 性质 2：发生间隔与发生时刻的分布

**定理 2**：设 $\{N(t), t \geq 0\}$ 为参数 $\lambda$ 的 Poisson 过程，第 $i$ 次计数的间隔、计数时刻分别为 $X_i, T_i$。

$$
\begin{cases}
\{X_i, i \geq 1\} \text{ 为 iid 随机变量，且 } X_i \sim Exp(\lambda) \\
T_i \sim Gamma(i, \lambda), \quad \text{即 } f_{T_i}(t) = \dfrac{(\lambda t)^{i-1}}{(i-1)!} \lambda e^{-\lambda t}
\end{cases}
$$

> **考点**：
> - 间隔时间 $X_i$ 独立同分布于指数分布 $Exp(\lambda)$
> - 发生时刻 $T_i$ 服从 Gamma 分布（Erlang 分布）
> - 期望：$E[X_i] = 1/\lambda$，$E[T_i] = i/\lambda$

### 性质 3：发生时刻的条件分布

**定理 3**：设 $\{N(t), t \geq 0\}$ 为参数 $\lambda$ 的 Poisson 过程，事件第 $i$ 次发生的时刻为 $T_i$，则：

$$
f(t_1, \ldots, t_n \mid N(t) = n) = \frac{n!}{t^n}, \quad 0 < t_1 < \cdots < t_n \leq t
$$

**注**：$f(t_1, \ldots, t_n \mid N(t) = n) = \dfrac{n!}{t^n}$ 恰为 $[0,t]$ 上 $n$ 个均匀分布随机变量的**顺序统计量** $(U_{(1)}, \ldots, U_{(n)})$ 的联合密度函数。

即：$(T_1, \ldots, T_n) \mid N(t) = n$ 与 $(U_{(1)}, \ldots, U_{(n)})$ **同分布**。

> **关键理解**：在 $N(t) = n$ 条件下，不考虑发生次序时，事件发生的时刻 $T_{i_1}, T_{i_2}, \ldots, T_{i_n}$ 可以看作 $[0,t]$ 上 $n$ 个独立同均匀分布的随机变量：
> $$T_{i_k} \mid N(t) = n \sim UNIF(0,t)$$

**推论 3.1**：$\{N(t), t \geq 0\}$ 为参数 $\lambda$ 的 Poisson 过程，事件发生的时刻为 $T_{i_k}$，则：

$$T_{i_k} \mid T_n = t \sim UNIF(0,t), \quad k = 1, 2, \ldots, n-1$$

> **例题考点**：条件密度、均匀分布的顺序统计量、边缘密度推导（如求 $f(x_1, x_2 \mid N(t)=3)$ 需先求联合密度再积分，或利用 $T_i$ 的均匀分布性质）。

### 性质 4：Poisson 过程的合并（叠加）

**定理 4**：设 $\{N_1(t), t \geq 0\}$ 和 $\{N_2(t), t \geq 0\}$ 分别为参数 $\lambda_1, \lambda_2$ 的**相互独立**的 Poisson 过程，则：

$$\{N_1(t) + N_2(t), t \geq 0\} \text{ 为参数 } \lambda_1 + \lambda_2 \text{ 的 Poisson 过程}$$

> **考点**：独立 Poisson 过程的和仍为 Poisson 过程，参数相加。可用于合并多个独立事件流。

### 性质 5：Poisson 过程的随机分解（一）——固定概率分解

**定理 5**：设 $\{N(t), t \geq 0\}$ 为参数 $\lambda$ 的 Poisson 过程，每个顾客在到达时以概率 $p$ 被独立划分为第 1 类，以概率 $q = 1-p$ 被独立划分为第 2 类。$N_1(t), N_2(t)$ 分别表示 $[0,t]$ 内到达的第 1、2 类顾客数，则：

$$\{N_1(t), t \geq 0\}, \{N_2(t), t \geq 0\} \text{ 分别是参数为 } \lambda p, \lambda q \text{ 的 Poisson 过程，且相互独立}$$

> **考点**：
> - 以**固定概率**分解后，子过程仍为 Poisson 过程
> - 子过程参数 = 原参数 $\\times$ 分类概率
> - 子过程之间**相互独立**

### 性质 6：Poisson 过程的随机分解（二）——时变概率分解

**定理 6**：设 $\{N(t), t \geq 0\}$ 为参数 $\lambda$ 的 Poisson 过程，若顾客在 $T = s$ 时刻到达，则以概率 $p_i(s)$ 被独立划分为第 $i$ 类（$i = 1, 2, \ldots, n$），$\sum_{i=1}^n p_i(s) = 1$。$N_i(t)$ 表示 $[0,t]$ 内到达的第 $i$ 类顾客数，则：

$$N_i(t) \sim P(\lambda t p_i), \quad \text{且相互独立}$$

其中：$p_i = \dfrac{1}{t} \int_0^t p_i(s) ds$

> **重要注**：$\{N_i(t), t \geq 0\}$ **不是齐次 Poisson 过程**（因为参数 $\lambda p_i = \dfrac{\lambda}{t} \int_0^t p_i(s) ds$ 不一定是常数）。

> **考点对比**：
> - 分解（一）：固定概率 $p$ $\\rightarrow$ 子过程为齐次 Poisson 过程
> - 分解（二）：时变概率 $p_i(s)$ $\\rightarrow$ 子过程不是齐次 Poisson 过程（但 $N_i(t)$ 仍服从 Poisson 分布）

---

## 三、非齐次 Poisson 过程（Non-homogeneous Poisson Process）

### 3.1 概念与背景

当事件发生的强度随时间变化时，即 $\lambda = \lambda(t)$，但**仍保持独立增量**，则得到**非齐次 Poisson 过程**。

**例**：
- 系统故障发生的强度随运行时间变大
- 昆虫产卵的强度随年龄、季节变化
- 人口增长的强度随人口基数变化
- 放射性物质衰变的强度随质量大小变化

### 3.2 定义

计数过程 $\{N(t), t \geq 0\}$ 称为**强度为 $\lambda(t)$ 的非齐次 Poisson 过程**，当且仅当：

$$
\begin{cases}
N(0) = 0 \\
\text{独立增量} \\
P\{N(t+h) - N(t) = 1\} = \lambda(t) h + o(h), \quad P\{N(t+h) - N(t) \geq 2\} = o(h)
\end{cases}
$$

> **与齐次的区别**：齐次 Poisson 过程中 $\lambda$ 为常数；非齐次中 $\lambda(t)$ 随时间变化。**共同点**：均满足独立增量。

### 3.3 性质

**定理 1（计数分布）**：设 $\{N(t), t \geq 0\}$ 为强度 $\lambda(t)$ 的非齐次 Poisson 过程，$\forall t > 0, s \geq 0$：

$$N(t+s) - N(s) \sim P(m)$$

即：

$$P\{N(t+s) - N(s) = k\} = \frac{m^k}{k!} e^{-m}$$

其中：$m = m(s,t) = \int_s^{s+t} \lambda(x) dx$ 称为**累积强度函数**。

> **考点**：非齐次 Poisson 过程的增量仍服从 Poisson 分布，但参数为累积强度 $m$ 而非 $\lambda t$。

**定理 2（发生时刻分布）**：设 $\{N(t), t \geq 0\}$ 为强度 $\lambda(t)$ 的非齐次 Poisson 过程，事件发生时刻为 $T_i$，其密度函数为 $f_{T_i}(t)$，则：

$$f_{T_i}(t) = \frac{m^{i-1}}{(i-1)!} \lambda(t) e^{-m}, \quad \text{其中 } m = \int_0^t \lambda(x) dx$$

> **对比**：齐次情况下 $\lambda(t) = \lambda$ 为常数，$m = \lambda t$，此时 $f_{T_i}(t) = \dfrac{(\lambda t)^{i-1}}{(i-1)!} \lambda e^{-\lambda t}$，即退化为 Gamma 分布。

---

## 四、复合 Poisson 过程（Compound Poisson Process）

### 4.1 概念与背景

在齐次 Poisson 过程 $\{N(t), t \geq 0\}$ 中，事件每次发生的时刻 $T_i$ 产生一个**报酬** $Y_i$，关注 $[0,t]$ 内产生的**总报酬**：

$$X(t) = \sum_{i=1}^{N(t)} Y_i$$

**模型含义**：
- $N(t)$：$[0,t]$ 内到达某车站的车辆数，$Y_i$：第 $i$ 辆车上的乘客数
- $N(t)$：$[0,t]$ 内到达某商场的顾客数，$Y_i$：第 $i$ 个顾客的消费额
- $N(t)$：$[0,t]$ 内某保险公司收到的索赔次数，$Y_i$：第 $i$ 次索赔的额度
- $N(t)$：$[0,t]$ 内到达某银行的顾客数，$Y_i$：第 $i$ 个顾客的取钱数额

### 4.2 定义

令 $X(t) = \sum_{i=1}^{N(t)} Y_i$，其中：
- $\{N(t), t \geq 0\}$ 是参数为 $\lambda$ 的 Poisson 过程
- $\{Y_i, i \geq 1\}$ 是 iid（独立同分布）随机变量
- $Y_i$ 独立于 $N(t)$

则称随机过程 $\{X(t), t \geq 0\}$ 是**复合 Poisson 过程**。

### 4.3 性质

**定理 3（期望与方差）**：设 $\{X(t), t \geq 0\}$ 是复合 Poisson 过程，则：

$$
\begin{cases}
E[X(t)] = \lambda t \cdot E[Y_i] \\
Var[X(t)] = \lambda t \cdot E[Y_i^2]
\end{cases}
$$

> **考点**：
> - 期望 = Poisson 过程期望 $\\times$ 单次报酬期望
> - 方差 = Poisson 过程期望 $\\times$ 单次报酬二阶矩（注意不是 $Var[Y_i]$，而是 $E[Y_i^2]$）
> - 证明思路：利用条件期望/方差公式，以 $N(t)$ 为条件

**定理 4（概率计算/正态近似）**：设 $\{X(t), t \geq 0\}$ 是复合 Poisson 过程，$Y_i$ 表示事件在第 $i$ 次发生时被分类的情况，其 PMF 为 $Y_i \sim \begin{pmatrix} \alpha_1 & \alpha_2 & \cdots & \alpha_n \\ p_1 & p_2 & \cdots & p_n \end{pmatrix}$，$N_j(t)$ 表示 $[0,t]$ 内第 $j$ 类事件发生的次数，则：

$$X(t) \approx N(\mu, \sigma^2) \quad \text{（近似服从）}$$

其中：$\mu = E[X(t)]$，$\sigma^2 = Var[X(t)]$

> **考点**：当 $t$ 较大时，复合 Poisson 过程可用正态分布近似计算概率，如 $P(a \leq X(t) \leq b)$。

---

## 五、条件（混合）Poisson 过程（Conditional / Mixed Poisson Process）

### 5.1 背景与概念

从齐次 Poisson 过程出发，三种推广路径：

| 推广方向 | 变化 | 结果 |
|---------|------|------|
| 到达强度 $\lambda \\rightarrow \\lambda(t)$ | 强度随时间变化 | 非齐次 Poisson 过程 |
| 到达时刻产生报酬 | 每次事件附带随机变量 | 复合 Poisson 过程 |
| 到达强度 $\lambda \\rightarrow$ r.v. $L$ | 强度本身是随机变量 | 条件（混合）Poisson 过程 |

### 5.2 定义

设 $\{N(t), t \geq 0\}$ 是计数过程，$L > 0$ 是随机变量，若 $\{N(t) \mid L = \lambda, t \geq 0\}$ 是强度为 $\lambda$ 的 Poisson 过程，则称 $\{N(t), t \geq 0\}$ 是**条件（混合）Poisson 过程**。

> **重要注**：条件 Poisson 过程**不是 Poisson 过程**，风险理论中常用作意外事件发生模型。

### 5.3 主要结论

**(1) 期望与方差**

TH. 设 $\{N(t), t \geq 0\}$ 是条件 Poisson 过程，则：

$$
\begin{cases}
E[N(t)] = t \cdot E[L] \\
Var[N(t)] = t \cdot E[L] + t^2 \cdot Var[L]
\end{cases}
$$

> **考点**：由于 $L$ 是随机变量，存在额外的不确定性，因此方差比 Poisson 过程更大（多了 $t^2 Var[L]$ 项）。

**(2) 任意时段内发生 $k$ 次的概率**

TH. 设 $\{N(t), t \geq 0\}$ 是条件 Poisson 过程，$L$ 为连续型（密度 $g(\lambda)$）或离散型（分布 $\{p_i, i \\geq 1\}$），则 $\forall s \\geq 0, t > 0$：

$$
P\{N(s+t) - N(s) = k\} = 
\begin{cases}
\displaystyle\int_0^{\\infty} \frac{(\\lambda t)^k}{k!} e^{-\\lambda t} \\cdot g(\\lambda) d\\lambda, & L \\text{ 连续型} \\
\displaystyle\\sum_{i=1}^{\\infty} \\frac{(\\lambda_i t)^k}{k!} e^{-\\lambda_i t} \\cdot p_i, & L \\text{ 离散型}
\end{cases}
$$

> **考点**：全概率公式/条件期望的应用——以 $L$ 为条件，先求条件概率，再对 $L$ 的分布求期望。

---

## 六、典型例题与训练考点汇总

| 编号 | 题目类型 | 主要考点 |
|-----|---------|---------|
| 训练 1 | 保险公司索赔贴现平均值 | 复合 Poisson 过程、条件期望、Poisson 过程的时刻条件分布、贴现因子 |
| 训练 2 | 证明 $E[N(s) \\mid N(t)=i]$ | 条件期望、Poisson 过程的独立增量性、均匀分布条件 |
| 训练 3 | 店主 $y$-policy 平均利润 | 复合 Poisson 过程、截断分布、期望计算、等待成本 |
| 例题 4 | 隐性 AIDS 病人数量估计 | 非齐次/复合 Poisson 过程、CDF $G(t)$、潜伏期建模、全概率公式 |
| 课后训练 | 飞机起飞概率 | 随机分解（一）、两个独立 Poisson 过程的竞争、首次到达时间 |
| 思考题 | 求 $f(x_1, x_2 \\mid N(t)=3)$ | 条件密度、联合 $\\rightarrow$ 边缘、均匀分布顺序统计量、变量变换 |
| 训练 | 迁入家庭人数概率 | 复合 Poisson 过程、正态近似、离散分布 $Y_i$ 的期望与方差计算 |

---

## 七、核心公式速查表

| 内容 | 公式 |
|-----|------|
| Poisson 过程增量分布 | $N(t+s) - N(s) \\sim P(\\lambda t)$ |
| 间隔时间分布 | $X_i \\sim Exp(\\lambda)$，iid |
| 发生时刻分布 | $T_i \\sim Gamma(i, \\lambda)$ |
| 条件联合密度 | $f(t_1,\\ldots,t_n \\mid N(t)=n) = \\dfrac{n!}{t^n}$ |
| 合并性质 | $N_1 + N_2 \\sim P((\\lambda_1 + \\lambda_2)t)$ |
| 分解（一） | $N_i \\sim P(\\lambda p_i)$，独立 |
| 复合过程期望 | $E[X(t)] = \\lambda t \\cdot E[Y_i]$ |
| 复合过程方差 | $Var[X(t)] = \\lambda t \\cdot E[Y_i^2]$ |
| 非齐次增量分布 | $N(t+s) - N(s) \\sim P(m)$，$m = \\int_s^{s+t} \\lambda(x)dx$ |
| 条件过程期望 | $E[N(t)] = t \\cdot E[L]$ |
| 条件过程方差 | $Var[N(t)] = t \\cdot E[L] + t^2 \\cdot Var[L]$ |

---

*笔记整理完毕，后续单元笔记可参照此格式继续补充。*
