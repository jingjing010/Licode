# 450. 删除二叉搜索树中的节点 —— 小白详细题解

> 一句话题解：**先找到，再分三种情况删**——没孩子直接删；一个孩子让孩子顶上；两个孩子就请"右子树里最小的结点"（后继）来顶替。

---

## 📖 第一步：先读懂题目

在 BST 里删掉值为 `key` 的结点，删完后**仍然要是 BST**，返回新的根（根本身可能被删掉）。

示例 1：删除 3。

```
        5                    5                     5
       / \                  / \                   / \
      3   6      ==>       4   6       或        2   6
     / \   \              /     \                 \   \
    2   4   7            2       7                 4   7
```

两种结果都对：中序遍历都是 `2,4,5,6,7`。所以本 OJ **不比较树的形状**，而是检查你返回的树是不是合法 BST、结点是不是恰好少了 `key`，通过后输出中序遍历。

**几个需要注意的细节：**

1. `key` 可能**不在树里**（示例 2），这时树保持不变。
2. 树可能为空（示例 3）。
3. 被删的可能是**根**，所以函数要返回新的根，而不是总返回原来的 `root`。
4. 结点最多 10⁴ 个，链状树深度可达 10⁴。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. "返回新子树的根"式递归

修改树结构时最好用的写法：

```c
root->left = deleteNode(root->left, key);
```

意思是："把左子树删完以后的**新根**接回到 `root->left`"。这样左子树的根即使被删了、换成了别的结点，父结点也自动接上了，不需要单独记录"父结点"。

### 2. 释放结点

被删的结点是 `malloc` 出来的，删掉后可以 `free` 它。注意 **先保存好要用的指针再 `free`**，`free` 之后就不能再访问 `root->left` 之类的成员了。

### 3. BST 的后继

结点 x 的**后继**是比 x 大的结点里最小的那个，也就是 **x 右子树里最左边的结点**：先往右走一步，再一路向左走到底。后继没有左孩子（否则它就不是最左的了）。

---

## 💡 第三步：思路一 —— 拿出所有值，去掉 key，重新建一棵平衡 BST

### 思路

最"暴力"但一定正确的办法：

1. 中序遍历把所有值按从小到大存进数组，跳过 `key`。
2. 用第 108 题的方法把**有序数组**建成一棵 BST：取中间的数做根，左半边建左子树，右半边建右子树。

这样完全不需要思考"怎么删"，缺点是 O(n)，而且把整棵树都重建了。

### 手动模拟（示例 1）

| 步骤 | 结果 |
|---|---|
| 中序遍历并跳过 3 | `[2,4,5,6,7]` |
| 中间的 5 做根 | 左半 `[2,4]`，右半 `[6,7]` |
| `[2,4]` 中间取 2（下标 (0+1)/2=0） | 2 的右孩子 4 |
| `[6,7]` 中间取 6 | 6 的右孩子 7 |

得到 `[5,2,6,null,4,null,7]`，正是示例里的另一个正确答案。

### 代码

```c
// 中序遍历收集值，跳过 key
void collect(struct TreeNode* node, int key, int* vals, int* n) {
    if (node == NULL) return;
    collect(node->left, key, vals, n);
    if (node->val != key) vals[(*n)++] = node->val;
    collect(node->right, key, vals, n);
}

// 用有序数组 vals[l..r] 建平衡 BST
struct TreeNode* buildBST(int* vals, int l, int r) {
    if (l > r) return NULL;
    int mid = (l + r) / 2;
    struct TreeNode* node = (struct TreeNode*)malloc(sizeof(struct TreeNode));
    node->val = vals[mid];
    node->left = buildBST(vals, l, mid - 1);
    node->right = buildBST(vals, mid + 1, r);
    return node;
}

struct TreeNode* deleteNode(struct TreeNode* root, int key) {
    int* vals = (int*)malloc(sizeof(int) * 10000);   // 结点最多 10^4 个
    int n = 0;
    collect(root, key, vals, &n);
    struct TreeNode* res = buildBST(vals, 0, n - 1);
    free(vals);
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n)**：遍历一次 + 建树一次。
- **空间复杂度 O(n)**：数组和新建的结点。

---

## 🚀 第四步：思路二 —— 找到后分三种情况删除（O(h)）

### 思路

`deleteNode(root, key)` 返回"在以 `root` 为根的子树中删掉 `key` 之后的新根"。

1. `root` 为空：返回 `NULL`（没找到）。
2. `key < root->val`：去左子树删，`root->left = deleteNode(root->left, key)`，返回 `root`。
3. `key > root->val`：去右子树删，同理。
4. `key == root->val`：要删的就是 `root`：

| 情况 | 做法 |
|---|---|
| 没有左孩子 | 用右孩子顶替（右孩子也可能为空，正好覆盖"叶子"的情况） |
| 没有右孩子 | 用左孩子顶替 |
| 左右都有 | 找后继 `s`（右子树最左结点），把 `s` 从原位置摘下来，让它坐到 `root` 的位置上 |

"摘下后继"：`s` 没有左孩子，所以它的父结点 `parent` 只要把 `parent->left` 改成 `s->right` 就行。特殊情况是 `s` 就是 `root->right`（右孩子本身没有左孩子），这时不用摘，直接让它接上 `root->left`。

### 手动模拟（删除 5：`[5,3,8,null,null,6,9,null,7]`）

```
      5                      6
     / \                    / \
    3   8        ==>       3   8
       / \                    / \
      6   9                  7   9
       \
        7
