给你二叉树的根节点 `root` ，返回其节点值的 **层序遍历** 。 （即逐层地，从左到右访问所有节点）。

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
输出：[[3],[9,20],[15,7]]
```

### 示例 2

```
输入：root = [1]
输出：[[1]]
```

### 示例 3

```
输入：root = []
输出：[]
```

### 提示

- 树中节点数目在范围 `[0, 2000]` 内
- `-1000 <= Node.val <= 1000`

### 函数说明

```c
struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
};

int** levelOrder(struct TreeNode* root, int* returnSize, int** returnColumnSizes);
```

- `struct TreeNode` 已由系统定义，**不要**在代码里重复定义
- `root`：二叉树的根结点，空树为 `NULL`
- 返回值：用 `malloc` 申请的二维数组，第 `i` 行是第 `i` 层从左到右的结点值
- `*returnSize`：返回的行数（即层数）
- `*returnColumnSizes`：你需要 `malloc` 一个长度为层数的 `int` 数组，第 `i` 个元素是第 `i` 层的结点个数，并把它的地址写进 `*returnColumnSizes`

### 自定义输入格式

```
[3,9,20,null,null,15,7]
```

只有 1 行：二叉树的层序表示，`null` 表示空结点，空树写作 `[]`。
