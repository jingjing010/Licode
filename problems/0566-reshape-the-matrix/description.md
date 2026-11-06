在 MATLAB 中，有一个非常有用的函数 `reshape` ，它可以将一个 `m x n` 矩阵重塑为另一个大小不同（`r x c`）的新矩阵，但保留其原始数据。

给你一个由二维数组 `mat` 表示的 `m x n` 矩阵，以及两个正整数 `r` 和 `c` ，分别表示想要的重构的矩阵的行数和列数。

重构后的矩阵需要将原始矩阵的所有元素以相同的 **行遍历顺序** 填充。

如果具有给定参数的 `reshape` 操作是可行且合理的，则输出新的重塑矩阵；否则，输出原始矩阵。

### 示例 1

```
输入：mat = [[1,2],[3,4]], r = 1, c = 4
输出：[[1,2,3,4]]
```

### 示例 2

```
输入：mat = [[1,2],[3,4]], r = 2, c = 4
输出：[[1,2],[3,4]]
```

### 提示

- `m == mat.length`
- `n == mat[i].length`
- `1 <= m, n <= 100`
- `-1000 <= mat[i][j] <= 1000`
- `1 <= r, c <= 300`

### 函数说明

```c
int** matrixReshape(int** mat, int matSize, int* matColSize, int r, int c, int* returnSize, int** returnColumnSizes);
```

- `mat`：原矩阵，`mat[i]` 是第 `i` 行的首地址
- `matSize`：原矩阵的行数 `m`；`matColSize[i]`：第 `i` 行的列数（本题每行都是 `n`）
- `r`、`c`：想要的新矩阵的行数和列数
- 返回值：用 `malloc` 申请的二维数组（先申请"行指针数组"，再为每一行申请空间）
- `*returnSize`：返回矩阵的行数
- `*returnColumnSizes`：你需要 `malloc` 一个长度为 `*returnSize` 的数组，存放每一行的列数，并把它的地址写进 `*returnColumnSizes`

### 自定义输入格式

```
[[1,2],[3,4]]
1
4
```

共 3 行，依次是矩阵 `mat`、`r`、`c`。
