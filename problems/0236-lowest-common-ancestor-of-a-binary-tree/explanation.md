# 236. 二叉树的最近公共祖先 —— 小白详细题解

> 最近公共祖先（LCA）是树上的经典问题。思路一"找两条路径再比较"非常直观；思路二的递归只有 6 行，但需要想清楚"递归函数返回的是什么"。

---

## 📖 第一步：先读懂题目

**祖先**：从根走到某个结点，路上经过的所有结点（**包括它自己**）都是它的祖先。
**最近公共祖先**：既是 p 的祖先、又是 q 的祖先的结点中，**最深**（离根最远）的那个。

示例树：

```
        3
      /   \
     5     1
    / \   / \
   6   2 0   8
      / \
     7   4
```

| p | q | p 的祖先 | q 的祖先 | 公共祖先 | 最近的 |
|---|---|---|---|---|---|
| 5 | 1 | 3, 5 | 3, 1 | 3 | **3** |
| 5 | 4 | 3, 5 | 3, 5, 2, 4 | 3, 5 | **5** |
| 7 | 4 | 3, 5, 2, 7 | 3, 5, 2, 4 | 3, 5, 2 | **2** |

**几个需要注意的细节：**

1. 一个结点可以是**自己的祖先**，所以示例 2 的答案是 5 本身。
2. `p`、`q` 是**结点指针**，比较时直接比较指针 `root == p`，不需要比较值。
3. 结点最多 10⁵ 个，树可能是一条很深的链。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 指针比较

`root == p` 比较的是**两个指针是否指向同一个结点**（地址相同）。本题值互不相同，比较 `root->val == p->val` 也可以，但比较指针更直接、更通用。

### 2. 返回指针的递归

递归函数返回 `struct TreeNode*`，可以用 `NULL` 表示"没找到"，用一个结点指针表示"找到了某个东西"。

### 3. 用数组保存路径

思路一中要把"从根到 p 的路径"存进数组，需要配合一个长度变量。找不到时要把刚加进去的结点**撤销**（回溯）。

---

## 💡 第三步：思路一 —— 分别求出两条路径，比较公共前缀

### 思路

1. 找出从根到 `p` 的路径 `pathP`，从根到 `q` 的路径 `pathQ`（都从根开始）。
2. 两条路径从头开始一起往后比较，**最后一个相同的结点**就是最近公共祖先。

找路径的方法（DFS + 回溯）：

- 把当前结点加入路径；
- 如果它就是目标，返回"找到了"；
- 否则去左子树找、去右子树找，任何一边找到就返回"找到了"；
- 两边都没有，把当前结点从路径里删掉（回溯），返回"没找到"。

### 手动模拟（p = 7, q = 4）

| 下标 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| pathP | 3 | 5 | 2 | 7 |
| pathQ | 3 | 5 | 2 | 4 |
| 相同？ | ✓ | ✓ | ✓ | ✗ |

最后一个相同的是下标 2 的结点 `2`。

### 代码

```c
// 在以 node 为根的子树里找 target；找到返回 true，并且 path[0..*len-1] 是从根到 target 的路径
bool findPath(struct TreeNode* node, struct TreeNode* target, struct TreeNode** path, int* len) {
    if (node == NULL) return false;
    path[(*len)++] = node;                                  // 先把自己加进路径
    if (node == target) return true;                        // 找到了
    if (findPath(node->left, target, path, len)) return true;
    if (findPath(node->right, target, path, len)) return true;
    (*len)--;                                               // 两边都没有：回溯，把自己删掉
    return false;
}

struct TreeNode* lowestCommonAncestor(struct TreeNode* root, struct TreeNode* p, struct TreeNode* q) {
    // 路径长度最多等于结点数 10^5
    struct TreeNode** pathP = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * 100000);
    struct TreeNode** pathQ = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * 100000);
    int lenP = 0, lenQ = 0;
    findPath(root, p, pathP, &lenP);
    findPath(root, q, pathQ, &lenQ);

    struct TreeNode* ans = root;                            // 根一定是公共祖先
    for (int i = 0; i < lenP && i < lenQ; i++) {
        if (pathP[i] != pathQ[i]) break;                    // 从这里开始分叉
        ans = pathP[i];                                     // 记录最后一个相同的结点
    }
    free(pathP);
    free(pathQ);
    return ans;
}
```

