# 49. 字母异位词分组 —— 小白详细题解

> 这道题的核心只有一句话：**给每个单词找一个"身份证号"，身份证号相同的放一组**。难点主要在 C 语言里怎么管理"数组的数组的字符串"。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 给你一堆单词，把"用的字母完全一样、只是顺序不同"的单词归到同一组里，最后把所有组交出去。

"字母异位词"就是**字母打乱重排**得到的词：`eat`、`tea`、`ate` 都由 1 个 `a`、1 个 `e`、1 个 `t` 组成，所以是一组。

拿示例 1 来说，我们把每个单词的字母**排个序**，看看会发生什么：

| 原单词 | 字母排序后 | 属于哪组 |
|---|---|---|
| eat | aet | 第 0 组 |
| tea | aet | 第 0 组 |
| tan | ant | 第 1 组 |
| ate | aet | 第 0 组 |
| nat | ant | 第 1 组 |
| bat | abt | 第 2 组 |

排序后一样的单词就是一组：`{eat, tea, ate}`、`{tan, nat}`、`{bat}`。

**几个需要注意的细节：**

1. **空字符串 `""` 也是一个单词**，它自己（和其他空串）组成一组。示例 2 的答案是 `[[""]]`，不是 `[]`。
2. **相同的单词也要都保留**：`["a","a"]` 的答案是 `[["a","a"]]`，不能去重。
3. 组的顺序、组内的顺序都随意，判题时会统一排序后再比较。
4. 字母个数也要一样：`ab` 和 `aab` **不是**异位词（字母种类相同，但 `a` 的个数不同）。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 看懂 `char***` 这个"三颗星"

```c
char*** groupAnagrams(char** strs, int strsSize, int* returnSize, int** returnColumnSizes)
```

一颗一颗星地拆：

| 类型 | 含义 | 本题中的例子 |
|---|---|---|
| `char*` | 一个字符串 | `"eat"` |
| `char**` | 字符串数组（一组单词） | `["eat","tea","ate"]` |
| `char***` | 字符串数组的数组（很多组） | `[["eat","tea","ate"],["tan","nat"],["bat"]]` |

所以返回值 `res` 的用法是：`res[g]` 是第 `g` 组，`res[g][j]` 是第 `g` 组里的第 `j` 个单词。

### 2. 两个"返回长度"的参数

C 语言的数组不知道自己多长，所以要额外告诉调用者：

- `*returnSize = 组数;` —— 一共几组
- `*returnColumnSizes = cols;` —— `cols[g]` 是第 `g` 组有几个单词。`cols` 本身也要用 `malloc` 申请

```c
int* cols = (int*)malloc(sizeof(int) * groups);
...
*returnColumnSizes = cols;   // 注意是 *returnColumnSizes，修改调用者的变量
```

### 3. 字符串的复制与排序

- `strlen(s)`：字符串长度（不含 `'\0'`）。
- 想得到"排序后的单词"，**不能直接排 `strs[i]`**（那会改掉原单词，最后交出去的就不是原词了）。要先复制一份：

```c
char* key = (char*)malloc(len + 1);   // +1 是给结尾的 '\0' 留位置
strcpy(key, strs[i]);                 // 连同 '\0' 一起复制
```

- 排序字符可以用标准库的 `qsort`，要自己写一个比较函数：

```c
int cmpChar(const void* a, const void* b) {
    return *(const char*)a - *(const char*)b;   // 小的排前面
}
qsort(key, len, sizeof(char), cmpChar);        // 只排前 len 个，'\0' 不动
```

### 4. 比较两个字符串用 `strcmp`

`strcmp(a, b)` 返回 0 表示相等。**千万不能写 `a == b`**，那比较的是两个地址，而不是内容。

---

## 💡 第三步：思路一 —— 排序做标签 + 把相同标签排到一起

### 思路

最朴素的想法是"两两比较"：拿每个单词去和后面所有单词比是不是异位词。但 `n = 10^4` 时要比约 5000 万对，每对还要比较一串字母，太慢了。

