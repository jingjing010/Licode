# 34. 在排序数组中查找元素的第一个和最后一个位置 —— 小白详细题解

> 普通二分只回答"有没有"，这道题要回答"从哪开始、到哪结束"。学会**找边界的二分**，以后一大类二分题都能套。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 给你一排**从小到大排好**的数（可以有重复），找出 `target` 第一次出现和最后一次出现的位置。没有就返回 `[-1,-1]`。

示例 1：`nums = [5,7,7,8,8,10], target = 8`

| 下标 | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 数值 | 5 | 7 | 7 | **8** | **8** | 10 |

8 从下标 3 开始，到下标 4 结束，答案 `[3,4]`。

**几个需要注意的细节：**

1. 数组可能是**空的**（`numsSize == 0`），这时直接返回 `[-1,-1]`，千万别访问 `nums[0]`。
2. 数组里可能**全是 target**，比如 `[7,7,7,7]`，答案是 `[0,3]`。
3. 题目要求 `O(log n)`，所以"先二分找到一个 8，再向左右一格一格扩展"在最坏情况（全是 8）下会退化成 O(n)。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 返回数组：`malloc` + `*returnSize`

```c
int* res = (int*)malloc(sizeof(int) * 2);   // 在堆上申请 2 个 int
*returnSize = 2;                            // 告诉调用者数组长度是 2
```

局部数组 `int res[2];` 在函数返回后就失效了，不能返回它。

### 2. 防溢出的中点写法

```c
int mid = lo + (hi - lo) / 2;   // 推荐
int mid = (lo + hi) / 2;        // 下标很大时 lo + hi 可能超过 int 范围
```

### 3. `static` 辅助函数

可以在主函数外面再写一个小函数（比如 `lowerBound`），加上 `static` 表示"只在这个文件里用"，避免和别的名字冲突。

---

## 💡 第三步：思路一 —— 线性扫描（最容易想到）

### 思路

从左往右扫，第一次遇到 `target` 记为开始；继续扫，最后一次遇到的就是结束。

### 代码

```c
int* searchRange(int* nums, int numsSize, int target, int* returnSize) {
    int* res = (int*)malloc(sizeof(int) * 2);
    *returnSize = 2;
    res[0] = -1;                          // 先假设没找到
    res[1] = -1;
    for (int i = 0; i < numsSize; i++) {
        if (nums[i] == target) {
            if (res[0] == -1) res[0] = i; // 第一次遇到：记为开始
            res[1] = i;                   // 每遇到一次都更新结束位置
        }
    }
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n)**：n = 10⁵ 能过，但不满足题目 `O(log n)` 的要求。
- **空间复杂度 O(1)**。

---

## 🚀 第四步：思路二 —— 两次"找左边界"的二分

### 思路

定义一个函数 `lowerBound(x)`：返回数组里**第一个 `>= x` 的位置**（都比 x 小就返回 `n`）。

- 开始位置 = `lowerBound(target)`。如果这个位置越界了，或者那里的数不等于 `target`，说明 target 不存在。
- 结束位置 = `lowerBound(target + 1) - 1`：第一个 `>= target+1` 的位置的前一格，就是最后一个 `target`。

`lowerBound` 用**左闭右开**区间 `[lo, hi)`：

- `nums[mid] < x`：mid 和它左边都不可能是答案 → `lo = mid + 1`
- `nums[mid] >= x`：mid 可能就是答案，但左边也许还有 → `hi = mid`（保留 mid）
- 循环结束时 `lo == hi`，就是答案。

### 手动模拟（`nums = [5,7,7,8,8,10]`，求 `lowerBound(8)`）

| 轮次 | lo | hi | mid | nums[mid] | 比较 | 操作 |
|---|---|---|---|---|---|---|
| 1 | 0 | 6 | 3 | 8 | 8 >= 8 | hi = 3 |
| 2 | 0 | 3 | 1 | 7 | 7 < 8 | lo = 2 |
| 3 | 2 | 3 | 2 | 7 | 7 < 8 | lo = 3 |
| 结束 | 3 | 3 | | | | 返回 3 |

再求 `lowerBound(9)` 得到 5（下标 5 的 10 是第一个 >= 9 的），结束位置 = 5 - 1 = 4。答案 `[3,4]` ✅

### 代码

```c
// 返回第一个 >= x 的下标；如果所有数都 < x，返回 n
static int lowerBound(int* nums, int n, long long x) {
    int lo = 0, hi = n;                 // 左闭右开 [lo, hi)
    while (lo < hi) {                   // 区间非空
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] < x) {
            lo = mid + 1;               // mid 太小，答案在右边
        } else {
            hi = mid;                   // mid 可能是答案，保留它
        }
    }
    return lo;
}

int* searchRange(int* nums, int numsSize, int target, int* returnSize) {
    int* res = (int*)malloc(sizeof(int) * 2);
    *returnSize = 2;
    int l = lowerBound(nums, numsSize, target);
    if (l == numsSize || nums[l] != target) {   // 越界或不相等：不存在
        res[0] = -1;
        res[1] = -1;
        return res;
    }
    res[0] = l;
    // target + 1 用 long long，防止 target = INT_MAX 时溢出
    res[1] = lowerBound(nums, numsSize, (long long)target + 1) - 1;
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(log n)**：两次二分。
- **空间复杂度 O(1)**。

---

## ⚠️ 第五步：小白常见错误

1. **空数组也去读 `nums[0]`** → 运行错误。`lowerBound` 返回 `n` 时必须先判断 `l == numsSize`，再看 `nums[l]`。
2. **找到一个 target 后向两边线性扩展** → 全是 target 的数组（如 10⁵ 个 7）会退化成 O(n)，不符合题目要求。
3. **左闭右开写成 `hi = numsSize - 1` 但循环条件仍用 `lo < hi`** → 最后一个元素永远检查不到，比如 `[1,2,3]` 找 3 会出错。
4. **`hi = mid - 1` 写在"找左边界"里** → 可能把唯一的答案 mid 丢掉。找边界时 `nums[mid] >= x` 的那一侧要写 `hi = mid`。
5. **`target + 1` 溢出**：`target` 是 int，如果它等于 `INT_MAX`，加 1 就溢出了。用 `(long long)target + 1` 更安全。
6. **忘了 `*returnSize = 2`** → 判题系统认为你返回了空数组。

---

## 📊 第六步：两种方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 线性扫描 | O(n) | O(1) | ⭐ | 先理解题意 |
| 两次 lowerBound | O(log n) | O(1) | ⭐⭐ | 题目要求，必须掌握 |

---

## 🔗 举一反三

- **35. 搜索插入位置**：答案就是 `lowerBound(target)`。
- **278. 第一个错误的版本**：同样是"找第一个满足条件的位置"。
- **思考题**：只写一个"找最后一个 `<= x` 的位置"（upperBound - 1）的函数，能不能同样求出两个端点？
