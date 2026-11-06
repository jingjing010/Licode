# 173. 二叉搜索树迭代器 —— 小白详细题解

> 一句话题解：**把"迭代版中序遍历"拆成一步一步执行**——栈里存着"还没访问的左链"，每次 `next` 弹出一个、再把它右子树的左链压进去。

---

## 📖 第一步：先读懂题目

这是一道**设计题**：你要实现一个"迭代器"对象，调用者会反复问它：

- `hasNext()`：后面还有数吗？
- `next()`：给我下一个数。

而"下一个"指的是 BST **中序遍历**（从小到大）的下一个。示例：

```
      7
     / \
    3   15
       /  \
      9    20
```

中序遍历是 `3, 7, 9, 15, 20`。

| 操作 | 返回 | 说明 |
|---|---|---|
| BSTIterator(root) | null | 创建，指针在最小值"前面" |
| next() | 3 | 最小的数 |
| next() | 7 | |
| hasNext() | true | 还有 9、15、20 |
| next() | 9 | |
| hasNext() | true | |
| next() | 15 | |
| hasNext() | true | |
| next() | 20 | 最大的数 |
| hasNext() | false | 取完了 |

**几个需要注意的细节：**

1. 题目保证 `next()` 调用时一定还有数，不用处理"取完了还调用 `next`"。
2. 结点最多 10⁵ 个，树可能是一条长链。
3. **进阶**要求：`next`/`hasNext` 均摊 O(1)，额外内存 O(h)（h 是树高），也就是**不能**把所有值都存下来。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 力扣 C 语言的"类"写法

C 没有类，力扣用"结构体 + 一组函数"来模拟：

```c
typedef struct {
    // 你自己决定放什么成员
} BSTIterator;

BSTIterator* bSTIteratorCreate(struct TreeNode* root);  // 相当于构造函数，要 malloc 一个对象返回
int bSTIteratorNext(BSTIterator* obj);                  // obj 就是"this"
bool bSTIteratorHasNext(BSTIterator* obj);
void bSTIteratorFree(BSTIterator* obj);                 // 析构：释放 Create 里申请的内存
```

结构体里放什么完全由你设计，比如一个数组 + 一个下标，或者一个栈。

### 2. 可以自动变大的数组（realloc）

不知道要存多少个元素时，先开一个小数组，满了就用 `realloc` 扩成两倍：

```c
if (size == cap) {
    cap *= 2;
    arr = (int*)realloc(arr, sizeof(int) * cap);   // 内容会被保留
}
arr[size++] = x;
```

每个元素平均只被搬运常数次，所以总代价仍是 O(n)。

### 3. `Free` 只释放自己申请的

树的结点是调用者的，迭代器**不能**去 `free` 它们；只释放 `Create` 里 `malloc` 的东西。

---

## 💡 第三步：思路一 —— 先把中序遍历结果存进数组

### 思路

1. `Create` 时做一遍完整的中序遍历，把所有值按顺序存进数组 `vals`，下标 `idx = 0`。
2. `next`：返回 `vals[idx++]`。
3. `hasNext`：`idx < size`。

非常直接，但需要 O(n) 的额外内存，不满足进阶要求。

### 手动模拟（示例）

`Create` 后：`vals = [3, 7, 9, 15, 20]`，`idx = 0`。

| 操作 | idx（操作前） | 返回 | idx（操作后） |
|---|---|---|---|
| next | 0 | 3 | 1 |
| next | 1 | 7 | 2 |
| hasNext | 2 | true（2 < 5） | 2 |
| …… | | | |
| hasNext | 5 | false | 5 |

### 代码

```c
typedef struct {
    int* vals;      // 中序遍历结果
    int size;       // 已存的个数
    int cap;        // 数组容量
    int idx;        // 下一次 next 要返回的位置
} BSTIterator;

// 中序遍历：左 -> 根 -> 右，把值追加到 it->vals
void inorder(BSTIterator* it, struct TreeNode* node) {
    if (node == NULL) return;
    inorder(it, node->left);
    if (it->size == it->cap) {                          // 满了就扩容
        it->cap *= 2;
        it->vals = (int*)realloc(it->vals, sizeof(int) * it->cap);
    }
    it->vals[it->size++] = node->val;
    inorder(it, node->right);
}

BSTIterator* bSTIteratorCreate(struct TreeNode* root) {
    BSTIterator* it = (BSTIterator*)malloc(sizeof(BSTIterator));
    it->cap = 16;
    it->size = 0;
    it->idx = 0;
    it->vals = (int*)malloc(sizeof(int) * it->cap);
    inorder(it, root);                                  // 一次性遍历完
    return it;
}

int bSTIteratorNext(BSTIterator* obj) {
    return obj->vals[obj->idx++];                       // 取当前的，下标后移
}

bool bSTIteratorHasNext(BSTIterator* obj) {
    return obj->idx < obj->size;
}

void bSTIteratorFree(BSTIterator* obj) {
    free(obj->vals);                                    // 先释放成员
    free(obj);                                          // 再释放对象本身
}
```

### 复杂度分析

- **时间复杂度**：`Create` O(n)；`next`、`hasNext` O(1)。
- **空间复杂度 O(n)**：存了所有值。

---

