# 49. 字母异位词分组 —— 小白详细题解

> 这道题的关键是给每个单词找一个"**身份证**"：互为异位词的单词，身份证一模一样。之后就是"按身份证分组"。C 语言的难点在于返回值是三颗星的 `char***`，我们会一层一层拆开讲。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 有一堆单词。如果两个单词**用的字母和每个字母的个数完全一样**（只是顺序不同），它们就是一伙的。请把每一伙分成一组。

拿示例 1 `["eat","tea","tan","ate","nat","bat"]` 来说：

| 单词 | 字母排序后 | 属于哪组 |
|---|---|---|
| eat | aet | 第 1 组 |
| tea | aet | 第 1 组 |
| tan | ant | 第 2 组 |
| ate | aet | 第 1 组 |
| nat | ant | 第 2 组 |
| bat | abt | 第 3 组 |

分组结果：`["eat","tea","ate"]`、`["tan","nat"]`、`["bat"]`。

**几个需要注意的细节：**

1. **字母个数也要一样**：`"aab"` 和 `"abb"` 用的字母都是 a、b，但个数不同，**不是**异位词。
2. **空字符串 `""` 也是一个单词**，所有空串互为异位词，分在同一组。
3. **相同的单词**（比如出现两次 `"abc"`）也要放进同一组，两次都要保留。
4. 组的顺序、组内的顺序都随意（本 OJ 会排好序再比较）。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 拆解 `char***`

```c
char*** groupAnagrams(char** strs, int strsSize, int* returnSize, int** returnColumnSizes)
```

| 类型 | 含义 | 例子 |
|---|---|---|
| `char*` | 一个字符串 | `"eat"` |
| `char**` | 一组字符串（字符串数组） | `["eat","tea","ate"]` |
| `char***` | 很多组（字符串数组的数组） | `[["eat","tea","ate"],["tan","nat"],["bat"]]` |

所以要这样申请：

```c
char*** res = (char***)malloc(sizeof(char**) * 组数);   // 每个元素是一组（char**）
res[g] = (char**)malloc(sizeof(char*) * 这一组的个数);    // 每组里放若干个字符串指针（char*）
res[g][j] = strs[i];                                    // 直接存原字符串的指针，不用复制内容
```

`*returnSize` 写组数，`*returnColumnSizes` 写"每组有几个字符串"的数组——和"合并区间"返回二维 `int` 数组是一样的套路。

### 2. 给字符串里的字母排序：计数排序

只有 26 个小写字母，与其用 `qsort`，不如**数一数每个字母出现几次**，再按 a~z 的顺序写出来：

```c
int cnt[26] = {0};
for (int i = 0; s[i]; i++) cnt[s[i] - 'a']++;     // 'a' → 0, 'b' → 1, ...
// 再按 a, b, c ... 的顺序，每个字母写 cnt[c] 次
```

`s[i] - 'a'` 把字母变成 0~25 的下标，这是字母题最常用的写法。

### 3. 复制出新字符串要多留 1 个字节给 `'\0'`

```c
char* key = (char*)malloc(len + 1);   // len 个字母 + 1 个 '\0'
key[len] = '\0';                      // 别忘了结尾
```

### 4. 比较字符串用 `strcmp`，不能用 `==`

`key1 == key2` 比较的是两个**地址**是否相同，内容一样但地址不同时结果是假。比较内容要用 `strcmp(key1, key2) == 0`。

---

## 💡 第三步：思路一 —— 标签排序后分组

### 思路

1. 给每个单词算出它的**标签**（把字母排序后的字符串），比如 `"tea"` → `"aet"`。
2. 把单词的下标按**标签的字典序**排序。排完后，标签相同的单词就**挨在一起**了。
3. 从头扫一遍，标签和前一个不同就开启新的一组。

### 手动模拟（示例 1）

| 步骤 | 内容 |
|---|---|
| 算标签 | eat→aet, tea→aet, tan→ant, ate→aet, nat→ant, bat→abt |
| 按标签排序 | bat(abt), eat(aet), tea(aet), ate(aet), tan(ant), nat(ant) |
| 分组 | [bat] \| [eat, tea, ate] \| [tan, nat] |

### 代码

