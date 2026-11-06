# 105. 从前序与中序遍历序列构造二叉树 —— 小白详细题解

> 这道题考的是对遍历顺序的**深刻理解**：前序告诉你"谁是根"，中序告诉你"谁在左、谁在右"。两者结合，就能一层一层把树还原出来。

---

## 📖 第一步：先读懂题目

- **前序**（根 → 左 → 右）：第一个数一定是**根**。
- **中序**（左 → 根 → 右）：根把序列分成两半，左边全是左子树，右边全是右子树。

示例 1：`preorder = [3,9,20,15,7]`，`inorder = [9,3,15,20,7]`

| 步骤 | 推理 |
|---|---|
| 1 | 前序第一个是 `3` → 根是 3 |
| 2 | 在中序里找到 3：左边 `[9]` 是左子树，右边 `[15,20,7]` 是右子树 |
| 3 | 左子树有 1 个结点，所以前序里 3 后面的 1 个 `[9]` 是左子树的前序，剩下 `[20,15,7]` 是右子树的前序 |
| 4 | 右子树：前序第一个 `20` 是根；中序 `[15,20,7]` 中 20 左边 `[15]`、右边 `[7]` |

还原出来：

```
    3
   / \
  9  20
    /  \
   15   7
```

**几个需要注意的细节：**

1. 值**互不相同**，所以在中序里找根的位置是唯一的。这是能还原的前提。
2. 关键是算出**左子树的结点个数** `leftSize`，用它在前序数组里切段。
3. 结点要自己 `malloc`。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 用下标区间代替"切数组"

C 语言里切子数组很麻烦，我们用下标表示：前序的 `[preL, preR]` 段、中序的 `[inL, inR]` 段。递归时只传下标，不复制数据。

### 2. 用数组当哈希表

值的范围是 `[-3000, 3000]`，可以开一个 `pos[6001]` 的数组，`pos[val + 3000]` 记录 `val` 在中序里的下标。`+ 3000` 是为了把负数变成合法的数组下标。

### 3. `static` 全局数组

`pos` 要在多次递归调用之间共享，可以写成函数外的 `static int pos[6001];`。每次调用 `buildTree` 时重新填一遍即可（旧数据会被覆盖）。

---

## 💡 第三步：思路一 —— 递归 + 在中序里线性查找根

### 思路

定义 `build(preL, preR, inL, inR)`：用 `preorder[preL..preR]` 和 `inorder[inL..inR]` 构造子树。

1. 区间为空（`preL > preR`）返回 `NULL`。
2. 根的值 `rootVal = preorder[preL]`。
3. 在 `inorder[inL..inR]` 里找到 `rootVal` 的下标 `k`。
4. 左子树结点个数 `leftSize = k - inL`。
5. 左子树：前序 `[preL+1, preL+leftSize]`，中序 `[inL, k-1]`。
6. 右子树：前序 `[preL+leftSize+1, preR]`，中序 `[k+1, inR]`。

### 手动模拟（示例 1）

| 调用 | 前序段 | 中序段 | 根 | k | leftSize |
|---|---|---|---|---|---|
| build(0,4,0,4) | [3,9,20,15,7] | [9,3,15,20,7] | 3 | 1 | 1 |
| build(1,1,0,0) | [9] | [9] | 9 | 0 | 0 |
| build(2,4,2,4) | [20,15,7] | [15,20,7] | 20 | 3 | 1 |
| build(3,3,2,2) | [15] | [15] | 15 | 2 | 0 |
| build(4,4,4,4) | [7] | [7] | 7 | 4 | 0 |

### 代码

