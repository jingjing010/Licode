# 98. 验证二叉搜索树 —— 小白详细题解

> 这道题有一个经典陷阱：**只和孩子比较是不够的**。弄懂它，你就真正理解了二叉搜索树（BST）的定义。

---

## 📖 第一步：先读懂题目

**二叉搜索树**：对每个结点来说，**整个**左子树里的数都比它小，**整个**右子树里的数都比它大。

示例 2 `[5,1,4,null,null,3,6]`：

```
    5
   / \
  1   4      ← 4 在 5 的右子树里，却比 5 小 → 不合法
     / \
    3   6
```

再看一个更隐蔽的例子 `[5,4,6,null,null,3,7]`：

```
    5
   / \
  4   6
     / \
    3   7    ← 3 < 6，作为 6 的左孩子没问题；但 3 在 5 的右子树里，3 < 5 → 不合法！
```

| 检查方式 | 结论 |
|---|---|
| 只看"父 > 左孩子、父 < 右孩子" | 5>4 ✓、5<6 ✓、6>3 ✓、6<7 ✓ → 误判为 true ❌ |
| 看"整个子树" | 3 在 5 的右子树里但比 5 小 → **false** ✓ |

**几个需要注意的细节：**

1. 是**严格**小于/大于，有相等的值就不合法（`[1,1]` 是 false）。
2. 结点值可以是 `INT_MIN`（−2147483648）或 `INT_MAX`（2147483647），用 `int` 做边界会出问题。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. `long long` 和 `LLONG_MIN` / `LLONG_MAX`

`int` 的范围是 [−2³¹, 2³¹−1]，`long long` 是 [−2⁶³, 2⁶³−1]。如果用 `INT_MIN` 当"没有下界"，那么一个值恰好为 `INT_MIN` 的结点就会被误判（`INT_MIN <= INT_MIN` 成立）。用 `long long` 的 `LLONG_MIN` 当初始下界，就不会和任何 `int` 值相等。

### 2. 带"额外信息"的递归

递归函数除了结点，还可以带上**从上面传下来的限制**，比如 `(node, low, high)`："这个结点的值必须在 `(low, high)` 之间"。

---

## 💡 第三步：思路一 —— 递归传上下界

### 思路

每个结点的值都被它的所有祖先限制在一个开区间 `(low, high)` 里：

- 根结点：`(-∞, +∞)`。
- 往**左**走：左子树都要比当前结点小 → 上界变成 `node->val`，下界不变。
- 往**右**走：右子树都要比当前结点大 → 下界变成 `node->val`，上界不变。

只要有一个结点不在自己的区间里，就不是 BST。

### 手动模拟（`[5,4,6,null,null,3,7]`）

| 结点 | 允许区间 | 在区间里吗？ |
|---|---|---|
| 5 | (−∞, +∞) | ✓ |
| 4 | (−∞, 5) | ✓ |
| 6 | (5, +∞) | ✓ |
| 3 | (5, 6) | ✗ → **false** |

### 代码

```c
// 判断以 node 为根的子树是否是 BST，且所有值都在开区间 (low, high) 内
bool check(struct TreeNode* node, long long low, long long high) {
    if (node == NULL) return true;                         // 空树是 BST
    if (node->val <= low || node->val >= high) return false;   // 超出允许范围
    // 左子树：上界收紧为 node->val；右子树：下界收紧为 node->val
    return check(node->left, low, node->val) && check(node->right, node->val, high);
}

bool isValidBST(struct TreeNode* root) {
    return check(root, LLONG_MIN, LLONG_MAX);   // 一开始没有限制
}
```

### 复杂度分析

- **时间复杂度 O(n)**：每个结点检查一次。
- **空间复杂度 O(h)**：递归栈。

---

## 🚀 第四步：思路二 —— 中序遍历必须严格递增

### 思路

BST 有一个非常漂亮的性质：**中序遍历（左 → 根 → 右）得到的序列一定是严格递增的**，反过来也成立。

所以只要做一次中序遍历（第 94 题），边遍历边和**上一个**访问的值比较：如果当前值 ≤ 上一个值，就不是 BST。

### 手动模拟（示例 2：`[5,1,4,null,null,3,6]`）

中序序列：`1, 5, 3, 4, 6`

| 当前值 | 上一个值 | 递增？ |
|---|---|---|
| 1 | 无 | ✓ |
| 5 | 1 | ✓ |
| 3 | 5 | ✗ → **false** |

### 代码

```c
bool isValidBST(struct TreeNode* root) {
    // 用数组模拟栈做中序遍历，结点最多 10^4 个
    struct TreeNode** stack = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * 10000);
    int top = 0;
    struct TreeNode* cur = root;
    bool hasPrev = false;      // 是否已经访问过结点（第一个结点没有"上一个"）
    int prev = 0;              // 上一个访问的值
    bool ok = true;

    while (cur != NULL || top > 0) {
        while (cur != NULL) {              // 一路向左压栈
            stack[top++] = cur;
            cur = cur->left;
        }
        cur = stack[--top];                // 弹出，访问
        if (hasPrev && cur->val <= prev) { // 不是严格递增
            ok = false;
            break;
        }
        hasPrev = true;
        prev = cur->val;
        cur = cur->right;                  // 转向右子树
    }

    free(stack);
    return ok;
}
```

> 💬 为什么要 `hasPrev`，而不是把 `prev` 初始化成 `INT_MIN`？因为第一个结点的值可能就是 `INT_MIN`，`INT_MIN <= INT_MIN` 会被误判为不合法。

### 复杂度分析

- **时间复杂度 O(n)**，**空间复杂度 O(h)**（栈）。

---

## ⚠️ 第五步：小白常见错误

1. **只和左右孩子比较**：
   ```c
   if (root->left && root->left->val >= root->val) return false;   // ❌ 不够
   ```
   `[5,4,6,null,null,3,7]` 会被误判为 true。
2. **用 `int` 做边界**：`check(root, INT_MIN, INT_MAX)`，遇到 `[2147483647]` 时 `val >= high` 成立，误判为 false。
3. **允许相等**：写成 `node->val < low || node->val > high`，`[1,1]` 会被误判为 true。题目要求**严格**大小关系。
4. **中序遍历时 `prev` 初始为 `INT_MIN`**：当最小结点就是 `INT_MIN` 时误判。用 `hasPrev` 标记，或者用 `long long prev = LLONG_MIN`。
5. **先把中序结果存进数组再检查，数组开小了**：结点有 10⁴ 个，开 100 个就越界了。

---

## 📊 第六步：两种方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 递归传上下界 | O(n) | O(h) | ⭐⭐ | 直接对应定义，最推荐 |
| 中序遍历判递增 | O(n) | O(h) | ⭐⭐ | 利用 BST 性质，很多 BST 题都用得上 |

---

## 🔗 举一反三

- **94. 二叉树的中序遍历**：思路二的基础。
- **230. 二叉搜索树中第 K 小的元素**：中序遍历的第 k 个就是答案。
- **99. 恢复二叉搜索树**：有两个结点被交换了，用中序遍历找出它们。
- **思考题**：如果题目允许左子树中出现**等于**根的值（≤），代码要改哪里？
