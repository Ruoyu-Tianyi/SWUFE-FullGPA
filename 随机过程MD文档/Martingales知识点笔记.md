# Martingales（鞅）与 Brownian Motion（布朗运动）知识点笔记

> 来源课件：`14_martingales(1).pdf`（共 27 页）
> 说明：本笔记仅整理核心定义、推导与模型结论，**跳过课后思考、课后拓展及附录推导**。

---

## 一、Martingales（鞅）

### 1.1 离散时间鞅的定义（公平博弈）

设随机过程 $\{X_n, n \geq 0\}$ 满足：

$$E\big[|X_n|\big] < +\infty, \quad \forall n \geq 0$$

且

$$E\big[X_{n+1} \mid X_n, X_{n-1}, \ldots, X_0\big] = X_n$$

则称 $\{X_n, n \geq 0\}$ 为 **Martingale（鞅）**。

**直观理解**：在已知当前及以前全部信息的条件下，下一时刻的期望值恰好等于当前值——即"公平博弈"，没有系统性的盈利或亏损趋势。

#### 上鞅（Supermartingale）与下鞅（Submartingale）

- **上鞅**：$E[X_{n+1} \mid \ldots] \leq X_n$（趋势向下或不变）
- **下鞅**：$E[X_{n+1} \mid \ldots] \geq X_n$（趋势向上或不变）

### 1.2 σ 代数流（Filtration）与适应过程

为严格刻画"信息累积"，引入 σ 代数流：

$$\mathcal{F}_0 \subset \mathcal{F}_1 \subset \mathcal{F}_2 \subset \cdots \subset \mathcal{F}_n \subset \cdots$$

- $\mathcal{F}_n$ 表示到时刻 $n$ 为止所掌握的全部信息（由 $X_0, X_1, \ldots, X_n$ 生成的 σ 代数）。
- **适应过程**：$X_n$ 是 $\mathcal{F}_n$**-可测**的，即 $X_n$ 的值完全由 $\mathcal{F}_n$ 中的信息决定。

鞅的严格定义可写为：

$$E\big[X_{n+1} \mid \mathcal{F}_n\big] = X_n$$

### 1.3 连续时间鞅

对连续时间随机过程 $\{X(t), t \geq 0\}$，若存在 σ 代数流 $\{\mathcal{F}_t, t \geq 0\}$，满足：

$$E\big[|X(t)|\big] < +\infty, \quad E\big[X(t) \mid \mathcal{F}_s\big] = X(s), \quad \forall\, 0 \leq s < t$$

则称 $\{X(t), t \geq 0\}$ 为**连续时间鞅**。

### 1.4 Doob 型鞅（条件期望构造法）

设 $X$ 与 $\{Y_i, i \geq 1\}$ 是同一概率空间上的随机变量，定义：

$$\mathcal{F}_n = \sigma(Y_1, Y_2, \ldots, Y_n), \quad Z_n \triangleq E\big[X \mid \mathcal{F}_n\big]$$

若 $E[|X|] < +\infty$，则随机过程 $\{Z_n, n \geq 1\}$ 是关于 $\{\mathcal{F}_n, n \geq 1\}$ 的**鞅**。

**证明要点**：

$$E\big[Z_n \mid \mathcal{F}_{n-1}\big] = E\big\{E[X \mid \mathcal{F}_n] \mid \mathcal{F}_{n-1}\big\} = E\big[X \mid \mathcal{F}_{n-1}\big] = Z_{n-1}$$

（利用条件期望的塔性质：$\mathcal{F}_{n-1} \subset \mathcal{F}_n$）

### 1.5 待定系数法构造鞅：Branch 过程（分支过程）

**模型**：$\{X_n, n \geq 1\}$ 为 Branch 过程。
- 第 $i$ 个个体在死亡时产生 $Y_i$ 个下一代个体；
- $\{Y_i, i \geq 1\}$ 为 i.i.d. 随机变量，$E[Y_i] = m > 0$；
- $X_n$ 表示第 $n$ 代的个体总数，$X_1 = a$；
- $X_n$ 与 $Y_i$ 独立。

**构造鞅**：令

$$Z_n = \sum_{i=1}^{n}\Big[X_i - E\big(X_i \mid X_1, \ldots, X_{i-1}\big)\Big]$$

取 $\mathcal{F}_n = \sigma(X_1, X_2, \ldots, X_n)$，则 $\{Z_n, n \geq 1\}$ 是关于 $\{\mathcal{F}_n, n \geq 1\}$ 的鞅。

**验证思路**：
1. $Z_n$ 为 $\mathcal{F}_n$-可测；
2. $E[|Z_n|] < +\infty$（由 $X_i \in L^1$ 保证）；
3. $E[Z_{n+1} \mid \mathcal{F}_n] = Z_n$（利用条件期望的塔性质与 $E[X_{n+1} \mid \mathcal{F}_n]$ 的抵消）。

