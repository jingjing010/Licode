# 39. 组合总和 —— 小白详细题解

> 这道题是「可以重复选」的组合问题。核心难点只有一个：**怎么避免 `[2,2,3]` 和 `[2,3,2]` 被当成两个答案**。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 给你几种面值互不相同的「硬币」（每种无限多枚），问凑出 `target` 有哪些**不同的凑法**。凑法只看「每种硬币用了几枚」，不看顺序。

拿示例 1 `candidates = [2,3,6,7], target = 7` 来说：

| 凑法 | 2 用了几次 | 3 用了几次 | 6 用了几次 | 7 用了几次 | 和 |
|---|---|---|---|---|---|
| [2,2,3] | 2 | 1 | 0 | 0 | 7 ✅ |
| [7] | 0 | 0 | 0 | 1 | 7 ✅ |
| [2,2,2] | 3 | 0 | 0 | 0 | 6 ❌ |
| [3,3] | 0 | 2 | 0 | 0 | 6 ❌ |

只有两种，答案 `[[2,2,3],[7]]`。

**几个需要注意的细节：**

1. **同一个数可以用很多次**：`[2,2,3]` 用了两次 2。
2. **顺序不同不算新组合**：`[2,2,3]`、`[2,3,2]`、`[3,2,2]` 只能出现一次。
3. 可能一个组合都没有（示例 3），这时返回空数组，`*returnSize = 0`。
4. 题目保证组合数少于 150 个，所以结果数组可以直接开 150 行。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 返回「每行长度不同」的二维数组

和 46 题、78 题一样：

```c
int** res = (int**)malloc(sizeof(int*) * 150);             // 最多 150 行
*returnColumnSizes = (int*)malloc(sizeof(int) * 150);      // 每行的长度
(*returnColumnSizes)[k] = len;                             // 第 k 行有 len 个数，括号不能省
```

### 2. 组合最长有多长？

每个数至少是 2，`target` 最大 40，所以一个组合最多 40 / 2 = **20** 个数，`int path[20]` 就够。

### 3. `qsort` 排序

```c
int cmp(const void* a, const void* b) {
    return *(const int*)a - *(const int*)b;   // 返回负数：a 排前面
}
qsort(candidates, candidatesSize, sizeof(int), cmp);
```

`qsort` 是标准库自带的排序函数，第 4 个参数是「怎么比较两个元素」的函数。

---

## 💡 第三步：思路一 —— 回溯：每种数「再选一个 / 换下一种」

### 思路

怎么保证不重复？规定：**按下标顺序决定每种数用几个**。先决定 `candidates[0]` 用几个，再决定 `candidates[1]` 用几个……这样每个组合只会以一种方式被生成。

递归函数 `dfs(i, remain)` 表示：现在考虑第 `i` 种数，还差 `remain` 没凑够。每一步只有两个选择：

1. **再选一个 `candidates[i]`**：放进 `path`，`remain` 减掉它，**`i` 不变**（还可以继续选它）；
2. **不再选 `candidates[i]` 了**：换下一种，`dfs(i + 1, remain)`。

结束条件：

- `remain == 0`：凑够了，记录答案；
- `remain < 0` 或 `i == n`：凑不成，返回。

### 手动模拟（`candidates = [2,3], target = 5`，记 c0=2, c1=3）

| 调用 | path | remain | 选择 |
|---|---|---|---|
| dfs(0, 5) | [] | 5 | 再选一个 2 |
| dfs(0, 3) | [2] | 3 | 再选一个 2 |
| dfs(0, 1) | [2,2] | 1 | 再选 2 → remain = -1 失败；换下一种 → dfs(1, 1)：选 3 失败，i 到头失败 |
| dfs(0, 3) | [2] | 3 | 换下一种 → dfs(1, 3) |
| dfs(1, 3) | [2] | 3 | 选 3 → remain = 0，**记录 [2,3]** ✅ |
| dfs(0, 5) | [] | 5 | 换下一种 → dfs(1, 5)：[3] 剩 2，再选 3 失败…… |

### 代码

```c
// i：当前考虑 candidates[i]；remain：还差多少；path[0..len-1]：已选的数
void dfs(int* c, int n, int i, int remain, int* path, int len,
         int** res, int* colSizes, int* cnt) {
    if (remain == 0) {                                      // 凑够了，记录答案
        res[*cnt] = (int*)malloc(sizeof(int) * (len + 1));  // +1 防止 malloc(0)
        for (int k = 0; k < len; k++) res[*cnt][k] = path[k];
        colSizes[*cnt] = len;
        (*cnt)++;
        return;
    }
    if (remain < 0 || i == n) return;                       // 凑过头了 / 没有数可选了

    path[len] = c[i];                                       // 选择 1：再选一个 c[i]
    dfs(c, n, i, remain - c[i], path, len + 1, res, colSizes, cnt);   // i 不变，还能再选它
    dfs(c, n, i + 1, remain, path, len, res, colSizes, cnt);          // 选择 2：换下一种数
}

int** combinationSum(int* candidates, int candidatesSize, int target, int* returnSize, int** returnColumnSizes) {
    int** res = (int**)malloc(sizeof(int*) * 150);          // 题目保证少于 150 个组合
    *returnColumnSizes = (int*)malloc(sizeof(int) * 150);
    int path[20];                                           // 每个数 >= 2，最多 20 个
    *returnSize = 0;
    dfs(candidates, candidatesSize, 0, target, path, 0, res, *returnColumnSizes, returnSize);
    return res;
}
```

### 复杂度分析

- **时间复杂度**：和搜索树的大小成正比，粗略上界 O(n · 2^(target/min))，但本题数据范围很小，实际很快。
- **空间复杂度 O(target / min)**：递归深度最多是「组合长度 + 种类数」。

