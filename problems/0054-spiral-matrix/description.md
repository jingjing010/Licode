给你一个 `m` 行 `n` 列的矩阵 `matrix` ，请按照 **顺时针螺旋顺序** ，返回矩阵中的所有元素。

### 示例 1

```
输入：matrix = [[1,2,3],[4,5,6],[7,8,9]]
输出：[1,2,3,6,9,8,7,4,5]
```

### 示例 2

```
输入：matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
输出：[1,2,3,4,8,12,11,10,9,5,6,7]
```

### 提示

- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 10`
- `-100 <= matrix[i][j] <= 100`

### 函数说明

```c
int* spiralOrder(int** matrix, int matrixSize, int* matrixColSize, int* returnSize);
```

- `matrix`：二维数组，`matrix[i][j]` 是第 `i` 行第 `j` 列的元素
- `matrixSize`：行数 `m`；`matrixColSize`：每一行的列数组成的数组，列数 `n` 就是 `matrixColSize[0]`
- 返回值：用 `malloc` 申请的数组，按顺时针螺旋顺序存放所有元素
- `*returnSize`：你必须把返回数组的长度（这里是 `m × n`）写进这个指针指向的变量

### 自定义输入格式

```
[[1,2,3],[4,5,6],[7,8,9]]
```

只有 1 行，是二维数组 `matrix`。
