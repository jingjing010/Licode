# 28. 找出字符串中第一个匹配项的下标 —— 小白详细题解

> 这就是 C 标准库函数 `strstr` 要做的事。暴力法人人都能写，而它的优化版 **KMP 算法**是字符串匹配的经典，值得花时间弄懂。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 在一大段文字 `haystack`（干草堆）里找一小段文字 `needle`（针），返回它**第一次出现**的位置；找不到就返回 -1。

示例 1：`haystack = "sadbutsad"`, `needle = "sad"`

| 下标 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| haystack | **s** | **a** | **d** | b | u | t | s | a | d |

`"sad"` 在下标 0 和 6 都出现了，题目要**第一个**，所以返回 0。

**几个需要注意的细节：**

1. 要的是**连续**的一段（子串），不是挑几个字符（子序列）。
2. `needle` 可能比 `haystack` 还长，这时一定找不到。
3. 返回的是 `needle` 第一个字符在 `haystack` 中的下标。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 先求长度，别在循环条件里反复调用 `strlen`

```c
int n = strlen(haystack), m = strlen(needle);
for (int i = 0; i + m <= n; i++) { ... }     // ✅ 长度只算一次
for (int i = 0; i < strlen(haystack); i++)   // ❌ 每轮都重新数一遍，O(n) 变 O(n²)
```

### 2. 为什么起点只枚举到 `n - m`？

如果起点 `i > n - m`，从 `i` 开始剩下的字符不足 `m` 个，不可能放下 `needle`。写成 `i + m <= n` 还能顺便处理 `m > n` 的情况（循环一次都不执行）。

### 3. 标准库 `strstr`

`strstr(h, nd)` 返回 `nd` 在 `h` 中第一次出现位置的**指针**，找不到返回 `NULL`。指针相减就是下标：`p - h`。学会自己实现之后，平时写代码可以直接用它。

---

## 💡 第三步：思路一 —— 暴力匹配（最容易想到）

### 思路

把 `needle` 对齐到 `haystack` 的每个可能起点 `i`，逐个字符比较；全部相同就返回 `i`，遇到不同就换下一个起点。

### 手动模拟（`haystack = "leetcode"`, `needle = "leeto"`）

| 起点 i | 比较过程 | 结果 |
|---|---|---|
| 0 | l=l, e=e, e=e, t=t, c≠o | ❌ |
| 1 | e≠l | ❌ |
| 2 | e≠l | ❌ |
| 3 | t≠l | ❌ |

`n - m = 3`，起点 0~3 都失败，返回 -1。

### 代码

```c
int strStr(char* haystack, char* needle) {
    int n = strlen(haystack);
    int m = strlen(needle);

    // 枚举起点 i：从 i 开始至少还要剩 m 个字符
    for (int i = 0; i + m <= n; i++) {
        int j = 0;
        // 逐个字符比较，直到不同或者 needle 比完
        while (j < m && haystack[i + j] == needle[j]) {
            j++;
        }
        if (j == m) {          // needle 的 m 个字符全部匹配上了
            return i;
        }
    }
    return -1;                 // 所有起点都失败
}
```

### 复杂度分析

- **时间复杂度 O((n - m + 1) × m)**：最坏情况如 `haystack = "aaaa...a"`、`needle = "aa...ab"`，每个起点都要比到最后一位才失败。本题 n、m ≤ 10⁴，最坏约 2500 万次比较，能过。
- **空间复杂度 O(1)**。

---

## 🚀 第四步：思路二 —— KMP 算法（O(n + m)）

### 暴力法浪费在哪？

看 `haystack = "aabaaabaaac"`、`needle = "aabaaac"`：从起点 0 比到第 6 位才失败（`b ≠ c`）。此时我们其实已经知道 `haystack[0..5] = "aabaaa"`，暴力法却把这些信息全扔了，从起点 1 重新比。

KMP 的想法是：**主串指针 `i` 永不回退**，失败时只移动 `needle` 的指针 `j`，跳到一个“已经确定能匹配上”的位置。

### 前缀函数 `next` 数组

`next[j]` 的含义：`needle[0..j]` 这一段里，**既是前缀又是后缀**的最长长度（不能是整段本身）。

