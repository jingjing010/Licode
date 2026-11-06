# 101. 对称二叉树 —— 小白详细题解

> 这道题的关键是：**一个结点不够用，要同时拿着两个结点一起比较**。学会"双指针递归"，后面判断相同的树、子树等题都是一个套路。

---

## 📖 第一步：先读懂题目

**轴对称**就是：从根结点画一条竖直的线，左半边和右半边像照镜子一样，**形状相同、对应位置的值也相同**。

示例 1 `[1,2,2,3,4,4,3]`：

```
      1
    /   \
   2     2        镜像位置配对：
  / \   / \       左边的 2 ↔ 右边的 2
 3   4 4   3      左边的 3（最外侧）↔ 右边的 3（最外侧）
                  左边的 4（内侧）↔ 右边的 4（内侧）
```

示例 2 `[1,2,2,null,3,null,3]`：

```
    1
   / \
  2   2
   \   \
    3   3
```

左边的 2 只有**右**孩子，那它的镜像（右边的 2）应该只有**左**孩子，但实际也是右孩子 → 不对称，输出 `false`。

**几个需要注意的细节：**

1. 不是比较"左孩子和右孩子的值相等"就完了，要比较的是**镜像位置**：外侧对外侧，内侧对内侧。
2. 形状也要对称：一边有结点、对应位置没有，就不对称。
3. 树至少有 1 个结点；只有根结点的树是对称的。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. `bool` 类型

本 OJ 已经包含 `<stdbool.h>`，可以直接用 `bool`、`true`、`false`。

### 2. 辅助函数

`isSymmetric` 只有一个参数，但我们需要同时比较**两棵**子树。办法是自己写一个两个参数的辅助函数，再在 `isSymmetric` 里调用它。辅助函数要写在 `isSymmetric` **前面**（或者先声明），否则编译器不认识它。

### 3. `&&` 的短路

`A && B && C`：只要 `A` 为假，后面的 `B`、`C` 就不再计算。利用这一点，值不相等时就不会继续往下递归，省时间。

---

## 💡 第三步：思路一 —— 递归（双指针）

### 思路

写一个函数 `check(a, b)`，判断以 `a`、`b` 为根的两棵树是否**互为镜像**：

1. `a`、`b` 都为空 → 镜像（`true`）。
2. 只有一个为空 → 不是（`false`）。
3. 都不为空：要求
   - `a->val == b->val`；
   - `a` 的**左**子树和 `b` 的**右**子树互为镜像（外侧对外侧）；
   - `a` 的**右**子树和 `b` 的**左**子树互为镜像（内侧对内侧）。

整棵树对称 ⇔ `check(root->left, root->right)`。

### 手动模拟（示例 2）

| 调用 | a | b | 结果 |
|---|---|---|---|
| check(2, 2) | 左边的 2 | 右边的 2 | 值相等，继续 |
| check(2.left, 2.right) | 空 | 3 | 一个为空 → **false** |

由于 `&&` 短路，直接得到 `false`。

### 代码

```c
// 判断两棵树 a、b 是否互为镜像
bool check(struct TreeNode* a, struct TreeNode* b) {
    if (a == NULL && b == NULL) return true;    // 都空：镜像
    if (a == NULL || b == NULL) return false;   // 只有一个空：形状不对称
    if (a->val != b->val) return false;         // 值不同：不对称

    // 外侧对外侧，内侧对内侧
    return check(a->left, b->right) && check(a->right, b->left);
}

bool isSymmetric(struct TreeNode* root) {
    if (root == NULL) return true;               // 空树算对称（本题不会出现）
    return check(root->left, root->right);
}
```

### 复杂度分析

- **时间复杂度 O(n)**：每个结点最多被比较一次。
- **空间复杂度 O(h)**：递归栈深度。

---

## 🚀 第四步：思路二 —— 迭代（队列里成对放结点）

### 思路

把"需要比较的一对结点"成对地放进队列：每次取出两个比较，再把它们的孩子按**镜像配对**的方式成对放回去。

1. 入队 `(root->left, root->right)`。
2. 每次出队两个结点 `a`、`b`：
   - 都空：这一对没问题，继续；
   - 一个空或值不同：返回 `false`；
   - 否则依次入队 `(a->left, b->right)` 和 `(a->right, b->left)`。
3. 队列空了还没发现问题 → `true`。

### 代码

```c
bool isSymmetric(struct TreeNode* root) {
    if (root == NULL) return true;

    // 每个结点（包括空孩子）最多入队一次，2 * 1000 + 2 个位置足够
    struct TreeNode** queue = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * 2005);
    int head = 0, tail = 0;
    queue[tail++] = root->left;
    queue[tail++] = root->right;

    bool ok = true;
    while (head < tail) {
        struct TreeNode* a = queue[head++];      // 成对取出
        struct TreeNode* b = queue[head++];
        if (a == NULL && b == NULL) continue;    // 两个都空，看下一对
        if (a == NULL || b == NULL || a->val != b->val) {
            ok = false;
            break;
        }
        queue[tail++] = a->left;                 // 外侧配对
        queue[tail++] = b->right;
        queue[tail++] = a->right;                // 内侧配对
        queue[tail++] = b->left;
    }

    free(queue);
    return ok;
}
```

### 复杂度分析

- **时间复杂度 O(n)**，**空间复杂度 O(n)**。

---

## ⚠️ 第五步：小白常见错误

1. **配对配错**：写成 `check(a->left, b->left) && check(a->right, b->right)`，这判断的是"两棵树相同"，不是"镜像"。
2. **先访问 `a->val` 再判空**：`if (a->val != b->val)` 写在判空前面，遇到空指针直接崩溃。
3. **只比较每个结点的左右孩子值**：`root->left->val == root->right->val` 并递归下去，示例 2 这种"形状不对称"会判断错，而且会访问空指针。
4. **用中序遍历结果是否回文来判断**：`[1,2,2,2,null,2]` 的中序是 `[2,2,1,2,2]`，回文，但树并不对称。
5. **辅助函数写在 `isSymmetric` 后面且没声明**：编译报 implicit declaration 的警告甚至错误。

---

## 📊 第六步：两种方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 递归双指针 | O(n) | O(h) | ⭐ | 首选，代码最清晰 |
| 迭代 + 队列成对比较 | O(n) | O(n) | ⭐⭐ | 进阶要求，理解"成对入队" |

---

## 🔗 举一反三

- **100. 相同的树**：把配对方式改成"左对左、右对右"。
- **226. 翻转二叉树**：对称 ⇔ 翻转后与原树相同。
- **572. 另一棵树的子树**：在每个结点上调用"相同的树"。
- **思考题**：能不能先把左子树翻转，再判断它与右子树是否相同？这样做会修改原树，有什么副作用？
