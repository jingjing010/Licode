# 51. N 皇后 —— 小白详细题解

> N 皇后是回溯算法最经典的「困难」题。别被难度吓到：它其实就是 46 题全排列加上「斜线不能冲突」这个条件。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 在 n×n 的棋盘上放 n 个皇后，任意两个皇后**不能在同一行、同一列、同一条斜线上**。列出所有放法。

`n = 4` 的一种放法（`Q` 是皇后）：

| 行\列 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| 0 | . | Q | . | . |
| 1 | . | . | . | Q |
| 2 | Q | . | . | . |
| 3 | . | . | Q | . |

每行、每列都只有一个皇后，任意两个也不在同一条斜线上。

**几个需要注意的细节：**

1. n 个皇后、n 行，又不能同行 → **每一行恰好一个皇后**。这是解题的突破口。
2. `n = 2`、`n = 3` **无解**，返回空数组。
3. 输出格式是「每种解法 = n 个字符串」，每个字符串是棋盘的一行，比如 `".Q.."`。
4. n ≤ 9，解的个数最多 352 个（n = 9）。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 怎么判断两个格子在同一条斜线上？

| 斜线方向 | 特点 | 例子 |
|---|---|---|
| 主对角线 `↘` | `行 - 列` 相同 | (0,1)、(1,2)、(2,3)：行-列都是 -1 |
| 副对角线 `↙` | `行 + 列` 相同 | (0,3)、(1,2)、(2,1)：行+列都是 3 |

所以两个皇后 (r1,c1)、(r2,c2) 在同一斜线上 ⟺ `|r1 - r2| == |c1 - c2|`。

### 2. `memset` 填充字符

```c
char* row = (char*)malloc(n + 1);
memset(row, '.', n);      // 前 n 个字符都填成 '.'
row[n] = '\0';            // 别忘了结尾
```

### 3. `char***` 返回值

和 131 题一样：所有解法的数组（`char***`）→ 每种解法是 n 行（`char**`）→ 每行是一个字符串（`char*`）。

---

## 💡 第三步：思路一 —— 逐行回溯 + 逐个检查冲突

### 思路

用 `pos[r]` 记录第 `r` 行的皇后放在第几列。

1. 从第 0 行开始，尝试把皇后放在第 0、1、……、n-1 列。
2. 放之前检查：和前面每一行 `i` 的皇后是否**同列**（`pos[i] == c`）或**同斜线**（`|r - i| == |c - pos[i]|`）。
3. 不冲突就放下，递归处理下一行；全部 n 行都放好了，就把 `pos` 转成棋盘字符串存起来。

### 手动模拟（n = 4，找第一个解）

| 行 | 尝试列 | 结果 | pos |
|---|---|---|---|
| 0 | 0 | 放 | [0] |
| 1 | 0、1 冲突，2 | 放 | [0,2] |
| 2 | 0~3 全冲突 | 回溯 | [0] |
| 1 | 3 | 放 | [0,3] |
| 2 | 1 | 放 | [0,3,1] |
| 3 | 0~3 全冲突 | 回溯，一路退回第 0 行 | |
| 0 | 1 | 放 | [1] |
| 1 | 3 | 放 | [1,3] |
| 2 | 0 | 放 | [1,3,0] |
| 3 | 2 | 放，找到解 `.Q.. / ...Q / Q... / ..Q.` | [1,3,0,2] |

### 代码

