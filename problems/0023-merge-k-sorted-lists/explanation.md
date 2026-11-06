# 23. 合并 K 个升序链表 —— 小白详细题解

> 这道"困难题"其实是第 21 题"合并两个有序链表"的升级版。难点不在代码，而在于**怎样合并才不会做重复劳动**。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 给你 K 条各自排好序的链表，把它们**全部合成一条**排好序的链表。

示例 1：

| 链表 | 内容 |
|---|---|
| lists[0] | 1 -> 4 -> 5 |
| lists[1] | 1 -> 3 -> 4 |
| lists[2] | 2 -> 6 |
| 合并结果 | 1 -> 1 -> 2 -> 3 -> 4 -> 4 -> 5 -> 6 |

**几个需要注意的细节：**

1. `lists` 可能是**空数组**（`listsSize == 0`，示例 2），要返回 `NULL`。
2. `lists` 里可能有**空链表**（`lists[i] == NULL`，示例 3），不能直接访问 `lists[i]->val`。
3. 设所有链表的结点总数为 N（≤ 10⁴），链表个数为 K（≤ 10⁴）。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. `struct ListNode** lists` 是什么？

它是一个数组，数组的每个元素是一个 `struct ListNode*`（某条链表的头指针）：

```c
lists[0]         // 第 0 条链表的头结点指针
lists[0]->val    // 第 0 条链表头结点的值（前提：lists[0] != NULL）
```

### 2. 合并两个有序链表（第 21 题）

本题所有方法都依赖这个零件，务必熟练：

```c
static struct ListNode* mergeTwo(struct ListNode* a, struct ListNode* b) {
    struct ListNode dummy;                  // 哑结点
    struct ListNode* tail = &dummy;         // 结果链表的尾巴
    while (a != NULL && b != NULL) {
        if (a->val <= b->val) { tail->next = a; a = a->next; }
        else                  { tail->next = b; b = b->next; }
        tail = tail->next;
    }
    tail->next = (a != NULL) ? a : b;       // 剩下的整段接上
    return dummy.next;
}
```

---

## 💡 第三步：思路一 —— 逐一合并（最容易想到）

### 思路

用一个变量 `ans` 表示"目前合并好的结果"，一开始是 `NULL`（空链表）。然后依次把 `lists[0]`、`lists[1]`……合并进去：

```
ans = merge(ans, lists[0])
ans = merge(ans, lists[1])
ans = merge(ans, lists[2])
……
```

### 手动模拟（示例 1）

| 步骤 | 合并 | ans |
|---|---|---|
| 1 | NULL + [1,4,5] | [1,4,5] |
| 2 | [1,4,5] + [1,3,4] | [1,1,3,4,4,5] |
| 3 | [1,1,3,4,4,5] + [2,6] | [1,1,2,3,4,4,5,6] |

### 代码

```c
// 合并两个有序链表（第 21 题）
static struct ListNode* mergeTwo(struct ListNode* a, struct ListNode* b) {
    struct ListNode dummy;
    struct ListNode* tail = &dummy;
    while (a != NULL && b != NULL) {
        if (a->val <= b->val) { tail->next = a; a = a->next; }
        else                  { tail->next = b; b = b->next; }
        tail = tail->next;
    }
    tail->next = (a != NULL) ? a : b;
    return dummy.next;
}

struct ListNode* mergeKLists(struct ListNode** lists, int listsSize) {
    struct ListNode* ans = NULL;               // 一开始结果是空链表
    for (int i = 0; i < listsSize; i++) {
        ans = mergeTwo(ans, lists[i]);         // 把第 i 条链表合并进结果
    }
    return ans;                                // listsSize == 0 时直接返回 NULL
}
```

`mergeTwo` 本身就能处理 `NULL`（空链表），所以不需要额外特判空链表。

### 复杂度分析

- **时间复杂度 O(K·N)**：`ans` 越来越长，每次合并都要把它从头再走一遍。最坏情况（K 条长度为 1 的链表）大约走 1 + 2 + … + K ≈ K²/2 步。本题 K ≤ 10⁴，约 5×10⁷ 步，能过，但不够快。
- **空间复杂度 O(1)**。