---

## 二、Brownian Motion（布朗运动）

### 2.1 历史背景与发展

| 时间 | 人物 | 贡献 |
|------|------|------|
| 1827 | R. Brown（英国植物学家） | 在显微镜下发现花粉微粒在溶液中作无规则运动 |
| 1900 | Bachelier（法国数学家） | 博士论文中研究一维 Brown 运动的随机模型，将股价变化解释为 Brown 运动，**开创近代金融数学** |
| 1905 | Einstein | 解释 Brown 运动源于分子之间大量高速（$10^{19} \sim 10^{21}$ 次/秒）碰撞；推导出任意时刻 $t$ 微粒位置 $X(t) \sim N(0, t)$ |
| 1923 | Wiener | 发表系列论文系统研究 Brown 运动，并给出**数学定义**，故又称 **Wiener 过程** |
| 二战期间 | 伊藤清 | 提出关于 Brown 运动的计算理论：**伊藤积分** |

### 2.2 与一维对称随机游走的关系（逼近思维）

**一维对称随机游走**：DTMC $\{X_n, n \geq 0\}$，状态空间 $S = \{0, \pm 1, \pm 2, \ldots\}$，出发点 $X_0 = 0$。
- 单位时间转移一步；
- 一步转移概率：$P_{i, i+1} = 0.5$，$P_{i, i-1} = 0.5$；
- 每次运动方向（向左或向右）相互独立。

**模型结论**：$S$ 为**零常返状态集**，稳态概率 $\pi_j = 0$，稳态概率分布不存在——微粒将"飘向远方"。

**想法**：连续时间下情况如何？

**实现（逼近思维）**：
- 步长：$1 \to \Delta y \to 0$
- 间隔时间：$1 \to \Delta t \to 0$
- 取 $\Delta y = \sigma\sqrt{\Delta t}$

**近似表达**：

$$X(t) \approx \sum_{i=1}^{[t/\Delta t]} \Delta y \cdot Y_i, \quad Y_i \sim \begin{pmatrix} -1 & 1 \\ 0.5 & 0.5 \end{pmatrix}$$

**近似分布**（由 CLT）：

$$\sum_{i=1}^{[t/\Delta t]} \Delta y \cdot Y_i \;\sim\; N\Big(0, \;[t/\Delta t]\,(\Delta y)^2\Big) \;\sim\; N(0, \sigma^2 t)$$

当 $\Delta t \to 0$ 时：

$$X(t) \sim N(0, \sigma^2 t)$$

**结论**：对称随机游走 $\{X_n, n = 0, 1, 2, \ldots\} \xrightarrow{\Delta t \to 0, \, \Delta y \to 0}$ 连续时间 SP $\{X(t), t \geq 0\}$（布朗运动过程）。

### 2.3 概率特征

对 $\{X(t), t \geq 0\}$：
- $X(0) = 0$；
- 具有**平稳增量**、**独立增量**；
- $X(t)$ 具有正态分布：$X(t) \sim N(0, \sigma^2 t)$。

### 2.4 Brownian Motion（Wiener 过程）的数学定义

随机过程 $\{X(t), t \geq 0\}$ 称为 **Brownian Motion（or Wiener）过程**，当且仅当：

$$\begin{cases}
X(0) = 0 \\[6pt]
\{X(t), t \geq 0\} \text{ 具有平稳增量、独立增量} \\[6pt]
X(t) \sim N(0, \sigma^2 t)
\end{cases}$$

称 $\sigma^2$ 为 Brownian Motion 过程的**方差参数**。

若 $\sigma = 1$，则称为**标准 Brownian Motion（BM）**，记为：

$$\{B(t), \, t \geq 0\} \quad \text{或} \quad \{W(t), \, t \geq 0\}$$

### 2.5 注记与性质

1. **起点平移**：若 $\{B_x(t), t \geq 0\}$ 是起点 $B(0) = x$、方差 $\sigma^2 = 1$ 的 Brownian Motion，则
   $$\{B_x(t) - x, \, t \geq 0\} \text{ 为标准 BM}$$

2. **标准化**：若 $\{X(t), t \geq 0\}$ 是起点 $B(0) = x$、方差为 $\sigma^2$ 的 Brownian Motion，则
   $$\Big\{\frac{X(t) - x}{\sigma}, \, t \geq 0\Big\} \text{ 为标准 BM}$$

3. **与随机游走的极限关系**：$\{B(t), t \geq 0\}$ 是一维对称随机游走 $\{X_n, n = 0, 1, 2, \ldots\}$ 的极限情况。