```

| 步骤 | 说明 |
|---|---|
| 找到 5，左右都有 | 需要后继 |
| 从 8 一路向左 | 后继 s = 6，parent = 8 |
| 摘下 6 | `8->left = 6->right`，即 7 |
| 6 顶替 5 | `6->left = 3`，`6->right = 8` |
| 返回 6 | 新根 |

### 代码

```c
struct TreeNode* deleteNode(struct TreeNode* root, int key) {
    if (root == NULL) return NULL;                       // 没找到 key
    if (key < root->val) {
        root->left = deleteNode(root->left, key);        // 在左子树删，接回新的左子树
        return root;
    }
    if (key > root->val) {
        root->right = deleteNode(root->right, key);      // 在右子树删
        return root;
    }

    // 走到这里：root 就是要删的结点
    struct TreeNode* rep;                                // 顶替 root 的结点
    if (root->left == NULL) {
        rep = root->right;                               // 没有左孩子：右孩子顶上（可能为 NULL）
    } else if (root->right == NULL) {
        rep = root->left;                                // 没有右孩子：左孩子顶上
    } else {
        struct TreeNode* parent = root;                  // 找后继：右子树的最左结点
        rep = root->right;
        while (rep->left != NULL) {
            parent = rep;
            rep = rep->left;
        }
        if (parent != root) {                            // 后继不是 root 的右孩子时，先把它摘下来
            parent->left = rep->right;                   //   它的右子树接到它原来的位置
            rep->right = root->right;                    //   它接管 root 的右子树
        }
        rep->left = root->left;                          // 它接管 root 的左子树
    }
    free(root);                                          // 释放被删结点
    return rep;
}
```

### 复杂度分析

- **时间复杂度 O(h)**：找结点 O(h)，找后继也只往下走，合计 O(h)。
- **空间复杂度 O(h)**：递归栈。

---

## ⚠️ 第五步：小白常见错误

1. **只递归不接回**：

   ```c
   if (key < root->val) deleteNode(root->left, key);   // ❌ 返回的新左子树被丢掉了
   ```

   左孩子正好是被删结点时，`root->left` 还指着已经 `free` 的内存。
2. **总是返回原来的 `root`**：如果被删的是根，原来的 `root` 已经不在树里了（甚至被释放了）。
3. **后继是 `root->right` 本身时还执行 `rep->right = root->right`**：这会让 `rep->right` 指向自己，形成环。所以要区分 `parent != root` 的情况。
4. **先 `free(root)` 再读 `root->left`**：释放后再访问是未定义行为，可能"碰巧"能跑，但随时会出错。
5. **用值替换的方法时忘了删后继**：有人把后继的值复制到 `root->val` 后，忘了再到右子树里把后继删掉，结果树里出现两个相同的值。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 取出所有值重建平衡 BST | O(n) | O(n) | ⭐⭐ | 保底做法，不推荐面试 |
| 递归查找 + 后继顶替 | O(h) | O(h) | ⭐⭐⭐ | 推荐，满足进阶要求 |

---

## 🔗 举一反三

- **701. 二叉搜索树中的插入操作**：删除的"兄弟题"，比删除简单得多。
- **669. 修剪二叉搜索树**：一次删掉一个区间以外的所有结点。
- **思考题**：两个孩子时用**前驱**（左子树最大的结点）顶替行不行？代码要改哪几处？
