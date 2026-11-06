给你两个整数 `left` 和 `right` ，表示区间 `[left, right]` ，返回此区间内所有数字 **按位与** 的结果（包含 `left` 、`right` 端点）。

### 示例 1

```
输入：left = 5, right = 7
输出：4
```

### 示例 2

```
输入：left = 0, right = 0
输出：0
```

### 示例 3

```
输入：left = 1, right = 2147483647
输出：0
```

### 提示

- `0 <= left <= right <= 2^31 - 1`

### 函数说明

```c
int rangeBitwiseAnd(int left, int right);
```

- `left`、`right`：区间的左右端点（包含）
- 返回值：`left & (left + 1) & ... & right` 的结果

### 自定义输入格式

```
5
7
```

第 1 行是 `left`，第 2 行是 `right`。
