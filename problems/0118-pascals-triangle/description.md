给定一个非负整数 *`numRows`*，生成「杨辉三角」的前 *`numRows`* 行。

在「杨辉三角」中，每个数是它左上方和右上方的数的和。

```
    1
   1 1
  1 2 1
 1 3 3 1
1 4 6 4 1
```

### 示例 1

```
输入: numRows = 5
输出: [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]
```

### 示例 2

```
输入: numRows = 1
输出: [[1]]
```

### 提示

- `1 <= numRows <= 30`

### 函数说明

```c
int** generate(int numRows, int* returnSize, int** returnColumnSizes);
```

- `numRows`：要生成的行数
- 返回值：用 `malloc` 申请的二维数组，第 `i` 行是杨辉三角的第 `i` 行（每一行也要单独 `malloc`）
- `*returnSize`：返回的行数（这里就是 `numRows`）
- `*returnColumnSizes`：你需要 `malloc` 一个长度为行数的 int 数组，第 `i` 个元素是第 `i` 行的长度，并把它的地址写进 `*returnColumnSizes`

### 自定义输入格式

```
5
```

只有 1 行，是整数 `numRows`。
