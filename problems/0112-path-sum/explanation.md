# 112. 路径总和 —— 小白详细题解

> 这道题练的是"**一边往下走，一边把信息传下去**"的递归写法，以及对"叶子"的准确判断。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 从根出发，一直走到某个**叶子**（左右孩子都为空的结点），把路上的数加起来。有没有哪一条这样的路，加起来正好是 `targetSum`？

示例 1：`targetSum = 22`

```
          5
         / \
        4   8
       /   / \
      11  13  4
     /  \      \
    7    2      1
```

| 根到叶子的路径 | 和 | 等于 22 吗 |
|---|---|---|
| 5 → 4 → 11 → 7 | 27 | ❌ |
| 5 → 4 → 11 → 2 | 22 | ✅ |
| 5 → 8 → 13 | 26 | ❌ |
| 5 → 8 → 4 → 1 | 18 | ❌ |

存在一条，答案是 `true`。

**几个需要注意的细节：**

1. 路径必须**走到叶子**。树 `[1,2]`、`targetSum = 1`：根结点 1 自己的和就是 1，但它有左孩子，不是叶子，所以答案是 `false`。
2. 结点值可以是**负数**，所以不能"和已经超过 target 就停止往下走"。
3. 空树没有任何路径，**一律返回 `false`**（即使 `targetSum = 0`）。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 递归参数"往下传"

前面几题的递归是"从下往上要答案"（比如高度）。这题需要把"还差多少"传给孩子：

```c
hasPathSum(root->left, targetSum - root->val)
```

每一层的 `targetSum` 都是自己的一份拷贝（值传递），改了不会影响别的分支——正好是我们想要的。

### 2. 短路求值 `||`

```c
return hasPathSum(root->left, rest) || hasPathSum(root->right, rest);
```

左子树已经找到了，就**不会**再去找右子树。

### 3. 判断叶子

```c
root->left == NULL && root->right == NULL
```

---

## 💡 第三步：思路一 —— 递归（DFS，目标值逐层相减）

### 思路

站在结点 `root` 上：

1. 空树：没有路径，返回 `false`。
2. 叶子：路径到头了，看 `root->val == targetSum`。
3. 否则：剩下要凑的数是 `rest = targetSum - root->val`，去左子树或右子树里找"和为 `rest` 的路径"，任意一边找到就行。

### 手动模拟（示例 1，只看成功的那条分支）

| 结点 | 进来时的 target | 是叶子吗 | 传给孩子的 rest |
|---|---|---|---|
| 5 | 22 | 否 | 17 |
| 4 | 17 | 否 | 13 |
| 11 | 13 | 否 | 2 |
| 7 | 2 | 是，7 ≠ 2 | `false` |
| 2 | 2 | 是，2 == 2 | **`true`** |

### 代码

```c
bool hasPathSum(struct TreeNode* root, int targetSum) {
    if (root == NULL) return false;                     // 空树没有路径
    if (root->left == NULL && root->right == NULL)      // 叶子：看最后一个数是不是正好凑齐
        return root->val == targetSum;
    int rest = targetSum - root->val;                   // 还差多少
    return hasPathSum(root->left, rest) || hasPathSum(root->right, rest);
}
```

### 复杂度分析

- **时间复杂度 O(n)**：每个结点最多访问一次。
- **空间复杂度 O(h)**：递归栈，最坏（链）是 O(n)。

---

## 🚀 第四步：思路二 —— 迭代（用栈同时保存结点和当前和）

### 思路

不用递归，就自己用栈模拟。关键是：栈里不仅要存**结点**，还要存"**从根走到这个结点时的路径和**"，用两个平行数组即可：

1. 压入 `(root, root->val)`。
2. 弹出 `(node, sum)`：如果是叶子并且 `sum == targetSum`，返回 `true`。
3. 否则把孩子压栈，和为 `sum + 孩子的值`。
4. 栈空了还没找到，返回 `false`。

### 手动模拟（示例 2：`[1,2,3]`, target = 5）

| 步骤 | 弹出 | 是叶子？sum | 压入 |
|---|---|---|---|
| 1 | (1, 1) | 否 | (2, 3)、(3, 4) |
| 2 | (3, 4) | 是，4 ≠ 5 | — |
| 3 | (2, 3) | 是，3 ≠ 5 | — |
| 4 | 栈空 | | 返回 `false` |

### 代码

```c
bool hasPathSum(struct TreeNode* root, int targetSum) {
    if (root == NULL) return false;
    // 每个结点最多入栈一次，最多 5000 个
    struct TreeNode** st = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * 5000);
    int* sums = (int*)malloc(sizeof(int) * 5000);     // sums[i]：根到 st[i] 的路径和
    int top = 0;
    st[top] = root; sums[top] = root->val; top++;
    bool found = false;
    while (top > 0) {
        top--;
        struct TreeNode* node = st[top];
        int sum = sums[top];
        if (node->left == NULL && node->right == NULL && sum == targetSum) {
            found = true;                              // 找到了
            break;
        }
        if (node->right) { st[top] = node->right; sums[top] = sum + node->right->val; top++; }
        if (node->left)  { st[top] = node->left;  sums[top] = sum + node->left->val;  top++; }
    }
    free(st);
    free(sums);
    return found;
}
```

### 复杂度分析

- **时间复杂度 O(n)**。
- **空间复杂度 O(n)**：栈。

---

## ⚠️ 第五步：小白常见错误

1. **把空结点当成路径终点**：
   ```c
   if (root == NULL) return targetSum == 0;   // ❌
   ```
   树 `[1,2]`、target = 1：根的右孩子是空，`targetSum - 1 == 0`，会错误地返回 `true`。终点必须是叶子。
2. **空树 + target 为 0 返回 true**：示例 3 明确空树返回 `false`。
3. **因为有负数，"剪枝"写错**：`if (rest < 0) return false;` 这种"超了就停"的优化只在全是正数时成立，本题会漏掉答案。
4. **在叶子处多减了一次**：先 `targetSum -= root->val`，再判断 `root->val == targetSum`，相当于减了两次。要么比较 `rest == 0`，要么比较 `root->val == targetSum`，只选一种。
5. **迭代时用一个全局 `sum` 变量**：不同分支共用一个和，回退时没有减回去，答案就乱了。每个结点要配一份自己的路径和。

---

## 📊 第六步：两种方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 递归 DFS | O(n) | O(h) | ⭐ | **首选**，四行搞定 |
| 栈迭代 | O(n) | O(n) | ⭐⭐ | 学会"结点 + 附加信息"一起入栈 |

---

## 🔗 举一反三

- **113. 路径总和 II**：不只判断有没有，还要把所有路径都找出来（回溯）。
- **437. 路径总和 III**：路径不必从根开始、不必到叶子结束（前缀和）。
- **129. 求根节点到叶节点数字之和**：同样是"往下传一个值"的递归。
- **思考题**：如果要求路径上结点数最少的那条满足条件的路径，用 DFS 还是 BFS 更合适？
