# 02｜Python 基础（Python Basics）

[返回复习导航](00_复习导航.md)

本章目标：看懂短代码、逐行追踪变量和输出，解释容器与控制流程。课程链接的 Python Cheatsheet 是参考大全，本章围绕课堂列出的基础主题整理。

## 1. 类型、运算与字符串

| 内容 | 语法/例子 | 结果或含义 |
|---|---|---|
| 整数、浮点、字符串、布尔 | `int`, `float`, `str`, `bool` | `3`、`3.0`、`"3"`、`True` 类型不同 |
| 普通除法 | `7 / 2` | `3.5` |
| 向下取整除法 | `7 // 2`；`-7 // 2` | `3`；`-4`，向负无穷取整 |
| 取余（Modulo） | `7 % 2` | `1` |
| 幂（Exponentiation） | `2 ** 3` | `8`，不是 `2 ^ 3` |
| 比较 | `== != < <= > >=` | 返回布尔值；`=` 是赋值 |
| 逻辑 | `and`, `or`, `not` | 组合或取反条件 |
| 类型转换 | `int("3")`, `float("3.5")`, `str(3)` | 无法转换时会报错 |
| 长度与类型 | `len(x)`, `type(x)` | 字符串/容器长度；对象类型 |

先括号，再幂，再乘除与取余，再加减；不确定时使用括号。`-2 ** 2` 是 `-(2 ** 2)=-4`，`(-2) ** 2=4`。

```python
price = 12.5
quantity = 3
revenue = price * quantity
print(f"Revenue = {revenue:.2f}")  # Revenue = 37.50
text = "machine learning"
print(text.upper())               # 大写，不修改原字符串
```

格式化字符串（f-string）用 `{表达式}` 插值，`.2f` 表示保留两位小数。`input()` 的返回值为字符串，数值计算前需要适当转换。`int(3.9)` 得到 `3`，不是四舍五入。

## 2. 四类容器

| 类型 | 创建 | 有顺序 | 可变（Mutable） | 重复值 |
|---|---|---|---|---|
| 列表（List） | `[1, 2, 2]` | 有，可按位置索引 | 是 | 允许 |
| 元组（Tuple） | `(1, 2, 2)`；单元素 `(1,)` | 有，可按位置索引 | 元组元素位置不可重新赋值 | 允许 |
| 字典（Dictionary） | `{"a": 1, "b": 2}` | 保留插入顺序 | 是 | 键唯一，值可重复 |
| 集合（Set） | `{1, 2}`；空集合 `set()` | 无位置顺序保证 | 是 | 元素唯一 |

Python 3.7 起，字典保留插入顺序；读取 `d[1]` 仍表示键为 `1`，不是“第 2 个元素”。集合 `set` 可增删，不能按位置索引；不可变集合另有 `frozenset`，不必与基础 `set` 混淆。空的 `{}` 是字典。

可变性说的是对象本身能否改变，而非变量能否重新绑定。元组中若含列表，那个列表仍可变；基础题通常只使用简单元素。

```python
items = [10, 20, 30]
items.append(40)                 # 加入一个元素
items.extend([50, 60])           # 逐个加入多个元素
last = items.pop()               # 删除并返回末尾元素
prices = {"tea": 5, "coffee": 8}
prices["tea"] = 6               # 更新已有键
prices.get("juice", 0)          # 缺失键返回默认值
unique_items = set([1, 1, 2])    # {1, 2}
```

`append([3,4])` 加入一个嵌套列表；`extend([3,4])` 加入两个元素。`x.sort()` 原地排序，返回 `None`；`sorted(x)` 返回新的排序列表。

## 3. 索引与切片

索引（Indexing）从 0 开始，负数从末尾计数。切片（Slicing）的形式为 `x[start:stop:step]`，**包含起点、不包含终点**。

```python
x = [10, 20, 30, 40, 50]
print(x[0], x[-1])     # 10 50
print(x[1:4])          # [20, 30, 40]
print(x[::2])          # [10, 30, 50]
print(x[::-1])         # [50, 40, 30, 20, 10]
```

列表的 `+` 是连接，`*` 是重复：`[1,2]+[3,4] → [1,2,3,4]`；`[1,2]*2 → [1,2,1,2]`。这与 NumPy 的逐元素运算不同。

```python
a = [1, 2, 3]
b = a               # 同一个列表
c = a[:]            # 浅复制
b[0] = 9
print(a, c)         # [9, 2, 3] [1, 2, 3]
```

浅复制（Shallow Copy）复制外层容器；若内部含可变对象，内部对象可能仍共享。本课基本一维数值例子中，修改切片元素不会改变原列表。

## 4. 条件与循环

