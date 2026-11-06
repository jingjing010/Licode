给你一个二维整数数组 `matrix`， 返回 `matrix` 的 **转置矩阵** 。

矩阵的 **转置** 是指将矩阵的主对角线翻转，交换矩阵的行索引与列索引。

### 示例 1

```
输入：matrix = [[1,2,3],[4,5,6],[7,8,9]]
输出：[[1,4,7],[2,5,8],[3,6,9]]
```

### 示例 2

```
输入：matrix = [[1,2,3],[4,5,6]]
输出：[[1,4],[2,5],[3,6]]
```

### 提示

- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 1000`
- `1 <= m * n <= 10^5`
- `-10^9 <= matrix[i][j] <= 10^9`

### 函数说明

```c
int** transpose(int** matrix, int matrixSize, int* matrixColSize, int* returnSize, int** returnColumnSizes);
```

- `matrix`：二维数组，`matrixSize`：行数 `m`，`matrixColSize[i]`：第 `i` 行的列数（都等于 `n`）
- 返回值：用 `malloc` 申请的转置矩阵（`n` 行 `m` 列）
- `*returnSize`：必须设置为结果矩阵的行数（即 `n`）
- `*returnColumnSizes`：必须指向一个用 `malloc` 申请的长度为 `n` 的数组，每个元素都是 `m`

### 自定义输入格式

```
[[1,2,3],[4,5,6]]
```

只有 1 行，是二维数组 `matrix`。
