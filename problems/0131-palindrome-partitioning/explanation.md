# 131. 分割回文串 —— 小白详细题解

> 这道题是「切割型回溯」：在字符串上一刀一刀地切，每切出一段都要检查它是不是回文。学会它，所有「把字符串切成若干段」的题都是同一个套路。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 用刀把字符串 `s` 切成若干段（每段至少 1 个字符，顺序不能乱），要求**每一段都是回文**（正着读和倒着读一样）。列出所有切法。

拿示例 1 `s = "aab"` 来说，长度为 3 的串有 2 个「缝隙」，每个缝隙切或不切，一共 4 种切法：

| 切法 | 每一段 | 每段都是回文吗？ |
|---|---|---|
| 不切 | `aab` | ❌ `aab` 倒过来是 `baa` |
| 只切第 1 个缝 | `a` \| `ab` | ❌ `ab` 不是回文 |
| 只切第 2 个缝 | `aa` \| `b` | ✅ |
| 两个缝都切 | `a` \| `a` \| `b` | ✅ |

所以答案是 `[["a","a","b"],["aa","b"]]`。

**几个需要注意的细节：**

1. **单个字符一定是回文**，所以「每个字符切成一段」永远是一个合法方案，答案至少有 1 个。
2. 每种方案内部的段**必须按原来的顺序排列**，不能打乱。
3. 长度为 n 的串最多有 2ⁿ⁻¹ 种切法；`"aaaaaaaaaaaaaaaa"`（16 个 a）每种切法都合法，有 2¹⁵ = **32768** 个方案。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 三层指针 `char***` 是什么？

| 类型 | 含义 | 本题里是 |
|---|---|---|
| `char*` | 一个字符串 | 一段，比如 `"aa"` |
| `char**` | 字符串数组 | 一种方案，比如 `["aa","b"]` |
| `char***` | 「字符串数组」的数组 | 所有方案 |

所以要 `malloc` 三层：所有方案的数组 → 每种方案的字符串数组 → 每个字符串。`*returnColumnSizes[i]` 记录第 `i` 种方案有几段。

### 2. 取出子串 `s[start..end]`

C 语言没有 `substr`，要自己复制：

```c
int len = end - start + 1;
char* piece = (char*)malloc(len + 1);      // +1 给 '\0'
memcpy(piece, s + start, len);             // s + start 是子串开头的地址
piece[len] = '\0';                         // 手动加结尾
```

### 3. 双指针判断回文

```c
bool isPal(char* s, int l, int r) {
    while (l < r) {
        if (s[l] != s[r]) return false;    // 两头不一样，不是回文
        l++; r--;                          // 往中间收
    }
    return true;
}
```

---

## 💡 第三步：思路一 —— 回溯 + 每次现场判断回文

### 思路

递归函数 `dfs(start)` 表示：`s[0..start-1]` 已经切好了，现在从 `start` 开始切**下一段**。

1. 如果 `start == n`：整串都切完了，记录当前方案。
2. 否则，枚举这一段的结尾 `end = start, start+1, …, n-1`：
   - 如果 `s[start..end]` 是回文：把这一段记进方案，递归 `dfs(end + 1)`，回来后把这一段撤掉；
   - 不是回文就跳过（剪枝）。

为了方便，方案里每一段只记录「起点」和「长度」，等到记录答案时再真正复制出字符串。

### 手动模拟（`s = "aab"`）

| 调用 | 尝试的段 | 是回文？ | 当前方案 |
|---|---|---|---|
| dfs(0) | `a`（0..0） | ✅ → dfs(1) | [a] |
| dfs(1) | `a`（1..1） | ✅ → dfs(2) | [a, a] |
| dfs(2) | `b`（2..2） | ✅ → dfs(3) **记录** | [a, a, b] |
| dfs(1) | `ab`（1..2） | ❌ 跳过 | [a] |
| dfs(0) | `aa`（0..1） | ✅ → dfs(2) | [aa] |
| dfs(2) | `b`（2..2） | ✅ → dfs(3) **记录** | [aa, b] |
| dfs(0) | `aab`（0..2） | ❌ 跳过 | [] |

