# 106. 从中序与后序遍历序列构造二叉树 —— 小白详细题解

> 一句话题解：**后序的最后一个是根，中序里根的左边是左子树、右边是右子树**，切开以后对两边做同样的事（分治递归）。

---

## 📖 第一步：先读懂题目

先回忆三种遍历顺序：

| 遍历 | 顺序 | 示例 1 的结果 |
|---|---|---|
| 中序 inorder | 左 → 根 → 右 | `[9,3,15,20,7]` |
| 后序 postorder | 左 → 右 → **根** | `[9,15,7,20,3]` |

现在反过来：只给你这两个数组，把原来的树"拼"回去。

```
    3
   / \
  9  20
    /  \
   15   7
```

**关键观察：**

1. 后序最后一个数 `3` 一定是**根**（根总是最后访问）。
2. 在中序里找到 `3`：它左边 `[9]` 是左子树的全部结点，右边 `[15,20,7]` 是右子树的全部结点。
3. 左子树有 1 个结点，所以后序数组的前 1 个 `[9]` 是左子树的后序，接下来 3 个 `[15,7,20]` 是右子树的后序。
4. 对左右两部分重复上面的过程。

**几个需要注意的细节：**

1. 值**互不相同**，所以"在中序里找到根"的位置是唯一的。
2. 结点最多 3000 个，树可能是一条链，递归深度可达 3000。
3. 输出是你构造的树的层序表示，由系统打印。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 创建结点

```c
struct TreeNode* node = (struct TreeNode*)malloc(sizeof(struct TreeNode));
node->val = v;
node->left = NULL;      // malloc 出来的内存是"垃圾值"，指针一定要初始化
node->right = NULL;
```

### 2. 用下标区间表示"子数组"

C 语言里切数组不方便（没有 Python 的切片），我们不复制数组，而是用两个下标 `[l, r]` 表示"原数组中从 l 到 r 的这一段"。`l > r` 表示空段。

### 3. 用数组代替哈希表

值的范围是 `[-3000, 3000]`，可以开一个长度 6001 的数组 `pos`，`pos[v + 3000]` 记录值 `v` 在中序里的下标。加上 3000 是为了让负数也变成合法下标。

---

## 💡 第三步：思路一 —— 分治 + 线性查找根

### 思路

写一个递归函数 `build(inL, inR, postL, postR)`：用中序 `inorder[inL..inR]` 和后序 `postorder[postL..postR]`（这两段描述的是同一棵子树）构造子树。

1. 如果区间为空，返回 `NULL`。
2. 根的值 = `postorder[postR]`。
3. 在 `inorder[inL..inR]` 里从左往右找它，下标记为 `k`；左子树结点个数 `leftSize = k - inL`。
4. 左子树：中序 `[inL, k-1]`，后序 `[postL, postL+leftSize-1]`。
5. 右子树：中序 `[k+1, inR]`，后序 `[postL+leftSize, postR-1]`。

### 手动模拟（示例 1）

| 调用 | 中序段 | 后序段 | 根 | k | 左子树大小 |
|---|---|---|---|---|---|
| 整棵树 | [9,3,15,20,7] | [9,15,7,20,3] | 3 | 1 | 1 |
| 左子树 | [9] | [9] | 9 | 0 | 0 |
| 右子树 | [15,20,7] | [15,7,20] | 20 | 3 | 1 |
| 20 的左 | [15] | [15] | 15 | 2 | 0 |
| 20 的右 | [7] | [7] | 7 | 4 | 0 |

### 代码

```c
// 用 inorder[inL..inR] 和 postorder[postL..postR] 构造子树
struct TreeNode* build(int* inorder, int* postorder, int inL, int inR, int postL, int postR) {
    if (inL > inR) return NULL;                         // 空区间 -> 空树

    int rootVal = postorder[postR];                     // 后序最后一个是根
    struct TreeNode* node = (struct TreeNode*)malloc(sizeof(struct TreeNode));
    node->val = rootVal;

    int k = inL;
    while (inorder[k] != rootVal) k++;                  // 在中序里找根的位置
    int leftSize = k - inL;                             // 左子树有几个结点

    node->left = build(inorder, postorder, inL, k - 1, postL, postL + leftSize - 1);
    node->right = build(inorder, postorder, k + 1, inR, postL + leftSize, postR - 1);
    return node;
}

struct TreeNode* buildTree(int* inorder, int inorderSize, int* postorder, int postorderSize) {
    return build(inorder, postorder, 0, inorderSize - 1, 0, postorderSize - 1);
}
```