```c
// 第 r 行放在第 c 列，会不会和前面 0 ~ r-1 行的皇后冲突
bool canPlace(int* pos, int r, int c) {
    for (int i = 0; i < r; i++) {
        if (pos[i] == c) return false;                    // 同一列
        if (abs(r - i) == abs(c - pos[i])) return false;  // 同一条斜线
    }
    return true;
}

void backtrack(int n, int r, int* pos, char*** res, int* cnt) {
    if (r == n) {                                         // n 行都放好了，生成棋盘
        char** board = (char**)malloc(sizeof(char*) * n);
        for (int i = 0; i < n; i++) {
            board[i] = (char*)malloc(n + 1);
            memset(board[i], '.', n);                     // 先全部填 '.'
            board[i][pos[i]] = 'Q';                       // 再把皇后放上去
            board[i][n] = '\0';
        }
        res[*cnt] = board;
        (*cnt)++;
        return;
    }
    for (int c = 0; c < n; c++) {
        if (!canPlace(pos, r, c)) continue;
        pos[r] = c;                                       // 第 r 行放在第 c 列
        backtrack(n, r + 1, pos, res, cnt);               // 去放下一行
        // 回溯：下一轮循环会覆盖 pos[r]，不需要额外撤销
    }
}

char*** solveNQueens(int n, int* returnSize, int** returnColumnSizes) {
    char*** res = (char***)malloc(sizeof(char**) * 400);  // n <= 9 时最多 352 个解
    int pos[9];
    int cnt = 0;
    backtrack(n, 0, pos, res, &cnt);

    *returnSize = cnt;
    *returnColumnSizes = (int*)malloc(sizeof(int) * 400);
    for (int i = 0; i < cnt; i++) (*returnColumnSizes)[i] = n;   // 每种解法都有 n 行
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n! · n)**：第 0 行 n 种选择，第 1 行最多 n-1 种……每次检查冲突要 O(n)。
- **空间复杂度 O(n)**：递归深度 n 和 `pos` 数组（结果本身不算）。

---

## 🚀 第四步：思路二 —— 用三个布尔数组 O(1) 判断冲突

### 思路

思路一每放一个皇后都要和前面所有皇后比一遍。其实可以用数组记录「哪些列、哪些斜线已经被占了」：

| 数组 | 下标 | 大小 | 含义 |
|---|---|---|---|
| `col[c]` | 列号 c | n | 第 c 列有皇后 |
| `diag1[r + c]` | 行 + 列 | 2n - 1 | 这条 `↙` 斜线有皇后 |
| `diag2[r - c + n - 1]` | 行 - 列 + (n-1) | 2n - 1 | 这条 `↘` 斜线有皇后 |

> ❓ 为什么要 `+ n - 1`？`r - c` 的范围是 `-(n-1)` 到 `n-1`，会出现负数，不能做数组下标。加上 `n - 1` 后范围变成 `0` 到 `2n-2`。

放皇后时把三个标记设为 `true`，回溯时改回 `false`。

### 代码

```c
void backtrack(int n, int r, int* pos, bool* col, bool* diag1, bool* diag2,
               char*** res, int* cnt) {
    if (r == n) {
        char** board = (char**)malloc(sizeof(char*) * n);
        for (int i = 0; i < n; i++) {
            board[i] = (char*)malloc(n + 1);
            memset(board[i], '.', n);
            board[i][pos[i]] = 'Q';
            board[i][n] = '\0';
        }
        res[*cnt] = board;
        (*cnt)++;
        return;
    }
    for (int c = 0; c < n; c++) {
        // O(1) 判断：列、两条斜线都没被占
        if (col[c] || diag1[r + c] || diag2[r - c + n - 1]) continue;
        col[c] = diag1[r + c] = diag2[r - c + n - 1] = true;      // 做选择：占用
        pos[r] = c;
        backtrack(n, r + 1, pos, col, diag1, diag2, res, cnt);
        col[c] = diag1[r + c] = diag2[r - c + n - 1] = false;     // 撤销选择：释放
    }
}

char*** solveNQueens(int n, int* returnSize, int** returnColumnSizes) {
    char*** res = (char***)malloc(sizeof(char**) * 400);
    int pos[9];
    bool col[9] = {false};
    bool diag1[17] = {false}, diag2[17] = {false};    // 2n - 1 <= 17
    int cnt = 0;
    backtrack(n, 0, pos, col, diag1, diag2, res, &cnt);

    *returnSize = cnt;
    *returnColumnSizes = (int*)malloc(sizeof(int) * 400);
    for (int i = 0; i < cnt; i++) (*returnColumnSizes)[i] = n;
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n!)**：判断冲突从 O(n) 降到 O(1)（生成棋盘还需要 O(n²)，但只在找到解时才做）。
- **空间复杂度 O(n)**。

---

## ⚠️ 第五步：小白常见错误

1. **只检查了一条斜线**：只判断 `r + c` 或只判断 `r - c`，会得到很多错误的「解」。两个方向都要检查。
2. **`r - c` 直接当下标**：可能是负数，数组越界。要加 `n - 1` 做偏移。
3. **思路二忘了撤销标记**：找到第一个解后标记全是 `true`，后面再也放不下，只能得到 1 个解（甚至 0 个）。
4. **棋盘字符串忘记 `'\0'`**：输出变成乱码。
5. **`n = 2`、`n = 3` 时出错**：它们无解，`*returnSize` 必须是 0，程序不能崩溃。
6. **`*returnColumnSizes` 填成了 1 或解的个数**：它表示「每种解法有几行」，应该是 `n`。

---

## 📊 第六步：两种方法对比

| 方法 | 时间复杂度 | 额外空间 | 难度 | 建议 |
|---|---|---|---|---|
| 逐个检查冲突 | O(n! · n) | O(n) | ⭐⭐⭐ | 思路直观，先写对 |
| 三个布尔数组 | O(n!) | O(n) | ⭐⭐⭐ | 标准写法，面试常考 |

> 🎯 **学习建议**：画一个 4×4 的棋盘，把每个格子的 `r + c` 和 `r - c` 写上去，你会一眼看出同一斜线上的数字相同。

---

## 🔗 举一反三

- **52. N 皇后 II**：只要解的个数，不用生成棋盘，代码更短。还可以用**位运算**把三个数组压成三个整数，更快。
- **46. 全排列**：N 皇后的 `pos` 数组本身就是 0~n-1 的一个排列。
- **37. 解数独**：同样是「填格子 + 检查行、列、宫格冲突」的回溯。
- **思考题**：n = 8 时一共有 92 个解。利用棋盘的**左右对称**，能不能只搜索一半，把时间减少一半？
