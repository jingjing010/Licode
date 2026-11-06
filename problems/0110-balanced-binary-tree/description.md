给定一个二叉树，判断它是否是 **平衡二叉树** 。

**平衡二叉树** 是指该树所有节点的左右子树的高度相差不超过 1。

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
输出：true
```

### 示例 2

```
          1
         / \
        2   2
       / \
      3   3
     / \
    4   4
```

```
输入：root = [1,2,2,3,3,null,null,4,4]
输出：false
```

### 示例 3

```
输入：root = []
输出：true
```

### 提示

- 树中的节点数在范围 `[0, 5000]` 内
- `-10^4 <= Node.val <= 10^4`

### 函数说明

```c
struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
};

bool isBalanced(struct TreeNode* root);
```

- `struct TreeNode` 已由系统定义，**不要**在代码里重复定义
- `root`：二叉树的根结点，空树为 `NULL`
- 返回值：是平衡二叉树返回 `true`，否则返回 `false`

### 自定义输入格式

```
[3,9,20,null,null,15,7]
```

只有 1 行：二叉树的层序表示，`null` 表示空结点，空树写作 `[]`。
