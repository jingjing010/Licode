# 107. 二叉树的层序遍历 II —— 小白详细题解

> 这是第 102 题的"倒过来"版本。核心还是**按层 BFS**，多出来的只是一步"把结果反转"。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 把树一层一层地读出来，每层从左往右；但最后交上去的时候，**最底下那层放最前面**，根所在的层放最后面。

示例 1：`[3,9,20,null,null,15,7]`

```
    3          ← 第 1 层
   / \
  9  20        ← 第 2 层
    /  \
   15   7      ← 第 3 层
```

| 从上到下读（第 102 题） | 自底向上（本题） |
|---|---|
| [3] | [15,7] |
| [9,20] | [9,20] |
| [15,7] | [3] |

所以答案是 `[[15,7],[9,20],[3]]`。

**几个需要注意的细节：**

1. **只反转层的顺序**，每一层内部仍然是**从左到右**。`[9,20]` 不能变成 `[20,9]`。
2. 空树返回空数组：`*returnSize = 0`。
3. 返回值有三样东西要准备好：二维数组本身、每行的长度数组 `*returnColumnSizes`、行数 `*returnSize`。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 二维数组 `int**` 的返回方式

`int** res` 是"指针的数组"：`res[i]` 是一个 `int*`，指向第 i 行。每行长度不一样，所以要单独用 `cols[i]` 记录。

```c
int** res = (int**)malloc(sizeof(int*) * 最多行数);   // 行指针数组
int* cols = (int*)malloc(sizeof(int) * 最多行数);     // 每行长度
res[k] = (int*)malloc(sizeof(int) * 这一行的长度);     // 每一行单独申请
```

### 2. `int** returnColumnSizes` 为什么是两个星号

函数要"返回"一个 `int*`（长度数组）给调用者，C 只能传值，所以调用者把自己变量的**地址**给你，你写 `*returnColumnSizes = cols;` 才能改到调用者那边——和 `*returnSize = 层数;` 是同一个道理。

### 3. 交换两个指针

反转数组时要交换两行。交换的只是**行指针**（8 个字节），不需要把整行数据复制一遍：

```c
int* t = res[i]; res[i] = res[j]; res[j] = t;
```

---

## 💡 第三步：思路一 —— BFS 从上到下，最后反转

### 思路

1. 完全按照第 102 题的写法：用队列，每轮先记下队列长度 `size`（就是这一层的结点数），出队 `size` 个，把值写进新的一行，同时把孩子入队。
2. 全部层收集完后，用双指针 `i`（从头）和 `j`（从尾）往中间走，交换 `res[i]` 与 `res[j]`，同时交换 `cols[i]` 与 `cols[j]`。

### 手动模拟（示例 1）

| 轮次 | 队列（出队前） | size | 写入的一行 | 入队 |
|---|---|---|---|---|
| 1 | [3] | 1 | [3] | 9, 20 |
| 2 | [9, 20] | 2 | [9,20] | 15, 7 |
| 3 | [15, 7] | 2 | [15,7] | 无 |

收集结果 `[[3],[9,20],[15,7]]`，反转：交换第 0 行和第 2 行 → `[[15,7],[9,20],[3]]`。

### 代码

```c
int** levelOrderBottom(struct TreeNode* root, int* returnSize, int** returnColumnSizes) {
    // 层数最多等于结点数 2000
    int** res = (int**)malloc(sizeof(int*) * 2001);
    int* cols = (int*)malloc(sizeof(int) * 2001);
    int levels = 0;                       // 已经收集了几层
    *returnSize = 0;
    *returnColumnSizes = cols;            // 空树也要给一个合法的指针
    if (root == NULL) return res;

    // 队列：每个结点只入队一次
    struct TreeNode** q = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * 2001);
    int head = 0, tail = 0;
    q[tail++] = root;
    while (head < tail) {
        int size = tail - head;           // 这一层有几个结点，先记下来
        int* row = (int*)malloc(sizeof(int) * size);
        for (int i = 0; i < size; i++) {
            struct TreeNode* node = q[head++];        // 出队
            row[i] = node->val;
            if (node->left) q[tail++] = node->left;   // 孩子入队（属于下一层）
            if (node->right) q[tail++] = node->right;
        }
        res[levels] = row;
        cols[levels] = size;
        levels++;
    }
    free(q);

    // 反转"层的顺序"：行指针和行长度要一起交换
    for (int i = 0, j = levels - 1; i < j; i++, j--) {
        int* tr = res[i]; res[i] = res[j]; res[j] = tr;
        int tc = cols[i]; cols[i] = cols[j]; cols[j] = tc;
    }
    *returnSize = levels;
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n)**：每个结点入队出队各一次；反转只交换 O(层数) 个指针。
- **空间复杂度 O(n)**：队列和结果数组。

---

## 🚀 第四步：思路二 —— 先算层数，直接写到倒序位置（DFS）

### 思路

如果**事先知道总层数** `depth`，那第 `d` 层（根是第 0 层）在答案里的位置就是 `depth - 1 - d`，可以直接写到正确位置，不用最后反转：

1. 第一遍 DFS：求树高 `depth`，同时统计每层的结点数 `cnt[d]`。
2. 按 `cnt` 为每一行 `malloc` 好空间。
3. 第二遍 DFS（先左后右，保证同层从左到右）：把结点值追加到第 `depth - 1 - d` 行的末尾。

### 手动模拟（示例 1，depth = 3）

| 访问顺序 | 结点 | 层 d | 写入第几行 depth-1-d |
|---|---|---|---|
| 1 | 3 | 0 | 2 |
| 2 | 9 | 1 | 1 |
| 3 | 20 | 1 | 1 |
| 4 | 15 | 2 | 0 |
| 5 | 7 | 2 | 0 |

结果：第 0 行 `[15,7]`，第 1 行 `[9,20]`，第 2 行 `[3]`。

### 代码

```c
// 第一遍：统计每层结点数，返回以 node 为根的子树高度
int countLevels(struct TreeNode* node, int d, int* cnt) {
    if (node == NULL) return 0;
    cnt[d]++;                                          // 第 d 层多一个结点
    int l = countLevels(node->left, d + 1, cnt);
    int r = countLevels(node->right, d + 1, cnt);
    return (l > r ? l : r) + 1;
}

