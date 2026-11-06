# 114. 二叉树展开为链表 —— 小白详细题解

> 这道题考的是**指针操作**：不创建新结点，只改 `left`、`right` 指针，把一棵树"拉直"。先用数组把顺序记下来是最稳的办法，再去挑战原地 O(1) 写法。

---

## 📖 第一步：先读懂题目

把树改造成一条"链"：

- 每个结点的 `left` 都变成 `NULL`；
- `right` 指向链上的下一个结点；
- 链上结点的顺序 = 原树的**先序遍历**（根 → 左 → 右）。

示例 1 `[1,2,5,3,4,null,6]`：

```
      1
     / \
    2   5
   / \   \
  3   4   6
```

| 先序遍历步骤 | 访问 | 序列 |
|---|---|---|
| 1 | 根 1 | 1 |
| 2 | 1 的左子树：2，再 3、4 | 1,2,3,4 |
| 3 | 1 的右子树：5，再 6 | 1,2,3,4,5,6 |

展开后：`1 → 2 → 3 → 4 → 5 → 6`（全部通过 `right` 相连），层序输出 `[1,null,2,null,3,null,4,null,5,null,6]`。

**几个需要注意的细节：**

1. 函数返回 `void`，要**直接修改**原树；判题程序会从原来的 `root` 开始打印。
2. 不要 `malloc` 新结点，用原来的结点重新连线。
3. 所有 `left` 都要置为 `NULL`，漏一个输出就不对。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 指针数组

```c
struct TreeNode** list = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * 2000);
```

`list[i]` 是第 i 个结点的**地址**。通过 `list[i]->right = list[i + 1];` 就能把它们串起来——改的是原结点本身。

### 2. 改指针之前先保存

重新连线时，经常要先把某个指针**存到临时变量**里，否则一改就"找不回来了"。这是所有链表题的通用技巧。

---

## 💡 第三步：思路一 —— 先序遍历存数组，再依次连接

### 思路

1. 先序遍历整棵树，把每个结点的地址按顺序存进数组 `list`。
2. 遍历数组：`list[i]->left = NULL`，`list[i]->right = list[i + 1]`（最后一个的 `right` 是 `NULL`）。

因为第 1 步已经把顺序全部记下来了，第 2 步随便怎么改指针都不会影响结果。

### 代码

```c
// 先序遍历，把结点地址依次存进 list
void preorder(struct TreeNode* node, struct TreeNode** list, int* cnt) {
    if (node == NULL) return;
    list[(*cnt)++] = node;                 // 根
    preorder(node->left, list, cnt);       // 左
    preorder(node->right, list, cnt);      // 右
}

void flatten(struct TreeNode* root) {
    struct TreeNode** list = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * 2000);
    int cnt = 0;
    preorder(root, list, &cnt);            // 1. 记下先序顺序

    for (int i = 0; i < cnt; i++) {        // 2. 按顺序重新连线
        list[i]->left = NULL;
        list[i]->right = (i + 1 < cnt) ? list[i + 1] : NULL;
    }
    free(list);
}
```

### 复杂度分析

- **时间复杂度 O(n)**：遍历一次 + 连线一次。
- **空间复杂度 O(n)**：数组存了 n 个指针。

---

## 🚀 第四步：思路二 —— 原地展开（O(1) 额外空间）

### 思路

看当前结点 `cur`。如果它有左子树，先序遍历的顺序是：`cur` → 左子树全部 → 右子树全部。

那么在链表里，**右子树应该接在左子树的最后一个结点后面**。左子树在先序遍历中最后访问的是哪个？是左子树里**一直往右走到头**的那个结点（记为 `pre`）。

于是对 `cur` 做三步操作：

1. `pre->right = cur->right`：把右子树接到左子树最右结点的后面；
2. `cur->right = cur->left`：左子树整体挪到右边；
3. `cur->left = NULL`。

然后 `cur = cur->right`，继续处理下一个结点。没有左子树的结点直接往右走。

### 手动模拟（示例 1）

| 步骤 | cur | 左子树最右结点 pre | 操作后的链（沿 right） |
|---|---|---|---|
| 1 | 1 | 4 | 4 的 right 接上 5；1 → 2(3,4) → … → 5 → 6 |
| 2 | 2 | 3 | 3 的 right 接上 4；1 → 2 → 3 → 4 → 5 → 6 |
| 3 | 3 | 无左子树 | 往右走 |
| 4 | 4、5、6 | 都无左子树 | 往右走，结束 |

### 代码

```c
void flatten(struct TreeNode* root) {
    struct TreeNode* cur = root;
    while (cur != NULL) {
        if (cur->left != NULL) {
            // 1. 找到左子树中"最后访问"的结点：一直往右走到头
            struct TreeNode* pre = cur->left;
            while (pre->right != NULL) pre = pre->right;

            // 2. 把右子树接到它后面
            pre->right = cur->right;
            // 3. 左子树挪到右边，左指针置空
            cur->right = cur->left;
            cur->left = NULL;
        }
        cur = cur->right;          // 处理链上的下一个结点
    }
}
```

### 复杂度分析

- **时间复杂度 O(n)**：每个结点作为 `cur` 一次；找 `pre` 时走过的路径，之后都会被拉进链里，每条边最多被多走一次。
- **空间复杂度 O(1)**：只用了两个指针。

---

## ⚠️ 第五步：小白常见错误

1. **忘了 `cur->left = NULL`**：结点之间还残留着左孩子关系，打印出来的树不是一条只有右孩子的链，判 Wrong Answer。
2. **先改 `cur->right` 再接右子树**：`cur->right = cur->left;` 写在 `pre->right = cur->right;` 前面，原来的右子树就丢了。
3. **递归时边遍历边改指针**：
   ```c
   // ❌ 先序遍历的同时修改 right，后面 preorder(node->right) 拿到的已经是改过的指针
   prev->right = node; prev->left = NULL; preorder(node->left); preorder(node->right);
   ```
   需要在修改前先用变量把 `node->right` 保存下来。
4. **新建结点组成链表**：函数是 `void`，判题程序从原 `root` 开始打印，新建的链表根本看不到。
5. **数组开小**：结点最多 2000 个。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 先序存数组再连接 | O(n) | O(n) | ⭐ | 先写这个，保证正确 |
| 原地展开（找左子树最右结点） | O(n) | O(1) | ⭐⭐⭐ | 进阶要求 |

---

## 🔗 举一反三

- **144. 二叉树的前序遍历**：本题顺序的来源。
- **206. 反转链表**：同样需要"改指针前先保存"。
- **897. 递增顺序搜索树**：按**中序**展开成链。
- **思考题**：如果按"右 → 左 → 根"的顺序遍历，并维护一个 `prev` 指针，每次让 `node->right = prev`，能否也完成展开？为什么要反着来？
