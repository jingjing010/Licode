# 118. 杨辉三角 —— 小白详细题解

> 这道题的算法非常简单，真正的难点是 **C 语言怎么返回一个"二维数组"**。把这道题吃透，以后所有返回 `int**` 的题都不怕了。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 生成杨辉三角的前 `numRows` 行。每行两头是 1，中间每个数 = 它"左上方"和"正上方"两个数之和。

把三角形**靠左对齐**写出来，规律就很清楚了：

| 行号 i | 第 0 列 | 第 1 列 | 第 2 列 | 第 3 列 | 第 4 列 |
|---|---|---|---|---|---|
| 0 | 1 | | | | |
| 1 | 1 | 1 | | | |
| 2 | 1 | **2** | 1 | | |
| 3 | 1 | 3 | 3 | 1 | |
| 4 | 1 | 4 | **6** | 4 | 1 |

例如第 4 行第 2 列的 6 = 第 3 行第 1 列的 3 + 第 3 行第 2 列的 3。

**几个需要注意的细节：**

1. 第 `i` 行（从 0 开始数）有 `i + 1` 个数，每行长度**不一样**。
2. 每行第一个和最后一个数都是 1。
3. `numRows = 30` 时最大的数是 C(29,14) = 77558760，`int` 放得下。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 函数签名拆解

```c
int** generate(int numRows, int* returnSize, int** returnColumnSizes)
```

| 部分 | 含义 |
|---|---|
| `int**`（返回值） | "指向 int* 的指针"，也就是一个**存放每行地址的数组** |
| `int* returnSize` | 你要通过它告诉调用者：一共返回了**几行** |
| `int** returnColumnSizes` | 你要 `malloc` 一个数组记录**每行有几个数**，再把这个数组的地址写进 `*returnColumnSizes` |

### 2. "锯齿形"二维数组的内存长什么样？

```
res ──▶ [ res[0] | res[1] | res[2] | ... ]    ← 先 malloc 这一排"行指针"
            │        │        │
            ▼        ▼        ▼
           [1]     [1,1]   [1,2,1]            ← 再为每一行单独 malloc
```

所以要 malloc **两层**：

```c
int** res = (int**)malloc(sizeof(int*) * numRows);   // 第一层：numRows 个"行指针"
res[i] = (int*)malloc(sizeof(int) * (i + 1));        // 第二层：第 i 行有 i+1 个 int
```

注意第一层用的是 `sizeof(int*)`（指针的大小），第二层是 `sizeof(int)`。

### 3. 为什么是 `*returnColumnSizes = ...` 而不是 `returnColumnSizes = ...`？

调用者大概是这么写的：

```c
int* colSizes;                                   // 调用者自己的变量
int** ans = generate(5, &rows, &colSizes);       // 把这个变量的地址传给你
```

你拿到的 `returnColumnSizes` 是"调用者变量的地址"。只有写 `*returnColumnSizes = 新数组`，才是把新数组的地址**存进调用者的变量**里。访问其中第 i 个元素时要写 `(*returnColumnSizes)[i]`，括号不能省（`[]` 的优先级比 `*` 高）。

---

## 💡 第三步：思路一 —— 用组合数公式直接算

### 思路

杨辉三角第 `i` 行第 `j` 个数就是组合数 C(i, j)。同一行里相邻两项有关系：

C(i, j) = C(i, j-1) × (i - j + 1) / j

所以每一行从 1 开始，乘一个、除一个，就能依次算出来，不需要上一行。

### 手动模拟（第 4 行）

| j | 计算 | 结果 |
|---|---|---|
| 0 | 起点 | 1 |
| 1 | 1 × 4 / 1 | 4 |
| 2 | 4 × 3 / 2 | 6 |
| 3 | 6 × 2 / 3 | 4 |
| 4 | 4 × 1 / 4 | 1 |

### 代码

```c
int** generate(int numRows, int* returnSize, int** returnColumnSizes) {
    int** res = (int**)malloc(sizeof(int*) * numRows);          // 存每行的地址
    *returnColumnSizes = (int*)malloc(sizeof(int) * numRows);   // 存每行的长度

    for (int i = 0; i < numRows; i++) {
        res[i] = (int*)malloc(sizeof(int) * (i + 1));   // 第 i 行有 i+1 个数
        (*returnColumnSizes)[i] = i + 1;

        long long c = 1;                 // C(i, 0) = 1；用 long long 防止乘法中间溢出
        for (int j = 0; j <= i; j++) {
            res[i][j] = (int)c;
            c = c * (i - j) / (j + 1);   // 由 C(i, j) 推出 C(i, j+1)
        }
    }

    *returnSize = numRows;               // 一共 numRows 行
    return res;
}
```