```c
static char** gKeys;   // 给 qsort 的比较函数用：gKeys[i] 是第 i 个单词的标签

// 计数排序：返回 s 的字母排好序后的新字符串（malloc 得到）
char* makeKey(const char* s) {
    int cnt[26] = {0};
    int len = 0;
    for (; s[len] != '\0'; len++) cnt[s[len] - 'a']++;   // 数每个字母出现几次
    char* key = (char*)malloc(len + 1);
    int p = 0;
    for (int c = 0; c < 26; c++) {
        for (int t = 0; t < cnt[c]; t++) key[p++] = (char)('a' + c);
    }
    key[p] = '\0';
    return key;
}

// 比较两个下标：按它们的标签的字典序
int cmpByKey(const void* a, const void* b) {
    int i = *(const int*)a, j = *(const int*)b;
    return strcmp(gKeys[i], gKeys[j]);
}

char*** groupAnagrams(char** strs, int strsSize, int* returnSize, int** returnColumnSizes) {
    int n = strsSize;
    // 1. 每个单词算标签；idx 是下标数组，待会儿排序它
    gKeys = (char**)malloc(sizeof(char*) * n);
    int* idx = (int*)malloc(sizeof(int) * n);
    for (int i = 0; i < n; i++) {
        gKeys[i] = makeKey(strs[i]);
        idx[i] = i;
    }

    // 2. 按标签排序下标，标签相同的单词会挨在一起
    qsort(idx, n, sizeof(int), cmpByKey);

    // 3. 最多 n 组，先按最大可能申请
    char*** res = (char***)malloc(sizeof(char**) * n);
    int* cols = (int*)malloc(sizeof(int) * n);
    int groups = 0;

    // 4. 扫描：每一段标签相同的连续区间 [i, j) 就是一组
    int i = 0;
    while (i < n) {
        int j = i;
        while (j < n && strcmp(gKeys[idx[j]], gKeys[idx[i]]) == 0) j++;
        res[groups] = (char**)malloc(sizeof(char*) * (j - i));
        for (int t = i; t < j; t++) {
            res[groups][t - i] = strs[idx[t]];   // 直接放原字符串的指针
        }
        cols[groups] = j - i;
        groups++;
        i = j;
    }

    // 5. 释放临时的标签
    for (int t = 0; t < n; t++) free(gKeys[t]);
    free(gKeys);
    free(idx);

    *returnSize = groups;
    *returnColumnSizes = cols;
    return res;
}
```

> 💬 **为什么要用全局变量 `gKeys`？** `qsort` 的比较函数只能拿到两个元素的地址，没有办法额外传参数。我们排序的是下标，比较时需要查标签，只好把标签数组放在全局变量里。

### 复杂度分析

设单词个数为 n，单词最长为 L：

- **时间复杂度 O(n·L + n log n · L)**：算标签 O(n·L)；排序要比较 O(n log n) 次，每次 `strcmp` 最多 O(L)。
- **空间复杂度 O(n·L)**：存所有标签。

---

## 🚀 第四步：思路二 —— 哈希表直接分组

### 思路

思路一花了 O(n log n) 次比较去排序，其实我们**并不需要组和组之间有顺序**，只需要"标签相同的放一起"。

用一个哈希表：**标签 → 组号**。

1. 对每个单词算标签。
2. 在哈希表里查这个标签：
   - 查到了：这个单词属于那一组。
   - 没查到：新开一组，把"标签 → 新组号"存进哈希表。
3. 第一遍只记录每个单词属于哪组（`gid[i]`）和每组有几个（`sizes[g]`）；第二遍按组号把字符串放进去。

为什么要扫两遍？因为 C 语言的数组要先知道大小才能 `malloc`。第一遍数清楚每组几个，第二遍就能一次性申请好。

### 哈希函数

字符串的哈希可以用经典的 **FNV-1a**：从一个初始值出发，每个字符先异或进来、再乘一个大质数。不用深究，当成固定写法：

```c
unsigned int h = 2166136261u;
for (; *s; s++) h = (h ^ (unsigned char)*s) * 16777619u;
```

### 手动模拟（示例 1）

| 单词 | 标签 | 哈希表里有吗？ | 组号 gid | 每组个数 sizes |
|---|---|---|---|---|
| eat | aet | 没有 → 新开第 0 组 | 0 | [1] |
| tea | aet | 有，第 0 组 | 0 | [2] |
| tan | ant | 没有 → 新开第 1 组 | 1 | [2, 1] |
| ate | aet | 有，第 0 组 | 0 | [3, 1] |
| nat | ant | 有，第 1 组 | 1 | [3, 2] |
| bat | abt | 没有 → 新开第 2 组 | 2 | [3, 2, 1] |

### 代码

