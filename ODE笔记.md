# 1.5：一阶线性方程（Linear First-Order Equations）

## 二、解法核心：积分因子法（Integrating Factor Method）

**套路句：**

> For a linear first-order equation
>  $y' + p(x)y = g(x)$,
>  we can use an *integrating factor*
>  $\mu(x) = e^{\int p(x)\,dx}$.

### Step 0：先整理成标准形式

先确保写成：
$$
y' + p(x)y = g(x)
$$
如果原方程不是这个样子，需要**先除一下**，让 $y'$ 前面的系数变成 1。

------

### Step 1：找到积分因子 integrating factor

定义：
$$
\mu(x) = e^{\int p(x)\,dx}
$$
这个 $\mu(x)$ 就叫做 **integrating factor（积分因子）**。

------

### Step 2：把方程整体乘以 $\mu(x)$

方程：
$$
y' + p(x)y = g(x)
$$
两边同乘 $\mu(x)$：
$$
\mu(x)y' + \mu(x)p(x)y = \mu(x)g(x)
$$
神奇的地方在于：左边会变成一个**积的导数**：
$$
\frac{d}{dx}[\mu(x)y] = \mu(x)g(x)
$$

> 这一步是整个方法的“魔术核心”：
>  选 $\mu(x)$ 就是为了让左边刚好变成一个导数。

------

### Step 3：对两边积分

$$
\frac{d}{dx}[\mu(x)y] = \mu(x)g(x)
$$

积分：
$$
\int \frac{d}{dx}[\mu(x)y]\,dx = \int \mu(x)g(x)\,dx
$$
得到：
$$
\mu(x)y = \int \mu(x)g(x)\,dx + C
$$

------

### Step 4：解出 $y$

$$
y(x) = \frac{1}{\mu(x)}\left(\int \mu(x)g(x)\,dx + C\right)
$$

如果还有初值（initial condition） $y(x_0)=y_0$，就代入求 $ C $。

#  **1.6：一些特殊的一阶方程（Special First-Order Equations）**

## 1.6.1 一阶齐次方程（Homogeneous first-order ODE）

### 解法套路（一定要记）

当看到可以写成 $y' = F(y/x)$ 时，立刻使用代换：

> 令
> $$
> v = \frac{y}{x}\quad (\text{或者写 }y = vx),
> $$
> 这是最标准的 substitution。

因为 $y = vx$，所以
$$
y' = v + x v'.
$$
把这两个代换进原方程，就得到一个关于 $v, x$ 的方程，一般会变成 **可分离变量（separable）** 的形式。

### (3) 例子（看结构就好）

例：
$$
y' = \frac{x + y}{x}.
$$
先整理：
$$
y' = 1 + \frac{y}{x} = 1 + v.
$$
又因为 $y = vx\Rightarrow y' = v + xv'$，代入：
$$
v + x v' = 1 + v \quad\Rightarrow\quad x v' = 1.
$$
于是
$$
\frac{dv}{dx} = \frac{1}{x}
$$
是可分离的：
$$
dv = \frac{1}{x}dx \quad\Rightarrow\quad v = \ln|x| + C.
$$
最后再把 $v = y/x$ 换回去：
$$
\frac{y}{x} = \ln|x| + C \quad\Rightarrow\quad y = x(\ln|x| + C).
$$
这就是通解。

> 你暂时只要记住套路：
>  **“认出 $F(y/x)$ → 令 $y=vx$ → 变成关于 v 的 separable 方程”。**

## 1.6.2Bernoulli 方程（Bernoulli equation）

### (1) 识别形式

Bernoulli 方程的标准形式是：
$$
y' + p(x)y = q(x)y^{n},\quad n\neq 0,1.
$$
只要你看到“一阶线性”左边，再加一个 $y^n$ 在右边，就是它。

**关键词：**

- *Bernoulli equation* Bernoulli 方程
- *nonlinear* 非线性
- *reduction to a linear equation* 降阶/化成线性

### (2) 核心想法

虽然它看起来是非线性，但可以通过代换变成线性的一阶方程：

> 令
> $$
> v = y^{1-n}.
> $$

然后利用链式法则把 $v'$ 表示成 $y, y'$，代回原式后，居然变成关于 $v$ 的**线性方程**，再用 1.5 的 integrating factor 方法解。

### (推导理解就行）

# 2.1 基本概念：二阶线性方程的形式与分类

### 1. 一般形式（general form）

二阶微分方程的最一般线性形式是：
$$
a(x)y'' + b(x)y' + c(x)y = g(x),
$$
其中

- $y = y(x)$ 是未知函数
- $y' = \dfrac{dy}{dx}$，$y'' = \dfrac{d^2y}{dx^2}$
- $a(x), b(x), c(x), g(x)$ 都是已知函数
- 要求 $a(x) \neq 0$（否则就不是严格的“二阶”）

