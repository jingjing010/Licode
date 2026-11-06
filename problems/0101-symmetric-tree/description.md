给你一个二叉树的根节点 `root` ， 检查它是否轴对称。

### 示例 1

```
      1
    /   \
   2     2
  / \   / \
 3   4 4   3
```

```
输入：root = [1,2,2,3,4,4,3]
输出：true
```

### 示例 2

```
    1
   / \
  2   2
   \   \
    3   3
```

```
输入：root = [1,2,2,null,3,null,3]
输出：false
```

### 提示

- 树中节点数目在范围 `[1, 1000]` 内
- `-100 <= Node.val <= 100`

**进阶：** 你可以运用递归和迭代两种方法解决这个问题吗？

### 函数说明

```c
struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
};

bool isSymmetric(struct TreeNode* root);
```

- `struct TreeNode` 已由系统定义，**不要**在代码里重复定义
- `root`：二叉树的根结点（至少有 1 个结点）
- 返回值：轴对称返回 `true`，否则返回 `false`

### 自定义输入格式

```
[1,2,2,3,4,4,3]
```

只有 1 行：二叉树的层序表示，`null` 表示空结点。输出 `true` 或 `false`。
