# 208. 实现 Trie (前缀树) —— 小白详细题解

> 这是一道「设计类」题：不是写一个函数，而是用结构体 + 一组函数模拟一个「类」。前缀树（字典树）是处理「一堆单词 + 前缀查询」的标准数据结构。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 做一个「单词本」，支持三件事：
> 1. `insert(word)`：往本子里记一个单词；
> 2. `search(word)`：问这个单词**完整地**记过没有；
> 3. `startsWith(prefix)`：问有没有哪个记过的单词**以它开头**。

拿示例 1 走一遍：

| 步骤 | 操作 | 单词本里的内容 | 返回 | 原因 |
|---|---|---|---|---|
| 1 | `Trie()` | 空 | null | 创建对象，没有返回值 |
| 2 | `insert("apple")` | apple | null | 没有返回值 |
| 3 | `search("apple")` | apple | true | 完整记过 |
| 4 | `search("app")` | apple | **false** | 只记过 apple，没记过 app 这个完整单词 |
| 5 | `startsWith("app")` | apple | true | apple 以 app 开头 |
| 6 | `insert("app")` | apple, app | null | |
| 7 | `search("app")` | apple, app | true | 现在完整记过了 |

**几个需要注意的细节：**

1. `search` 和 `startsWith` 的区别就在第 4 步：**前缀存在 ≠ 单词存在**。
2. 一个单词本身也是它自己的前缀：插入 `"abc"` 后 `startsWith("abc")` 是 `true`。
3. 同一个单词可能被插入多次，不能因此出错。
4. 单词只含小写字母 `a`~`z`，长度最多 2000，操作最多 3 万次。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 用「结构体 + 函数」模拟类

C 语言没有 `class`。力扣的约定是：

| 其他语言 | C 语言写法 |
|---|---|
| `Trie trie = new Trie();` | `Trie* obj = trieCreate();` |
| `trie.insert("apple");` | `trieInsert(obj, "apple");` |
| `trie.search("app");` | `trieSearch(obj, "app");` |
| 对象被回收 | `trieFree(obj);` |

结构体里放什么成员完全由你决定，模板里的 `int unused;` 只是占位，要换掉。

### 2. 结构体里放「指向自己类型」的指针

树的结点需要指向孩子结点，孩子也是同一种结构体。但模板写的是**匿名**结构体：

```c
typedef struct {
    Trie* children[26];   // ❌ 编译错误：此时 Trie 这个名字还没定义完
} Trie;
```

解决办法是给结构体起个「标签名」，在内部用 `struct Trie*`：

```c
typedef struct Trie {          // 这里的 Trie 是结构体标签
    struct Trie* children[26]; // 用 struct Trie* 指向孩子
    bool isEnd;
} Trie;                        // 这里的 Trie 是 typedef 出来的类型名
```

### 3. `calloc`：申请并清零

`calloc(1, sizeof(Trie))` 和 `malloc(sizeof(Trie))` 一样申请一块内存，但它会**把内容全部清零**——所有孩子指针都是 `NULL`、`isEnd` 是 `false`，正好是一个「空结点」。用 `malloc` 的话里面是随机垃圾值，必须手动初始化。

### 4. 字符转下标

`'a'`~`'z'` 的 ASCII 码是连续的，所以 `c - 'a'` 正好是 `0`~`25`，可以直接当数组下标。

---

## 💡 第三步：思路一 —— 把单词存进数组，逐个比较（最朴素）

### 思路

- `insert`：把单词复制一份存进一个大数组（已经存过就不再存）。
- `search`：把数组里每个单词和 `word` 用 `strcmp` 比较，相等就是 `true`。
- `startsWith`：用 `strncmp(单词, prefix, prefix长度)` 比较前 `len` 个字符。

### 手动模拟（示例 1 的第 3~5 步，数组里只有 `"apple"`）

| 操作 | 比较 | 结果 |
|---|---|---|
| `search("apple")` | `strcmp("apple", "apple") == 0` | true |
| `search("app")` | `strcmp("apple", "app") != 0` | false |
| `startsWith("app")` | `strncmp("apple", "app", 3) == 0` | true |

### 代码