**英文关键词：**

- *second-order differential equation*：二阶微分方程
- *linear differential equation*：线性微分方程
- *coefficient functions*：系数函数 $a(x), b(x), c(x)$

把两边都除以 $a(x)$，可以得到**标准形式（standard form）**：
$$
y'' + p(x)y' + q(x)y = r(x),
$$
其中$ p(x) = \frac{b(x)}{a(x)},\quad q(x)=\frac{c(x)}{a(x)},\quad r(x)=\frac{g(x)}{a(x)}. $

### 3. 齐次 / 非齐次（homogeneous vs nonhomogeneous）

标准形式：
$$
y'' + p(x)y' + q(x)y = r(x).
$$

- 如果 $r(x) \equiv 0$，则称为**齐次二阶线性方程**
  $$
  y'' + p(x)y' + q(x)y = 0
  $$
  → *homogeneous linear equation*

- 如果 $r(x) \not\equiv 0$，则称为**非齐次二阶线性方程**
  $$
  y'' + p(x)y' + q(x)y = r(x)
  $$
  → *nonhomogeneous linear equation*

这点后面很重要，因为：

> 一般解 = 齐次方程的一般解 + 一个非齐次方程的特解
>  （这个在 2.3/2.4 正式讲 superposition principle）

### 4. 初值问题（IVP）和边值问题（BVP）

**二阶初值问题（initial value problem, IVP）** 典型形式：
$$
\begin{cases}
y'' + p(x)y' + q(x)y = r(x),\\
y(x_0) = y_0,\\
y'(x_0) = y_0'.
\end{cases}
$$
两条条件，因为是**二阶** → 直觉上需要两个常数。

**边值问题（boundary value problem, BVP）**（以后 4、5 章会碰）：
$$
\begin{cases}
y'' + p(x)y' + q(x)y = r(x),\\
y(a) = \alpha,\\
y(b) = \beta.
\end{cases}
$$

### 5. 线性方程的一个核心性质：叠加原理（superposition principle）——先给你植个概念

对齐次二阶线性方程
$$
y'' + p(x)y' + q(x)y = 0
$$
有一个非常重要的结论（本节会提出，后面细化）：

> 如果 $y_1(x)$、$y_2(x)$ 都是解，那么任意线性组合
> $$
> y(x) = C_1 y_1(x) + C_2 y_2(x)
> $$
> 也是一个解。

这就是 **superposition principle（叠加原理）**：
 **线性方程的齐次解空间是一个线性空间。**

# **2.2：常系数齐次二阶线性方程（Homogeneous Linear Equations with Constant Coefficients）**

## 一、方程的形式 & 特征方程

$$
y'' + ay' + by = 0,
$$

其中 $a,b$ 是常数（constant coefficients）。

**英文关键词：**

- *homogeneous linear equation with constant coefficients*
- *characteristic equation*：特征方程 / 特征方程式
- *root* / *root of the characteristic equation*：特征根

## 二、三种情况（一定要背的“解的结构”）

特征方程：
$$
r^2 + ar + b = 0
$$

### 两个不相等的实根 $r_1 \neq r_2$

如果特征方程有 **两个不同实根**：
$$
r_1,\ r_2\in \mathbb{R},\ r_1\neq r_2
$$
则通解为
$$
y = C_1 e^{r_1 x} + C_2 e^{r_2 x}.
$$
**关键词：** distinct real roots

------

### 重根（double root）$r_1 = r_2 = r$

如果特征方程只有一个实根（判别式 $=0$）：
$$
r_1 = r_2 = r
$$
则通解为
$$
y = (C_1 + C_2 x)e^{rx}.
$$
**关键词：** repeated root / double root

------

### 共轭复根 $r = \alpha \pm i\beta$（$\beta \neq 0$）

如果特征方程有复根：
$$
r_{1,2} = \alpha \pm i\beta,\quad \beta\neq 0,
$$
通解可写为
$$
y = e^{\alpha x}\big( C_1 \cos \beta x + C_2 \sin \beta x \big).
$$
**关键词：** complex conjugate roots, oscillation（振荡）

> 记忆小句：
>  **“实根给指数，复根给指数乘 cos/sin，重根多一个 x。”**

## 核心套路（超短版）

$$
y'' + ay' + by = 0
$$

1. 设 $y = e^{rx}$ → 得到**特征方程**
   $$
   r^2 + ar + b = 0
   $$

2. 解这个二次方程，得到根：

   - 两个不同实根 $r_1\neq r_2$：
     $$
     y = C_1 e^{r_1 x} + C_2 e^{r_2 x}
     $$

   - 重根 $r$：
     $$
     y = (C_1 + C_2 x)e^{rx}
     $$

   - 复根 $\alpha \pm i\beta$：
     $$
     y = e^{\alpha x}(C_1\cos\beta x + C_2\sin\beta x)
     $$

