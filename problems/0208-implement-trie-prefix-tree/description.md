**[Trie](https://baike.baidu.com/item/字典树/9825209)**（发音类似 "try"）或者说 **前缀树** 是一种树形数据结构，用于高效地存储和检索字符串数据集中的键。这一数据结构有相当多的应用情景，例如自动补全和拼写检查。

请你实现 Trie 类：

- `Trie()` 初始化前缀树对象。
- `void insert(String word)` 向前缀树中插入字符串 `word` 。
- `boolean search(String word)` 如果字符串 `word` 在前缀树中，返回 `true`（即，在检索之前已经插入）；否则，返回 `false` 。
- `boolean startsWith(String prefix)` 如果之前已经插入的字符串 `word` 的前缀之一为 `prefix` ，返回 `true` ；否则，返回 `false` 。

### 示例 1

```
输入
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
输出
[null, null, true, false, true, null, true]

解释
Trie trie = new Trie();
trie.insert("apple");
trie.search("apple");   // 返回 True
trie.search("app");     // 返回 False
trie.startsWith("app"); // 返回 True
trie.insert("app");
trie.search("app");     // 返回 True
```

### 提示

- `1 <= word.length, prefix.length <= 2000`
- `word` 和 `prefix` 仅由小写英文字母组成
- `insert`、`search` 和 `startsWith` 调用次数 **总计** 不超过 `3 * 10^4` 次

### 函数说明

```c
typedef struct {
    // 自己设计结构体的成员
} Trie;

Trie* trieCreate();
void trieInsert(Trie* obj, char* word);
bool trieSearch(Trie* obj, char* word);
bool trieStartsWith(Trie* obj, char* prefix);
void trieFree(Trie* obj);
```

- `trieCreate`：创建并返回一个空的前缀树（用 `malloc` 申请）
- `trieInsert` / `trieSearch` / `trieStartsWith`：对应题目中的三个操作，`obj` 是 `trieCreate` 返回的指针
- `trieFree`：释放整棵前缀树占用的全部内存，所有操作结束后会被调用一次
- C 语言里「类」用结构体 + 一组函数来模拟，判题程序按输入的操作序列依次调用这些函数

### 自定义输入格式

```
["Trie","insert","search","search","startsWith","insert","search"]
[[],["apple"],["apple"],["app"],["app"],["app"],["app"]]
```

第 1 行是操作名数组，第 2 行是每个操作的参数（`Trie` 没有参数，写 `[]`）。输出每个操作的返回值，没有返回值的输出 `null`。
