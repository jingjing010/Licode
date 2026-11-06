# 79. 单词搜索 —— 小白详细题解

> 这是「网格上的回溯」入门题：走一步、试一试、不行就退回来。重点是**做标记**和**撤销标记**。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 在一个字母方格里，从某个格子出发，每次只能往**上下左右**走一格，**每个格子最多用一次**。问：能不能按顺序走出单词 `word`？

拿示例 1 的网格来说：

| 行\列 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| 0 | **A**① | **B**② | **C**③ | E |
| 1 | S | F | **C**④ | S |
| 2 | A | **D**⑥ | **E**⑤ | E |

找 `"ABCCED"`：A(0,0) → B(0,1) → C(0,2) → C(1,2) → E(2,2) → D(2,1)，找到了，返回 `true`。

示例 3 找 `"ABCB"`：A → B → C 之后，下一个 B 只能是 (0,1)，但它已经用过了，所以返回 `false`。

**几个需要注意的细节：**

1. 起点可以是任何格子。
2. **同一个格子不能用两次**——这是本题最容易错的地方。
3. 大小写不同算不同字母，`'a' != 'A'`。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 字符串以 `'\0'` 结尾

`word` 是 `char*`，结尾有一个看不见的 `'\0'`。所以 `word[k] == '\0'` 表示**已经匹配完整个单词**，不需要额外传长度。

### 2. 回溯 = 递归 + 撤销

```c
char t = board[r][c];
board[r][c] = '#';     // 做标记：这一格正在使用
// 递归去试下一步
board[r][c] = t;       // 撤销标记：退回来以后，这一格可以被别的路线使用
```

为什么要撤销？因为从**别的起点**或**别的方向**过来时，这一格是可以再用的。只有「当前这条路线」上不能重复。

### 3. `bool` 和短路 `||`

`a || b || c || d`：只要前面某一个为 `true`，后面的就不会执行。用在这里正好是「某个方向找到了就不用再试别的方向」。

---

## 💡 第三步：思路一 —— 回溯（DFS）

### 思路

定义 `dfs(r, c, k)`：**从格子 (r, c) 开始，能不能匹配 `word` 从第 k 个字母开始的部分？**

1. 如果 `word[k] == '\0'`：整个单词都匹配完了，返回 `true`。
2. 如果 (r, c) 越界、或者字母不等于 `word[k]`（已用过的格子被标成 `'#'`，也一定不相等）：返回 `false`。
3. 否则：标记 (r, c)，去四个方向找 `word[k+1]`；最后撤销标记。

主函数里把每个格子都当起点试一次。

### 手动模拟（示例 3：`"ABCB"`）

| 调用 | 格子 | 字母 | 要找 | 结果 |
|---|---|---|---|---|
| dfs(0,0,0) | (0,0) | A | A | 相等，标记，往下找 B |
| dfs(0,1,1) | (0,1) | B | B | 相等，标记，往下找 C |
| dfs(0,2,2) | (0,2) | C | C | 相等，标记，往下找 B |
| dfs(1,2,3) | (1,2) | C | B | 不等，返回 false |
| dfs(0,3,3) | (0,3) | E | B | 不等，返回 false |
| dfs(0,1,3) | (0,1) | `#` | B | 已用过，返回 false |
| …… | | | | 全部失败，最终 false |

### 代码

```c
// 从 (r, c) 开始，能否匹配 word[k] 以及它后面的所有字母
bool dfs(char** board, int m, int n, int r, int c, char* word, int k) {
    if (word[k] == '\0') return true;                   // 全部匹配完了
    if (r < 0 || r >= m || c < 0 || c >= n) return false; // 越界
    if (board[r][c] != word[k]) return false;           // 字母不对（或已被标记成 '#'）

    char saved = board[r][c];
    board[r][c] = '#';                                  // 做标记：本条路线已使用
    bool found = dfs(board, m, n, r + 1, c, word, k + 1) ||
                 dfs(board, m, n, r - 1, c, word, k + 1) ||
                 dfs(board, m, n, r, c + 1, word, k + 1) ||
                 dfs(board, m, n, r, c - 1, word, k + 1);
    board[r][c] = saved;                                // 撤销标记（回溯）
    return found;
}

bool exist(char** board, int boardSize, int* boardColSize, char* word) {
    int m = boardSize, n = boardColSize[0];
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (dfs(board, m, n, i, j, word, 0)) return true;  // 每个格子都试着当起点
        }
    }
    return false;
}
```

### 复杂度分析

- **时间复杂度 O(m·n·3^L)**：L 是单词长度。每个起点出发，除了第一步有 4 个方向，之后每步最多 3 个方向（不能走回头路）。
- **空间复杂度 O(L)**：递归深度最多 L。

---

## 🚀 第四步：思路二 —— 回溯 + 剪枝

### 思路

