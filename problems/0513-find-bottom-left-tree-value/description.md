给定一个二叉树的 **根节点** `root`，请找出该二叉树的 **最底层 最左边** 节点的值。

假设二叉树中至少有一个节点。

### 示例 1

```
    2
   / \
  1   3
```

```
输入：root = [2,1,3]
输出：1
```

### 示例 2

```
        1
       / \
      2   3
     /   / \
    4   5   6
       /
      7
```

```
输入：root = [1,2,3,4,null,5,6,null,null,7]
输出：7
```

### 提示

- 二叉树的节点个数的范围是 `[1, 10^4]`
- `-2^31 <= Node.val <= 2^31 - 1`

### 函数说明

```c
struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
};

int findBottomLeftValue(struct TreeNode* root);
```

- `struct TreeNode` 已由系统定义，**不要**在代码里重复定义
- `root`：二叉树的根结点（至少有 1 个结点）
- 返回值：最底层最左边结点的值

### 自定义输入格式

```
[1,2,3,4,null,5,6,null,null,7]
```

只有 1 行：二叉树的层序表示，`null` 表示空结点。
