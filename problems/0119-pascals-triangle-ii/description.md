给定一个非负索引 `rowIndex`，返回「杨辉三角」的第 `rowIndex` 行。

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
输入：rowIndex = 3
输出：[1,3,3,1]
```

### 示例 2

```
输入：rowIndex = 0
输出：[1]
```

### 示例 3

```
输入：rowIndex = 1
输出：[1,1]
```

### 提示

- `0 <= rowIndex <= 33`

**进阶：**你可以优化你的算法到 `O(rowIndex)` 空间复杂度吗？

### 函数说明

```c
int* getRow(int rowIndex, int* returnSize);
```

- `rowIndex`：要返回的行号（从 0 开始）
- 返回值：第 `rowIndex` 行的所有数，**必须用 `malloc` 分配**（判题程序会负责释放）
- `returnSize`：你需要把返回数组的长度写到 `*returnSize` 中

### 自定义输入格式

```
3
```

只有 1 行，是整数 `rowIndex`。