```python
score = 75
if score >= 90:
    grade = "A"
elif score >= 60:
    grade = "Pass"
else:
    grade = "Fail"
```

`if/elif/else` 链只执行第一个成立的分支。缩进决定语句归属。`0`、`None`、空字符串及空容器通常为假；非空字符串 `"False"` 为真。

| 语法 | 含义 |
|---|---|
| `range(5)` | `0,1,2,3,4` |
| `range(1,6,2)` | `1,3,5` |
| `for x in values:` | 依次遍历元素 |
| `while condition:` | 条件成立就继续，需要保证条件最终可变化 |
| `break` | 退出当前最内层循环 |
| `continue` | 跳过本轮剩余语句，开始下一轮 |
| `pass` | 什么也不做，仅作为占位语句 |

```python
names = ["Amy", "Bo"]
scores = [80, 90]
for i, name in enumerate(names):
    print(i, name)                   # 索引与值
for name, score in zip(names, scores):
    print(name, score)               # 对应元素配对
for key, value in {"a": 1, "b": 2}.items():
    print(key, value)                # 字典键值对
```

`zip()` 默认在最短输入耗尽时结束。直接 `for key in d` 遍历字典的键；`.values()` 遍历值，`.items()` 遍历键值对。

## 5. 推导式、函数与导入

推导式（Comprehension）把简单循环表达为一个构造容器的表达式：

```python
squares = [x ** 2 for x in range(5) if x % 2 == 0]  # [0, 4, 16]
mapping = {x: x ** 2 for x in range(3)}             # {0: 0, 1: 1, 2: 4}
remainders = {x % 2 for x in range(5)}              # {0, 1}
labels = ["high" if x >= 3 else "low" for x in range(5)]
```

末尾 `if` 表示筛选哪些元素进入结果；前面的 `a if 条件 else b` 表示每个元素取什么值。

```python
def revenue(price, quantity=1):
    total = price * quantity       # 局部变量
    return total

answer = revenue(8, quantity=3)     # 24
print(answer)

import math
print(math.sqrt(9))                # 3.0
```

函数（Function）通过参数（Argument / Parameter）接收输入，通过 `return` 交回结果；没有执行 `return 值` 时返回 `None`。`print()` 显示内容，不能替代 `return`。函数内创建的普通局部变量（Local Variable）只在局部作用域可用。

包/模块（Package / Module）通过 `import` 引入；`import numpy as np` 是为模块取别名，不改变其功能。避免把变量命名为 `list`、`sum` 等内置名称，以免遮蔽原功能。

## 6. Notebook 中的文字与公式

代码单元（Code Cell）运行 Python；Markdown 单元记录解释。常用 Markdown：`# 标题`、`**粗体**`、`- 列表`、`[文字](网址)`。LaTeX 行内公式用 `$...$`，独立公式用 `$$...$$`。这些是写作和解释工具，不会自动执行 Python。

## 7. 纸笔例题与解答

**题目：写出最后的 `total` 与 `out`。**

```python
total = 0
out = []
for n in range(1, 7):
    if n == 5:
        break
    if n % 2 == 0:
        continue
    total += n
    out.append(n ** 2)
```

**解答：** `n=1` 时累加 1、加入 1；`n=2` 跳过；`n=3` 累加 3、加入 9；`n=4` 跳过；`n=5` 退出，因此 `total=4`，`out=[1,9]`。虽然 `range` 包含 6，循环没有执行到 6。

## 8. 易错点与自测

常见错误：把 `=` 当比较；忘记切片/range 的终点不包含；把 `pass` 当成跳过本轮；把 `print` 当返回值；把列表连接当数值相加；把字典插入顺序当位置索引。

1. `len({1,1,2})` 是多少？`type({})` 是什么？
2. `a=[3,1,2]; b=a.sort()` 后，`a` 和 `b` 是什么？
3. `[x+1 for x in range(4) if x>1]` 是什么？
4. 函数只执行 `print(3)`，把调用结果赋给 `x`，`x` 是什么？
5. `list(range(5,0,-2))` 是什么？

**简答：** 1. `2`，`dict`。2. `[1,2,3]` 与 `None`。3. `[3,4]`。4. `None`。5. `[5,3,1]`。

## 课程来源

- [Python Basics](https://bana409.harrywang.me/docs/lectures/python-basics)
- [Python 课堂小组练习](https://bana409.harrywang.me/docs/lectures/python-basics/in-class-group-exercise)
- [教师 Python Cheatsheet](https://www.harrywang.me/blog/python-cheatsheet)
- [Python 官方：数据结构](https://docs.python.org/3/tutorial/datastructures.html)（核对字典顺序与集合可变性）

纸笔例题与自测为复习自编。