```c
#define MAXW 30000                    // 最多 3 万次操作，最多存 3 万个单词

typedef struct {
    char* words[MAXW];                // 存每个单词（malloc 出来的副本）
    int count;                        // 已经存了几个
} Trie;

Trie* trieCreate() {
    Trie* obj = (Trie*)malloc(sizeof(Trie));
    obj->count = 0;
    return obj;
}

bool trieSearch(Trie* obj, char* word) {
    for (int i = 0; i < obj->count; i++) {
        if (strcmp(obj->words[i], word) == 0) return true;   // 完全相同
    }
    return false;
}

void trieInsert(Trie* obj, char* word) {
    if (trieSearch(obj, word)) return;                    // 已经存过，不重复存
    // word 指向的内存属于调用者，必须复制一份自己保存
    char* copy = (char*)malloc(strlen(word) + 1);         // +1 给 '\0'
    strcpy(copy, word);
    obj->words[obj->count++] = copy;
}

bool trieStartsWith(Trie* obj, char* prefix) {
    int len = strlen(prefix);
    for (int i = 0; i < obj->count; i++) {
        // 只比较前 len 个字符；单词比 prefix 短时会在 '\0' 处不相等，自然返回非 0
        if (strncmp(obj->words[i], prefix, len) == 0) return true;
    }
    return false;
}

void trieFree(Trie* obj) {
    for (int i = 0; i < obj->count; i++) free(obj->words[i]);   // 先释放每个单词
    free(obj);                                                  // 再释放结构体本身
}
```

### 复杂度分析

- **时间复杂度**：`insert` / `search` / `startsWith` 每次都要扫一遍所有单词，最坏 O(N·L)（N 是单词数，L 是单词长度）。3 万次操作时最坏约 10⁸~10⁹ 次字符比较，**数据大时可能超时**。
- **空间复杂度 O(N·L)**：存下所有单词。

> 💬 这个方法慢在哪？查 `"apple"` 时，`"banana"`、`"cat"` 这些首字母都对不上的单词也要一个个比较。如果能「按首字母分组，组里再按第二个字母分组……」，就能直接跳过不相关的单词——这就是前缀树。

---

## 🚀 第四步：思路二 —— 前缀树（标准解法）

### 思路

把每个单词一个字母一个字母地「挂」在树上：

- 每个结点有 26 个孩子指针 `children[0..25]`，分别对应 `'a'`~`'z'`；
- 从根出发，沿着单词的字母一路往下走，每个字母走一条边；
- 结点上有个标记 `isEnd`：**有单词在这里结束**时为 `true`。

插入 `"apple"` 和 `"app"` 后，树长这样（`*` 表示 `isEnd = true`）：

```
(根)
 └─ a
     └─ p
         └─ p*        ← "app" 在这里结束
             └─ l
                 └─ e*    ← "apple" 在这里结束
```

三个操作：

| 操作 | 做法 |
|---|---|
| `insert(word)` | 沿字母往下走，孩子不存在就新建一个结点；走完把最后的结点 `isEnd = true` |
| `search(word)` | 沿字母往下走，中途孩子不存在就 `false`；走完还要看 `isEnd` |
| `startsWith(prefix)` | 沿字母往下走，中途孩子不存在就 `false`；**能走完就是 `true`** |

`search` 和 `startsWith` 的走法完全一样，可以共用一个「沿着字符串往下走」的辅助函数，只是最后判断不同。

### 手动模拟（示例 1）

| 操作 | 走过的路径 | 走到的结点 | 判断 | 返回 |
|---|---|---|---|---|
| `insert("apple")` | 根→a→p→p→l→e（全部新建） | e | 设 `isEnd = true` | null |
| `search("apple")` | 根→a→p→p→l→e | e | `isEnd` 为真 | true |
| `search("app")` | 根→a→p→p | 第二个 p | `isEnd` 为**假** | false |
| `startsWith("app")` | 根→a→p→p | 第二个 p | 走完了 | true |
| `insert("app")` | 根→a→p→p（都已存在） | 第二个 p | 设 `isEnd = true` | null |
| `search("app")` | 根→a→p→p | 第二个 p | `isEnd` 为真 | true |

### 代码

