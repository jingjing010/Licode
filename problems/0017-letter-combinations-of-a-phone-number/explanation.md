# 17. 电话号码的字母组合 —— 小白详细题解

> 这是最适合入门「回溯」的一道题：每一位数字就是一层选择，没有任何剪枝和去重，纯粹练习「逐位填写 + 递归」。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 老式手机上，每个数字键印着几个字母（2 是 abc，3 是 def……）。给你按下的一串数字，列出**每个键各挑一个字母**能拼出的所有字符串。

拿示例 1 `digits = "23"` 来说：第 1 位从 `abc` 里挑一个，第 2 位从 `def` 里挑一个：

| 第 1 位 \ 第 2 位 | d | e | f |
|---|---|---|---|
| **a** | ad | ae | af |
| **b** | bd | be | bf |
| **c** | cd | ce | cf |

一共 3 × 3 = **9** 种。

**几个需要注意的细节：**

1. `digits` 可能是空串 `""`，这时要返回**空数组**（`*returnSize = 0`），而不是包含一个空串的数组 `[""]`。
2. `7` 和 `9` 对应 **4** 个字母（pqrs、wxyz），其余都是 3 个。
3. 组合总数 = 每位字母个数的乘积，最多 4 × 4 × 4 × 4 = 256 个。
4. 顺序任意，判题时会排序。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 字符串数组做「映射表」

```c
const char* map[10] = {"", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};
```

`map[2]` 就是 `"abc"`。下标 0、1 不对应字母，放空串占位，这样就能直接用数字当下标。

### 2. 数字字符转整数：`digits[i] - '0'`

`digits[i]` 是**字符** `'2'`（ASCII 码 50），不是整数 2。`'2' - '0'` 才等于 2。

### 3. 返回 `char**`（字符串数组）

| 层次 | 要做什么 |
|---|---|
| 外层 `char**` | `malloc(sizeof(char*) * 总数)`：一排「字符串指针」 |
| 每个字符串 | `malloc(长度 + 1)`：多 1 个字节放结尾的 `'\0'` |
| `*returnSize` | 写入字符串的个数 |

> ❓ **为什么要 `+1`？** C 语言的字符串靠结尾的 `'\0'` 判断在哪结束。`"ad"` 实际占 3 个字节：`'a'`、`'d'`、`'\0'`。忘了它，打印时就会一直读到内存里的垃圾。

---

## 💡 第三步：思路一 —— 回溯（逐位填写）

### 思路

用一个字符数组 `path` 表示「正在拼的字符串」。递归函数 `dfs(i)` 负责填第 `i` 位：

1. 如果 `i == n`：所有位都填好了，把 `path` 复制一份存进答案。
2. 否则，取出第 `i` 个数字对应的字母串，**每个字母都试一次**：`path[i] = 字母`，然后递归 `dfs(i + 1)` 去填下一位。

> 💬 这里不需要显式「撤销」：下一次循环会直接用新字母覆盖 `path[i]`。

### 手动模拟（`digits = "23"`）

| 调用 | 第 i 位可选 | path | 动作 |
|---|---|---|---|
| dfs(0) | abc | `_ _` | 先试 a |
| dfs(1) | def | `a _` | 先试 d |
| dfs(2) | — | `a d` | 填满，记录 "ad" |
| dfs(1) | def | `a _` | 再试 e → 记录 "ae"，再试 f → 记录 "af" |
| dfs(0) | abc | `_ _` | 再试 b → 依次记录 "bd" "be" "bf" |
| dfs(0) | abc | `_ _` | 再试 c → 依次记录 "cd" "ce" "cf" |

### 代码

