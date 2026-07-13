# CTMC（连续时间马尔可夫链）知识点笔记

> 整理自课件：10_CTMC_1、11_CTMC_2、13_CTMC_3  
> 已跳过所有「课后思考」「课后拓展」内容。  
> **修正说明**：全文数学符号已统一用 `$` 包裹，一致化公式与反向时间速率符号已按课件校正。

---

## 1. 定义与基本结构

### 1.1 CTMC 定义

随机过程 $\{X(t), t \geq 0\}$ 称为**连续时间马尔可夫链（CTMC）**，若满足：
- 状态空间 $S$ 离散（有限或可数无限）；
- **马尔可夫性**：对任意 $t \geq 0, h > 0$，有

$$
P\big[X(t+h) = j \mid X(t) = i, \text{过去}\big] = P\big[X(t+h) = j \mid X(t) = i\big]
$$

即未来只依赖于当前状态，与过去无关。

### 1.2 逗留时间定理

**定理**：CTMC 在状态 $i$ 的逗留时间 $\tau_i$ 服从指数分布：

$$
\tau_i \sim \text{Exp}(q_i)
$$

其中 $q_i$ 为状态 $i$ 的**转移速率**（或称离开速率），满足：

$$
q_i = -P'_{ii}(0) = \frac{1}{E[\tau_i]} = \sum_{j \neq i} q_{ij}
$$

- $q_{ij}$（$i \neq j$）为从 $i$ 到 $j$ 的转移速率；
- 离开 $i$ 的速率为所有 $q_{ij}$ 之和。

---

## 2. 转移速率矩阵 $Q$（生成元）

### 2.1 定义

$Q = (q_{ij})$ 称为**状态转移速率矩阵**或**生成元（Infinitesimal Generator）**，满足：
- 对角线：$q_{ii} = -q_i = -\sum_{j \neq i} q_{ij}$
- 非对角线：$q_{ij} \geq 0$（$i \neq j$）
- 每行之和：$\sum_{j} q_{ij} = 0$

### 2.2 嵌入 DTMC

从 CTMC 构造**嵌入离散时间马尔可夫链** $\{Y_n, n = 0,1,2,\ldots\}$：
- **转移概率**：$P_{ij} = q_{ij} / q_i$（$i \neq j$）
- **对角线**：$P_{ii} = 0$（即嵌入 DTMC 不存在自环）

> 注意：嵌入 DTMC 只记录状态转移序列，不记录时间信息。

### 2.3 CTMC 的等价定义

$\{X(t), t \geq 0\}$ 是 CTMC $\Longleftrightarrow$
- 系统在每一个状态的逗留时间服从**互独的指数分布**；
- 状态之间的转移构成 DTMC。

---

## 3. 生灭过程（Birth-Death Process）

生灭过程是仅允许相邻状态转移的 CTMC：
- **生速率** $\lambda_i$：从 $i \to i+1$ 的速率
- **灭速率** $\mu_i$：从 $i \to i-1$ 的速率
- 其他 $q_{ij} = 0$（$|i-j| > 1$）

生灭过程的转移速率图只有相邻状态之间的连线，是 CTMC 中结构最简单且应用最广的一类。

---

## 4. Kolmogorov 微分方程

### 4.1 向后方程（Backward Equation）

分量形式：

$$
P'_{ij}(t) = \sum_{k \neq i} q_{ik} \cdot P_{kj}(t) - q_i \cdot P_{ij}(t)
$$

矩阵形式：

$$
P'(t) = Q \cdot P(t)
$$

### 4.2 向前方程（Forward Equation）

分量形式：

$$
P'_{ij}(t) = \sum_{k \neq j} P_{ik}(t) \cdot q_{kj} - q_j \cdot P_{ij}(t)
$$

矩阵形式：

$$
P'(t) = P(t) \cdot Q
$$

> 向前方程在多数情况（包括 $S$ 有限、生灭过程）下成立。

### 4.3 解

满足初始条件 $P(0) = I$ 的解为：

$$
P(t) = e^{Qt}
$$

其中矩阵指数定义为 $e^{Qt} = \sum_{n=0}^{\infty} \frac{(Qt)^n}{n!}$。

---

## 5. 一致化方法（Uniformization）

为数值计算 $P(t)$，引入一致化方法。

