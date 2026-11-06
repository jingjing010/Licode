# 566. 重塑矩阵 —— 小白详细题解

> 算法很简单，难点在于 **C 语言如何返回一个二维数组**。这道题是练习 `int**` 和 `returnColumnSizes` 的最佳入门题。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 把一个 `m` 行 `n` 列的矩阵，按"从左到右、从上到下"的顺序把数字一个个读出来，再按同样的顺序填进一个 `r` 行 `c` 列的新矩阵。如果元素个数对不上（`m × n ≠ r × c`），就原样返回。

示例 1：`mat = [[1,2],[3,4]]`，`r = 1, c = 4`

```
原矩阵 2×2：        按行读出：          新矩阵 1×4：
  1 2        →     1, 2, 3, 4    →     1 2 3 4
  3 4
```

示例 2：`r = 2, c = 4` 需要 8 个元素，但只有 4 个，**做不到**，返回原矩阵 `[[1,2],[3,4]]`。

**几个需要注意的细节：**

1. 先判断 `m * n == r * c`，不相等直接返回原矩阵。
2. "行遍历顺序"就是我们平时读书的顺序：先读完第 0 行，再读第 1 行……

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 二维数组在 C 里长什么样？

力扣的 C 语言二维数组是"**指针的数组**"：

```
res ──→ [ res[0] ][ res[1] ][ res[2] ]      ← 行指针数组（int* 的数组），类型 int**
            │         │         │
            ↓         ↓         ↓
          [1,2,3]   [4,5,6]   [7,8,9]       ← 每一行是一个 int 数组，类型 int*
```

所以要 `malloc` **两层**：

```c
int** res = (int**)malloc(sizeof(int*) * r);     // 第一层：r 个行指针
for (int i = 0; i < r; i++) {
    res[i] = (int*)malloc(sizeof(int) * c);       // 第二层：每行 c 个 int
}
```

### 2. `returnSize` 和 `returnColumnSizes`

调用者需要知道你返回的矩阵**有几行、每行几列**：

| 参数 | 类型 | 你要做的事 |
|---|---|---|
| `returnSize` | `int*` | `*returnSize = 行数;` |
| `returnColumnSizes` | `int**` | 申请一个数组存每行的列数，再把**数组地址**写进 `*returnColumnSizes` |

```c
*returnColumnSizes = (int*)malloc(sizeof(int) * r);   // 申请存放"每行列数"的数组
for (int i = 0; i < r; i++) {
    (*returnColumnSizes)[i] = c;                       // 每行都是 c 列
}
```

> ⚠️ `(*returnColumnSizes)[i]` 的括号不能省！`*returnColumnSizes[i]` 会先算 `returnColumnSizes[i]`，意思完全不同，会访问非法内存。

### 3. 一维下标 ↔ 二维坐标

把 `m × n` 矩阵按行展开成一维，第 `k` 个元素（从 0 开始）在：

```
行 = k / n        列 = k % n
```

例如 2×2 矩阵中 `k = 3`：行 = 3 / 2 = 1，列 = 3 % 2 = 1，就是 `mat[1][1] = 4`。

---

## 💡 第三步：思路一 —— 两个"游标"同步移动

### 思路

1. 元素个数不相等 → 直接返回原矩阵（行数 `m`，列数数组就用 `matColSize`）。
2. 申请 `r × c` 的新矩阵。
3. 按行遍历原矩阵，同时用 `(row, col)` 记录"下一个要写到新矩阵的哪里"：每写一个，`col++`；`col` 到了 `c` 就换行（`row++`，`col = 0`）。

### 手动模拟（`mat = [[1,2,3],[4,5,6]]`，`r = 3, c = 2`）

| 读到 | 写到 (row, col) | 写完后 (row, col) |
|---|---|---|
| 1 | (0,0) | (0,1) |
| 2 | (0,1) | 换行 → (1,0) |
| 3 | (1,0) | (1,1) |
| 4 | (1,1) | 换行 → (2,0) |
| 5 | (2,0) | (2,1) |
| 6 | (2,1) | 换行 → (3,0) |

结果 `[[1,2],[3,4],[5,6]]`。

### 代码

