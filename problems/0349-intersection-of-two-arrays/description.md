给定两个数组 `nums1` 和 `nums2` ，返回 *它们的 交集* 。输出结果中的每个元素一定是 **唯一** 的。我们可以 **不考虑输出结果的顺序** 。

### 示例 1

```
输入：nums1 = [1,2,2,1], nums2 = [2,2]
输出：[2]
```

### 示例 2

```
输入：nums1 = [4,9,5], nums2 = [9,4,9,8,4]
输出：[4,9]
解释：[9,4] 也是可通过的
```

### 提示

- `1 <= nums1.length, nums2.length <= 1000`
- `0 <= nums1[i], nums2[i] <= 1000`

### 函数说明

```c
int* intersection(int* nums1, int nums1Size, int* nums2, int nums2Size, int* returnSize);
```

- `nums1`、`nums2`：两个数组，`nums1Size`、`nums2Size` 是它们的长度
- 返回值：用 `malloc` 申请的数组，存放交集中的元素（每个元素只出现一次，顺序任意）
- `*returnSize`：返回数组的长度

### 自定义输入格式

```
[4,9,5]
[9,4,9,8,4]
```

第 1 行是 `nums1`，第 2 行是 `nums2`。（判题时会把你返回的数组从小到大排序后输出）
