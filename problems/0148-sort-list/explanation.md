# 148. 排序链表 —— 小白详细题解

> 数组排序你可能已经会了，可链表不能用下标随便跳，很多排序算法都用不了。这道题告诉你：**归并排序**天生就适合链表。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 给你一条链表，把它按值从小到大排好，返回新的头结点。

示例 1：`[4,2,1,3]` → `[1,2,3,4]`。

**几个需要注意的细节：**

1. 链表可能为空（示例 3），也可能只有 1 个结点，这两种情况本身就是有序的，直接返回。
2. 最多 5×10⁴ 个结点。O(n²) 的排序（冒泡、插入）要做约 10⁹ 次比较，**会超时**。必须用 O(n log n) 的方法。
3. 排序后**头结点可能变了**（原来的头不一定是最小的），所以一定要返回新的头。
4. 值可能重复、可能为负数。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. `qsort`：C 标准库自带的排序

```c
int cmp(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b;
    return (x > y) - (x < y);    // x<y 返回 -1，x==y 返回 0，x>y 返回 1
}
qsort(arr, n, sizeof(int), cmp); // 对 int 数组 arr 的前 n 个元素升序排序
```

> ⚠️ 比较函数不要写成 `return x - y;`：当 `x`、`y` 一正一负且很大时，相减可能溢出 `int`。本题值不超过 10⁵ 不会溢出，但养成好习惯。

### 2. 合并两个有序链表（第 21 题）

归并排序的核心零件：

```c
static struct ListNode* merge(struct ListNode* a, struct ListNode* b) {
    struct ListNode dummy;                // 哑结点，放在栈上即可
    struct ListNode* tail = &dummy;
    while (a != NULL && b != NULL) {
        if (a->val <= b->val) { tail->next = a; a = a->next; }
        else                  { tail->next = b; b = b->next; }
        tail = tail->next;
    }
    tail->next = (a != NULL) ? a : b;     // 剩下的整段直接接上
    return dummy.next;
}
```

### 3. 快慢指针找中点

```c
struct ListNode *slow = head, *fast = head->next;
while (fast != NULL && fast->next != NULL) {
    slow = slow->next;
    fast = fast->next->next;
}
// slow 停在前半段的最后一个结点
```

`fast` 从 `head->next` 出发，能保证 2 个结点时 `slow` 停在第 1 个，把链表分成 1 + 1，而不是 2 + 0（2 + 0 会导致无限递归）。

---

## 💡 第三步：思路一 —— 拷到数组里排序（最容易想到）

### 思路

链表不好排，数组好排！

1. 遍历链表，把所有值存进数组
2. 用 `qsort` 排序
3. 再遍历一次链表，把排好的值按顺序**写回**每个结点

结点之间的连接关系一点没动，只是换了里面的值。

### 手动模拟（示例 1）

| 步骤 | 数组 | 链表 |
|---|---|---|
| 拷出 | [4,2,1,3] | 4 → 2 → 1 → 3 |
| qsort | [1,2,3,4] | 不变 |
| 写回 | | 1 → 2 → 3 → 4 |

### 代码

```c
static int cmpInt(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b;
    return (x > y) - (x < y);
}

struct ListNode* sortList(struct ListNode* head) {
    // 1. 数结点个数
    int n = 0;
    for (struct ListNode* p = head; p != NULL; p = p->next) n++;
    if (n <= 1) return head;                    // 0 或 1 个结点，已经有序

    // 2. 把值拷进数组
    int* vals = (int*)malloc(sizeof(int) * n);
    int i = 0;
    for (struct ListNode* p = head; p != NULL; p = p->next) vals[i++] = p->val;

    // 3. 排序
    qsort(vals, n, sizeof(int), cmpInt);

    // 4. 按顺序写回链表
    i = 0;
    for (struct ListNode* p = head; p != NULL; p = p->next) p->val = vals[i++];

    free(vals);
    return head;                                // 结点没动，头还是原来那个
}
```

### 复杂度分析

- **时间复杂度 O(n log n)**：`qsort` 的复杂度。
- **空间复杂度 O(n)**：额外数组。

> 💬 能 AC，但面试官想看的是"不借助数组，直接在链表上排序"。

---

## 🚀 第四步：思路二 —— 自顶向下归并排序（递归）

### 思路

归并排序三步走：

1. **拆**：用快慢指针找到中点，把链表**从中间断开**成两半
2. **递归**：分别把左半、右半排好序
3. **合**：把两个有序链表合并（第 21 题）

递归出口：空链表或只有 1 个结点，本来就有序。

### 手动模拟（示例 1：`4 2 1 3`）

```
sort(4 2 1 3)
├── 拆成 (4 2) 和 (1 3)
├── sort(4 2)
│   ├── 拆成 (4) 和 (2)
│   └── 合并 → 2 4
├── sort(1 3)
│   ├── 拆成 (1) 和 (3)
│   └── 合并 → 1 3
└── 合并 (2 4) 和 (1 3) → 1 2 3 4
```

### 代码