// 第二遍：先左后右，把值追加到对应的倒序行
void fill(struct TreeNode* node, int d, int depth, int** res, int* pos) {
    if (node == NULL) return;
    int row = depth - 1 - d;                           // 第 d 层在答案中的行号
    res[row][pos[row]++] = node->val;
    fill(node->left, d + 1, depth, res, pos);
    fill(node->right, d + 1, depth, res, pos);
}

int** levelOrderBottom(struct TreeNode* root, int* returnSize, int** returnColumnSizes) {
    int* cnt = (int*)calloc(2001, sizeof(int));        // cnt[d]：第 d 层的结点数，calloc 自动清零
    int depth = countLevels(root, 0, cnt);

    int** res = (int**)malloc(sizeof(int*) * (depth + 1));
    int* cols = (int*)malloc(sizeof(int) * (depth + 1));
    int* pos = (int*)calloc(depth + 1, sizeof(int));   // 每行已经写了几个
    for (int d = 0; d < depth; d++) {
        int row = depth - 1 - d;
        cols[row] = cnt[d];
        res[row] = (int*)malloc(sizeof(int) * cnt[d]);
    }
    fill(root, 0, depth, res, pos);

    free(cnt);
    free(pos);
    *returnSize = depth;
    *returnColumnSizes = cols;
    return res;
}
```

> 为什么 DFS 也能保证"同层从左到右"？因为先递归左子树、再递归右子树，同一层里左边的结点一定先被访问到。

### 复杂度分析

- **时间复杂度 O(n)**：两遍 DFS。
- **空间复杂度 O(n)**：递归栈 O(h) + 结果数组。

---

## ⚠️ 第五步：小白常见错误

1. **把每层内部也反转了**：
   ```c
   row[size - 1 - i] = node->val;   // ❌ 层内变成从右到左
   ```
   题目只要求层的顺序倒过来，每层内部仍然从左到右。
2. **反转时只交换了行指针，忘了交换 `cols`**：行和长度对不上，打印时会越界或少打印。
3. **没有先记下 `size`**：写成 `for (int i = 0; i < tail - head; i++)`，循环中 `tail` 在变，下一层的结点被混进这一层。
4. **空树时 `*returnColumnSizes` 没赋值**：调用者拿到的是一个野指针。养成习惯：函数一开始就给 `*returnSize` 和 `*returnColumnSizes` 赋值。
5. **每行用局部数组**：`int row[2000];` 函数返回后就失效了，必须 `malloc`。

---

## 📊 第六步：两种方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| BFS + 反转 | O(n) | O(n) | ⭐⭐ | **首选**，102 题模板加 5 行 |
| 两遍 DFS 直接定位 | O(n) | O(n) | ⭐⭐⭐ | 理解"按层号写入"的技巧 |

---

## 🔗 举一反三

- **102. 二叉树的层序遍历**：本题去掉反转就是它。
- **103. 二叉树的锯齿形层序遍历**：奇数层反转、偶数层不反转。
- **199. 二叉树的右视图**：每层只取最后一个。
- **515. 在每个树行中找最大值**：每层只取最大值。
- **思考题**：如果不允许最后反转，也不允许两遍遍历，能做到吗？（提示：先按层存进一个"栈"里。）
