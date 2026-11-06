# 103. 二叉树的锯齿形层序遍历 —— 小白详细题解

> 一句话题解：**照常做层序遍历，只是奇数层把结果倒过来放**。这道题是第 102 题（层序遍历）的小变形，重点练"二维数组怎么返回"。

---

## 📖 第一步：先读懂题目

把树一层一层地读出来，但方向来回切换：第 0 层从左往右，第 1 层从右往左，第 2 层又从左往右……

```
        1
      /   \
     2     3
    / \   / \
   4   5 6   7
```

| 层号 | 从左往右看到的 | 本层方向 | 放进答案的 |
|---|---|---|---|
| 0 | 1 | → | `[1]` |
| 1 | 2, 3 | ← | `[3,2]` |
| 2 | 4, 5, 6, 7 | → | `[4,5,6,7]` |

答案：`[[1],[3,2],[4,5,6,7]]`。

**几个需要注意的细节：**

1. 树可能是空的（示例 3），这时层数为 0，返回空。
2. "锯齿"只影响**结果的排列顺序**，不需要改变遍历时把孩子放进队列的顺序。
3. 每层结点个数不一样，所以要用 `*returnColumnSizes` 告诉调用者每一行有多长。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 返回"锯齿"二维数组：三个输出

力扣的 C 接口要你返回三样东西：

```c
int** res;                 // res[i] 是第 i 行（第 i 层）的数组
*returnSize = 层数;        // 一共几行
*returnColumnSizes = cols; // cols[i] 是第 i 行有几个数
```

`returnColumnSizes` 的类型是 `int**`：它是"一个 `int*` 变量的地址"。我们 `malloc` 一个 `int` 数组 `cols`，再通过 `*returnColumnSizes = cols;` 把它交给调用者。

### 2. 用数组模拟队列

```c
struct TreeNode** q = malloc(...);
int head = 0, tail = 0;
q[tail++] = root;          // 入队
struct TreeNode* t = q[head++];   // 出队
```

每个结点只入队一次，所以数组开"结点总数"那么大就够了（本题最多 2000 个）。

### 3. 一层一层地处理

开始处理某一层时，队列里**恰好**是这一层的全部结点，个数是 `tail - head`。先把它记成 `sz`，然后循环 `sz` 次，就只会处理这一层。

---

## 💡 第三步：思路一 —— 层序遍历，奇数层再反转

### 思路

1. 和第 102 题一样，用队列一层一层取结点，按从左往右的顺序把值放进这一层的数组 `row`。
2. 如果这一层的层号是奇数，就把 `row` 整个反转（首尾交换）。
3. 把 `row` 存进答案。

### 手动模拟（示例 1）

| 层号 | 本层出队顺序 | row（从左往右） | 是否反转 | 放进答案 |
|---|---|---|---|---|
| 0 | 3 | [3] | 否 | [3] |
| 1 | 9, 20 | [9,20] | 是 | [20,9] |
| 2 | 15, 7 | [15,7] | 否 | [15,7] |

### 代码