```c
const char* MAP[10] = {"", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};

// i：正在填第 i 位；path：已经填好的前 i 位；res / cnt：答案数组和已有个数
void dfs(char* digits, int n, int i, char* path, char** res, int* cnt) {
    if (i == n) {                                      // 每一位都填好了
        res[*cnt] = (char*)malloc(n + 1);              // +1 给 '\0'
        strcpy(res[*cnt], path);                       // 必须复制，path 之后还会被改
        (*cnt)++;
        return;
    }
    const char* letters = MAP[digits[i] - '0'];        // 第 i 个数字对应的字母
    for (int k = 0; letters[k] != '\0'; k++) {
        path[i] = letters[k];                          // 第 i 位放这个字母
        dfs(digits, n, i + 1, path, res, cnt);         // 去填下一位
    }
}

char** letterCombinations(char* digits, int* returnSize) {
    int n = strlen(digits);
    *returnSize = 0;
    if (n == 0) {                                      // 空串：返回空数组
        return (char**)malloc(sizeof(char*));
    }
    int total = 1;
    for (int i = 0; i < n; i++) total *= strlen(MAP[digits[i] - '0']);   // 组合总数

    char** res = (char**)malloc(sizeof(char*) * total);
    char path[5];                                      // 最多 4 位 + '\0'
    path[n] = '\0';                                    // 先把结尾放好
    dfs(digits, n, 0, path, res, returnSize);          // returnSize 本身就是 int*，可以直接当计数器
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n · 4ⁿ)**：最多 4ⁿ 个组合，每个复制 n 个字符。
- **空间复杂度 O(n)**：递归深度 n（答案本身不算）。

---

## 🚀 第四步：思路二 —— 迭代（一位一位地「扩展」）

### 思路

不用递归也可以：维护一个「当前所有组合」的列表，一开始只有一个空串 `""`。每读一位数字，就把列表里**每个**旧组合后面分别接上这位的每个字母，得到新列表。

| 处理到 | 列表 |
|---|---|
| 开始 | `[""]` |
| 数字 2（abc） | `["a","b","c"]` |
| 数字 3（def） | `["ad","ae","af","bd","be","bf","cd","ce","cf"]` |

由于总数可以提前算出，我们可以更直接地**按位置算出每个组合**：把第 `idx` 个组合看成一个「混合进制数」，最后一位变化最快（就像里程表）。

例如 `"23"`：每位都有 3 种字母，第 `idx` 个组合的第 1 位是 `idx / 3`，第 2 位是 `idx % 3`：

| idx | idx / 3 | idx % 3 | 组合 |
|---|---|---|---|
| 0 | 0 (a) | 0 (d) | ad |
| 1 | 0 (a) | 1 (e) | ae |
| 4 | 1 (b) | 1 (e) | be |
| 8 | 2 (c) | 2 (f) | cf |

### 代码

```c
const char* MAP[10] = {"", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};

char** letterCombinations(char* digits, int* returnSize) {
    int n = strlen(digits);
    *returnSize = 0;
    if (n == 0) return (char**)malloc(sizeof(char*));  // 空串：返回空数组

    int total = 1;
    for (int i = 0; i < n; i++) total *= strlen(MAP[digits[i] - '0']);

    char** res = (char**)malloc(sizeof(char*) * total);
    for (int idx = 0; idx < total; idx++) {
        res[idx] = (char*)malloc(n + 1);
        res[idx][n] = '\0';
        int x = idx;
        // 从最后一位往前，像拆十进制数的各位一样拆出每一位选哪个字母
        for (int i = n - 1; i >= 0; i--) {
            const char* letters = MAP[digits[i] - '0'];
            int len = strlen(letters);                 // 这一位的「进制」：3 或 4
            res[idx][i] = letters[x % len];
            x /= len;
        }
    }
    *returnSize = total;
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n · 4ⁿ)**，**空间复杂度 O(1)**（答案本身不算），没有递归。

---

## ⚠️ 第五步：小白常见错误

1. **空串返回了 `[""]`**：如果不特判，`total` 是 1，递归会立即记录一个空串。题目要求返回空数组 `[]`。
2. **`MAP[digits[i]]` 忘了减 `'0'`**：`digits[i]` 是 `'2'`（50），直接当下标越界。
3. **字符串没留 `'\0'` 的位置**：`malloc(n)` 少一个字节，`strcpy` 写越界，打印出乱码。
4. **把 `path` 直接存进答案**：`res[*cnt] = path;` 所有答案都指向同一个数组，最后全是 `"cf"`。
5. **以为每个数字都是 3 个字母**：`total = pow(3, n)` 在含 7 或 9 时开小了，数组越界崩溃。

---

## 📊 第六步：两种方法对比

| 方法 | 时间复杂度 | 额外空间 | 难度 | 建议 |
|---|---|---|---|---|
| 回溯 | O(n · 4ⁿ) | O(n) 递归栈 | ⭐⭐ | 通用模板，必须掌握 |
| 混合进制迭代 | O(n · 4ⁿ) | O(1) | ⭐⭐ | 不用递归，思路巧妙 |

> 🎯 **学习建议**：先写回溯版，把「第 i 层做第 i 个选择」的感觉建立起来；之后的组合、排列、N 皇后都是这个结构。

---

## 🔗 举一反三

- **22. 括号生成**：每一位只能放 `(` 或 `)`，但多了「合法性」限制，需要剪枝。
- **46. 全排列**：每一位从「还没用过的数」里选。
- **78. 子集**：每个元素「选或不选」，也是逐位决策。
- **思考题**：如果按键 `1` 对应 `""`（不能跳过），输入里出现 `1` 时答案应该是什么？