---

## 🚀 第四步：思路二 —— 排序 + for 循环 + 剪枝

### 思路

思路一里，`remain` 已经变成负数了才发现「凑过头」，白白多递归了一层。还有，如果 `candidates[i]` 已经比 `remain` 大，那它后面**更大**的数也不可能——前提是数组**有序**。

所以：

1. 先把 `candidates` **从小到大排序**；
2. `dfs(start, remain)` 用一个 for 循环，从 `start` 开始枚举「下一个放进组合的数」`candidates[i]`；
3. 递归时传 `i`（**不是 `i + 1`**），表示下一个数只能从 `candidates[i]` 及之后选——既允许重复选自己，又保证组合内部不递减，不会出现 `[3,2]` 这种逆序的重复组合；
4. 一旦 `candidates[i] > remain`，**直接 `break`**，后面的数更大，都不用试了。

### 手动模拟（示例 1，排序后 `[2,3,6,7]`，target = 7）

| path | remain | 枚举 i 从 | 尝试 |
|---|---|---|---|
| [] | 7 | 0 | 2 → 递归；3 → 递归；6 → 递归；7 → **[7]** ✅ |
| [2] | 5 | 0 | 2 → 递归；3 → 递归；6 > 5，break |
| [2,2] | 3 | 0 | 2 → 递归；3 → **[2,2,3]** ✅；6 > 3，break |
| [2,2,2] | 1 | 0 | 2 > 1，break |
| [2,3] | 2 | 1 | 3 > 2，break（注意从 i=1 开始，不会回头选 2） |
| [3] | 4 | 1 | 3 → [3,3] 剩 1 → break；6 > 4，break |
| [6] | 1 | 2 | 6 > 1，break |

### 代码

```c
int cmp(const void* a, const void* b) {
    return *(const int*)a - *(const int*)b;
}

// start：下一个数只能从 candidates[start] 及之后选；remain：还差多少
void dfs(int* c, int n, int start, int remain, int* path, int len,
         int** res, int* colSizes, int* cnt) {
    if (remain == 0) {                                      // 凑够了，记录答案
        res[*cnt] = (int*)malloc(sizeof(int) * (len + 1));
        for (int k = 0; k < len; k++) res[*cnt][k] = path[k];
        colSizes[*cnt] = len;
        (*cnt)++;
        return;
    }
    for (int i = start; i < n; i++) {
        if (c[i] > remain) break;                           // 剪枝：有序，后面的更大，都不行
        path[len] = c[i];                                   // 做选择
        dfs(c, n, i, remain - c[i], path, len + 1, res, colSizes, cnt);  // 传 i：允许重复选
        // 撤销：len 是按值传的，回到这里自动恢复，下一轮循环会覆盖 path[len]
    }
}

int** combinationSum(int* candidates, int candidatesSize, int target, int* returnSize, int** returnColumnSizes) {
    qsort(candidates, candidatesSize, sizeof(int), cmp);    // 排序，剪枝的前提
    int** res = (int**)malloc(sizeof(int*) * 150);
    *returnColumnSizes = (int*)malloc(sizeof(int) * 150);
    int path[20];
    *returnSize = 0;
    dfs(candidates, candidatesSize, 0, target, path, 0, res, *returnColumnSizes, returnSize);
    return res;
}
```

### 复杂度分析

- **时间复杂度**：同样和搜索树大小成正比，但剪掉了所有「凑过头」的分支，实际比思路一快很多。
- **空间复杂度 O(target / min)**：递归深度。

---

## ⚠️ 第五步：小白常见错误

1. **for 循环每次都从 0 开始**：会同时生成 `[2,2,3]`、`[2,3,2]`、`[3,2,2]`，答案重复。要从 `start` 开始。
2. **递归传 `i + 1`**：每个数只能用一次，`[2,2,3]` 这种答案就找不到了（那是 40 题「组合总和 II」的写法）。
3. **没排序就 `break`**：数组无序时，`c[i] > remain` 不代表后面的数也大，会漏掉答案。没排序只能 `continue`。
4. **把 `path` 直接存进结果**：`res[*cnt] = path;` 所有组合共用同一块内存。必须 `malloc` 后复制。
5. **结果数组开太小**：只开 `candidatesSize` 行，组合数可能比候选数多得多，越界崩溃。题目保证少于 150，就开 150。
6. **`*returnColumnSizes[*cnt] = len`**：少了括号，写到错误的地址。函数里最好像上面那样把 `*returnColumnSizes` 作为普通 `int*` 传给递归函数。

---

## 📊 第六步：两种方法对比

| 方法 | 思路 | 是否需要排序 | 难度 | 建议 |
|---|---|---|---|---|
| 选 / 换下一种 | 二叉决策 | 不需要 | ⭐⭐ | 最容易理解为什么不重复 |
| for 循环 + 剪枝 | 多叉决策 | 需要 | ⭐⭐⭐ | 标准写法，剪枝后更快 |

> 🎯 **学习建议**：记住「组合问题用 `start` 防重复」：传 `i` 表示可以重复选自己，传 `i + 1` 表示每个只能用一次。

---

## 🔗 举一反三

- **40. 组合总和 II**：每个数只能用一次，且数组里有重复数字——递归传 `i + 1`，同一层跳过相同的数。
- **216. 组合总和 III**：从 1~9 里选 k 个不重复的数凑 n。
- **322. 零钱兑换**：同样是「硬币无限用」，但只问最少几枚，用动态规划。
- **思考题**：如果只问「有多少种组合」而不需要列出来，能不能不用回溯、改用动态规划？（提示：518 题「零钱兑换 II」）