更好的办法：

1. 给每个单词生成一个**标签 key = 字母排序后的字符串**。异位词的标签一定相同，不是异位词的标签一定不同。
2. 准备一个下标数组 `idx = [0, 1, 2, ..., n-1]`，**按标签排序**。排完后，标签相同的下标就**挨在一起**了。
3. 从头到尾扫一遍，把连续一段标签相同的单词装进同一组。

### 手动模拟（示例 1）

第 1 步，生成标签：

| 下标 | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 单词 | eat | tea | tan | ate | nat | bat |
| 标签 | aet | aet | ant | aet | ant | abt |

第 2 步，下标按标签排序（`abt < aet < ant`）：

| 排序后位置 | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 下标 idx | 5 | 0 | 1 | 3 | 2 | 4 |
| 标签 | abt | aet | aet | aet | ant | ant |

第 3 步，按连续相同标签切段：`[5]`、`[0,1,3]`、`[2,4]` → `[["bat"],["eat","tea","ate"],["tan","nat"]]`。

### 代码

```c
// 全局变量：qsort 的比较函数只能拿到两个元素的地址，要靠它访问每个下标对应的标签
static char** gKeys;

// 比较两个字符：给单词内部的字母排序用
static int cmpChar(const void* a, const void* b) {
    return *(const char*)a - *(const char*)b;
}

// 比较两个下标：按它们的标签（字典序）比较
static int cmpIdx(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b;
    return strcmp(gKeys[x], gKeys[y]);
}

char*** groupAnagrams(char** strs, int strsSize, int* returnSize, int** returnColumnSizes) {
    // 1. 为每个单词生成标签：复制一份，再把字母排序
    gKeys = (char**)malloc(sizeof(char*) * strsSize);
    for (int i = 0; i < strsSize; i++) {
        int len = strlen(strs[i]);
        gKeys[i] = (char*)malloc(len + 1);          // +1 给 '\0'
        strcpy(gKeys[i], strs[i]);                  // 不能直接改 strs[i]，答案要用原单词
        qsort(gKeys[i], len, sizeof(char), cmpChar);
    }

    // 2. 下标数组按标签排序，标签相同的下标会挨在一起
    int* idx = (int*)malloc(sizeof(int) * strsSize);
    for (int i = 0; i < strsSize; i++) idx[i] = i;
    qsort(idx, strsSize, sizeof(int), cmpIdx);

    // 3. 组数最多 strsSize 个，先按最大值申请
    char*** res = (char***)malloc(sizeof(char**) * strsSize);
    int* cols = (int*)malloc(sizeof(int) * strsSize);
    int groups = 0;

    int i = 0;
    while (i < strsSize) {
        // 找出 [i, j) 这一段：标签都和 idx[i] 的相同
        int j = i;
        while (j < strsSize && strcmp(gKeys[idx[j]], gKeys[idx[i]]) == 0) j++;

        res[groups] = (char**)malloc(sizeof(char*) * (j - i));   // 这一组有 j - i 个单词
        for (int p = i; p < j; p++) {
            res[groups][p - i] = strs[idx[p]];      // 直接存原单词的指针即可
        }
        cols[groups] = j - i;
        groups++;
        i = j;                                      // 跳到下一组的开头
    }

    // 4. 释放临时用的标签和下标数组
    for (int k = 0; k < strsSize; k++) free(gKeys[k]);
    free(gKeys);
    free(idx);

    *returnSize = groups;
    *returnColumnSizes = cols;
    return res;
}
```

### 复杂度分析

设单词个数为 n，最长单词长度为 k：

- **时间复杂度 O(n·k log k + n log n · k)**：每个单词内部排序 O(k log k)；下标排序要比较 O(n log n) 次，每次 `strcmp` 最多 O(k)。
- **空间复杂度 O(n·k)**：存所有标签。

---

## 🚀 第四步：思路二 —— 计数生成标签 + 哈希表（一遍扫描）