```c
// 合并两个有序链表（第 21 题）
static struct ListNode* merge(struct ListNode* a, struct ListNode* b) {
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

struct ListNode* sortList(struct ListNode* head) {
    if (head == NULL || head->next == NULL) return head;   // 0 或 1 个结点：已有序

    // 1. 快慢指针找中点：slow 停在前半段的末尾
    struct ListNode* slow = head;
    struct ListNode* fast = head->next;
    while (fast != NULL && fast->next != NULL) {
        slow = slow->next;
        fast = fast->next->next;
    }

    // 2. 从中间断开
    struct ListNode* right = slow->next;   // 后半段的头
    slow->next = NULL;                     // 前半段在这里结束

    // 3. 两半分别排序，再合并
    struct ListNode* l = sortList(head);
    struct ListNode* r = sortList(right);
    return merge(l, r);
}
```

### 复杂度分析

- **时间复杂度 O(n log n)**：每层拆分 + 合并共 O(n)，一共 log n 层。
- **空间复杂度 O(log n)**：递归栈的深度（每次对半拆）。

---

## 🌟 第五步：思路三 —— 自底向上归并排序（O(1) 空间）

### 思路

进阶要求常数空间，那就不能递归了。反过来想：

- 第 1 轮：每 **1** 个结点一组，相邻两组合并 → 得到若干长度为 2 的有序段
- 第 2 轮：每 **2** 个结点一组，相邻两组合并 → 长度为 4 的有序段
- 第 3 轮：每 **4** 个一组……
- 直到一组的长度 ≥ n，整条链表就有序了

需要一个小工具 `split(head, k)`：从 `head` 开始数 `k` 个结点，在那里断开，返回**剩下部分的头**。

### 手动模拟（示例 2：`-1 5 3 4 0`）

| 轮次 | 每组长度 | 合并过程 | 结果 |
|---|---|---|---|
| 1 | 1 | (-1)(5) → -1 5；(3)(4) → 3 4；(0) 单独 | -1 5 3 4 0 |
| 2 | 2 | (-1 5)(3 4) → -1 3 4 5；(0) 单独 | -1 3 4 5 0 |
| 3 | 4 | (-1 3 4 5)(0) → -1 0 3 4 5 | -1 0 3 4 5 |
| 4 | 8 ≥ 5 | 结束 | |

### 代码

```c
// 合并两个有序链表（第 21 题）
static struct ListNode* merge(struct ListNode* a, struct ListNode* b) {
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

// 从 head 开始保留 k 个结点并断开，返回剩余部分的头（不足 k 个时返回 NULL）
static struct ListNode* split(struct ListNode* head, int k) {
    for (int i = 1; head != NULL && i < k; i++) head = head->next;   // 走到第 k 个结点
    if (head == NULL) return NULL;
    struct ListNode* rest = head->next;
    head->next = NULL;                       // 断开
    return rest;
}

struct ListNode* sortList(struct ListNode* head) {
    // 1. 先数长度
    int n = 0;
    for (struct ListNode* p = head; p != NULL; p = p->next) n++;

    struct ListNode dummy;
    dummy.next = head;

    // 2. 每轮把长度为 step 的相邻两段合并，step 依次为 1、2、4、8……
    for (int step = 1; step < n; step *= 2) {
        struct ListNode* tail = &dummy;      // 已经处理好的部分的末尾
        struct ListNode* cur = dummy.next;   // 还没处理的部分的开头
        while (cur != NULL) {
            struct ListNode* left = cur;               // 第一段
            struct ListNode* right = split(left, step);   // 第二段
            cur = split(right, step);                  // 剩下的留给下一次
            tail->next = merge(left, right);           // 合并后接到已处理部分后面
            while (tail->next != NULL) tail = tail->next;   // tail 移到末尾
        }
    }
    return dummy.next;
}
```

### 复杂度分析

- **时间复杂度 O(n log n)**：一共 log n 轮，每轮拆分、合并、移动 `tail` 都是 O(n)。
- **空间复杂度 O(1)**：只用了几个指针，没有递归。

---

## ⚠️ 第六步：小白常见错误

1. **快慢指针都从 `head` 出发**：2 个结点时 `slow` 会走到第 2 个结点，拆成"2 个 + 0 个"，左边永远是 2 个，**无限递归**导致栈溢出。要让 `fast` 从 `head->next` 出发。
2. **找到中点后忘了断开**：没写 `slow->next = NULL`，左半段其实还是整条链表，同样无限递归。
3. **返回原来的 `head`**：归并排序会重新连接结点，原来的头可能跑到了中间。要返回 `merge` 的结果。
4. **用冒泡/插入排序**：O(n²)，5×10⁴ 个结点会超时。
5. **合并时忘了接上剩余部分** `tail->next = a ? a : b;`：会丢失结点。
6. **思路三里 `tail` 没有移动到末尾**：下一组合并结果会覆盖掉上一组，丢结点。

---

## 📊 第七步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 拷到数组 + qsort | O(n log n) | O(n) | ⭐ | 最快写出来的 AC 解法 |
| 自顶向下归并（递归） | O(n log n) | O(log n) | ⭐⭐ | **推荐**，面试标准答案 |
| 自底向上归并（迭代） | O(n log n) | O(1) | ⭐⭐⭐ | 满足进阶要求 |

> 🎯 **学习建议**：先把第 21 题"合并两个有序链表"和第 876 题"链表的中间结点"写熟，思路二就是把它们拼起来再加一层递归。

---

## 🔗 举一反三

- **21. 合并两个有序链表**：本题的核心零件。
- **23. 合并 K 个升序链表**：分治合并，思路几乎一样。
- **147. 对链表进行插入排序**：O(n²) 的链表排序，可以对比体会。
- **思考题**：快速排序能用在链表上吗？最坏情况会怎样？
