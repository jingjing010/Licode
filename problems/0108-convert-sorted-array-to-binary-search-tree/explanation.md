# 108. 将有序数组转换为二叉搜索树 —— 小白详细题解

> 这是第一道需要你**自己 `malloc` 结点、亲手造一棵树**的题。核心思想是"分治"：选中间当根，两边各自去造子树。

---

## 📖 第一步：先读懂题目

给你一个**升序**数组，用它的所有元素造一棵二叉搜索树（BST），并且要**平衡**：每个结点左右子树的高度差不超过 1。

示例 1 `nums = [-10,-3,0,5,9]`，两种合法答案：

```
      0                 0
     / \               / \
   -3   9            -10   5
   /   /               \    \
 -10  5                -3    9
```

不合法的例子——直接把数组串成一条链：

```
-10
   \
   -3
     \
      0        ← 是 BST，但根的左子树高度 0、右子树高度 4，不平衡
       \
        5
         \
          9
```

**几个需要注意的细节：**

1. 答案**不唯一**。本 OJ 会检查你的树是否"用了 nums 的全部元素、是 BST、并且平衡"，都满足就输出 `true`。
2. 每个结点都要自己 `malloc`，并且**记得把 `left`、`right` 设好**（叶子要设为 `NULL`）。
3. 数组严格递增，没有重复元素。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 用 `malloc` 创建结点

```c
struct TreeNode* node = (struct TreeNode*)malloc(sizeof(struct TreeNode));
node->val = 5;
node->left = NULL;     // malloc 出来的内存里是随机值，一定要手动初始化！
node->right = NULL;
```

### 2. 用下标区间表示"子数组"

C 语言里不方便"切出"一个子数组，但可以用两个下标 `[lo, hi]` 表示"`nums` 中从 `lo` 到 `hi` 这一段"，不需要复制数据。

### 3. 求中点防溢出

`mid = lo + (hi - lo) / 2` 和 `(lo + hi) / 2` 结果一样，但前者在 `lo + hi` 很大时不会溢出，是个好习惯。

---

## 💡 第三步：思路一 —— 分治：选中间元素当根

### 思路

1. BST 的中序遍历是升序的，所以 `nums` 就是目标树的中序遍历。不管选谁当根，它**左边的元素**都必须进左子树，**右边的元素**都必须进右子树。
2. 为了平衡，让左右两边的元素个数尽量相等 → 选**中间**的元素当根。
3. 左半段、右半段用**同样的方法**分别造出左子树和右子树。
4. 区间为空（`lo > hi`）时返回 `NULL`。

左右两半的元素个数最多差 1，递归下去每一层都如此，所以造出来的树一定是平衡的。

### 手动模拟（示例 1）

| 调用 build(lo, hi) | 区间内容 | mid | 根 | 左区间 | 右区间 |
|---|---|---|---|---|---|
| (0, 4) | [-10,-3,0,5,9] | 2 | 0 | (0,1) | (3,4) |
| (0, 1) | [-10,-3] | 0 | -10 | 空 | (1,1) |
| (1, 1) | [-3] | 1 | -3 | 空 | 空 |
| (3, 4) | [5,9] | 3 | 5 | 空 | (4,4) |
| (4, 4) | [9] | 4 | 9 | 空 | 空 |

得到的是上面右边那棵树 `[0,-10,5,null,-3,null,9]`。

### 代码

```c
// 用 nums[lo..hi] 构造一棵平衡 BST，返回根结点
struct TreeNode* build(int* nums, int lo, int hi) {
    if (lo > hi) return NULL;                    // 空区间 → 空树

    int mid = lo + (hi - lo) / 2;                // 中间位置（偶数个时取左边那个）
    struct TreeNode* root = (struct TreeNode*)malloc(sizeof(struct TreeNode));
    root->val = nums[mid];                       // 中间的数当根
    root->left = build(nums, lo, mid - 1);       // 左半段造左子树
    root->right = build(nums, mid + 1, hi);      // 右半段造右子树
    return root;
}

struct TreeNode* sortedArrayToBST(int* nums, int numsSize) {
    return build(nums, 0, numsSize - 1);         // 整个数组
}
```

### 复杂度分析

- **时间复杂度 O(n)**：每个元素恰好创建一个结点。
- **空间复杂度 O(log n)**：递归深度等于树高，平衡树高约 log₂n（返回的树本身不算）。

---

## 🚀 第四步：思路二 —— 选中间偏右（另一种合法答案）

### 思路

元素个数是偶数时，中间有两个数，选左边那个或右边那个都可以，造出来的树都平衡。把 `mid` 改成 `lo + (hi - lo + 1) / 2` 就是"偶数时选右边那个"。示例 1 会得到 `[0,-3,9,-10,null,5]`（上面左边那棵树）。

这个思路说明了为什么本题答案不唯一，也说明本 OJ 为什么要"检查合法性"而不是比较输出。

### 代码

```c
struct TreeNode* build(int* nums, int lo, int hi) {
    if (lo > hi) return NULL;
    int mid = lo + (hi - lo + 1) / 2;            // 偶数个时取右边那个
    struct TreeNode* root = (struct TreeNode*)malloc(sizeof(struct TreeNode));
    root->val = nums[mid];
    root->left = build(nums, lo, mid - 1);
    root->right = build(nums, mid + 1, hi);
    return root;
}

struct TreeNode* sortedArrayToBST(int* nums, int numsSize) {
    return build(nums, 0, numsSize - 1);
}
```

### 复杂度分析

与思路一相同：时间 O(n)，空间 O(log n)。

---

## ⚠️ 第五步：小白常见错误

1. **直接串成一条链**：
   ```c
   // ❌ 每个结点都挂在上一个的右边：是 BST 但不平衡，输出 false
   for (int i = 1; i < numsSize; i++) cur->right = newNode(nums[i]), cur = cur->right;
   ```
2. **`malloc` 后忘了把 `left`/`right` 设为 `NULL`**：叶子结点的孩子是随机地址，遍历时崩溃。本题中递归 `build(lo > hi)` 返回 `NULL` 正好帮你赋值了，但自己写其他造树代码时要注意。
3. **区间边界差一**：递归写成 `build(nums, lo, mid)` 和 `build(nums, mid, hi)`，`mid` 被重复使用，而且区间可能永远不变小，死递归栈溢出。
4. **用局部变量当结点**：`struct TreeNode node; return &node;` 函数返回后这块内存就失效了。必须 `malloc`。
5. **`hi` 传成 `numsSize`**：区间是闭区间 `[lo, hi]`，初始应为 `numsSize - 1`，否则会读到 `nums[numsSize]`（越界）。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 选中间偏左当根 | O(n) | O(log n) | ⭐ | 标准答案 |
| 选中间偏右当根 | O(n) | O(log n) | ⭐ | 理解答案不唯一 |

---

## 🔗 举一反三

- **109. 有序链表转换二叉搜索树**：链表不能随机访问中点，可以用快慢指针找中点。
- **105. 从前序与中序遍历序列构造二叉树**：同样是"确定根，再分治左右两段"。
- **1382. 将二叉搜索树变平衡**：先中序遍历得到有序数组，再用本题方法重建。
- **思考题**：如果每次都选第一个元素当根，造出来的树长什么样？高度是多少？