```c
struct TreeNode* build(int* preorder, int preL, int preR, int* inorder, int inL, int inR) {
    if (preL > preR) return NULL;                       // 空区间 → 空树

    int rootVal = preorder[preL];                       // 前序第一个是根
    int k = inL;
    while (inorder[k] != rootVal) k++;                  // 在中序里找根的位置
    int leftSize = k - inL;                             // 左子树有几个结点

    struct TreeNode* root = (struct TreeNode*)malloc(sizeof(struct TreeNode));
    root->val = rootVal;
    // 左子树：前序紧跟根的 leftSize 个；中序是根左边那段
    root->left = build(preorder, preL + 1, preL + leftSize, inorder, inL, k - 1);
    // 右子树：前序剩下的部分；中序是根右边那段
    root->right = build(preorder, preL + leftSize + 1, preR, inorder, k + 1, inR);
    return root;
}

struct TreeNode* buildTree(int* preorder, int preorderSize, int* inorder, int inorderSize) {
    return build(preorder, 0, preorderSize - 1, inorder, 0, inorderSize - 1);
}
```

### 复杂度分析

- **时间复杂度 O(n²)**（最坏）：每个结点都要在中序里线性找一次。树是一条链时，每次都要找很远。n = 3000 时约 450 万次比较，本题能过。
- **空间复杂度 O(h)**：递归栈。

---

## 🚀 第四步：思路二 —— 用数组哈希表 O(1) 定位根

### 思路

思路一的瓶颈是"在中序里找根"。由于值互不相同、范围又小，我们事先用 `pos` 数组记下每个值在中序里的下标，查找就变成 O(1)。

另外可以注意到：右子树的中序终点 `inR` 其实用不到（区间长度已经由前序段决定），所以参数还能再精简，不过保留它更好理解。

### 代码

```c
static int pos[6001];      // pos[val + 3000] = val 在 inorder 中的下标

struct TreeNode* build(int* preorder, int preL, int preR, int inL) {
    if (preL > preR) return NULL;

    int rootVal = preorder[preL];
    int k = pos[rootVal + 3000];                        // O(1) 找到根在中序里的位置
    int leftSize = k - inL;

    struct TreeNode* root = (struct TreeNode*)malloc(sizeof(struct TreeNode));
    root->val = rootVal;
    root->left = build(preorder, preL + 1, preL + leftSize, inL);
    root->right = build(preorder, preL + leftSize + 1, preR, k + 1);
    return root;
}

struct TreeNode* buildTree(int* preorder, int preorderSize, int* inorder, int inorderSize) {
    for (int i = 0; i < inorderSize; i++) {
        pos[inorder[i] + 3000] = i;                     // 预处理：记录每个值的位置
    }
    return build(preorder, 0, preorderSize - 1, 0);
}
```

### 复杂度分析

- **时间复杂度 O(n)**：预处理 O(n)，每个结点 O(1)。
- **空间复杂度 O(n)**：`pos` 数组 + 递归栈。

---

## ⚠️ 第五步：小白常见错误

1. **用中序的下标去切前序**：写成 `build(preorder, preL + 1, k, ...)`，`k` 是**中序**里的位置，和前序的下标没有直接关系。要用 `leftSize = k - inL` 换算。
2. **`leftSize` 写成 `k`**：只有在 `inL == 0` 时才碰巧正确，进入右子树后就错了。
3. **负数下标**：`pos[rootVal]` 在值为负数时越界，要加上偏移量 `3000`。
4. **区间边界差一**：右子树前序起点是 `preL + leftSize + 1`（跳过根和整个左子树），漏了 `+1` 会把左子树最后一个结点当成右子树的根。
5. **`malloc` 后不设置 `left` / `right`**：本写法中它们都由递归返回值赋值，所以没问题；但如果提前 `return` 一定要记得初始化。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 递归 + 线性查找根 | O(n²) | O(h) | ⭐⭐ | 先理解分治的切法 |
| 递归 + 哈希定位根 | O(n) | O(n) | ⭐⭐ | 标准答案 |

---

## 🔗 举一反三

- **106. 从中序与后序遍历序列构造二叉树**：后序的**最后一个**是根。
- **889. 根据前序和后序遍历构造二叉树**：答案可能不唯一，为什么？
- **108. 将有序数组转换为二叉搜索树**：同样是"选根 + 分治"。
- **思考题**：只给前序和中序，如果允许有重复值，还能唯一还原吗？举一个反例。
