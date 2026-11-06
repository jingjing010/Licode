# 78. 子集 —— 小白详细题解

> 子集问题是回溯的第二课：每个元素「选」或「不选」。它还有一个非常漂亮的**二进制**解法。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 给你几个互不相同的数，列出从中**任意挑若干个**（可以一个都不挑，也可以全挑）的所有方式。

`[1,2,3]` 的每个元素都有「选 / 不选」两种状态，所以一共 2 × 2 × 2 = **8** 个子集：

| 1 | 2 | 3 | 子集 |
|---|---|---|---|
| 不选 | 不选 | 不选 | [] |
| 不选 | 不选 | 选 | [3] |
| 不选 | 选 | 不选 | [2] |
| 不选 | 选 | 选 | [2,3] |
| 选 | 不选 | 不选 | [1] |
| 选 | 不选 | 选 | [1,3] |
| 选 | 选 | 不选 | [1,2] |
| 选 | 选 | 选 | [1,2,3] |

**几个需要注意的细节：**

1. **空集 `[]` 也是一个子集**，千万别漏。
2. 子集是「集合」，`[1,2]` 和 `[2,1]` 是同一个，不能重复输出。
3. n 个元素有 **2ⁿ** 个子集，n ≤ 10 时最多 1024 个。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 二维数组的返回方式

和 46 题一样：返回 `int**`，`*returnSize` 写行数，`*returnColumnSizes` 指向一个记录每行长度的数组。本题每行长度**不一样**（空集长度为 0）。

### 2. 位运算

| 写法 | 含义 | 例子 |
|---|---|---|
| `1 << n` | 2 的 n 次方 | `1 << 3` = 8 |
| `mask >> j & 1` | 取出 `mask` 二进制的第 j 位（0 或 1） | `5 >> 2 & 1` = 1（5 = 101₂） |

> 💬 `>>` 的优先级比 `&` 高，所以 `mask >> j & 1` 就是 `(mask >> j) & 1`。不放心就加括号。

---

## 💡 第三步：思路一 —— 回溯（选 / 不选）

### 思路

递归函数 `dfs(i)` 负责决定 `nums[i]` 选不选：

1. 如果 `i == n`：所有元素都决定完了，`path` 里就是一个子集，复制保存。
2. **选** `nums[i]`：放进 `path`，递归 `dfs(i + 1)`，然后**拿出来**（撤销）。
3. **不选** `nums[i]`：直接递归 `dfs(i + 1)`。

### 代码

```c
// i：现在决定 nums[i] 选不选；path[0..len-1]：已经选了的数
void dfs(int* nums, int n, int i, int* path, int len,
         int** res, int* colSizes, int* cnt) {
    if (i == n) {                                   // 每个数都决定完了，记录这个子集
        res[*cnt] = (int*)malloc(sizeof(int) * (len + 1));   // +1：防止 len 为 0 时 malloc(0)
        for (int k = 0; k < len; k++) res[*cnt][k] = path[k];
        colSizes[*cnt] = len;
        (*cnt)++;
        return;
    }
    path[len] = nums[i];                            // 选 nums[i]
    dfs(nums, n, i + 1, path, len + 1, res, colSizes, cnt);
    // 撤销：len 是按值传递的，回到这里时 len 还是原来的值，相当于把 nums[i] 拿出来了
    dfs(nums, n, i + 1, path, len, res, colSizes, cnt);   // 不选 nums[i]
}

int** subsets(int* nums, int numsSize, int* returnSize, int** returnColumnSizes) {
    int total = 1 << numsSize;                      // 2^n 个子集
    int** res = (int**)malloc(sizeof(int*) * total);
    *returnColumnSizes = (int*)malloc(sizeof(int) * total);
    int path[10];                                   // n 最大是 10
    int cnt = 0;
    dfs(nums, numsSize, 0, path, 0, res, *returnColumnSizes, &cnt);
    *returnSize = cnt;
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n · 2ⁿ)**：2ⁿ 个子集，每个复制最多 n 个数。
- **空间复杂度 O(n)**：递归深度 n（结果本身不算）。

---

## 🚀 第四步：思路二 —— 二进制枚举（不用递归）

### 思路

看第一步那张表：把「选」写成 1、「不选」写成 0，每个子集正好对应一个 n 位二进制数！

| mask（十进制） | 二进制（第 2 1 0 位） | 子集 |
|---|---|---|
| 0 | 000 | [] |
| 1 | 001 | [1] |
| 2 | 010 | [2] |
| 3 | 011 | [1,2] |
| 4 | 100 | [3] |
| 5 | 101 | [1,3] |
| 6 | 110 | [2,3] |
| 7 | 111 | [1,2,3] |

所以只要让 `mask` 从 `0` 数到 `2ⁿ - 1`，第 `j` 位是 1 就把 `nums[j]` 放进子集。

### 代码

```c
int** subsets(int* nums, int numsSize, int* returnSize, int** returnColumnSizes) {
    int total = 1 << numsSize;                          // 2^n
    int** res = (int**)malloc(sizeof(int*) * total);
    *returnColumnSizes = (int*)malloc(sizeof(int) * total);

    for (int mask = 0; mask < total; mask++) {
        res[mask] = (int*)malloc(sizeof(int) * (numsSize + 1));
        int len = 0;
        for (int j = 0; j < numsSize; j++) {
            if ((mask >> j) & 1) {                      // 第 j 位是 1：选 nums[j]
                res[mask][len++] = nums[j];
            }
        }
        (*returnColumnSizes)[mask] = len;               // 注意括号
    }
    *returnSize = total;
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n · 2ⁿ)**，**空间复杂度 O(1)**（结果本身不算），代码最短。

---

## ⚠️ 第五步：小白常见错误

1. **漏了空集**：比如只在「选了数」之后才记录答案，`returnSize` 少 1。
2. **结果数组开小了**：`malloc(sizeof(int*) * numsSize)` 只开了 n 行，实际需要 2ⁿ 行，越界崩溃。
3. **把 `path` 直接存进结果**：所有子集共用一块内存，最后全都一样。要 `malloc` 后复制。
4. **`*returnColumnSizes[mask] = len` 少括号**：优先级错误，写到了错误的地址。
5. **位运算写成 `mask & 1 << j` 却以为结果是 0/1**：`mask & (1 << j)` 的结果是 0 或 `2^j`，用在 `if` 里没问题，但如果拿去做加法或下标就错了。

---

## 📊 第六步：两种方法对比

| 方法 | 时间复杂度 | 额外空间 | 难度 | 建议 |
|---|---|---|---|---|
| 回溯（选/不选） | O(n · 2ⁿ) | O(n) 递归栈 | ⭐⭐ | 能推广到带条件的子集问题 |
| 二进制枚举 | O(n · 2ⁿ) | O(1) | ⭐⭐ | 最简洁，嵌入式里位操作很常用 |

> 🎯 **学习建议**：两种都写一遍。二进制枚举在 n 较小时（≤ 20）是万能的暴力枚举手段。

---

## 🔗 举一反三

- **90. 子集 II**：数组有重复元素，先排序，同一层里跳过相同的数。
- **77. 组合**：只要长度为 k 的子集，在回溯中加一个长度限制。
- **46. 全排列**：在意顺序的「子集」。
- **思考题**：怎样只用 `mask & (mask - 1)` 这个技巧，快速数出一个子集里有几个元素？
