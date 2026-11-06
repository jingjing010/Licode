给你一个 **无重复元素** 的整数数组 `candidates` 和一个目标整数 `target` ，找出 `candidates` 中可以使数字和为目标数 `target` 的 所有 **不同组合** ，并以列表形式返回。你可以按 **任意顺序** 返回这些组合。

`candidates` 中的 **同一个** 数字可以 **无限制重复被选取** 。如果至少一个数字的被选数量不同，则两种组合是不同的。

对于给定的输入，保证和为 `target` 的不同组合数少于 `150` 个。

### 示例 1

```
输入：candidates = [2,3,6,7], target = 7
输出：[[2,2,3],[7]]
解释：
2 和 3 可以形成一组候选，2 + 2 + 3 = 7 。注意 2 可以使用多次。
7 也是一个候选， 7 = 7 。
仅有这两种组合。
```

### 示例 2

```
输入：candidates = [2,3,5], target = 8
输出：[[2,2,2,2],[2,3,3],[3,5]]
```

### 示例 3

```
输入：candidates = [2], target = 1
输出：[]
```

### 提示

- `1 <= candidates.length <= 30`
- `2 <= candidates[i] <= 40`
- `candidates` 的所有元素 **互不相同**
- `1 <= target <= 40`

### 函数说明

```c
int** combinationSum(int* candidates, int candidatesSize, int target, int* returnSize, int** returnColumnSizes);
```

- `candidates`：数组首地址，`candidatesSize`：数组长度
- 返回值：用 `malloc` 申请的二维数组，每一行是一个组合
- `*returnSize`：写入组合的个数（没有组合时写 0）
- `*returnColumnSizes`：你需要 `malloc` 一个长度为行数的 `int` 数组，第 `i` 个元素写第 `i` 个组合的长度，再把它的地址赋给 `*returnColumnSizes`

### 自定义输入格式

```
[2,3,6,7]
7
```

第 1 行是数组 `candidates`，第 2 行是 `target`。（组合之间的顺序、组合内部数字的顺序都任意：判题时会先把每个组合内部从小到大排序，再把所有组合按字典序排序后输出）
