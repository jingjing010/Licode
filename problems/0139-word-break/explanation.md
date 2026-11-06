# 139. 单词拆分 —— 小白详细题解

> 字符串上的动态规划入门题。核心问题是：**"前 i 个字符能不能拆完"**。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 给你一个字符串和一本"单词字典"。问：能不能把字符串**从头到尾切成若干段**，每一段都是字典里的单词？单词可以重复用。

拿示例 3 `s = "catsandog"`、字典 `["cats","dog","sand","and","cat"]` 来说：

| 尝试 | 切法 | 结果 |
|---|---|---|
| 1 | cat + sand + og | "og" 不在字典 ❌ |
| 2 | cats + and + og | "og" 不在字典 ❌ |

所有切法最后都剩下 "og"，所以答案是 `false`。

**几个需要注意的细节：**

1. 单词可以**重复使用**（示例 2 用了两次 "apple"）。
2. 不需要用完字典里的所有单词。
3. 必须**恰好**拼成 s，不能有剩余字符。

---

## 🧰 第二步：这道题需要的 C 语言知识

1. **`strncmp(a, b, n)`**：比较两个字符串的前 n 个字符，相等返回 0。
2. **指针偏移 `s + i`**：表示"从 s 的第 i 个字符开始的字符串"，不需要复制子串。所以 `strncmp(s + i, word, len) == 0` 就是在判断"s 从位置 i 开始的 len 个字符是不是 word"。
3. **`char** wordDict`**：字符串数组，`wordDict[k]` 是第 k 个单词（一个 `char*`）。
4. **`calloc`**：申请并清零，`bool` 数组清零就是全部 `false`。

---

## 💡 第三步：思路一 —— 记忆化搜索

### 思路

定义 `can(i)`：从下标 i 开始的后缀 `s[i..]` 能否被拆分。

- `i == n`（走到末尾）→ `true`
- 否则枚举字典里每个单词 w：如果 s 从 i 开始恰好是 w，就看 `can(i + len(w))`

纯递归会**指数级超时**（例如 `"aaaa…ab"` 配上字典 `["a","aa","aaa",…]`，同一个位置会被反复尝试），所以要用 `memo[i]` 记住结果：0 没算过、1 能、2 不能。

### 代码

```c
char* g_s;          // 为了在递归中少传参数，用全局变量保存
int g_n;
char** g_dict;
int g_dictSize;
int* g_memo;        // 0：没算过  1：能拆  2：不能拆

static bool can(int i) {
    if (i == g_n) return true;                     // 整个串都拆完了
    if (g_memo[i] != 0) return g_memo[i] == 1;     // 算过了

    for (int k = 0; k < g_dictSize; k++) {
        int len = (int)strlen(g_dict[k]);
        // s 从 i 开始的 len 个字符等于这个单词，并且剩下的也能拆
        if (i + len <= g_n && strncmp(g_s + i, g_dict[k], len) == 0 && can(i + len)) {
            g_memo[i] = 1;
            return true;
        }
    }
    g_memo[i] = 2;
    return false;
}

bool wordBreak(char* s, char** wordDict, int wordDictSize) {
    g_s = s;
    g_n = (int)strlen(s);
    g_dict = wordDict;
    g_dictSize = wordDictSize;
    g_memo = (int*)calloc(g_n + 1, sizeof(int));   // 全部初始化为 0（没算过）
    bool ans = can(0);
    free(g_memo);
    return ans;
}
```

### 复杂度分析

- **时间复杂度 O(n × m × L)**：n 个位置各算一次，每次枚举 m 个单词、比较最多 L = 20 个字符。约 300 × 1000 × 20 = 6×10⁶。
- **空间复杂度 O(n)**。

---

## 🚀 第四步：思路二 —— 动态规划（自底向上）

### 思路

`dp[i]`：s 的**前 i 个字符**能否被拆分。

- `dp[0] = true`（空串当然能拆）
- `dp[i] = true` 当且仅当存在单词 w（长度 L），满足：
  - `dp[i - L]` 为 true（前面那部分能拆）
  - `s[i-L .. i-1]` 恰好等于 w（最后一段是这个单词）

### 手动模拟（示例 1：`s = "leetcode"`，字典 `["leet","code"]`）

| i | 前 i 个字符 | 能用的最后一个单词 | dp[i] |
|---|---|---|---|
| 0 | "" | — | true |
| 1~3 | "l"…"lee" | 无 | false |
| 4 | "leet" | "leet"，且 dp[0] = true | **true** |
| 5~7 | "leetc"…"leetcod" | 无 | false |
| 8 | "leetcode" | "code"，且 dp[4] = true | **true** |

### 代码

```c
bool wordBreak(char* s, char** wordDict, int wordDictSize) {
    int n = (int)strlen(s);
    // dp[i]：前 i 个字符能否拆分；calloc 后全部是 false
    bool* dp = (bool*)calloc(n + 1, sizeof(bool));
    dp[0] = true;                                   // 空串可以拆分

    for (int i = 1; i <= n; i++) {
        for (int k = 0; k < wordDictSize; k++) {
            int len = (int)strlen(wordDict[k]);
            if (len > i) continue;                  // 单词比前缀还长，不可能
            // 前 i-len 个字符能拆，并且 s[i-len..i-1] 正好是这个单词
            if (dp[i - len] && strncmp(s + i - len, wordDict[k], len) == 0) {
                dp[i] = true;
                break;                              // 找到一种就够了
            }
        }
    }

    bool ans = dp[n];
    free(dp);
    return ans;
}
```

### 复杂度分析

- **时间复杂度 O(n × m × L)**，和思路一相同。（如果预先把每个单词的长度存起来，可以省掉反复调用 `strlen`。）
- **空间复杂度 O(n)**。

---

## ⚠️ 第五步：小白常见错误

1. **贪心地每次匹配最长/最短的单词** → `"aaaaaaa"` 配 `["aaaa","aaa"]`：贪心取最长会变成 aaaa + aaa ✅，但换成 `"cars"` 配 `["car","ca","rs"]`，先取 "car" 剩 "s" 失败，正确拆法是 ca + rs。必须尝试所有可能。
2. **纯递归不加记忆化** → `"aaa…ab"` 这种数据会指数级超时。
3. **用 `strcmp` 代替 `strncmp`** → `strcmp(s + i, word)` 比较的是从 i 开始的**整个剩余字符串**，几乎永远不相等。
4. **`dp` 数组开成 n 而不是 n + 1** → `dp[n]` 越界。`dp[i]` 表示"前 i 个字符"，i 的范围是 0 ~ n。
5. **忘记检查 `len > i`** → `s + i - len` 指到字符串前面去了，越界访问。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 |
|---|---|---|---|
| 纯递归 | 指数级 | O(n) | ❌ 超时 |
| 记忆化搜索 | O(n·m·L) | O(n) | ⭐⭐ |
| 动态规划 | O(n·m·L) | O(n) | ⭐⭐ 推荐 |

---

## 🔗 举一反三

- **140. 单词拆分 II**：要输出所有拆分方案，需要回溯 + 记忆化。
- **字典树（Trie）优化**：把字典建成 208 题的前缀树，从每个位置出发沿树走，可以避免逐个比较单词。
- **思考题**：如果字典很大（10⁵ 个单词）而 s 很短，怎样枚举更快？（提示：枚举"最后一段的长度"，再用哈希表查这段在不在字典里。）
