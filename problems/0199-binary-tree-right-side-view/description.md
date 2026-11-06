给定一个二叉树的 **根节点** `root`，想象自己站在它的右侧，按照从顶部到底部的顺序，返回从右侧所能看到的节点值。

### 示例 1

```
    1        <---
   / \
  2   3      <---
   \   \
    5   4    <---
```

```
输入：root = [1,2,3,null,5,null,4]
输出：[1,3,4]
```

### 示例 2

```
      1      <---
     / \
    2   3    <---
   /
  4          <---
 /
5            <---
```

```
输入：root = [1,2,3,4,null,null,null,5]
输出：[1,3,4,5]
```

### 示例 3

```
输入：root = [1,null,3]
输出：[1,3]
```

### 示例 4

```
输入：root = []
输出：[]
```

### 提示

- 二叉树的节点个数的范围是 `[0,100]`
- `-100 <= Node.val <= 100`

### 函数说明

```c
struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
};

int* rightSideView(struct TreeNode* root, int* returnSize);
```

- `struct TreeNode` 已由系统定义，**不要**在代码里重复定义
- `root`：二叉树的根结点，空树为 `NULL`
- 返回值：用 `malloc` 申请的数组，从上到下存放每层最右边结点的值
- `*returnSize`：返回数组的长度（即树的层数）

### 自定义输入格式

```
[1,2,3,null,5,null,4]
```

只有 1 行：二叉树的层序表示，`null` 表示空结点，空树写作 `[]`。
