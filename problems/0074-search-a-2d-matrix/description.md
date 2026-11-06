给你一个满足下述两条属性的 `m x n` 整数矩阵：

- 每行中的整数从左到右按非严格递增顺序排列。
- 每行的第一个整数大于前一行的最后一个整数。

给你一个整数 `target` ，如果 `target` 在矩阵中，返回 `true` ；否则，返回 `false` 。

### 示例 1

```
1   3   5   7
10  11  16  20
23  30  34  60
```

```
输入：matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
输出：true
```

### 示例 2

```
输入：matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
输出：false
```

### 提示

- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 100`
- `-10^4 <= matrix[i][j], target <= 10^4`

### 函数说明

```c
bool searchMatrix(int** matrix, int matrixSize, int* matrixColSize, int target);
```

- `matrix`：二维数组，`matrix[i]` 是第 `i` 行的首地址
- `matrixSize`：行数 `m`
- `matrixColSize`：数组，`matrixColSize[i]` 是第 `i` 行的列数（本题每行都是 `n`，用 `matrixColSize[0]` 即可）
- 返回值：`target` 在矩阵中返回 `true`，否则返回 `false`

### 自定义输入格式

```
[[1,3,5,7],[10,11,16,20],[23,30,34,60]]
3
```

第 1 行是矩阵 `matrix`，第 2 行是 `target`。输出 `true` 或 `false`。
