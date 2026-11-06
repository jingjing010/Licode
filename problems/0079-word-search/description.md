给定一个 `m x n` 二维字符网格 `board` 和一个字符串单词 `word` 。如果 `word` 存在于网格中，返回 `true` ；否则，返回 `false` 。

单词必须按照字母顺序，通过相邻的单元格内的字母构成，其中"相邻"单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母不允许被重复使用。

### 示例 1

```
输入：board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
输出：true
```

### 示例 2

```
输入：board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "SEE"
输出：true
```

### 示例 3

```
输入：board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCB"
输出：false
```

### 提示

- `m == board.length`
- `n = board[i].length`
- `1 <= m, n <= 6`
- `1 <= word.length <= 15`
- `board` 和 `word` 仅由大小写英文字母组成

**进阶：** 你可以使用搜索剪枝的技术来优化解决方案，使其在 `board` 更大的情况下可以更快解决问题？

### 函数说明

```c
bool exist(char** board, int boardSize, int* boardColSize, char* word);
```

- `board`：二维字符网格，`board[i][j]` 是一个字母
- `boardSize`：行数 `m`；`boardColSize[i]`：第 `i` 行的列数（都等于 `n`）
- `word`：以 `'\0'` 结尾的字符串
- 返回值：能找到返回 `true`，否则返回 `false`
- 你可以修改 `board`（例如临时做标记）

### 自定义输入格式

```
[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
"ABCCED"
```

第 1 行是字符网格 `board`，第 2 行是带双引号的字符串 `word`。