```c
#define HASH_SIZE (1 << 15)    // 32768 个格子，比最多 10^4 个不同标签大得多

// 计数排序得到标签（malloc 得到的新字符串）
char* makeKey(const char* s) {
    int cnt[26] = {0};
    int len = 0;
    for (; s[len] != '\0'; len++) cnt[s[len] - 'a']++;
    char* key = (char*)malloc(len + 1);
    int p = 0;
    for (int c = 0; c < 26; c++) {
        for (int t = 0; t < cnt[c]; t++) key[p++] = (char)('a' + c);
    }
    key[p] = '\0';
    return key;
}

// FNV-1a 字符串哈希，结果落在 0 ~ HASH_SIZE-1
unsigned int hashStr(const char* s) {
    unsigned int h = 2166136261u;
    for (; *s; s++) h = (h ^ (unsigned char)*s) * 16777619u;
    return h & (HASH_SIZE - 1);
}

char*** groupAnagrams(char** strs, int strsSize, int* returnSize, int** returnColumnSizes) {
    int n = strsSize;
    static int table[HASH_SIZE];          // table[h]：这个格子里存的组号，-1 表示空
    for (int h = 0; h < HASH_SIZE; h++) table[h] = -1;

    char** keys = (char**)malloc(sizeof(char*) * n);   // 每个单词的标签
    int* gid = (int*)malloc(sizeof(int) * n);          // 每个单词属于哪一组
    int* firstOf = (int*)malloc(sizeof(int) * n);      // 每组第一个单词的下标（用来取这组的标签）
    int* sizes = (int*)calloc(n, sizeof(int));         // 每组有几个单词
    int groups = 0;

    // 1. 第一遍：确定每个单词的组号
    for (int i = 0; i < n; i++) {
        keys[i] = makeKey(strs[i]);
        unsigned int h = hashStr(keys[i]);
        // 线性探测：格子被"别的标签"占了就看下一个
        while (table[h] != -1 && strcmp(keys[firstOf[table[h]]], keys[i]) != 0) {
            h = (h + 1) & (HASH_SIZE - 1);
        }
        if (table[h] == -1) {             // 新标签：开一个新组
            table[h] = groups;
            firstOf[groups] = i;
            groups++;
        }
        gid[i] = table[h];
        sizes[gid[i]]++;
    }

    // 2. 按每组的大小申请空间
    char*** res = (char***)malloc(sizeof(char**) * groups);
    int* cols = (int*)malloc(sizeof(int) * groups);
    for (int g = 0; g < groups; g++) {
        res[g] = (char**)malloc(sizeof(char*) * sizes[g]);
        cols[g] = 0;                      // 先当"已放入的个数"用，放完正好等于 sizes[g]
    }

    // 3. 第二遍：把每个单词放进它的组
    for (int i = 0; i < n; i++) {
        int g = gid[i];
        res[g][cols[g]] = strs[i];
        cols[g]++;
    }

    // 4. 释放临时数组
    for (int i = 0; i < n; i++) free(keys[i]);
    free(keys);
    free(gid);
    free(firstOf);
    free(sizes);

    *returnSize = groups;
    *returnColumnSizes = cols;
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n·L)**：每个单词算标签 O(L)，哈希和比较平均 O(L)。
- **空间复杂度 O(n·L)**：存所有标签。

---

## ⚠️ 第五步：小白常见错误

1. **标签只记"用了哪些字母"，不记个数** → `"aab"` 和 `"abb"` 被错误地分到一组。
2. **用 `==` 比较两个标签** → 比的是地址，内容相同也会判成不同，每个单词都自成一组。要用 `strcmp(...) == 0`。
3. **`malloc(len)` 忘了 +1** → 没地方放 `'\0'`，`strcmp` 会一直读到别的内存里，结果随机甚至崩溃。
4. **标签直接在原字符串上排序**（原地修改 `strs[i]`）→ 返回的组里放的是 `strs[i]`，单词本身被改成了 `"aet"`，输出就错了。要复制一份再排序。
5. **`sizeof(char**)` 和 `sizeof(char*)` 搞混** → 在 64 位系统上两者恰好都是 8 字节，碰巧不出错；但类型意义不同，养成按"元素类型"写 `sizeof` 的习惯：`res` 的元素是 `char**`，`res[g]` 的元素是 `char*`。
6. **空字符串 `""` 没处理好** → 计数循环一次都不执行，标签也是 `""`，`malloc(0 + 1)` 放一个 `'\0'`。按上面的写法自然正确，不需要特判；但如果写成 `s[0] - 'a'` 之类的"先取第一个字母"就会出错。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 标签排序后分组 | O(n log n · L) | O(n·L) | ⭐⭐ | 不需要写哈希表，好理解 |
| 哈希表按标签分组 | O(n·L) | O(n·L) | ⭐⭐⭐ | 标准答案 |

> 💬 标签也可以不排序，直接用"26 个字母各出现几次"组成，比如 `"a1b0c2..."`。效果一样，单词很长时还更快。

---

## 🔗 举一反三

- **242. 有效的字母异位词**：判断两个单词是不是异位词——本题的基础。
- **438. 找到字符串中所有字母异位词**：滑动窗口 + 字母计数。
- **290. 单词规律**：同样是"给每个东西找身份证，再按身份证配对"。
- **思考题**：如果字符串里不止小写字母，还可能有大写、数字、中文，标签的做法要怎么改？