### 代码

```c
#define MAXR 32768                 // n <= 16 时最多 2^15 种方案

bool isPal(char* s, int l, int r) {
    while (l < r) {
        if (s[l] != s[r]) return false;
        l++;
        r--;
    }
    return true;
}

// start：从这里开始切下一段；k：当前方案已经有几段
// starts[i] / lens[i]：第 i 段的起点和长度
void dfs(char* s, int n, int start, int* starts, int* lens, int k,
         char*** res, int* colSizes, int* cnt) {
    if (start == n) {                                   // 切完了，记录这个方案
        char** plan = (char**)malloc(sizeof(char*) * k);
        for (int i = 0; i < k; i++) {
            plan[i] = (char*)malloc(lens[i] + 1);       // 每一段复制成独立的字符串
            memcpy(plan[i], s + starts[i], lens[i]);
            plan[i][lens[i]] = '\0';
        }
        res[*cnt] = plan;
        colSizes[*cnt] = k;
        (*cnt)++;
        return;
    }
    for (int end = start; end < n; end++) {
        if (!isPal(s, start, end)) continue;            // 这一段不是回文，换个结尾
        starts[k] = start;                              // 做选择：这一段是 s[start..end]
        lens[k] = end - start + 1;
        dfs(s, n, end + 1, starts, lens, k + 1, res, colSizes, cnt);   // 切剩下的部分
        // 撤销：k 是按值传递的，回到这里自然恢复，下一轮会覆盖 starts[k]
    }
}

char*** partition(char* s, int* returnSize, int** returnColumnSizes) {
    int n = strlen(s);
    char*** res = (char***)malloc(sizeof(char**) * MAXR);
    *returnColumnSizes = (int*)malloc(sizeof(int) * MAXR);
    int starts[16], lens[16];                           // 最多切成 16 段
    *returnSize = 0;
    dfs(s, n, 0, starts, lens, 0, res, *returnColumnSizes, returnSize);
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n · 2ⁿ)**：最多 2ⁿ⁻¹ 种方案，每种方案的生成和复制都是 O(n)；判断回文在最坏情况下还会再多一个 O(n) 因子。
- **空间复杂度 O(n)**：递归深度 n（答案本身不算）。

> 💬 慢在哪？同一段子串会被反复判断：比如 `s[2..5]` 是不是回文，在不同的分支里会被检查很多次。

---

## 🚀 第四步：思路二 —— 动态规划预处理回文 + 回溯

### 思路

把「`s[i..j]` 是不是回文」**提前全部算好**存进表 `pal[i][j]`，回溯时直接查表，O(1)。

怎么算？一个串是回文，当且仅当：**两头字符相同**，并且**去掉两头后中间部分也是回文**：

```
pal[i][j] = (s[i] == s[j]) && (j - i < 2 || pal[i+1][j-1])
```

- `j - i < 2` 表示长度为 1 或 2：两头相同就够了（中间没东西）。
- `pal[i][j]` 依赖 `pal[i+1][j-1]`（`i` 更大的那一行），所以 **`i` 要从大到小算**。

### 手动模拟（`s = "aab"` 的 `pal` 表，行是 i，列是 j）

| i \ j | 0 (a) | 1 (a) | 2 (b) |
|---|---|---|---|
| 0 | T | T（a==a，长度 2） | F（a≠b） |
| 1 | | T | F（a≠b） |
| 2 | | | T |

计算顺序：先算第 2 行，再算第 1 行，最后算第 0 行。

### 代码

```c
#define MAXR 32768                 // n <= 16 时最多 2^15 种方案

bool pal[16][16];                  // pal[i][j]：s[i..j] 是否回文