思路一在一些「刁钻」数据上会很慢，比如整个网格都是 `A`，单词是 `"AAAAAAAAAAAAAAB"`：每条路线都要走到最后一个字母才发现失败。两个简单的剪枝：

1. **字母数量剪枝**：先数一数网格里每种字母有几个。如果单词里某个字母出现的次数比网格里还多，那肯定找不到，直接返回 `false`。上面的例子网格里根本没有 `B`，瞬间结束。
2. **倒着找**：如果单词的首字母在网格里很多、尾字母很少，那就把单词**反过来**找（正着能走出来，倒着一定也能）。起点变少，搜索量大大减少。

### 代码

```c
bool dfs(char** board, int m, int n, int r, int c, char* word, int k) {
    if (word[k] == '\0') return true;
    if (r < 0 || r >= m || c < 0 || c >= n || board[r][c] != word[k]) return false;
    char saved = board[r][c];
    board[r][c] = '#';
    bool found = dfs(board, m, n, r + 1, c, word, k + 1) ||
                 dfs(board, m, n, r - 1, c, word, k + 1) ||
                 dfs(board, m, n, r, c + 1, word, k + 1) ||
                 dfs(board, m, n, r, c - 1, word, k + 1);
    board[r][c] = saved;
    return found;
}

bool exist(char** board, int boardSize, int* boardColSize, char* word) {
    int m = boardSize, n = boardColSize[0];
    int len = strlen(word);
    if (len > m * n) return false;            // 单词比格子还多，不可能

    // 1. 字母数量剪枝：cntBoard[ch] 是网格里字母 ch 的个数
    int cntBoard[128] = {0}, cntWord[128] = {0};
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            cntBoard[(int)board[i][j]]++;
    for (int i = 0; i < len; i++) {
        cntWord[(int)word[i]]++;
        if (cntWord[(int)word[i]] > cntBoard[(int)word[i]]) return false;
    }

    // 2. 拷贝一份单词（不要改题目给的 word），首字母更多时就倒过来找
    char w[16];                               // 单词最长 15，再加一个 '\0'
    strcpy(w, word);
    if (cntBoard[(int)w[0]] > cntBoard[(int)w[len - 1]]) {
        for (int i = 0, j = len - 1; i < j; i++, j--) {
            char t = w[i]; w[i] = w[j]; w[j] = t;
        }
    }

    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            if (dfs(board, m, n, i, j, w, 0)) return true;
    return false;
}
```

**代码中几个可能看不懂的地方：**

- `cntBoard[(int)board[i][j]]`：字符本质上是一个小整数（ASCII 码，`'A'` 是 65），可以直接当数组下标。大小写字母都小于 128，所以开 128 个格子就够。
- `char w[16]`：单词最长 15 个字母，再留 1 个位置给 `'\0'`。

### 复杂度分析

- 最坏时间复杂度仍是 O(m·n·3^L)，但实际数据上快很多。
- **空间复杂度 O(L)**。

---

## ⚠️ 第五步：小白常见错误

1. **忘了撤销标记**：`board[r][c] = '#'` 之后没改回来，从别的起点出发时这些格子就「消失」了，本来能找到的会返回 `false`。
2. **用 `return` 提前退出却没撤销**：比如写成 `if (dfs(...)) return true;` 放在恢复语句前面。本题找到就结束问题不大，但养成习惯：**标记和撤销要成对出现**。
3. **先判断 `word[k]` 再判断越界的顺序写反**：如果先访问 `board[r][c]` 再判断越界，会读到数组外面导致崩溃。
4. **单字母单词处理错**：例如 `board = [["a"]]`、`word = "a"`，第一层匹配成功后进入下一层，`word[1] == '\0'` 返回 `true`。如果你把「匹配完」的判断写成 `k == len - 1` 且放错位置，很容易漏掉这种情况。
5. **直接修改题目给的 `word` 做反转**：本题判题没问题，但在实际工程里修改调用者的数据是坏习惯，拷贝一份更安全。

---

## 📊 第六步：两种方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 回溯 DFS | O(m·n·3^L) | O(L) | ⭐⭐ | 必须掌握的模板 |
| 回溯 + 剪枝 | 最坏同上，实际快很多 | O(L) | ⭐⭐⭐ | 面试加分项 |

> 🎯 **学习建议**：「标记 → 递归 → 撤销」是回溯的灵魂，几乎所有回溯题都长这样。

---

## 🔗 举一反三

- **212. 单词搜索 II**：一次找很多个单词，需要配合 **208. 实现 Trie（前缀树）**。
- **200. 岛屿数量**：同样是网格 DFS，但不需要撤销标记（为什么？）。
- **46. 全排列**：用 `used[]` 数组做标记，同样要撤销。
- **思考题**：如果允许斜着走（8 个方向），代码要改哪里？