## 🚀 第四步：思路二 —— 用栈"暂停"中序遍历（O(h) 内存）

### 思路

回忆迭代版中序遍历（第 94 题）：

```c
while (cur != NULL || top > 0) {
    while (cur != NULL) { stack[top++] = cur; cur = cur->left; }   // 一路向左压栈
    cur = stack[--top];          // 弹出：这就是"下一个"最小的结点
    访问 cur;                     // ❌ 示意代码，不能直接运行
    cur = cur->right;            // 转向右子树
}
```

把它拆成三块：

- `Create`：把根**一路向左**压栈（这时栈顶就是最小值）。
- `next`：弹出栈顶 `node` 作为答案；再把 `node->right` **一路向左**压栈，为下一次做准备。
- `hasNext`：栈不空就还有。

栈里任何时候存的都是"一条从某结点往左下走的链"，长度不超过树高 h，所以内存 O(h)。每个结点恰好入栈、出栈各一次，n 次 `next` 总共 O(n)，**均摊** O(1)。

### 手动模拟（示例）

| 操作 | 弹出 | 压入（右孩子的左链） | 操作后的栈（底 → 顶） | 返回 |
|---|---|---|---|---|
| Create | — | 7, 3 | [7, 3] | null |
| next | 3 | 无（3 没有右孩子） | [7] | 3 |
| next | 7 | 15, 9 | [15, 9] | 7 |
| hasNext | — | — | [15, 9] | true |
| next | 9 | 无 | [15] | 9 |
| next | 15 | 20 | [20] | 15 |
| next | 20 | 无 | [] | 20 |
| hasNext | — | — | [] | false |

### 代码

```c
typedef struct {
    struct TreeNode** stack;   // 栈：存还没访问的结点
    int top;                   // 栈中元素个数
    int cap;                   // 栈容量
} BSTIterator;

// 从 node 开始一路向左，把沿途结点都压栈
void pushLeft(BSTIterator* it, struct TreeNode* node) {
    while (node != NULL) {
        if (it->top == it->cap) {                       // 栈满了就扩容（链状树很深）
            it->cap *= 2;
            it->stack = (struct TreeNode**)realloc(it->stack, sizeof(struct TreeNode*) * it->cap);
        }
        it->stack[it->top++] = node;
        node = node->left;
    }
}

BSTIterator* bSTIteratorCreate(struct TreeNode* root) {
    BSTIterator* it = (BSTIterator*)malloc(sizeof(BSTIterator));
    it->cap = 64;
    it->top = 0;
    it->stack = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * it->cap);
    pushLeft(it, root);                                 // 栈顶就是最小值
    return it;
}

int bSTIteratorNext(BSTIterator* obj) {
    struct TreeNode* node = obj->stack[--obj->top];     // 弹出当前最小的
    pushLeft(obj, node->right);                         // 它的右子树里的数紧跟在它后面
    return node->val;
}

bool bSTIteratorHasNext(BSTIterator* obj) {
    return obj->top > 0;                                // 栈里还有结点就还有下一个
}

void bSTIteratorFree(BSTIterator* obj) {
    free(obj->stack);
    free(obj);
}
```

### 复杂度分析

- **时间复杂度**：`next` 均摊 O(1)（单次最坏 O(h)），`hasNext` O(1)。
- **空间复杂度 O(h)**：栈里最多 h 个结点。

---

## ⚠️ 第五步：小白常见错误

1. **`Create` 返回局部变量的地址**：

   ```c
   BSTIterator it;              // ❌ 函数返回后 it 就失效了
   return &it;
   ```

   必须 `malloc` 一个对象再返回。
2. **`next` 里只弹栈，忘了压入右子树的左链**：示例中弹出 7 后若不压 15、9，后面就再也访问不到右子树。
3. **压右子树时只压了右孩子本身**：要从右孩子开始**一路向左**全部压栈，否则下一次弹出的是 15，而正确答案是 9。
4. **栈开固定大小 `stack[1000]`**：链状树深度可达 10⁵，会越界；要么开足 10⁵，要么像上面一样动态扩容。
5. **`Free` 里释放了树结点**：树属于调用者，迭代器不负责它；只释放自己 `malloc` 的栈和对象。
6. **思路一用全局数组存结果却不重置**：判题可能创建多个迭代器，全局变量会残留上一次的数据，所有状态都应放在结构体里。

---

## 📊 第六步：方法对比

| 方法 | next 时间 | hasNext 时间 | 额外空间 | 难度 | 建议 |
|---|---|---|---|---|---|
| 预先中序展开成数组 | O(1) | O(1) | O(n) | ⭐ | 先写这个保证正确 |
| 栈 + 受控中序遍历 | 均摊 O(1) | O(1) | O(h) | ⭐⭐ | 推荐，满足进阶要求 |

---

## 🔗 举一反三

- **94. 二叉树的中序遍历**：本题思路二就是把它的迭代写法"拆开"。
- **230. 二叉搜索树中第 K 小的元素**：用本题的迭代器调用 k 次 `next` 即可。
- **284. 窥视迭代器**：另一道迭代器设计题，多了 `peek` 操作。
- **思考题**：如果还要支持 `prev()`（回到上一个更小的数），你会怎么设计？
