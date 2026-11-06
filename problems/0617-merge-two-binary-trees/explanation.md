# 617. 合并二叉树 —— 小白详细题解

> "两棵树同步递归"的又一道经典题。关键一句话：**一边为空时，直接把另一边整棵拿过来。**

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 把两棵树叠在一起：两边都有结点的位置，值相加；只有一边有结点的位置，就用那一边的结点。

示例 1：

```
  root1:   1          root2:   2            合并后:    3
          / \                 / \                    / \
         3   2               1   3                  4   5
        /                     \   \                / \   \
       5                       4   7              5   4   7
```

| 位置 | root1 | root2 | 合并后 |
|---|---|---|---|
| 根 | 1 | 2 | 3 |
| 根.左 | 3 | 1 | 4 |
| 根.右 | 2 | 3 | 5 |
| 根.左.左 | 5 | 空 | 5 |
| 根.左.右 | 空 | 4 | 4 |
| 根.右.右 | 空 | 7 | 7 |

结果的层序表示 `[3,4,5,5,4,null,7]`。

**几个需要注意的细节：**

1. 两棵树都可能是空树；两棵都空，结果也是空树 `[]`。
2. 只有一边有结点时，这个结点**下面的整棵子树**都原样保留。
3. 结点数各最多 2000，值相加最多 2×10⁴，`int` 没问题。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 返回结构体指针

函数返回 `struct TreeNode*`，可以返回：

- 已有的结点（比如直接 `return root2;`），或
- 用 `malloc` 新建的结点。

本 OJ 和力扣都允许复用输入树的结点。

### 2. 用 `malloc` 新建结点

```c
struct TreeNode* node = (struct TreeNode*)malloc(sizeof(struct TreeNode));
node->val = 5;
node->left = NULL;      // malloc 的内存里是垃圾值，左右指针一定要手动置空或赋值
node->right = NULL;
```

### 3. 递归的返回值"接"到父结点上

```c
root1->left = mergeTrees(root1->left, root2->left);
```

递归函数返回合并后的左子树的根，把它挂到当前结点的 `left` 上。

---

## 💡 第三步：思路一 —— 递归（在 root1 上原地修改）

### 思路

1. 如果 `root1` 为空，合并结果就是 `root2`（可能也为空）。
2. 如果 `root2` 为空，合并结果就是 `root1`。
3. 两边都不空：把 `root2->val` 加到 `root1->val` 上，再递归合并左子树、右子树，把结果挂回 `root1`。
4. 返回 `root1`。

### 手动模拟（示例 1）

| 调用 merge(a, b) | 情况 | 做了什么 | 返回 |
|---|---|---|---|
| (1, 2) | 都不空 | 1+2=3，递归左右 | 结点 3 |
| (3, 1) | 都不空 | 3+1=4，递归左右 | 结点 4 |
| (5, 空) | b 空 | — | 结点 5（原样） |
| (空, 4) | a 空 | — | root2 中的结点 4 |
| (2, 3) | 都不空 | 2+3=5，递归左右 | 结点 5 |
| (空, 空) | a 空 | — | NULL |
| (空, 7) | a 空 | — | root2 中的结点 7 |

### 代码

```c
struct TreeNode* mergeTrees(struct TreeNode* root1, struct TreeNode* root2) {
    if (root1 == NULL) return root2;        // 一边为空：直接用另一边（整棵子树）
    if (root2 == NULL) return root1;
    root1->val += root2->val;               // 两边都有：值相加，存在 root1 上
    root1->left = mergeTrees(root1->left, root2->left);     // 合并左子树并挂回
    root1->right = mergeTrees(root1->right, root2->right);  // 合并右子树并挂回
    return root1;
}
```

### 复杂度分析

- **时间复杂度 O(min(n₁, n₂))**：只有两边都不空的位置才会继续递归，一边为空就直接返回了。
- **空间复杂度 O(min(h₁, h₂))**：递归栈。

---

## 🚀 第四步：思路二 —— 新建一棵树（不修改输入）

### 思路

思路一会改掉 `root1` 的内容。如果要求**不能修改输入**，就为每个"两边都有"的位置 `malloc` 一个新结点。一边为空的位置，仍然可以直接引用另一边的子树（只读不改，没问题）。

### 手动模拟（示例 2：`root1 = [1]`，`root2 = [1,2]`）

| 调用 | 情况 | 动作 |
|---|---|---|
| (1, 1) | 都不空 | 新建结点，值 2 |
| 左：(空, 2) | a 空 | 返回 root2 中的结点 2 |
| 右：(空, 空) | a 空 | 返回 NULL |

结果 `[2,2]`，`root1` 的值仍然是 1。

### 代码

```c
struct TreeNode* mergeTrees(struct TreeNode* root1, struct TreeNode* root2) {
    if (root1 == NULL) return root2;
    if (root2 == NULL) return root1;
    struct TreeNode* node = (struct TreeNode*)malloc(sizeof(struct TreeNode));
    node->val = root1->val + root2->val;                    // 新结点的值
    node->left = mergeTrees(root1->left, root2->left);      // 递归得到左右子树
    node->right = mergeTrees(root1->right, root2->right);
    return node;
}
```

### 复杂度分析

- **时间复杂度 O(min(n₁, n₂))**。
- **空间复杂度 O(min(n₁, n₂))**：新建的结点，加上递归栈。

---

## ⚠️ 第五步：小白常见错误

1. **一边为空时还往下递归**：
   ```c
   if (root1 == NULL && root2 == NULL) return NULL;
   int v = root1->val + root2->val;   // ❌ 只有一边为空时崩溃
   ```
   要先处理"只有一边为空"的情况。
2. **递归结果没有挂回去**：只写了 `mergeTrees(root1->left, root2->left);`，没有赋值给 `root1->left`。当 `root1->left` 为空、`root2->left` 不空时，`root2` 的那棵子树就丢了。
3. **新建结点没有初始化左右指针**：`malloc` 出来的 `left`、`right` 是随机值，打印时会访问非法内存。
4. **返回了局部变量的地址**：`struct TreeNode node; return &node;` 函数返回后这块内存就失效了，必须 `malloc`。
5. **两棵都为空时返回了一个值为 0 的新结点**：结果会多出一个 `0`，应该返回 `NULL`。

---

## 📊 第六步：两种方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 原地修改 root1 | O(min(n₁,n₂)) | O(h) | ⭐ | **首选**，最省空间 |
| 新建结点 | O(min(n₁,n₂)) | O(min(n₁,n₂)) | ⭐ | 不允许修改输入时用 |

> 也可以用队列做 BFS：队列里放"一对结点"，两边都不空就相加，再处理它们的孩子；如果 `root1` 某一边的孩子为空，直接把 `root2` 对应的孩子挂上去。

---

## 🔗 举一反三

- **100. 相同的树**、**101. 对称二叉树**：同样是"两棵树同步递归"。
- **226. 翻转二叉树**：递归时把返回值挂回父结点。
- **思考题**：如果合并规则改成"重叠时取较大值"，或者"只保留两边都有的结点"，代码要怎么改？