```c
typedef struct Trie {
    struct Trie* children[26];   // children[c] 是字母 'a'+c 对应的孩子，NULL 表示没有
    bool isEnd;                  // 是否有单词在这个结点结束
} Trie;

Trie* trieCreate() {
    // calloc 会把内存清零：26 个孩子都是 NULL，isEnd 是 false
    return (Trie*)calloc(1, sizeof(Trie));
}

void trieInsert(Trie* obj, char* word) {
    Trie* node = obj;                          // 从根出发
    for (int i = 0; word[i] != '\0'; i++) {
        int c = word[i] - 'a';                 // 'a'->0, 'b'->1, 'z'->25
        if (node->children[c] == NULL) {       // 这条路还没有，新建一个结点
            node->children[c] = trieCreate();
        }
        node = node->children[c];              // 往下走一步
    }
    node->isEnd = true;                        // 标记：有单词在这里结束
}

// 辅助函数：沿着字符串 s 往下走，返回最后到达的结点；中途走不通返回 NULL
static Trie* walk(Trie* node, char* s) {
    for (int i = 0; s[i] != '\0'; i++) {
        node = node->children[s[i] - 'a'];
        if (node == NULL) return NULL;         // 没有这条路
    }
    return node;
}

bool trieSearch(Trie* obj, char* word) {
    Trie* node = walk(obj, word);
    return node != NULL && node->isEnd;        // 能走完，并且有单词恰好在这里结束
}

bool trieStartsWith(Trie* obj, char* prefix) {
    return walk(obj, prefix) != NULL;          // 能走完就说明有单词以它开头
}

void trieFree(Trie* obj) {
    if (obj == NULL) return;
    for (int i = 0; i < 26; i++) {
        trieFree(obj->children[i]);            // 先递归释放所有孩子
    }
    free(obj);                                 // 再释放自己
}
```

**代码中几个可能看不懂的地方：**

- `walk` 前面的 `static`：表示这个函数只在本文件内使用，避免和判题程序里的函数重名。
- `trieFree` 必须**先释放孩子再释放自己**：如果先 `free(obj)`，再访问 `obj->children` 就是在读已经还给系统的内存。
- 根结点不对应任何字母，它只是所有单词的共同起点。

### 复杂度分析

- **时间复杂度**：每个操作都是 **O(L)**，L 是单词 / 前缀的长度，和已经存了多少单词**无关**。
- **空间复杂度 O(总字母数 × 26)**：最坏每个字母都新建一个结点，每个结点有 26 个指针。

> 这又是一次「用空间换时间」：每个结点 26 个指针很浪费内存，但换来了和单词数量无关的查询速度。

---

## ⚠️ 第五步：小白常见错误

1. **`search` 忘了检查 `isEnd`**：插入 `"apple"` 后 `search("app")` 会错误地返回 `true`（示例 1 第 4 步）。
2. **用 `malloc` 新建结点却不初始化**：`children` 里是随机值，`if (node->children[c] == NULL)` 判断失效，访问野指针直接崩溃。用 `calloc`，或者 `malloc` 后用循环把 26 个指针都设为 `NULL`、`isEnd = false`。
3. **匿名结构体里写 `Trie* children[26]`**：编译报错 `unknown type name 'Trie'`，要写成 `typedef struct Trie { struct Trie* children[26]; ... } Trie;`。
4. **思路一里直接保存 `word` 指针**：`obj->words[i] = word;` 只是记住了调用者那块内存的地址，内容以后可能被改掉或释放。必须 `malloc` + `strcpy` 复制一份。
5. **`trieFree` 只 `free(obj)`**：只释放了根结点，其余结点全部内存泄漏。
6. **字符没减 `'a'`**：`node->children[word[i]]` 下标是 97~122，数组只有 26 个，越界。

---

## 📊 第六步：两种方法对比

| 方法 | insert | search / startsWith | 空间 | 难度 | 建议 |
|---|---|---|---|---|---|
| 数组 + 逐个比较 | O(N·L) | O(N·L) | O(N·L) | ⭐ | 理解题意用，大数据会慢 |
| 前缀树 | O(L) | O(L) | O(N·L·26) | ⭐⭐ | 标准答案，一定要掌握 |

> 🎯 **学习建议**：把思路二的 `insert` / `walk` 默写熟练，它几乎是所有字典树题目的固定模板。

---

## 🔗 举一反三

- **211. 添加与搜索单词**：查询里可以有 `.` 通配任意字母，遇到 `.` 时要把 26 个孩子都递归试一遍。
- **212. 单词搜索 II**：把所有单词建成前缀树，再在网格里 DFS（结合 79 题）。
- **648. 单词替换**：用前缀树找每个单词的最短词根。
- **思考题**：如果还要支持 `countWordsStartingWith(prefix)`（以某前缀开头的单词有几个），结点里应该多存一个什么字段？
