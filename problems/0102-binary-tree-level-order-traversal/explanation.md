# 102. 二叉树的层序遍历 —— 小白详细题解

> 层序遍历（BFS）是树和图里最重要的模板之一。这道题的难点一半在算法，一半在 C 语言"返回二维数组"的写法。

---

## 📖 第一步：先读懂题目

**层序遍历**：从上到下一层一层地访问，每层内部从左到右。并且要把**每一层单独装进一个数组**。

示例 1 `[3,9,20,null,null,15,7]`：

```
    3        ← 第 0 层：[3]
   / \
  9  20      ← 第 1 层：[9,20]
    /  \
   15   7    ← 第 2 层：[15,7]
```

答案：`[[3],[9,20],[15,7]]`。

**几个需要注意的细节：**

1. 结果是**二维**的：要分清每个数属于哪一层，不能输出成一维的 `[3,9,20,15,7]`。
2. 空树返回空数组：`*returnSize = 0`。
3. 结点最多 2000 个，层数最多 2000（链状树）。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 力扣"返回二维数组"的三件套

```c
int** levelOrder(struct TreeNode* root, int* returnSize, int** returnColumnSizes)
```

| 你要做的事 | 代码 |
|---|---|
| 申请"行指针数组" | `int** res = malloc(sizeof(int*) * 最大行数);` |
| 每一行单独申请 | `res[i] = malloc(sizeof(int) * 这一行的长度);` |
| 申请"每行长度"数组并交出去 | `*returnColumnSizes = malloc(sizeof(int) * 最大行数);` |
| 写每行长度 | `(*returnColumnSizes)[i] = 这一行的长度;` |
| 写总行数 | `*returnSize = 行数;` |

> ⚠️ `(*returnColumnSizes)[i]` 的括号不能省！`*returnColumnSizes[i]` 会被理解成 `*(returnColumnSizes[i])`，完全是另一个意思。

### 2. 为什么 `returnColumnSizes` 是 `int**`？

因为你要在函数里**创建**一个数组（`int*`），再把它的地址交给调用者。要修改调用者手里的 `int*` 变量，就得拿到它的地址，也就是 `int**`。这和"要修改 `int` 就传 `int*`"是同一个道理，只是多了一层。

### 3. 用数组模拟队列

```c
queue[tail++] = x;   // 入队
x = queue[head++];   // 出队
```

---

## 💡 第三步：思路一 —— 深度优先 + 记录层号

### 思路

不一定非要按层访问！只要知道每个结点在**第几层**，就能把它放进对应的行：

1. 递归时多带一个参数 `depth`（当前层号）。
2. 先访问左子树再访问右子树，这样同一层里**左边的结点一定先被放进去**，顺序正确。
3. 由于每行的长度事先不知道，先给每行开足够大的空间（这里每层最多 2000 个，简单起见按 2000 开）。

### 代码

```c
// 把以 node 为根的子树里的结点，按层号放进 res
void dfs(struct TreeNode* node, int depth, int** res, int* cols, int* rows) {
    if (node == NULL) return;
    if (depth == *rows) {                                 // 第一次来到这一层：新开一行
        res[depth] = (int*)malloc(sizeof(int) * 2000);
        cols[depth] = 0;
        (*rows)++;
    }
    res[depth][cols[depth]++] = node->val;                // 放到这一行的末尾
    dfs(node->left, depth + 1, res, cols, rows);          // 先左后右，保证同层从左到右
    dfs(node->right, depth + 1, res, cols, rows);
}

int** levelOrder(struct TreeNode* root, int* returnSize, int** returnColumnSizes) {
    int** res = (int**)malloc(sizeof(int*) * 2000);       // 最多 2000 层
    int* cols = (int*)malloc(sizeof(int) * 2000);         // 每层的结点数
    int rows = 0;
    dfs(root, 0, res, cols, &rows);
    *returnSize = rows;
    *returnColumnSizes = cols;
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n)**：每个结点访问一次。
- **空间复杂度 O(n)**：结果本身；但每行都开了 2000 个位置，比较浪费内存。

---

## 🚀 第四步：思路二 —— 广度优先（队列，标准写法）

### 思路

1. 根结点入队。
2. 每一轮开始时，队列里**恰好是同一层的全部结点**，个数 `size = tail - head`。
3. 给这一层申请 `size` 个 `int`，出队 `size` 个结点，依次写入，并把它们的孩子入队（这些孩子都属于下一层）。
4. 队列空了就结束。

### 手动模拟（示例 1）

| 轮次 | 开始时队列 | size | 本层结果 | 入队的孩子 |
|---|---|---|---|---|
| 0 | [3] | 1 | [3] | 9, 20 |
| 1 | [9, 20] | 2 | [9,20] | 15, 7 |
| 2 | [15, 7] | 2 | [15,7] | 无 |

### 代码

```c
int** levelOrder(struct TreeNode* root, int* returnSize, int** returnColumnSizes) {
    int** res = (int**)malloc(sizeof(int*) * 2000);        // 最多 2000 层
    *returnColumnSizes = (int*)malloc(sizeof(int) * 2000); // 每层的结点数
    *returnSize = 0;
    if (root == NULL) return res;                          // 空树：0 行

    // 每个结点只入队一次，2000 个位置足够
    struct TreeNode** queue = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * 2000);
    int head = 0, tail = 0;
    queue[tail++] = root;

    while (head < tail) {
        int size = tail - head;                            // 这一层有几个结点
        int row = *returnSize;                             // 这一层是第几行
        res[row] = (int*)malloc(sizeof(int) * size);       // 刚好开 size 个
        (*returnColumnSizes)[row] = size;

        for (int i = 0; i < size; i++) {
            struct TreeNode* node = queue[head++];         // 出队
            res[row][i] = node->val;
            if (node->left)  queue[tail++] = node->left;   // 孩子入队，属于下一层
            if (node->right) queue[tail++] = node->right;
        }
        (*returnSize)++;                                   // 行数 +1
    }

    free(queue);
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n)**：每个结点入队出队各一次。
- **空间复杂度 O(n)**：队列 + 结果，每行恰好开够。

---

## ⚠️ 第五步：小白常见错误

1. **`*returnColumnSizes[i] = size`**：少了括号，优先级错误，程序崩溃。必须写 `(*returnColumnSizes)[i]`。
2. **忘记 `malloc` 每一行**：`res[row][i] = ...` 写进了一个野指针，Runtime Error。
3. **`size` 没有提前记下**：`for (i = 0; i < tail - head; i++)`，循环过程中 `tail`、`head` 都在变，会把下一层的结点混进这一层。
4. **空树时 `*returnColumnSizes` 没赋值**：有的调用者会读它，最好空树时也 `malloc` 一下或至少设置好 `*returnSize = 0`。
5. **把空孩子入队**：`queue[tail++] = node->left;` 不判空，之后出队访问 `node->val` 时崩溃。

---

## 📊 第六步：两种方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| DFS + 层号 | O(n) | O(n)（每行开满，较浪费） | ⭐⭐ | 理解"层号"思想 |
| BFS + 队列 | O(n) | O(n) | ⭐⭐ | 标准模板，务必背熟 |

---

## 🔗 举一反三

- **107. 二叉树的层序遍历 II**：自底向上，把结果数组反转即可。
- **103. 二叉树的锯齿形层序遍历**：奇数层反过来放。
- **199. 二叉树的右视图**：每层只取最后一个结点。
- **104. 二叉树的最大深度**：层数就是深度。
- **思考题**：如果不知道结点数上限，`res` 和队列开多大？（提示：先数一遍结点，或者用 `realloc` 扩容）