### 5.1 特殊情况：$q_i = q$（常数）

当所有状态离开速率相同 $q_i = q$ 时，状态转移次数 $N(t)$ 是参数为 $q$ 的 Poisson 过程：

$$
P_{ij}(t) = \sum_{n=0}^{\infty} \frac{(qt)^n}{n!} e^{-qt} \cdot P_{ij}^{(n)}
$$

其中 $P_{ij}^{(n)}$ 表示嵌入 DTMC 转移矩阵 $P$ 的 $n$ 次幂的 $(i,j)$ 元素。

### 5.2 一般情况：$q_i$ 互异

**想法**：将一般情况（$q_i$ 互异）一致化为特殊情况（$q_i = q^*$）。

取一致化速率：

$$
q^* = \frac{1}{E[\tau^*]} \geq \max_{i \in S} q_i
$$

构造一致化转移矩阵：

$$
P^* = I + \frac{Q}{q^*}
$$

则：

$$
P_{ij}(t) = \sum_{n=0}^{\infty} \frac{(q^* t)^n}{n!} e^{-q^* t} \cdot \big[(P^*)^n\big]_{ij}
$$

> 核心思想：将连续时间转移矩阵的求解转化为离散时间矩阵幂的加权求和。$(P^*)^n$ 表示矩阵 $P^*$ 的 $n$ 次幂。

---

## 6. 极限分布与稳态分布

### 6.1 极限概率的存在定理

CTMC $\{X(t), t \geq 0\}$ 中，$S = \{0,1,2,\ldots\}$，转移概率函数 $P(t) = (P_{ij}(t))$，转移速率矩阵 $Q$。若其嵌入 DTMC **不可约**：

- 若 $S$ 是非常返或零常返态集，则 $\lim_{t\to\infty} P_{ij}(t) = 0$，极限分布不存在（不构成 PMF）；
- 若 $S$ 是正常返态集，则极限概率存在且 $> 0$，此时 $\{p_j, j \in S\}$ 构成 PMF，称为**遍历链**。

### 6.2 平衡方程

极限概率 $p_j = \lim_{t\to\infty} P_{ij}(t)$ 满足：

$$
\begin{cases}
p_j \cdot q_j = \sum_{k \neq j} p_k \cdot q_{kj}, & \forall j \in S \\[6pt]
\sum_{j \in S} p_j = 1
\end{cases}
$$

或矩阵形式（记 $\mathbf{p} = (p_0, p_1, \ldots)$ 为行向量）：

$$
\mathbf{p} \cdot Q = 0, \quad \mathbf{p} \cdot \mathbf{e} = 1
$$

### 6.3 正常返判法

$S$ 不可约时：

$$
S \text{ 是正常返态集} \Longleftrightarrow \text{平衡方程 } \begin{cases} \mathbf{p} \cdot Q = 0 \\ \mathbf{p} \cdot \mathbf{e} = 1 \end{cases} \text{ 有解}
$$

### 6.4 与嵌入 DTMC 稳态概率的关系

设嵌入 DTMC 的稳态概率为 $\{\pi_j, j \in S\}$，则 CTMC 极限概率：

$$
p_j = \frac{\pi_j / q_j}{\sum_{i \in S} (\pi_i / q_i)}, \quad \text{或} \quad \pi_j = \frac{p_j \cdot q_j}{\sum_{j \in S} p_j \cdot q_j}
$$

> 直观理解：CTMC 在状态 $j$ 的极限概率，正比于嵌入链在 $j$ 的稳态概率 $\times$ 在 $j$ 的逗留时间（$1/q_j$）。

---

## 7. Gillespie 算法

基于 $Q$ 矩阵直接模拟 CTMC 样本路径的算法：
1. 已知当前状态 $i$，生成逗留时间 $\tau_i \sim \text{Exp}(q_i)$；
2. 按概率 $P_{ij} = q_{ij}/q_i$ 选择下一个状态 $j$；
3. 重复。

> 该算法是分子动力学、化学反应网络模拟中的标准方法。

---

## 8. 时间可逆的 CTMC（了解）

### 8.1 反向时间 CTMC

CTMC $\{X(t), t \geq 0\}$ 的**反向时间随机过程**仍然是 CTMC。

正向时间速率 $q_{ij}$ 与反向时间速率 $q_{ij}^*$ 的关系：

