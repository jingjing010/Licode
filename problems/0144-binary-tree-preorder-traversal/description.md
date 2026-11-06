给你二叉树的根节点 `root` ，返回它节点值的 **前序** 遍历。

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
输出：[1,2,3]
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
输出：[1,2,4,5,6,7,3,8,9]
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

- 树中节点数目在范围 `[0, 100]` 内
- `-100 <= Node.val <= 100`

**进阶：** 递归算法很简单，你可以通过迭代算法完成吗？

### 函数说明

```c
struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
};

int* preorderTraversal(struct TreeNode* root, int* returnSize);
```

- `struct TreeNode` 已由系统定义，**不要**在代码里重复定义
- `root`：二叉树的根结点，空树为 `NULL`
- 返回值：用 `malloc` 申请的数组，按前序顺序存放结点值
- `*returnSize`：返回数组的长度

### 自定义输入格式

```
[1,null,2,3]
```

只有 1 行：二叉树的层序表示，`null` 表示空结点，空树写作 `[]`。