> 💬 必须**先乘后除**：`c * (i - j)` 一定能被 `j + 1` 整除；如果先除就会因为整数除法丢掉小数而出错。

### 复杂度分析

- **时间复杂度 O(numRows²)**：一共要填 1 + 2 + … + numRows 个数。
- **空间复杂度 O(1)**（不计返回的数组）。

---

## 🚀 第四步：思路二 —— 逐行递推（最自然的做法）

### 思路

直接按定义来：每行两头填 1，中间的 `res[i][j] = res[i-1][j-1] + res[i-1][j]`。上一行已经算好了，直接拿来用。这种做法只用加法，不用担心乘法溢出，也是动态规划最入门的样子：**用已经算好的小问题，推出新的问题**。

### 手动模拟（从第 3 行推第 4 行）

上一行 `res[3] = [1, 3, 3, 1]`

| j | 计算 | res[4][j] |
|---|---|---|
| 0 | 两头是 1 | 1 |
| 1 | res[3][0] + res[3][1] = 1 + 3 | 4 |
| 2 | res[3][1] + res[3][2] = 3 + 3 | 6 |
| 3 | res[3][2] + res[3][3] = 3 + 1 | 4 |
| 4 | 两头是 1 | 1 |

### 代码

```c
int** generate(int numRows, int* returnSize, int** returnColumnSizes) {
    // 第一层：numRows 个"行指针"
    int** res = (int**)malloc(sizeof(int*) * numRows);
    // 每行长度数组，地址写回给调用者
    *returnColumnSizes = (int*)malloc(sizeof(int) * numRows);

    for (int i = 0; i < numRows; i++) {
        res[i] = (int*)malloc(sizeof(int) * (i + 1));   // 第二层：第 i 行
        (*returnColumnSizes)[i] = i + 1;

        res[i][0] = 1;                  // 行首是 1
        res[i][i] = 1;                  // 行尾是 1（i == 0 时和行首是同一个位置，没关系）
        for (int j = 1; j < i; j++) {   // 中间的数 = 左上 + 正上
            res[i][j] = res[i - 1][j - 1] + res[i - 1][j];
        }
    }

    *returnSize = numRows;
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(numRows²)**。
- **空间复杂度 O(1)**（不计返回的数组）。

---

## ⚠️ 第五步：小白常见错误

1. **只 malloc 了第一层** `int** res = malloc(...)`，然后直接写 `res[i][j] = 1` → `res[i]` 是野指针，程序崩溃。每一行都要单独 `malloc`。
2. **`*returnColumnSizes[i] = i + 1`** → 因为 `[]` 优先级比 `*` 高，这等于 `*(returnColumnSizes[i])`，访问了错误的内存。必须写 `(*returnColumnSizes)[i]`。
3. **忘记 malloc `*returnColumnSizes`** → 直接 `(*returnColumnSizes)[i] = ...` 写到了野指针上。
4. **第一层写成 `malloc(sizeof(int) * numRows)`** → 在 64 位系统上指针占 8 字节、`int` 占 4 字节，空间只有一半，会越界。
5. **中间循环写成 `j <= i`** → 会访问 `res[i-1][i]`，上一行根本没有这个位置。
6. **组合数公式先除后乘** `c = c / (j + 1) * (i - j)` → 整数除法会截断，比如 3 / 2 = 1，结果错误。

---

## 📊 第六步：两种方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 组合数公式 | O(numRows²) | O(1) | ⭐⭐ | 了解数学背景，注意溢出和除法顺序 |
| 逐行递推 | O(numRows²) | O(1) | ⭐ | 推荐，最直观、最不容易错 |

---

## 🔗 举一反三

- **119. 杨辉三角 II**：只要第 `rowIndex` 行，能不能只用 O(rowIndex) 的空间？（提示：在同一个数组上**从右往左**更新。）
- **62. 不同路径**：网格里每格的路径数 = 上方 + 左方，和杨辉三角是同一种递推。
- **思考题**：为什么第 4 种常见错误在 32 位系统上可能"碰巧"不出错？