---

## 🚀 第四步：思路二 —— 分治合并（两两配对）

### 思路

思路一慢在：**前面合并好的长链表被反复遍历**。

改进：像比赛"淘汰赛"一样**两两配对**合并：

- 第 1 轮：(0,1) (2,3) (4,5) …… K 条变成 K/2 条
- 第 2 轮：再两两合并，K/2 条变成 K/4 条
- ……一共 log₂K 轮，就只剩 1 条

每一轮里，**每个结点只被访问一次**，所以每轮总工作量是 O(N)，总共 O(N log K)。

用递归写最简洁：`mergeRange(l, r)` 表示"合并 `lists[l..r]`"：

- `l > r`：没有链表，返回 `NULL`
- `l == r`：只有一条，直接返回它
- 否则：从中间 `mid` 劈开，分别合并左右两半，再把两个结果合并

### 手动模拟（示例 1：K = 3）

```
mergeRange(0, 2)
├── mergeRange(0, 1)
│   ├── mergeRange(0, 0) = [1,4,5]
│   ├── mergeRange(1, 1) = [1,3,4]
│   └── 合并 → [1,1,3,4,4,5]
├── mergeRange(2, 2) = [2,6]
└── 合并 → [1,1,2,3,4,4,5,6]
```

### 代码

```c
// 合并两个有序链表（第 21 题）
static struct ListNode* mergeTwo(struct ListNode* a, struct ListNode* b) {
    struct ListNode dummy;
    struct ListNode* tail = &dummy;
    while (a != NULL && b != NULL) {
        if (a->val <= b->val) { tail->next = a; a = a->next; }
        else                  { tail->next = b; b = b->next; }
        tail = tail->next;
    }
    tail->next = (a != NULL) ? a : b;
    return dummy.next;
}

// 合并 lists[l] 到 lists[r] 这一段链表
static struct ListNode* mergeRange(struct ListNode** lists, int l, int r) {
    if (l > r) return NULL;                    // 一条都没有
    if (l == r) return lists[l];               // 只有一条，不用合并
    int mid = l + (r - l) / 2;                 // 从中间劈开
    struct ListNode* left = mergeRange(lists, l, mid);        // 合并左半边
    struct ListNode* right = mergeRange(lists, mid + 1, r);   // 合并右半边
    return mergeTwo(left, right);              // 左右两个结果再合并
}

struct ListNode* mergeKLists(struct ListNode** lists, int listsSize) {
    return mergeRange(lists, 0, listsSize - 1);   // listsSize == 0 时 l > r，返回 NULL
}
```

### 复杂度分析

- **时间复杂度 O(N log K)**：log K 层，每层 O(N)。
- **空间复杂度 O(log K)**：递归深度。

---

## 🌟 第五步：思路三 —— 小根堆（优先队列）

### 思路

换一个角度：合并结果的**下一个结点**，一定是 K 条链表**当前头结点中最小的那个**。

如果每次都在 K 个头结点里线性找最小值，要 O(K)，太慢。用**小根堆**（一种能 O(log K) 取出最小值的数据结构）：

1. 把所有非空链表的头结点放进堆
2. 每次弹出堆顶（最小的结点），接到结果链表末尾
3. 如果它后面还有结点，把 `next` 放进堆
4. 堆空了就结束

> 💬 **小根堆**是一棵用数组存储的完全二叉树：`heap[i]` 的孩子是 `heap[2i+1]` 和 `heap[2i+2]`，父亲是 `heap[(i-1)/2]`，并且**每个父亲都不大于它的孩子**，所以 `heap[0]` 永远是最小值。插入时把新元素放末尾然后"上浮"，删除堆顶时把末尾元素挪到顶部然后"下沉"。

### 代码

