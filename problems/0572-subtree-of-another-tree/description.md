给你两棵二叉树 `root` 和 `subRoot` 。检验 `root` 中是否包含和 `subRoot` 具有相同结构和节点值的子树。如果存在，返回 `true` ；否则，返回 `false` 。

二叉树 `tree` 的一棵子树包括 `tree` 的某个节点和这个节点的所有后代节点。`tree` 也可以看做它自身的一棵子树。

### 示例 1

```
  root:      3          subRoot:    4
            / \                    / \
           4   5                  1   2
          / \
         1   2
```

```
输入：root = [3,4,5,1,2], subRoot = [4,1,2]
输出：true
```

### 示例 2

```
  root:      3          subRoot:    4
            / \                    / \
           4   5                  1   2
          / \
         1   2
            /
           0
```

```
输入：root = [3,4,5,1,2,null,null,null,null,0], subRoot = [4,1,2]
输出：false
```

### 提示

- `root` 树上的节点数量范围是 `[1, 2000]`
- `subRoot` 树上的节点数量范围是 `[1, 1000]`
- `-10^4 <= root.val <= 10^4`
- `-10^4 <= subRoot.val <= 10^4`

### 函数说明

```c
struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
};

bool isSubtree(struct TreeNode* root, struct TreeNode* subRoot);
```

- `struct TreeNode` 已由系统定义，**不要**在代码里重复定义
- `root`、`subRoot`：两棵二叉树的根结点（都至少有 1 个结点）
- 返回值：`root` 中存在与 `subRoot` 完全相同的子树返回 `true`，否则返回 `false`

### 自定义输入格式

```
[3,4,5,1,2]
[4,1,2]
```

共 2 行：分别是 `root` 和 `subRoot` 的层序表示，`null` 表示空结点。