### 思路

思路一有两处可以优化：

1. **生成标签不必用 `qsort`**：单词只有小写字母，先数出每个字母出现几次（`c[0]` 个 a、`c[1]` 个 b……），再按 a→z 的顺序把字母"吐"出来，就直接得到排好序的字符串了。这叫**计数排序**，只要 O(k + 26)。
2. **分组不必排序**：用一个**哈希表**记录"标签 → 组号"。每来一个单词，查一下它的标签：
   - 查到了 → 放进那一组；
   - 没查到 → 新开一组，把"标签 → 新组号"存进哈希表。

哈希表的原理和第 1 题一样：用一个公式把字符串变成格子编号；格子被别的标签占了，就看下一个格子（线性探测）。字符串的哈希公式常用 `h = h * 33 + 字符`（叫 djb2）。

由于要先知道每组有几个单词才能 `malloc`，我们分两遍：第一遍算出每个单词的组号 `groupOf[i]` 并统计每组人数 `cnt[g]`；第二遍再把单词装进去。

### 手动模拟（示例 1）

| i | 单词 | 计数后的标签 | 哈希表里有吗？ | 组号 | 各组人数 cnt |
|---|---|---|---|---|---|
| 0 | eat | aet | 没有，新开第 0 组 | 0 | [1] |
| 1 | tea | aet | 有，是第 0 组 | 0 | [2] |
| 2 | tan | ant | 没有，新开第 1 组 | 1 | [2,1] |
| 3 | ate | aet | 有，是第 0 组 | 0 | [3,1] |
| 4 | nat | ant | 有，是第 1 组 | 1 | [3,2] |
| 5 | bat | abt | 没有，新开第 2 组 | 2 | [3,2,1] |

第二遍：第 0 组装 `eat, tea, ate`，第 1 组装 `tan, nat`，第 2 组装 `bat`。

### 代码

```c
#define HASH_SIZE 32768   // 格子数：2 的幂，且比单词数（最多 10^4）的两倍还大

// djb2 字符串哈希：把字符串变成一个整数
static unsigned int hashStr(const char* s) {
    unsigned int h = 5381;
    while (*s) h = h * 33 + (unsigned char)*s++;
    return h;
}

char*** groupAnagrams(char** strs, int strsSize, int* returnSize, int** returnColumnSizes) {
    static int table[HASH_SIZE];                     // 格子里存组号，-1 表示空格子
    for (int i = 0; i < HASH_SIZE; i++) table[i] = -1;

    char** keys = (char**)malloc(sizeof(char*) * strsSize);   // keys[g]：第 g 组的标签
    int* groupOf = (int*)malloc(sizeof(int) * strsSize);      // groupOf[i]：第 i 个单词在哪组
    int* cnt = (int*)calloc(strsSize, sizeof(int));           // cnt[g]：第 g 组有几个单词（calloc 会清零）
    int groups = 0;

    // ===== 第一遍：算出每个单词的组号 =====
    for (int i = 0; i < strsSize; i++) {
        // 1. 计数排序生成标签
        int len = strlen(strs[i]);
        int c[26] = {0};
        for (int j = 0; j < len; j++) c[strs[i][j] - 'a']++;   // 'a' 对应 0，'b' 对应 1，依此类推
        char* key = (char*)malloc(len + 1);
        int p = 0;
        for (int ch = 0; ch < 26; ch++) {
            for (int t = 0; t < c[ch]; t++) key[p++] = (char)('a' + ch);   // 按 a~z 依次写出
        }
        key[p] = '\0';

        // 2. 在哈希表里找这个标签：格子非空且标签不同，就看下一个格子
        unsigned int h = hashStr(key) & (HASH_SIZE - 1);
        while (table[h] != -1 && strcmp(keys[table[h]], key) != 0) {
            h = (h + 1) & (HASH_SIZE - 1);
        }
        if (table[h] == -1) {          // 3a. 没找到：新开一组
            table[h] = groups;
            keys[groups] = key;
            groups++;
        } else {                       // 3b. 找到了：标签已经存过，这份可以释放
            free(key);
        }
        groupOf[i] = table[h];
        cnt[groupOf[i]]++;
    }

    // ===== 第二遍：按组装单词 =====
    char*** res = (char***)malloc(sizeof(char**) * groups);
    int* cols = (int*)malloc(sizeof(int) * groups);
    for (int g = 0; g < groups; g++) {
        res[g] = (char**)malloc(sizeof(char*) * cnt[g]);
        cols[g] = 0;                   // 先当作"已经装了几个"的计数器用
    }
    for (int i = 0; i < strsSize; i++) {
        int g = groupOf[i];
        res[g][cols[g]] = strs[i];
        cols[g]++;                     // 装完后 cols[g] 正好等于 cnt[g]
    }

    for (int g = 0; g < groups; g++) free(keys[g]);
    free(keys);
    free(groupOf);
    free(cnt);

    *returnSize = groups;
    *returnColumnSizes = cols;
    return res;
}
```

