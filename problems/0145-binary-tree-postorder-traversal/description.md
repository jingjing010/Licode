给你一棵二叉树的根节点 `root` ，返回其节点值的 **后序遍历** 。

### 示例 1

```
    1
     \
      2
     /
    3
```

```
输入：root = [1,null,2,3]
输出：[3,2,1]
```

### 示例 2

```
          1
        /   \
       2     3
      / \     \
     4   5     8
        / \   /
       6   7 9
```

```
输入：root = [1,2,3,4,5,null,8,null,null,6,7,9]
输出：[4,6,7,5,2,9,8,3,1]
```

### 示例 3

```
输入：root = []
输出：[]
```

### 示例 4

```
输入：root = [1]
输出：[1]
```

### 提示

- 树中节点的数目在范围 `[0, 100]` 内
- `-100 <= Node.val <= 100`

**进阶：** 递归算法很简单，你可以通过迭代算法完成吗？

### 函数说明

```c
struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
};

int* postorderTraversal(struct TreeNode* root, int* returnSize);
```

- `struct TreeNode` 已由系统定义，**不要**在代码里重复定义
- `root`：二叉树的根结点，空树为 `NULL`
- 返回值：用 `malloc` 申请的数组，按后序顺序存放结点值
- `*returnSize`：返回数组的长度

### 自定义输入格式

```
[1,null,2,3]
```

只有 1 行：二叉树的层序表示，`null` 表示空结点，空树写作 `[]`。