### 复杂度分析

- **时间复杂度 O(n)**：找两条路径各遍历一次树。
- **空间复杂度 O(n)**：两个路径数组 + 递归栈。

---

## 🚀 第四步：思路二 —— 一次递归（经典写法）

### 思路

定义 `lowestCommonAncestor(root, p, q)` 的含义为：**在以 `root` 为根的子树里**，

- 如果 p、q 都在里面，返回它们的 LCA；
- 如果只有其中一个在里面，返回那一个；
- 如果都不在，返回 `NULL`。

于是：

1. `root` 为空，返回 `NULL`；`root` 就是 p 或 q，返回 `root`（不管另一个在不在它下面，答案都是它或者它就是"找到的那一个"）。
2. 去左子树找，得到 `l`；去右子树找，得到 `r`。
3. `l`、`r` 都不为空：p、q 分别在两边，`root` 就是 LCA。
4. 只有一边不为空：两个都在那一边（返回值就是它们的 LCA），或者只找到了一个，原样往上传。

### 手动模拟（p = 5, q = 4）

| 调用 | 结果 | 原因 |
|---|---|---|
| LCA(5) | 返回 5 | 5 就是 p，直接返回 |
| LCA(1) | 左 LCA(0)=NULL，右 LCA(8)=NULL → NULL | 右边没有 p、q |
| LCA(3) | l = 5, r = NULL → 返回 5 | 只有左边找到 |

答案 5。注意我们根本没有往 5 的下面去找 4——因为不需要：q 若在 5 下面，答案就是 5；若不在，那右边一定能找到 q，答案是 3。

### 代码

```c
struct TreeNode* lowestCommonAncestor(struct TreeNode* root, struct TreeNode* p, struct TreeNode* q) {
    if (root == NULL) return NULL;                 // 空树：什么都没找到
    if (root == p || root == q) return root;       // 自己就是其中之一

    struct TreeNode* l = lowestCommonAncestor(root->left, p, q);    // 左子树的结果
    struct TreeNode* r = lowestCommonAncestor(root->right, p, q);   // 右子树的结果

    if (l != NULL && r != NULL) return root;       // p、q 分居两侧，root 就是 LCA
    return (l != NULL) ? l : r;                    // 只有一侧有结果，把它往上传
}
```

### 复杂度分析

- **时间复杂度 O(n)**：每个结点最多访问一次。
- **空间复杂度 O(h)**：递归栈，最坏 O(n)。

---

## ⚠️ 第五步：小白常见错误

1. **把 `p`、`q` 当成数值**：写成 `root->val == p` 会编译警告/出错。`p` 是指针，要么比较 `root == p`，要么比较 `root->val == p->val`。
2. **忘了"自己也是自己的祖先"**：示例 2 中若继续往 5 下面找、最后返回 3，就错了。
3. **路径法忘记回溯**：`findPath` 里两边都没找到却不执行 `(*len)--`，路径里会混进无关的结点。
4. **路径数组开太小**：链状树深度可达 10⁵，`struct TreeNode* path[1000]` 会越界。
5. **两边都找到时返回了 `l`**：应该返回 `root`，因为 p、q 分在两边，最近的公共祖先就是当前结点。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 两条路径找公共前缀 | O(n) | O(n) | ⭐⭐ | 思路直观，先写这个 |
| 一次递归 | O(n) | O(h) | ⭐⭐⭐ | 经典写法，面试必会 |

---

## 🔗 举一反三

- **235. 二叉搜索树的最近公共祖先**：利用 BST 的大小关系，从根往下走即可，不需要遍历整棵树。
- **1650. 二叉树的最近公共祖先 III**：结点带父指针，转化为"两个链表的相交点"（第 160 题）。
- **思考题**：如果有很多组 (p, q) 询问，每次都 O(n) 太慢，能否预处理后加速？（搜索"倍增法求 LCA"）