**代码中几个可能看不懂的地方：**

- `strs[i][j] - 'a'`：字母减去 `'a'` 就得到 0~25 的编号，可以直接当数组下标。
- `& (HASH_SIZE - 1)`：`HASH_SIZE` 是 2 的幂时，等价于 `% HASH_SIZE`，而且结果一定非负。
- `static int table[...]`：放在静态区，不占栈空间；但每次调用都要重新填 -1，否则会留着上一次的数据。

### 复杂度分析

- **时间复杂度 O(n·k)**：每个单词计数 O(k)，哈希查找平均 O(1) 次 `strcmp`（每次 O(k)）。
- **空间复杂度 O(n·k)**：存每组的标签。

---

## ⚠️ 第五步：小白常见错误

1. **直接对 `strs[i]` 排序** → `qsort(strs[i], ...)` 会把原单词改掉，最后交出去的变成 `"aet"` 而不是 `"eat"`。一定要先复制。
2. **复制字符串时 `malloc(len)` 少了 1** → 没有给 `'\0'` 留位置，`strcpy` 写越界，结果随机出错。
3. **用 `==` 比较字符串** → `if (keyA == keyB)` 比的是地址，内容一样也会判成不同。要用 `strcmp(keyA, keyB) == 0`。
4. **忘了设置 `*returnColumnSizes`** → 调用者不知道每组有几个单词，输出为空或崩溃。
5. **把空字符串丢掉** → `[""]` 的答案是 `[[""]]`；长度为 0 的单词也必须参与分组。
6. **只比较"字母种类"不比较个数**（比如用 26 位的位掩码当标签）→ `ab` 和 `aab` 会被错误地分到一组。
7. **`static` 哈希表没有每次清空** → 判题时每个测试点是独立进程，看似没问题；但在力扣上同一进程会多次调用，残留数据会导致错误。养成每次初始化的习惯。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 两两比较 | O(n²·k) | O(n·k) | ⭐ | n = 10^4 时太慢 |
| 排序标签 + 排序分组 | O(n·k log k + n log n·k) | O(n·k) | ⭐⭐ | 不用写哈希表，好理解 |
| 计数标签 + 哈希表 | O(n·k) | O(n·k) | ⭐⭐⭐ | 最优，面试常考 |

> 🎯 **学习建议**："先算一个标签，再按标签归类"是一个非常通用的套路，先把思路一写对，再挑战哈希表版本。

---

## 🔗 举一反三

- **242. 有效的字母异位词**：只判断两个单词是不是异位词，就是本题"标签"的那一步。
- **438. 找到字符串中所有字母异位词**：用"字母计数"+ 滑动窗口在长字符串里找异位词。
- **1. 两数之和**：同样用哈希表把"查找"从 O(n) 降到 O(1)。
- **思考题**：如果单词里可以出现任意 ASCII 字符（不只是小写字母），计数标签要怎么改？