$$
\begin{cases}
q_{ij}^* = \dfrac{p_j}{p_i} \cdot q_{ji}, & i \neq j \\[8pt]
q_i^* = q_i
\end{cases}
$$

> 注：$q_{ij}^*$ 中上标 $*$ 表示反向时间，与一致化速率 $q^*$ 是不同的概念。

### 8.2 时间可逆的定义

设 CTMC 为遍历链（极限状态概率的 PMF 存在），则：

$$
\text{CTMC 时间可逆} \Longleftrightarrow q_{ij}^* = q_{ij}, \quad \forall i \neq j
$$

等价于：

$$
p_i \cdot q_{ij} = p_j \cdot q_{ji}, \quad \forall i \neq j, \; i,j \in S
$$

### 8.3 时间可逆的含义

$$
p_i \cdot q_{ij} = p_j \cdot q_{ji}
$$

$\Longleftrightarrow$ **"单位时间内 $i \to j$ 的平均次数" = "单位时间内 $j \to i$ 的平均次数"**

> 即时间可逆的物理意义：在稳态下，任何两个状态之间的转移流是平衡的。

### 8.4 时间可逆的判法

| 判法 | 条件 |
|------|------|
| **A. 利用定义** | $p_i q_{ij} = p_j q_{ji}, \quad \forall i \neq j, \; i,j \in S$ |
| **B. 利用含义** | 单位时间内 $i \to j$ 的平均次数 = 单位时间内 $j \to i$ 的平均次数 |
| **C. 利用嵌入 DTMC** | CTMC 时间可逆 $\Longleftrightarrow$ 嵌入 DTMC 时间可逆 |
| **D. 利用解可逆方程组** | 若方程组 $y_i q_{ij} = y_j q_{ji}$（$i \neq j$）且 $\sum_j y_j = 1$ 存在唯一解，则 CTMC 时间可逆，且 $\{y_j\}$ 就是极限概率分布 |

### 8.5 遍历的生灭过程

**遍历的生灭过程一定时间可逆。**

### 8.6 一个应用：M/M/C 的离去过程

> **例题**：证明 M/M/C 排队系统的离去过程与到达过程相同，即为参数 $\lambda$ 的 Poisson 过程。
>
> （利用时间可逆性可直接证明：正反向过程统计特性相同，故离去过程 = 到达过程的反向 = 同参数 Poisson 过程。）

---

## 附：核心公式速查

| 内容 | 公式 |
|------|------|
| 逗留时间 | $\tau_i \sim \text{Exp}(q_i)$，$q_i = 1/E[\tau_i]$ |
| $Q$ 矩阵 | $q_{ii} = -\sum_{j \neq i} q_{ij}$，行和 $= 0$ |
| 嵌入 DTMC | $P_{ij} = q_{ij}/q_i$（$i \neq j$），$P_{ii} = 0$ |
| Kolmogorov 向后 | $P'_{ij}(t) = \sum_{k \neq i} q_{ik} P_{kj}(t) - q_i P_{ij}(t)$ |
| Kolmogorov 向前 | $P'_{ij}(t) = \sum_{k \neq j} P_{ik}(t) q_{kj} - q_j P_{ij}(t)$ |
| 解 | $P(t) = e^{Qt}$ |
| 一致化（特殊） | $P_{ij}(t) = \sum_n \frac{(qt)^n}{n!} e^{-qt} P_{ij}^{(n)}$（$q_i = q$） |
| 一致化（一般） | $P_{ij}(t) = \sum_n \frac{(q^* t)^n}{n!} e^{-q^* t} \big[(P^*)^n\big]_{ij}$，其中 $P^* = I + Q/q^*$ |
| 平衡方程 | $p_j q_j = \sum_{k \neq j} p_k q_{kj}$，或 $\mathbf{p} \cdot Q = 0$ |
| CTMC 与嵌入 DTMC 关系 | $p_j = \frac{\pi_j / q_j}{\sum_i (\pi_i / q_i)}$ |
| 时间可逆 | $p_i q_{ij} = p_j q_{ji}$ |
| 反向时间速率 | $q_{ij}^* = \frac{p_j}{p_i} q_{ji}$（$i \neq j$） |

---

*笔记已修正完成。如有具体推导步骤或计算细节需要补充，请随时指出。*
