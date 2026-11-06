给定一个二叉树 `root` ，返回其最大深度。

二叉树的 **最大深度** 是指从根节点到最远叶子节点的最长路径上的节点数。

### 示例 1

```
    3
   / \
  9  20
    /  \
   15   7
```

```
输入：root = [3,9,20,null,null,15,7]
输出：3
```

### 示例 2

```
输入：root = [1,null,2]
输出：2
```

### 提示

- 树中节点的数量在 `[0, 10^4]` 区间内。
- `-100 <= Node.val <= 100`

### 函数说明

```c
struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
};

int maxDepth(struct TreeNode* root);
```

- `struct TreeNode` 已由系统定义，**不要**在代码里重复定义
- `root`：二叉树的根结点，空树为 `NULL`
- 返回值：树的最大深度（空树为 0）

### 自定义输入格式

```
[3,9,20,null,null,15,7]
```

只有 1 行：二叉树的层序表示，`null` 表示空结点，空树写作 `[]`。