4. **过程类型**：$\{B(t), t \geq 0\}$ 是**连续时间、连续状态**的随机过程。

### 2.6 三个经典鞅（Brownian Motion 的鞅性质）

**例题**：已知 $\{B(t), t \geq 0\}$ 是标准布朗运动。

**(1) 证明 $\{B(t), t \geq 0\}$ 是 Martingale**

- $E[|B(t)|] = \int_{\mathbb{R}} |x| \cdot \frac{1}{\sqrt{2\pi t}} e^{-\frac{x^2}{2t}} dx < +\infty$
- $\forall\, 0 \leq s < t$：
  $$E\big[B(t) \mid \mathcal{F}_s\big] = E\big[(B(t) - B(s)) + B(s) \mid \mathcal{F}_s\big] = E\big[B(t) - B(s)\big] + B(s) = B(s)$$
  （增量独立且 $E[B(t)-B(s)] = 0$）

**(2) 证明 $\{B^2(t) - t, \, t \geq 0\}$ 是 Martingale**

- $E\big[|B^2(t) - t|\big] \leq E[B^2(t)] + t = 2t < +\infty$
- $\forall\, 0 \leq s < t$：
  $$\begin{aligned}
  E\big[(B^2(t) - t) \mid \mathcal{F}_s\big]
  &= E\big[(B(t) - B(s) + B(s))^2 \mid \mathcal{F}_s\big] - t \\[4pt]
  &= E\big[(B(t) - B(s))^2\big] + B^2(s) + 2B(s)\,E\big[B(t) - B(s)\big] - t \\[4pt]
  &= (t - s) + B^2(s) - t \\[4pt]
  &= B^2(s) - s
  \end{aligned}$$

**(3) 证明 $\big\{e^{c \cdot B(t) - \frac{c^2}{2} t}, \, t \geq 0\big\}$ 是 Martingale（几何布朗运动）**

- $E\big[\big|e^{c B(t) - \frac{c^2}{2} t}\big|\big] = e^{-\frac{c^2 t}{2}} \cdot E\big[e^{c B(t)}\big] = e^{-\frac{c^2 t}{2}} \cdot e^{\frac{c^2}{2} t} = 1 < +\infty$
- $\forall\, 0 \leq s < t$：
  $$\begin{aligned}
  E\Big[e^{c B(t) - \frac{c^2}{2} t} \Big| \mathcal{F}_s\Big]
  &= e^{-\frac{c^2 t}{2}} \cdot E\Big[e^{c (B(t) - B(s)) + c B(s)} \Big| \mathcal{F}_s\Big] \\[4pt]
  &= e^{c B(s) - \frac{c^2 t}{2}} \cdot E\big[e^{c (B(t) - B(s))}\big] \\[4pt]
  &= e^{c B(s) - \frac{c^2 t}{2}} \cdot e^{\frac{c^2}{2}(t - s)} \\[4pt]
  &= e^{c B(s) - \frac{c^2}{2} s}
  \end{aligned}$$

> **几何布朗运动的应用**：二叉树模型是几何 BM 模型的离散形式；几何 BM 常被用作**资产价格随时间（连续）变化**的模型。

### 2.7 关于 Brownian Motion 的后续关注问题

课件中列出后续研究方向（本笔记仅罗列标题，具体推导略）：

1. **概率性质**：有限维联合 pdf、条件 pdf、样本路径的连续性、可微性、Markov 性、鞅性。
2. **反射原理**（Reflection Principle）。
3. **首达时刻** $T_a$：首达某状态 $a$ 的时刻的分布。
4. **最值分布**：$B(t)$ 在 $[0, t]$ 中的最大值/最小值的分布。
5. **零点概率**：$B_x(t)$ 在 $[0, t]$ 中的零点存在概率。
6. **变体过程**：
   - 带有漂移的 BM（Drifted BM）
   - 几何 BM（Geometric BM）
   - Brown Bridge（布朗桥）
   - 带有吸收值的 BM
   - 在 0 点反射的 BM
7. **积分过程**：$\{B(t), t \geq 0\}$ 的积分过程。
8. **随机积分**：关于 $\{B(t), t \geq 0\}$ 的积分（伊藤积分）。

---

## 三、附录说明（已跳过）

以下内容为课件附录/手写推导，属于课后拓展或补充证明，本笔记未展开：
- **附录 A**：Einstein 推导一维随机游走的粒子在 $[0, t]$ 上的位移 $B(t)$ 的概率分布（特征函数法）。
- **附录 B**：关于 $L^2$ 空间 $(\Omega, \mathcal{F}, P)$ 的构造（Banach Space、Hilbert Space、Euclid Space 的层次关系）。

---

*笔记整理完毕。*