### 复杂度分析

- **时间复杂度 O(n²)**：每个结点都要在中序里线性查找一次，链状树时每次要找很久。n = 3000 时约 450 万次比较，也能通过。
- **空间复杂度 O(h)**：递归栈，h 为树高。

---

## 🚀 第四步：思路二 —— 下标映射表 + 从后往前取根

### 为什么能优化

思路一的瓶颈是"在中序里找根"。值互不相同且范围很小，预先把"值 → 中序下标"存进数组 `pos`，查找就变成 O(1)。

再进一步：后序是"左 → 右 → 根"，**倒过来**就是"根 → 右 → 左"。如果我们按"先建右子树、再建左子树"的顺序递归，那么每次需要的根恰好是后序数组从后往前的下一个元素！用一个全局指针 `postIdx` 从末尾往前走即可，连后序区间都不用传。

### 手动模拟（示例 1）

| 步骤 | postIdx 指向 | 取出的根 | 中序区间 | 下一步 |
|---|---|---|---|---|
| 1 | 4 | 3 | [0,4] | 先建右子树 [2,4] |
| 2 | 3 | 20 | [2,4] | 先建右子树 [4,4] |
| 3 | 2 | 7 | [4,4] | 左右都空 |
| 4 | 1 | 15 | [2,2] | 20 的左子树 |
| 5 | 0 | 9 | [0,0] | 3 的左子树 |

### 代码

```c
int pos[6001];          // pos[v + 3000] = 值 v 在中序数组中的下标
int postIdx;            // 后序数组中"下一个根"的位置，从后往前走

struct TreeNode* build(int* postorder, int inL, int inR) {
    if (inL > inR) return NULL;

    int rootVal = postorder[postIdx--];                 // 取出当前子树的根
    struct TreeNode* node = (struct TreeNode*)malloc(sizeof(struct TreeNode));
    node->val = rootVal;

    int k = pos[rootVal + 3000];                        // O(1) 找到根在中序里的位置
    node->right = build(postorder, k + 1, inR);         // 注意：必须先建右子树！
    node->left = build(postorder, inL, k - 1);
    return node;
}

struct TreeNode* buildTree(int* inorder, int inorderSize, int* postorder, int postorderSize) {
    for (int i = 0; i < inorderSize; i++) pos[inorder[i] + 3000] = i;
    postIdx = postorderSize - 1;                        // 每次调用都要重新初始化
    return build(postorder, 0, inorderSize - 1);
}
```

### 复杂度分析

- **时间复杂度 O(n)**：每个结点只创建一次，查找 O(1)。
- **空间复杂度 O(n)**：映射表 + 递归栈。

---

## ⚠️ 第五步：小白常见错误

1. **思路二先建左子树**：后序倒着取是"根 → 右 → 左"，如果先递归左子树，取到的其实是右子树的根，整棵树就乱了。
2. **负数直接当下标**：`pos[rootVal]` 在值为负时越界，要加偏移量 `pos[rootVal + 3000]`。
3. **全局变量没有在 `buildTree` 里重新初始化**：`postIdx` 如果只在定义时赋值，多次调用时第二次就从错误的位置开始。
4. **后序区间算错**：右子树的后序区间是 `[postL + leftSize, postR - 1]`，最后要减 1，因为 `postR` 是根本身。
5. **`malloc` 后忘记给 `left`/`right` 赋值**：本题两种写法都会把它们赋值为递归结果（空区间返回 `NULL`），但自己写别的建树代码时要注意初始化。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 分治 + 线性查找根 | O(n²) | O(h) | ⭐⭐ | 先理解分治的切法 |
| 映射表 + 从后往前取根 | O(n) | O(n) | ⭐⭐⭐ | 推荐，最优解 |

---

## 🔗 举一反三

- **105. 从前序与中序遍历序列构造二叉树**：前序第一个是根，"从前往后取根、先建左子树"。
- **889. 根据前序和后序遍历构造二叉树**：没有中序时答案可能不唯一，想一想为什么。
- **思考题**：只给前序和后序，能唯一确定一棵二叉树吗？举一个反例。
