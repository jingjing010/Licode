给定两个整数数组 `preorder` 和 `inorder` ，其中 `preorder` 是二叉树的**先序遍历**， `inorder` 是同一棵树的**中序遍历**，请构造二叉树并返回其根节点。

### 示例 1

```
    3
   / \
  9  20
    /  \
   15   7
```

```
输入: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
输出: [3,9,20,null,null,15,7]
```

### 示例 2

```
输入: preorder = [-1], inorder = [-1]
输出: [-1]
```

### 提示

- `1 <= preorder.length <= 3000`
- `inorder.length == preorder.length`
- `-3000 <= preorder[i], inorder[i] <= 3000`
- `preorder` 和 `inorder` 均 **无重复** 元素
- `inorder` 均出现在 `preorder`
- `preorder` **保证** 为二叉树的前序遍历序列
- `inorder` **保证** 为二叉树的中序遍历序列

### 函数说明

```c
struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
};

struct TreeNode* buildTree(int* preorder, int preorderSize, int* inorder, int inorderSize);
```

- `struct TreeNode` 已由系统定义，**不要**在代码里重复定义
- `preorder`、`inorder`：前序、中序遍历数组，`preorderSize`、`inorderSize` 为它们的长度（两者相等）
- 返回值：构造出的树的根结点，每个结点都要用 `malloc` 申请

### 自定义输入格式

```
[3,9,20,15,7]
[9,3,15,20,7]
```

第 1 行是 `preorder`，第 2 行是 `inorder`。输出为构造出的树的层序表示。