void dfs(char* s, int n, int start, int* starts, int* lens, int k,
         char*** res, int* colSizes, int* cnt) {
    if (start == n) {                                   // 切完了，记录这个方案
        char** plan = (char**)malloc(sizeof(char*) * k);
        for (int i = 0; i < k; i++) {
            plan[i] = (char*)malloc(lens[i] + 1);
            memcpy(plan[i], s + starts[i], lens[i]);
            plan[i][lens[i]] = '\0';
        }
        res[*cnt] = plan;
        colSizes[*cnt] = k;
        (*cnt)++;
        return;
    }
    for (int end = start; end < n; end++) {
        if (!pal[start][end]) continue;                 // 查表，O(1)
        starts[k] = start;
        lens[k] = end - start + 1;
        dfs(s, n, end + 1, starts, lens, k + 1, res, colSizes, cnt);
    }
}

char*** partition(char* s, int* returnSize, int** returnColumnSizes) {
    int n = strlen(s);
    // 1. 预处理：i 从大到小，因为 pal[i][j] 要用到 pal[i+1][j-1]
    for (int i = n - 1; i >= 0; i--) {
        for (int j = i; j < n; j++) {
            pal[i][j] = (s[i] == s[j]) && (j - i < 2 || pal[i + 1][j - 1]);
        }
    }
    // 2. 回溯
    char*** res = (char***)malloc(sizeof(char**) * MAXR);
    *returnColumnSizes = (int*)malloc(sizeof(int) * MAXR);
    int starts[16], lens[16];
    *returnSize = 0;
    dfs(s, n, 0, starts, lens, 0, res, *returnColumnSizes, returnSize);
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n · 2ⁿ)**：预处理 O(n²)，回溯时判断回文变成 O(1)。
- **空间复杂度 O(n²)**：`pal` 表。

---

## ⚠️ 第五步：小白常见错误

1. **子串忘了加 `'\0'`**：`memcpy` 只复制字符，不会自动加结尾；打印时会读出一串乱码。
2. **`pal` 表的计算顺序反了**：`i` 从小到大算时，`pal[i+1][j-1]` 还没算出来（是 0），`"aba"` 会被误判为不是回文。
3. **结果数组开小了**：按 `n` 或 `n * n` 开，遇到 16 个 `a` 的 32768 个方案就会越界。
4. **把同一个 `path` 数组直接存进结果**：所有方案都指向同一块内存，最后全变成一样的。记录时必须 `malloc` 新的数组。
5. **递归传 `end` 而不是 `end + 1`**：下一段又从 `end` 开始，同一个字符被用了两次，还可能无限递归。
6. **`*returnColumnSizes[*cnt] = k`**：少了括号，优先级错误写到别处。像上面那样把 `*returnColumnSizes` 作为普通 `int*` 传进递归函数最安全。

---

## 📊 第六步：两种方法对比

| 方法 | 时间复杂度 | 额外空间 | 难度 | 建议 |
|---|---|---|---|---|
| 回溯 + 现场判断回文 | O(n² · 2ⁿ) 最坏 | O(n) | ⭐⭐ | 先写对它 |
| DP 预处理 + 回溯 | O(n · 2ⁿ) | O(n²) | ⭐⭐⭐ | 标准答案，查表更快 |

> 🎯 **学习建议**：「切割问题」就是「组合问题」换了个样子：组合是选哪些**元素**，切割是选在哪些**位置**下刀。

---

## 🔗 举一反三

- **5. 最长回文子串**：同一张 `pal[i][j]` 表，求最长的那个 `T`。
- **132. 分割回文串 II**：只问最少切几刀，用动态规划。
- **93. 复原 IP 地址**：同样是切割型回溯，每段要满足「0~255 且没有前导零」。
- **思考题**：如果只问「有多少种分割方案」而不用列出来，你能用 `pal` 表写一个 O(n²) 的动态规划吗？
