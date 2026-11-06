给定一个二叉树的根节点 `root` ，和一个整数 `targetSum` ，求该二叉树里节点值之和等于 `targetSum` 的 **路径** 的数目。

**路径** 不需要从根节点开始，也不需要在叶子节点结束，但是路径方向必须是向下的（只能从父节点到子节点）。

### 示例 1

```
          10
         /  \
        5    -3
       / \     \
      3   2    11
     / \   \
    3  -2   1
```

```
输入：root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8
输出：3
解释：和等于 8 的路径有 3 条：5 -> 3，5 -> 2 -> 1，-3 -> 11。
```

### 示例 2

```
输入：root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
输出：3
```

### 提示

- 二叉树的节点个数的范围是 `[0,1000]`
- `-10^9 <= Node.val <= 10^9`
- `-1000 <= targetSum <= 1000`

### 函数说明

```c
struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
};

int pathSum(struct TreeNode* root, int targetSum);
```

- `struct TreeNode` 已由系统定义，**不要**在代码里重复定义
- `root`：二叉树的根结点，空树为 `NULL`
- 返回值：满足条件的路径条数

### 自定义输入格式

```
[10,5,-3,3,2,null,11,3,-2,null,1]
8
```

第 1 行是二叉树的层序表示（`null` 表示空结点，空树写作 `[]`），第 2 行是 `targetSum`。