```c
// 往小根堆里插入结点 node（按 val 比较），*size 是堆中元素个数
static void heapPush(struct ListNode** heap, int* size, struct ListNode* node) {
    int i = (*size)++;
    heap[i] = node;                              // 先放到末尾
    while (i > 0) {                              // 上浮：比父亲小就交换
        int parent = (i - 1) / 2;
        if (heap[parent]->val <= heap[i]->val) break;
        struct ListNode* t = heap[parent];
        heap[parent] = heap[i];
        heap[i] = t;
        i = parent;
    }
}

// 弹出并返回堆顶（最小的结点）
static struct ListNode* heapPop(struct ListNode** heap, int* size) {
    struct ListNode* top = heap[0];
    heap[0] = heap[--(*size)];                   // 末尾元素挪到堆顶
    int i = 0;
    while (1) {                                  // 下沉：和较小的孩子交换
        int l = 2 * i + 1, r = 2 * i + 2, smallest = i;
        if (l < *size && heap[l]->val < heap[smallest]->val) smallest = l;
        if (r < *size && heap[r]->val < heap[smallest]->val) smallest = r;
        if (smallest == i) break;
        struct ListNode* t = heap[smallest];
        heap[smallest] = heap[i];
        heap[i] = t;
        i = smallest;
    }
    return top;
}

struct ListNode* mergeKLists(struct ListNode** lists, int listsSize) {
    struct ListNode** heap = (struct ListNode**)malloc(sizeof(struct ListNode*) * (listsSize + 1));
    int size = 0;
    for (int i = 0; i < listsSize; i++) {
        if (lists[i] != NULL) heapPush(heap, &size, lists[i]);   // 只放非空链表的头
    }

    struct ListNode dummy;
    struct ListNode* tail = &dummy;
    dummy.next = NULL;
    while (size > 0) {
        struct ListNode* node = heapPop(heap, &size);   // 当前所有头结点中最小的
        tail->next = node;
        tail = node;
        if (node->next != NULL) heapPush(heap, &size, node->next);   // 它的下一个补进堆
    }
    tail->next = NULL;
    free(heap);
    return dummy.next;
}
```

### 复杂度分析

- **时间复杂度 O(N log K)**：每个结点进出堆各一次，每次 O(log K)。
- **空间复杂度 O(K)**：堆里最多 K 个结点。

---

## ⚠️ 第六步：小白常见错误

1. **没处理 `listsSize == 0`**：直接访问 `lists[0]` 会越界。
2. **访问空链表的 `val`**：`lists[i]` 可能是 `NULL`，写 `lists[i]->val` 会崩溃（示例 3）。堆写法里一定要先判断非空再入堆。
3. **把所有值拷进数组排序后 `malloc` 新链表**：能 AC，但没有利用"已经有序"的条件，面试时不是想要的答案。
4. **分治写法的 `mid` 和递归区间写错**：写成 `mergeRange(l, mid - 1)` 和 `mergeRange(mid, r)` 时，`l + 1 == r` 会得到 `mid == l`，左区间为空、右区间不变，无限递归。
5. **堆的下沉只和左孩子比较**：要在左右孩子中选**较小**的那个交换，否则堆的性质被破坏，结果不是有序的。
6. **合并两个链表时忘了接上剩余部分**：会丢失结点。

---

## 📊 第七步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 逐一合并 | O(K·N) | O(1) | ⭐ | 先写这个，理解问题 |
| 分治合并 | O(N log K) | O(log K) | ⭐⭐ | **推荐**，代码短且最优 |
| 小根堆 | O(N log K) | O(K) | ⭐⭐⭐ | 学习"堆"这个数据结构的好机会 |

> 🎯 **学习建议**：分治合并和第 148 题"排序链表"的归并排序几乎一模一样——那里是把一条链表拆开再合并，这里是一开始就已经拆好了。

---

## 🔗 举一反三

- **21. 合并两个有序链表**：本题的基本零件。
- **148. 排序链表**：同样的分治 + 合并思想。
- **215. 数组中的第 K 个最大元素**、**347. 前 K 个高频元素**：经典的堆应用。
- **思考题**：如果 K 条链表非常长、内存放不下，只能一个一个结点地"流式"读取，哪种方法最合适？
