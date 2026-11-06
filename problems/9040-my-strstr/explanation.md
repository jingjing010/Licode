# 9040. 实现 strstr —— 小白详细题解

> 在一段文本里找一个子串，是嵌入式里解析模块回复的日常操作：`if (strstr(rx_buf, "OK"))`。这道题先写出人人都能看懂的"暴力匹配"，再介绍面试加分项 **KMP 算法**——它保证在最坏情况下也只扫描 haystack 一遍。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 在长字符串 `haystack`（干草堆）里找短字符串 `needle`（针）第一次出现的位置，返回指向那个位置的指针；找不到返回 `NULL`。

拿示例 2 来说（`haystack = "aaab"`，`needle = "ab"`）：

| 起点 | haystack 从起点开始 | 和 "ab" 比较 | 结果 |
|---|---|---|---|
| 0 | **a a** a b | a=a，a≠b | 失败 |
| 1 | a **a a** b | a=a，a≠b | 失败 |
| 2 | a a **a b** | a=a，b=b | **成功，返回 haystack + 2** |

**几个需要注意的细节：**

1. `needle` 是空串时返回 `haystack`（判题输出 0）。这是 C 标准的规定。
2. 返回的是**指针**，不是下标。判题程序会用 `返回值 - haystack` 换算成下标。
3. 有多处匹配时返回**第一处**。
4. `needle` 比 `haystack` 长时一定找不到。
5. 参数是 `const char*`，返回值却是 `char*`，返回前要强制转换 `(char*)`——这是标准库的历史设计。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 指针就是位置

`haystack + 2` 就是"haystack 中下标 2 的位置"。找到匹配后直接返回起点指针，调用者可以从这里接着读：

```c
char* p = strstr(rx_buf, "+IPD,");
if (p) {
    int len = atoi(p + 5);   // 跳过 "+IPD," 这 5 个字符，读出数据长度
}
```

### 2. `NULL` 表示"没找到"

返回指针的函数通常用 `NULL` 表示失败，调用者**必须先判断**再使用，否则就是空指针访问（单片机上通常直接 HardFault）。

### 3. 去掉 `const` 的强制转换

```c
const char* start = haystack;
return (char*)start;   // 不转换会有警告：返回值丢失了 const 限定
```

---

## 💡 第三步：思路一 —— 暴力匹配（朴素算法）

### 思路

1. `needle` 为空直接返回 `haystack`
2. 让起点 `start` 从 haystack 的每个位置出发：
   - 用 `h`、`n` 两个指针从 `start` 和 `needle` 开始逐个比较
   - 字符相同就都往后走；`needle` 走到 `'\0'` 说明**全部匹配**，返回 `start`
   - 遇到不同字符就放弃这个起点，换下一个
3. 所有起点都失败，返回 `NULL`

### 手动模拟（示例 3：`"+CME ERROR: 10"` 找 `"OK"`）

每个起点的第一个字符都要和 `'O'` 比较：`+`、`C`、`M`、`E`、空格、`E`、`R`、`R`、`O`……在下标 8 的 `'O'` 处第一个字符相同，但下一个是 `'R'` ≠ `'K'`，失败。所有起点都失败，返回 `NULL`，输出 `-1`。

### 代码

```c
char* my_strstr(const char* haystack, const char* needle) {
    // 空串规定返回 haystack
    if (*needle == '\0') {
        return (char*)haystack;
    }
    // 依次尝试 haystack 的每个位置作为起点
    for (const char* start = haystack; *start != '\0'; start++) {
        const char* h = start;
        const char* n = needle;
        // 两个字符相同就一起往后走，直到 needle 结束或者出现不同
        while (*n != '\0' && *h == *n) {
            h++;
            n++;
        }
        // needle 已经走到 '\0'：全部匹配成功
        if (*n == '\0') {
            return (char*)start;
        }
    }
    return NULL;   // 所有起点都失败
}
```

> 💡 `while` 条件里不需要判断 `*h != '\0'`：如果 `*h` 是 `'\0'` 而 `*n` 不是，`*h == *n` 自然为假，循环就会停下。

### 复杂度分析

- **时间复杂度 O(n × m)**：n、m 分别是 haystack 和 needle 的长度。最坏情况比如 `"aaaa...ab"` 里找 `"aa...ab"`，每个起点都要比较到 needle 的最后一个字符才失败。
- **空间复杂度 O(1)**。

日常解析 AT 回复时 needle 很短（`"OK"`、`"ERROR"`），暴力匹配完全够用，这也是很多嵌入式 C 库的实际实现方式。

---

## 🚀 第四步：思路二 —— KMP 算法（优化）

### 为什么能优化？

暴力匹配失败后，起点只往后挪一格，**之前已经比较过的字符全部作废**。但其实我们已经知道这些字符是什么了（它们和 needle 的前一部分相同）。

例如在 `"ababd..."` 里找 `"ababc"`：比到第 5 个字符 `d ≠ c` 时失败。已经匹配的 `"abab"` 的**结尾 `"ab"` 恰好等于 needle 的开头 `"ab"`**，所以不用退回去，直接认为"已经匹配了 2 个字符"，继续拿 `d` 和 needle 的第 3 个字符比较即可。**haystack 的指针永远不回退**。

### next 数组（部分匹配表）

`next[i]` = needle 的前 `i+1` 个字符中，"**既是前缀又是后缀**"的最长长度（不能是整个串本身）。

| i | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| needle[i] | a | b | a | b | c |
| 前 i+1 个字符 | a | ab | aba | abab | ababc |
| 最长相同前后缀 | — | — | a | ab | — |
| next[i] | 0 | 0 | 1 | 2 | 0 |

