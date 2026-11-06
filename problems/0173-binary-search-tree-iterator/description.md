实现一个二叉搜索树迭代器类 `BSTIterator` ，表示一个按中序遍历二叉搜索树（BST）的迭代器：

- `BSTIterator(TreeNode root)` 初始化 `BSTIterator` 类的一个对象。BST 的根节点 `root` 会作为构造函数的一部分给出。指针应初始化为一个不存在于 BST 中的数字，且该数字小于 BST 中的任何元素。
- `boolean hasNext()` 如果向指针右侧遍历存在数字，则返回 `true` ；否则返回 `false` 。
- `int next()` 将指针向右移动，然后返回指针处的数字。

注意，指针初始化为一个不存在于 BST 中的数字，所以对 `next()` 的首次调用将返回 BST 中的最小元素。

你可以假设 `next()` 调用总是有效的，也就是说，当调用 `next()` 时，BST 的中序遍历中至少存在一个下一个数字。

### 示例 1

```
      7
     / \
    3   15
       /  \
      9    20
```

```
输入
["BSTIterator", "next", "next", "hasNext", "next", "hasNext", "next", "hasNext", "next", "hasNext"]
[[[7, 3, 15, null, null, 9, 20]], [], [], [], [], [], [], [], [], []]
输出
[null, 3, 7, true, 9, true, 15, true, 20, false]

解释
BSTIterator bSTIterator = new BSTIterator([7, 3, 15, null, null, 9, 20]);
bSTIterator.next();    // 返回 3
bSTIterator.next();    // 返回 7
bSTIterator.hasNext(); // 返回 True
bSTIterator.next();    // 返回 9
bSTIterator.hasNext(); // 返回 True
bSTIterator.next();    // 返回 15
bSTIterator.hasNext(); // 返回 True
bSTIterator.next();    // 返回 20
bSTIterator.hasNext(); // 返回 False
```

### 提示

- 树中节点的数目在范围 `[1, 10^5]` 内
- `0 <= Node.val <= 10^6`
- 最多调用 `10^5` 次 `hasNext` 和 `next` 操作

**进阶：** 你可以设计一个满足下述条件的解决方案吗？`next()` 和 `hasNext()` 操作均摊时间复杂度为 `O(1)` ，并使用 `O(h)` 内存。其中 `h` 是树的高度。

### 函数说明

```c
struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
};

typedef struct {
    /* 由你设计 */
} BSTIterator;

BSTIterator* bSTIteratorCreate(struct TreeNode* root);
int bSTIteratorNext(BSTIterator* obj);
bool bSTIteratorHasNext(BSTIterator* obj);
void bSTIteratorFree(BSTIterator* obj);
```

- `struct TreeNode` 已由系统定义，**不要**在代码中重复定义
- `bSTIteratorCreate`：用 BST 的根结点创建迭代器，返回 `malloc` 出来的对象指针
- `bSTIteratorNext`：返回下一个（更大的）元素
- `bSTIteratorHasNext`：是否还有下一个元素
- `bSTIteratorFree`：释放迭代器自己申请的内存（**不要**释放树的结点）

### 自定义输入格式

```
["BSTIterator","next","next","hasNext","next","hasNext","next","hasNext","next","hasNext"]
[[[7,3,15,null,null,9,20]],[],[],[],[],[],[],[],[],[]]
```

第 1 行是操作名数组，第 1 个必须是 `"BSTIterator"`；第 2 行是对应的参数数组，构造函数的参数是 BST 的层序表示（`null` 表示空结点），其余操作的参数都是 `[]`。
输出力扣风格的结果数组：构造函数输出 `null`，`next` 输出整数，`hasNext` 输出 `true`/`false`。
