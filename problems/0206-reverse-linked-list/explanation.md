# 206. 反转链表 —— 小白详细题解

> 链表题的"九九乘法表"。几乎所有复杂的链表题（K 个一组翻转、回文链表、重排链表……）都要用到它，一定要亲手写熟。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 给你一串用箭头连起来的结点 `1 -> 2 -> 3 -> 4 -> 5`，请你把**所有箭头都掉个头**，变成 `5 -> 4 -> 3 -> 2 -> 1`，并返回新的第一个结点。

用示例 1 看看每个结点的 `next` 是怎么变的：

| 结点 | 反转前 next 指向 | 反转后 next 指向 |
|---|---|---|
| 1 | 2 | NULL（变成了最后一个） |
| 2 | 3 | 1 |
| 3 | 4 | 2 |
| 4 | 5 | 3 |
| 5 | NULL | 4（变成了头结点） |

**几个需要注意的细节：**

1. 空链表（`head == NULL`）要返回 `NULL`，不能崩溃。
2. 原来的头结点反转后变成**尾结点**，它的 `next` 必须改成 `NULL`，否则会形成环。
3. 返回的是**原来的最后一个结点**，不是 `head`。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 结构体指针和 `->`

```c
struct ListNode {
    int val;                 // 结点里存的数
    struct ListNode *next;   // 指向下一个结点的指针，最后一个结点的 next 是 NULL
};
```

`p->next` 等价于 `(*p).next`：顺着指针 `p` 找到那个结点，再取它的 `next` 成员。

### 2. 改指针之前先"备份"

链表只能顺着 `next` 往后走。如果你直接写 `cur->next = prev;`，那 `cur` 后面的结点就再也找不到了（没有任何变量记着它）。所以要先：

```c
struct ListNode* next = cur->next;   // 先把后面的链表"抓住"
cur->next = prev;                    // 再放心地改箭头
```

---

## 💡 第三步：思路一 —— 借助数组（最容易想到）

### 思路

链表不能"倒着走"，但数组可以！

1. 先遍历一遍链表，把所有**结点指针**依次存进数组 `nodes`
2. 再倒着遍历数组，让 `nodes[i]->next = nodes[i-1]`
3. `nodes[0]`（原来的头）的 `next` 设为 `NULL`，返回 `nodes[n-1]`

### 手动模拟（示例 2：`head = [1,2]`）

| 步骤 | 操作 | 结果 |
|---|---|---|
| 1 | 存数组 | nodes = [结点1, 结点2]，n = 2 |
| 2 | i = 1：nodes[1]->next = nodes[0] | 2 -> 1 |
| 3 | nodes[0]->next = NULL | 2 -> 1 -> NULL |
| 4 | 返回 nodes[1] | [2,1] |

### 代码

```c
struct ListNode* reverseList(struct ListNode* head) {
    if (head == NULL) return NULL;          // 空链表直接返回

    // 1. 数一数有多少个结点
    int n = 0;
    for (struct ListNode* p = head; p != NULL; p = p->next) n++;

    // 2. 把结点指针依次存进数组
    struct ListNode** nodes = (struct ListNode**)malloc(sizeof(struct ListNode*) * n);
    int i = 0;
    for (struct ListNode* p = head; p != NULL; p = p->next) nodes[i++] = p;

    // 3. 倒着把箭头连起来：第 i 个指向第 i-1 个
    for (i = n - 1; i > 0; i--) {
        nodes[i]->next = nodes[i - 1];
    }
    nodes[0]->next = NULL;                  // 原来的头变成了尾巴

    struct ListNode* newHead = nodes[n - 1];
    free(nodes);                            // 数组用完要释放（结点本身不能释放！）
    return newHead;
}
```

> 💬 `struct ListNode**` 是"指向结点指针的指针"，在这里就当作"元素类型是 `struct ListNode*` 的数组"。

### 复杂度分析

- **时间复杂度 O(n)**：遍历两遍链表 + 一遍数组。
- **空间复杂度 O(n)**：数组存了 n 个指针。

---

## 🚀 第四步：思路二 —— 迭代，三个指针原地反转（最优）

### 思路

能不能不要数组？可以！我们从头往后走，**一边走一边把箭头掉头**：

- `prev`：已经反转好的那一段的头（一开始是 `NULL`）
- `cur`：当前正要处理的结点（一开始是 `head`）
- `next`：临时变量，备份 `cur` 原来的下一个结点