```c
int** matrixReshape(int** mat, int matSize, int* matColSize, int r, int c, int* returnSize, int** returnColumnSizes) {
    int m = matSize;            // 原矩阵行数
    int n = matColSize[0];      // 原矩阵列数（每行都一样）

    // 1. 元素个数对不上，无法重塑，原样返回
    if (m * n != r * c) {
        *returnSize = m;
        *returnColumnSizes = matColSize;    // 原矩阵的列数数组可以直接用
        return mat;
    }

    // 2. 申请 r 行 c 列的新矩阵，以及记录每行列数的数组
    int** res = (int**)malloc(sizeof(int*) * r);
    *returnColumnSizes = (int*)malloc(sizeof(int) * r);
    for (int i = 0; i < r; i++) {
        res[i] = (int*)malloc(sizeof(int) * c);
        (*returnColumnSizes)[i] = c;
    }

    // 3. 按行读原矩阵，按行写新矩阵
    int row = 0, col = 0;               // 新矩阵中下一个要写的位置
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            res[row][col] = mat[i][j];
            col++;
            if (col == c) {             // 这一行写满了，换到下一行开头
                row++;
                col = 0;
            }
        }
    }

    *returnSize = r;
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(m·n)**：每个元素拷贝一次。
- **空间复杂度 O(1)**：除了返回的矩阵，只用了几个变量。

---

## 🚀 第四步：思路二 —— 用一维下标直接换算

### 思路

既然两个矩阵都是"按行展开成同一条一维序列"，那第 `k` 个元素：

- 在**原矩阵**中的位置是 `[k / n][k % n]`；
- 在**新矩阵**中的位置是 `[k / c][k % c]`。

一个循环 `k` 从 0 到 `m*n - 1` 就搞定，不需要手动维护"换行"。

### 手动模拟（示例 1：`n = 2`，`c = 4`）

| k | 原位置 [k/2][k%2] | 值 | 新位置 [k/4][k%4] |
|---|---|---|---|
| 0 | [0][0] | 1 | [0][0] |
| 1 | [0][1] | 2 | [0][1] |
| 2 | [1][0] | 3 | [0][2] |
| 3 | [1][1] | 4 | [0][3] |

### 代码

```c
int** matrixReshape(int** mat, int matSize, int* matColSize, int r, int c, int* returnSize, int** returnColumnSizes) {
    int m = matSize, n = matColSize[0];
    if (m * n != r * c) {               // 无法重塑，返回原矩阵
        *returnSize = m;
        *returnColumnSizes = matColSize;
        return mat;
    }

    int** res = (int**)malloc(sizeof(int*) * r);
    *returnColumnSizes = (int*)malloc(sizeof(int) * r);
    for (int i = 0; i < r; i++) {
        res[i] = (int*)malloc(sizeof(int) * c);
        (*returnColumnSizes)[i] = c;
    }

    // 第 k 个元素：原矩阵 [k/n][k%n] → 新矩阵 [k/c][k%c]
    for (int k = 0; k < m * n; k++) {
        res[k / c][k % c] = mat[k / n][k % n];
    }

    *returnSize = r;
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(m·n)**；**空间复杂度 O(1)**（不含返回值）。代码更短，"一维 ↔ 二维换算"是矩阵题的常用技巧。

---

## ⚠️ 第五步：小白常见错误

1. **没有判断 `m * n == r * c`** → 示例 2 会越界写入或输出错误的矩阵。
2. **只申请了行指针，没给每一行 `malloc`** → `res[i][j] = ……` 写入野指针，程序崩溃。
3. **`*returnColumnSizes[i] = c`（少了括号）** → 运算符优先级错误，访问非法内存。
4. **忘记设置 `*returnSize` / `*returnColumnSizes`** → 判题程序不知道矩阵多大，输出为空或崩溃。
5. **把 `k / n`、`k % n` 中的 `n` 写成 `c`（或反过来）** → 原矩阵按原列数 `n` 换算，新矩阵按新列数 `c` 换算，不能混用。
6. **返回局部二维数组 `int res[300][300];`** → 函数返回后内存失效；而且它的类型也不是 `int**`。

---

## 📊 第六步：两种方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 说明 |
|---|---|---|---|---|
| 双游标同步移动 | O(m·n) | O(1) | ⭐ | 最直观 |
| 一维下标换算 | O(m·n) | O(1) | ⭐ | 代码最短，矩阵题常用技巧 |

---

## 🔗 举一反三

- **867. 转置矩阵**：同样返回二维数组，新矩阵是 `n × m`。
- **2022. 将一维数组转变成二维数组**：本题的"一维版"。
- **思考题**：如果要求按**列遍历顺序**重塑（先读第 0 列，再读第 1 列），换算公式应该怎么改？
