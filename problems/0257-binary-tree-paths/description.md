给你一个二叉树的根节点 `root` ，按 **任意顺序** ，返回所有从根节点到叶子节点的路径。

**叶子节点** 是指没有子节点的节点。

### 示例 1

```
    1
   / \
  2   3
   \
    5
```

```
输入：root = [1,2,3,null,5]
输出：["1->2->5","1->3"]
```

### 示例 2

```
输入：root = [1]
输出：["1"]
```

### 提示

- 树中节点的数目在范围 `[1, 100]` 内
- `-100 <= Node.val <= 100`

### 函数说明

```c
struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
};

char** binaryTreePaths(struct TreeNode* root, int* returnSize);
```

- `struct TreeNode` 已由系统定义，**不要**在代码里重复定义
- `root`：二叉树的根结点（至少有 1 个结点）
- 返回值：用 `malloc` 申请的字符串数组，每个字符串是一条路径，格式如 `"1->2->5"`，每个字符串也要 `malloc` 且以 `'\0'` 结尾
- `*returnSize`：路径条数
- 路径可以按**任意顺序**返回（判题时会先把所有字符串排序再比较）

### 自定义输入格式

```
[1,2,3,null,5]
```

只有 1 行：二叉树的层序表示，`null` 表示空结点。
