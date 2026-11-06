给定二叉树的根节点 `root` ，返回所有左叶子之和。

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
输出：24
解释：在这个二叉树中，有两个左叶子，分别是 9 和 15，所以返回 24
```

### 示例 2

```
输入：root = [1]
输出：0
```

### 提示

- 节点数在 `[1, 1000]` 范围内
- `-1000 <= Node.val <= 1000`

### 函数说明

```c
struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
};

int sumOfLeftLeaves(struct TreeNode* root);
```

- `struct TreeNode` 已由系统定义，**不要**在代码里重复定义
- `root`：二叉树的根结点（至少有 1 个结点）
- 返回值：所有左叶子的值之和（没有左叶子时为 0）

### 自定义输入格式

```
[3,9,20,null,null,15,7]
```

只有 1 行：二叉树的层序表示，`null` 表示空结点。