每一步做四件事：**备份 next → 掉头 → prev 前进 → cur 前进**。

### 手动模拟（示例 1：`[1,2,3,4,5]`）

| 步骤 | cur | next（备份） | 执行 cur->next = prev 后 | prev 指向的已反转部分 |
|---|---|---|---|---|
| 开始 | 1 | - | - | NULL |
| 1 | 1 | 2 | 1 -> NULL | 1 |
| 2 | 2 | 3 | 2 -> 1 | 2 -> 1 |
| 3 | 3 | 4 | 3 -> 2 | 3 -> 2 -> 1 |
| 4 | 4 | 5 | 4 -> 3 | 4 -> 3 -> 2 -> 1 |
| 5 | 5 | NULL | 5 -> 4 | 5 -> 4 -> 3 -> 2 -> 1 |

`cur` 变成 `NULL`，循环结束，返回 `prev`（结点 5）。

### 代码

```c
struct ListNode* reverseList(struct ListNode* head) {
    struct ListNode* prev = NULL;   // 已反转部分的头，一开始什么都没有
    struct ListNode* cur = head;    // 当前要处理的结点

    while (cur != NULL) {
        struct ListNode* next = cur->next;  // 1. 备份：先记住后面的链表
        cur->next = prev;                   // 2. 掉头：当前结点指向前一个
        prev = cur;                         // 3. prev 前进一步
        cur = next;                         // 4. cur 前进一步
    }
    return prev;                    // cur 为 NULL 时，prev 就是新的头结点
}
```

空链表时 `cur` 一开始就是 `NULL`，循环一次都不执行，直接返回 `NULL`，不需要特判。

### 复杂度分析

- **时间复杂度 O(n)**：每个结点只处理一次。
- **空间复杂度 O(1)**：只用了 3 个指针变量。

---

## 🌀 补充：思路三 —— 递归

递归的想法："先把 `head` 后面的部分反转好，再把 `head` 接到末尾"。

```c
struct ListNode* reverseList(struct ListNode* head) {
    // 递归出口：空链表或只有一个结点，反转后就是自己
    if (head == NULL || head->next == NULL) return head;

    // 先把 head->next 开头的后半段反转，newHead 是反转后的头（原来的最后一个结点）
    struct ListNode* newHead = reverseList(head->next);

    // 此时 head->next 是后半段反转后的"尾巴"，让它指回 head
    head->next->next = head;
    head->next = NULL;              // head 变成新的尾巴
    return newHead;
}
```

递归简洁，但需要 O(n) 的函数调用栈空间；链表特别长时（比如几十万个结点）可能栈溢出。

---

## ⚠️ 第五步：小白常见错误

1. **没有备份 `next` 就改箭头**：先写 `cur->next = prev;` 再写 `cur = cur->next;`，此时 `cur->next` 已经是 `prev` 了，`cur` 会往回走，结果错误甚至死循环。
2. **返回 `head` 而不是 `prev`**：`head` 反转后是尾结点，返回它只会得到 `[1]`。
3. **忘记把原头结点的 `next` 设为 `NULL`**（数组写法、递归写法常见）：结点 1 和结点 2 互相指向，形成环，输出会无限长。
4. **空链表崩溃**：数组写法里没判断 `head == NULL` 就访问 `nodes[0]->next`，会访问空指针导致 Runtime Error。
5. **`free` 了结点**：思路一里只能 `free(nodes)` 这个指针数组，千万别 `free` 链表结点本身，否则返回的链表就是野指针。
6. **递归写法里漏了 `head->next = NULL`**：同第 3 条，会形成环。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 借助数组 | O(n) | O(n) | ⭐ | 帮助理解"箭头掉头" |
| 迭代三指针 | O(n) | O(1) | ⭐⭐ | **必须背熟**，面试首选 |
| 递归 | O(n) | O(n) 栈 | ⭐⭐⭐ | 练习递归思维 |

> 🎯 **学习建议**：拿一张纸画出 5 个方框和箭头，按照迭代写法的四步亲手改一遍箭头，比看十遍代码都管用。

---

## 🔗 举一反三

- **92. 反转链表 II**：只反转第 `left` 到第 `right` 个结点。
- **24. 两两交换链表中的节点**、**25. K 个一组翻转链表**：反转的"分段版"。
- **234. 回文链表**：把后半段反转后与前半段比较。
- **思考题**：如果要求"反转后输出，但不能修改原链表"，你会怎么做？