```c
int** zigzagLevelOrder(struct TreeNode* root, int* returnSize, int** returnColumnSizes) {
    *returnSize = 0;                       // 先当作空树处理
    *returnColumnSizes = NULL;
    if (root == NULL) return NULL;         // 空树：0 层

    // 结点最多 2000 个，队列、答案行数都不会超过 2000
    struct TreeNode** q = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * 2000);
    int** res = (int**)malloc(sizeof(int*) * 2000);
    int* cols = (int*)malloc(sizeof(int) * 2000);
    int head = 0, tail = 0, level = 0;
    q[tail++] = root;

    while (head < tail) {
        int sz = tail - head;                          // 这一层有几个结点
        int* row = (int*)malloc(sizeof(int) * sz);
        for (int i = 0; i < sz; i++) {
            struct TreeNode* t = q[head++];            // 出队
            row[i] = t->val;                           // 先按从左往右放
            if (t->left != NULL) q[tail++] = t->left;  // 孩子入队（永远先左后右）
            if (t->right != NULL) q[tail++] = t->right;
        }
        if (level % 2 == 1) {                          // 奇数层：首尾交换，整体反转
            for (int i = 0, j = sz - 1; i < j; i++, j--) {
                int tmp = row[i];
                row[i] = row[j];
                row[j] = tmp;
            }
        }
        res[level] = row;
        cols[level] = sz;
        level++;
    }

    free(q);
    *returnSize = level;
    *returnColumnSizes = cols;
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n)**：每个结点入队出队各一次；反转的总代价也是 O(n)。
- **空间复杂度 O(n)**：队列和答案。

---

## 🚀 第四步：思路二 —— 直接写到正确的位置（不用反转）

### 思路

每层开始时已经知道这一层有 `sz` 个结点。第 `i` 个出队的结点（从 0 数）：

- 偶数层：放到 `row[i]`；
- 奇数层：放到 `row[sz - 1 - i]`，也就是从数组尾巴往前放。

这样一次就放好了，省掉反转的那一步。思路一、二本质相同，思路二更简洁。

> 也有人用"双端队列"真的改变取结点的方向，但那样要同时调整孩子的入队顺序，很容易写错。**只改写入位置**是最不容易出错的做法。

### 代码

```c
int** zigzagLevelOrder(struct TreeNode* root, int* returnSize, int** returnColumnSizes) {
    *returnSize = 0;
    *returnColumnSizes = NULL;
    if (root == NULL) return NULL;

    struct TreeNode** q = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * 2000);
    int** res = (int**)malloc(sizeof(int*) * 2000);
    int* cols = (int*)malloc(sizeof(int) * 2000);
    int head = 0, tail = 0, level = 0;
    q[tail++] = root;

    while (head < tail) {
        int sz = tail - head;
        int* row = (int*)malloc(sizeof(int) * sz);
        for (int i = 0; i < sz; i++) {
            struct TreeNode* t = q[head++];
            int pos = (level % 2 == 0) ? i : sz - 1 - i;   // 奇数层从后往前放
            row[pos] = t->val;
            if (t->left != NULL) q[tail++] = t->left;
            if (t->right != NULL) q[tail++] = t->right;
        }
        res[level] = row;
        cols[level] = sz;
        level++;
    }

    free(q);
    *returnSize = level;
    *returnColumnSizes = cols;
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n)**，**空间复杂度 O(n)**。

---

## ⚠️ 第五步：小白常见错误

1. **忘了设置 `*returnColumnSizes`**：只返回了 `res` 和 `*returnSize`，调用者不知道每行多长，会读到垃圾数据甚至崩溃。
2. **在 `for` 循环条件里直接写 `tail - head`**：

   ```c
   for (int i = 0; i < tail - head; i++)   // ❌ 循环中 tail、head 都在变
   ```

   必须先 `int sz = tail - head;` 把这一层的个数固定下来。
3. **奇数层把孩子入队顺序也反过来**：例如奇数层先放右孩子，会把下一层的顺序也打乱，结果再翻一次就错了。入队顺序永远"先左后右"，只改写入位置。
4. **空树没有特判**：`root == NULL` 时如果照样 `q[tail++] = root`，出队后访问 `t->val` 会崩溃。
5. **把 `returnColumnSizes` 当成 `int*` 直接写**：`returnColumnSizes[i] = sz;` 是错的，要先 `malloc` 一个 `cols` 数组，再 `*returnColumnSizes = cols;`。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 层序遍历 + 奇数层反转 | O(n) | O(n) | ⭐⭐ | 最好想 |
| 层序遍历 + 直接写到倒序位置 | O(n) | O(n) | ⭐⭐ | 推荐，代码最短 |

---

## 🔗 举一反三

- **102. 二叉树的层序遍历**：本题去掉"锯齿"就是它。
- **107. 二叉树的层序遍历 II**：从最底层往上输出，同样是"层序遍历 + 调整存放位置"。
- **199. 二叉树的右视图**：每层只取最后一个结点。
- **思考题**：如果要求"每 3 层换一次方向"，代码里只需要改哪一行？
