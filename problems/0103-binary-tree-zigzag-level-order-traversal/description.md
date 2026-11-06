给你二叉树的根节点 `root` ，返回其节点值的 **锯齿形层序遍历** 。（即先从左往右，再从右往左进行下一层遍历，以此类推，层与层之间交替进行）。

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
输出：[[3],[20,9],[15,7]]
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
- `-100 <= Node.val <= 100`

### 函数说明

```c
struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
};

int** zigzagLevelOrder(struct TreeNode* root, int* returnSize, int** returnColumnSizes);
```

- `struct TreeNode` 已由系统定义，**不要**在代码中重复定义
- `root`：二叉树的根结点，可能为 `NULL`
- 返回值：`malloc` 出来的二维数组，第 `i` 行是第 `i` 层（锯齿顺序）的结点值
- `*returnSize`：写入层数
- `*returnColumnSizes`：写入一个 `malloc` 出来的数组，第 `i` 个元素是第 `i` 层的结点个数

### 自定义输入格式

```
[3,9,20,null,null,15,7]
```

只有 1 行：二叉树的层序表示（`null` 表示空结点）。