以 `needle = "aabaaac"` 为例：

| j | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| needle[j] | a | a | b | a | a | a | c |
| needle[0..j] | a | aa | aab | aaba | aabaa | aabaaa | aabaaac |
| 最长相等前后缀 | — | a | — | a | aa | aa | — |
| next[j] | 0 | 1 | 0 | 1 | 2 | 2 | 0 |

**匹配时怎么用**：`needle` 已经匹配了 `j` 个字符，下一位失败了。这 `j` 个字符的末尾有 `next[j-1]` 个字符和 `needle` 的开头相同，所以直接令 `j = next[j-1]`，继续比较，不用回退 `i`。

### 代码

```c
int strStr(char* haystack, char* needle) {
    int n = strlen(haystack);
    int m = strlen(needle);

    // ===== 1. 求 needle 的 next 数组 =====
    int* next = (int*)malloc(sizeof(int) * m);
    next[0] = 0;                       // 只有 1 个字符时，没有真前后缀
    int j = 0;                         // j：当前最长相等前后缀的长度
    for (int i = 1; i < m; i++) {
        // 不相等就回退 j，直到 j 为 0 或者能接上
        while (j > 0 && needle[i] != needle[j]) {
            j = next[j - 1];
        }
        if (needle[i] == needle[j]) {  // 能接上，长度 +1
            j++;
        }
        next[i] = j;
    }

    // ===== 2. 在 haystack 中匹配 =====
    j = 0;                             // j：needle 已经匹配了几个字符
    for (int i = 0; i < n; i++) {      // i 只往前走，永不回退
        while (j > 0 && haystack[i] != needle[j]) {
            j = next[j - 1];           // 失配：needle 指针跳回去
        }
        if (haystack[i] == needle[j]) {
            j++;
        }
        if (j == m) {                  // 全部匹配
            free(next);
            return i - m + 1;          // 起点 = 终点 - 长度 + 1
        }
    }
    free(next);
    return -1;
}
```

> 💬 求 `next` 和匹配的代码几乎一模一样——求 `next` 本质上就是“needle 自己匹配自己”。

### 复杂度分析

- **时间复杂度 O(n + m)**：`i` 只增不减；`j` 每次最多 +1，回退的总次数不会超过增加的总次数。
- **空间复杂度 O(m)**：`next` 数组。

---

## ⚠️ 第五步：小白常见错误

1. **起点枚举到 `n - 1`** → `haystack[i + j]` 可能越过 `'\0'` 读到数组外面。用 `i + m <= n` 控制。
2. **在循环条件里写 `strlen`** → 每轮都重新计算长度，最坏情况超时。
3. **用 `unsigned` 写 `i <= n - m`** → 如果 `strlen` 返回的 `size_t` 直接相减，`m > n` 时 `n - m` 会变成一个巨大的正数，导致越界。先转成 `int` 再算。
4. **KMP 中失配时写成 `j = next[j]`** → 应该是 `next[j - 1]`，因为已匹配的是 `needle[0..j-1]`。
5. **KMP 中 `while` 写成 `if`** → 失配后可能需要**连续多次**回退，只退一次会漏掉匹配。
6. **返回 `i - m` 而不是 `i - m + 1`** → 匹配完成时 `i` 指向最后一个匹配的字符，起点要加 1。

---

## 📊 第六步：两种方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 暴力匹配 | O(n × m) | O(1) | ⭐ | 必须会，日常够用 |
| KMP | O(n + m) | O(m) | ⭐⭐⭐⭐ | 面试高频，理解 next 数组是关键 |

> 🎯 **学习建议**：KMP 第一次看不懂很正常。建议拿 `"aabaaac"` 在纸上把 `next` 数组和匹配过程完整走一遍，比看十遍代码都有用。

---

## 🔗 举一反三

- **459. 重复的子字符串**：也能用 KMP 的 `next` 数组一行判断。
- **214. 最短回文串**：KMP 的进阶应用。
- **思考题**：如果要找出 `needle` 的**所有**出现位置，KMP 的代码要怎么改？（提示：`j == m` 时不要返回，而是令 `j = next[j - 1]` 继续。）
