给定一个二叉树，找出其最小深度。

最小深度是从根节点到最近叶子节点的最短路径上的节点数量。

**说明：** 叶子节点是指没有子节点的节点。

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
输出：2
```

### 示例 2

```
输入：root = [2,null,3,null,4,null,5,null,6]
输出：5
```

### 提示

- 树中节点数的范围在 `[0, 10^5]` 内
- `-1000 <= Node.val <= 1000`

### 函数说明

```c
struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
};

int minDepth(struct TreeNode* root);
```

- `struct TreeNode` 已由系统定义，**不要**在代码里重复定义
- `root`：二叉树的根结点，空树为 `NULL`
- 返回值：树的最小深度（空树为 0）

### 自定义输入格式

```
[3,9,20,null,null,15,7]
```

只有 1 行：二叉树的层序表示，`null` 表示空结点，空树写作 `[]`。
