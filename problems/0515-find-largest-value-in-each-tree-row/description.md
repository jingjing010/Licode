给定一棵二叉树的根节点 `root` ，请找出该二叉树中每一层的最大值。

### 示例 1

```
          1
         / \
        3   2
       / \   \
      5   3   9
```

```
输入：root = [1,3,2,5,3,null,9]
输出：[1,3,9]
```

### 示例 2

```
输入：root = [1,2,3]
输出：[1,3]
```

### 提示

- 二叉树的节点个数的范围是 `[0, 10^4]`
- `-2^31 <= Node.val <= 2^31 - 1`

### 函数说明

```c
struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
};

int* largestValues(struct TreeNode* root, int* returnSize);
```

- `struct TreeNode` 已由系统定义，**不要**在代码里重复定义
- `root`：二叉树的根结点，空树为 `NULL`
- 返回值：用 `malloc` 申请的数组，第 `i` 个元素是第 `i` 层（根为第 0 层）的最大值
- `*returnSize`：返回数组的长度（即层数，空树为 0）

### 自定义输入格式

```
[1,3,2,5,3,null,9]
```

只有 1 行：二叉树的层序表示，`null` 表示空结点，空树写作 `[]`。
