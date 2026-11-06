以数组 `intervals` 表示若干个区间的集合，其中单个区间为 `intervals[i] = [starti, endi]` 。请你合并所有重叠的区间，并返回 *一个不重叠的区间数组，该数组需恰好覆盖输入中的所有区间* 。

### 示例 1

```
输入：intervals = [[1,3],[2,6],[8,10],[15,18]]
输出：[[1,6],[8,10],[15,18]]
解释：区间 [1,3] 和 [2,6] 重叠, 将它们合并为 [1,6].
```

### 示例 2

```
输入：intervals = [[1,4],[4,5]]
输出：[[1,5]]
解释：区间 [1,4] 和 [4,5] 可被视为重叠区间。
```

### 示例 3

```
输入：intervals = [[4,7],[1,4]]
输出：[[1,7]]
解释：区间 [1,4] 和 [4,7] 可被视为重叠区间。
```

### 提示

- `1 <= intervals.length <= 10^4`
- `intervals[i].length == 2`
- `0 <= starti <= endi <= 10^4`

### 函数说明

```c
int** merge(int** intervals, int intervalsSize, int* intervalsColSize,
            int* returnSize, int** returnColumnSizes);
```

- `intervals`：二维数组，`intervals[i][0]` 是第 `i` 个区间的左端点，`intervals[i][1]` 是右端点
- `intervalsSize`：区间个数；`intervalsColSize`：每一行的长度数组（本题每行都是 2）
- 返回值：用 `malloc` 申请的二维数组，每一行是一个用 `malloc` 申请的长度为 2 的 `int` 数组
- `*returnSize`：返回的区间个数
- `*returnColumnSizes`：你需要 `malloc` 一个长度为 `*returnSize` 的 `int` 数组，每个元素写 2，再把它的地址写进 `*returnColumnSizes`

### 自定义输入格式

```
[[1,3],[2,6],[8,10],[15,18]]
```

只有 1 行，是二维数组 `intervals`。（返回的区间顺序任意，判题时会把它们按左端点从小到大排序后输出）