匹配时如果已经匹配了 `k` 个字符、下一个字符失配，就令 `k = next[k-1]`，然后继续尝试；`k` 减到 0 还失配，就让 haystack 前进一格。

### 手动模拟（示例 2：`"aaab"` 找 `"ab"`，`next = [0, 0]`）

| i | haystack[i] | 匹配前 k | 比较 | 匹配后 k |
|---|---|---|---|---|
| 0 | a | 0 | a = needle[0] | 1 |
| 1 | a | 1 | a ≠ needle[1]='b' → k = next[0] = 0；a = needle[0] | 1 |
| 2 | a | 1 | 同上 | 1 |
| 3 | b | 1 | b = needle[1] | 2 = m，**找到**，起点 = 3 - 2 + 1 = 2 |

### 代码

```c
char* my_strstr(const char* haystack, const char* needle) {
    size_t m = 0;
    while (needle[m] != '\0') m++;          // needle 的长度
    if (m == 0) return (char*)haystack;

    // 1. 构造 next 数组：next[i] 是 needle[0..i] 的最长相同前后缀长度
    int* next = (int*)malloc(sizeof(int) * m);
    next[0] = 0;
    size_t k = 0;                           // 当前最长相同前后缀的长度
    for (size_t i = 1; i < m; i++) {
        while (k > 0 && needle[i] != needle[k]) k = next[k - 1];   // 失配就回退
        if (needle[i] == needle[k]) k++;
        next[i] = (int)k;
    }

    // 2. 扫描 haystack，k 表示当前已经匹配了 needle 的前 k 个字符
    k = 0;
    for (size_t i = 0; haystack[i] != '\0'; i++) {
        while (k > 0 && haystack[i] != needle[k]) k = next[k - 1]; // 失配：利用 next 跳转，i 不回退
        if (haystack[i] == needle[k]) k++;
        if (k == m) {                       // 完整匹配，起点是 i - m + 1
            free(next);
            return (char*)(haystack + i - m + 1);
        }
    }
    free(next);
    return NULL;
}
```

### 复杂度分析

- **时间复杂度 O(n + m)**：构造 next 是 O(m)；扫描时 `i` 只增不减，`k` 每次增加最多 1，回退的总次数不超过增加的总次数，所以是 O(n)。
- **空间复杂度 O(m)**：next 数组。

---

## 🔌 嵌入式实战：在接收缓冲区里找关键字

```c
// 等待模块回复 OK 或 ERROR，超时返回 -1
int wait_reply(uint32_t timeout_ms) {
    uint32_t t0 = millis();
    while (millis() - t0 < timeout_ms) {
        rx_buf[rx_len] = '\0';                  // strstr 需要 '\0' 结尾！
        if (strstr(rx_buf, "OK\r\n"))    return 0;
        if (strstr(rx_buf, "ERROR\r\n")) return 1;
    }
    return -1;
}
```

两个工程细节：

1. 串口收到的数据**没有 `'\0'`**，调用 strstr 前要手动补上，并且缓冲区要多留 1 个字节。
2. 如果模块返回的数据里可能含有字节 0（二进制数据），strstr 会提前停下，这时要用 `memmem`（GNU 扩展）或者自己写按长度匹配的版本。

---

## ⚠️ 第五步：小白常见错误

1. **不判断 needle 为空**：暴力代码里 `*n == '\0'` 一开始就成立，但如果 haystack 也是空串，`for` 循环一次都不执行，会错误地返回 `NULL`。所以要在最前面单独处理。
2. **匹配失败后起点跳得太远**：

   ```c
   // ❌ 失败后直接从 h 的位置继续找，会漏掉重叠的匹配
   start = h;
   ```

   在 `"aaab"` 里找 `"ab"` 时会跳过下标 2，返回 `NULL`。暴力法失败后起点只能前进 1 格（只有 KMP 能安全地"跳"）。
3. **返回 `h` 而不是 `start`**：匹配成功时 `h` 已经走到了匹配段的末尾，返回值应该是起点。
4. **使用返回值前不判断 NULL**：`atoi(strstr(buf, "+IPD,") + 5)` 在没找到时访问 `NULL + 5`，直接崩溃。
5. **对没有 `'\0'` 的接收缓冲区调用 strstr**：会一路读到缓冲区之外。
6. **KMP 回退写成 `k = next[k]`**：下标错位，构造的 next 和匹配过程都会出错。记住是 `next[k - 1]`（已经匹配的前 k 个字符的最长相同前后缀）。

---

## 📊 第六步：两种方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 暴力匹配 | O(n × m) | O(1) | ⭐⭐ | 面试必须能写出来；嵌入式常用 |
| KMP | O(n + m) | O(m) | ⭐⭐⭐⭐ | 面试加分项；needle 长、数据量大时使用 |

> 🎯 **学习建议**：先把暴力匹配写熟，能讲清"起点、h、n 三个指针各自的作用"。KMP 先理解"haystack 指针不回退"这个核心思想，再手算几个 next 数组。

---

## 🔗 举一反三

- **力扣 28. 找出字符串中第一个匹配项的下标**：本题的下标版本，可以直接用 KMP 的代码。
- **9038. 实现 strcmp**：暴力匹配的内层循环和 strcmp 非常像。
- **strchr**：在字符串里找一个字符，是 needle 长度为 1 的特例。试着实现 `char* my_strchr(const char* s, int c)`，注意 `c == '\0'` 时要返回指向结尾 `'\0'` 的指针。
- **思考题**：串口数据是一个字节一个字节到达的。如果要在**中断里**边收边检测 `"OK\r\n"`，不把数据攒成字符串再调用 strstr，KMP 的"状态 k"能帮上什么忙？（提示：这就是一个状态机。）
