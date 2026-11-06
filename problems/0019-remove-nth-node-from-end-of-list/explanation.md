# 19. 删除链表的倒数第 N 个结点 —— 小白详细题解

> 这道题能学到两个链表常用技巧：**哑结点**（解决"删头结点"的麻烦）和**快慢指针保持固定间距**（一趟扫描定位倒数第 n 个）。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 从链表**末尾往前数**第 n 个结点，把它删掉，返回新链表的头。

示例 1：`head = [1,2,3,4,5], n = 2`

| 正数位置 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| 值 | 1 | 2 | 3 | **4** | 5 |
| 倒数位置 | 5 | 4 | 3 | **2** | 1 |

倒数第 2 个是 4，删掉后得到 `[1,2,3,5]`。

**几个需要注意的细节：**

1. 倒数第 n 个 = 正数第 `L - n + 1` 个（L 是链表长度）。
2. **要删的可能是头结点**（比如 `n == L`，示例 2）。这时返回的头结点变了，要特别小心。
3. 删除后链表可能为空，返回 `NULL`。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 怎么删除链表中的一个结点？

单链表删除结点 `x`，必须找到它的**前一个结点** `prev`，然后让 `prev` 直接"跳过" `x`：

```c
struct ListNode* del = prev->next;   // 要删除的结点
prev->next = del->next;              // 前一个结点直接指向后一个，del 就从链表中"断开"了
free(del);                           // 释放被删结点的内存（可选，但是好习惯）
```

### 2. 哑结点：让头结点也有"前一个"

头结点没有前一个结点，删它时只能特殊处理。办法是在最前面放一个**假头** `dummy`：

```c
struct ListNode dummy;
dummy.next = head;   // dummy -> 1 -> 2 -> ...
// 现在每个真实结点都有"前一个"了，最后返回 dummy.next
```

---

## 💡 第三步：思路一 —— 先求长度，再删除（两趟扫描）

### 思路

1. 第一趟：数出链表长度 `L`
2. 要删的是正数第 `L - n + 1` 个，它的前一个是第 `L - n` 个
3. 从 `dummy`（看作第 0 个）出发走 `L - n` 步，就到了要删结点的前一个
4. 跳过它

### 手动模拟（示例 1：L = 5, n = 2）

从 dummy 出发走 `5 - 2 = 3` 步：

| 步数 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| prev | dummy | 1 | 2 | **3** |

`prev` 停在 3，`prev->next` 是 4，跳过它：`3 -> 5`。

### 代码

```c
struct ListNode* removeNthFromEnd(struct ListNode* head, int n) {
    // 1. 求链表长度
    int len = 0;
    for (struct ListNode* p = head; p != NULL; p = p->next) len++;

    // 2. 哑结点：保证要删除的结点一定有"前一个结点"（包括删头结点的情况）
    struct ListNode dummy;
    dummy.next = head;

    // 3. 从 dummy 出发走 len - n 步，到达"要删除结点的前一个"
    struct ListNode* prev = &dummy;
    for (int i = 0; i < len - n; i++) {
        prev = prev->next;
    }

    // 4. 删除 prev->next
    struct ListNode* del = prev->next;
    prev->next = del->next;
    free(del);

    return dummy.next;          // 头结点可能被删了，所以返回 dummy.next 而不是 head
}
```

### 复杂度分析

- **时间复杂度 O(L)**：遍历两遍。
- **空间复杂度 O(1)**。

---

## 🚀 第四步：思路二 —— 快慢指针（一趟扫描）

### 思路

想象两个人走路，`fast` 比 `slow` **领先 n 步**，两人同速前进。当 `fast` 走到**最后一个结点**时，`slow` 离最后一个结点也是 n 步——正好停在**倒数第 n+1 个**，也就是要删结点的前一个！

1. `fast`、`slow` 都从 `dummy` 出发
2. `fast` 先走 n 步
3. 两个一起走，直到 `fast->next == NULL`（fast 在最后一个结点）
4. 删除 `slow->next`

### 手动模拟（示例 1：n = 2）

链表：`dummy -> 1 -> 2 -> 3 -> 4 -> 5`

| 阶段 | slow | fast |
|---|---|---|
| 开始 | dummy | dummy |
| fast 先走 2 步 | dummy | 2 |
| 一起走 | 1 | 3 |
| 一起走 | 2 | 4 |
| 一起走 | 3 | 5（fast->next 为 NULL，停） |

`slow` 停在 3，删掉 `slow->next`（4）。

### 代码

```c
struct ListNode* removeNthFromEnd(struct ListNode* head, int n) {
    struct ListNode dummy;          // 哑结点
    dummy.next = head;
    struct ListNode* fast = &dummy;
    struct ListNode* slow = &dummy;

    // 1. fast 先走 n 步，和 slow 拉开 n 的距离
    for (int i = 0; i < n; i++) {
        fast = fast->next;
    }

    // 2. 一起走，直到 fast 到达最后一个结点
    while (fast->next != NULL) {
        fast = fast->next;
        slow = slow->next;
    }

    // 3. 此时 slow 是倒数第 n+1 个结点，删除它的下一个
    struct ListNode* del = slow->next;
    slow->next = del->next;
    free(del);

    return dummy.next;
}
```

### 复杂度分析

- **时间复杂度 O(L)**：只遍历一遍。
- **空间复杂度 O(1)**。

---

## ⚠️ 第五步：小白常见错误

1. **不用哑结点，删头结点时出错**：示例 2 `[1], n = 1` 要删的就是头结点，没有前一个结点，直接写 `prev->next = ...` 会访问空指针。
2. **返回 `head` 而不是 `dummy.next`**：头结点被删除（还被 `free` 了）后再返回 `head`，就是返回一个野指针。
3. **步数差一（off-by-one）**：快慢指针都从 `dummy` 出发时，`fast` 先走 n 步、循环条件是 `fast->next != NULL`；如果都从 `head` 出发，就要改成先走 n 步、条件是 `fast != NULL`……两套写法混用最容易出错。拿 `[1,2], n = 2` 手动验证一遍最保险。
4. **删除时只写 `slow->next = slow->next->next;` 就 `free(slow->next)`**：此时 `slow->next` 已经是下一个结点了，你释放的是错误的结点。要先用 `del` 保存被删结点。
5. **`struct ListNode* dummy;` 声明成指针却没有分配内存**：`dummy->next = head;` 会访问野指针。要么声明成结构体变量 `struct ListNode dummy;`，要么 `malloc`。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 扫描次数 | 建议 |
|---|---|---|---|---|
| 求长度后删除 | O(L) | O(1) | 2 趟 | 最直观，先写这个 |
| 快慢指针 | O(L) | O(1) | 1 趟 | 进阶要求，面试常考 |

> 🎯 **学习建议**：哑结点几乎可以用在所有"可能修改头结点"的链表题上，形成习惯能少踩很多坑。

---

## 🔗 举一反三

- **面试题 02.02. 返回倒数第 k 个节点**：只找不删，同样的快慢指针。
- **876. 链表的中间结点**：快指针走两步、慢指针走一步。
- **203. 移除链表元素**：删除所有等于 `val` 的结点，同样推荐用哑结点。
- **思考题**：如果 `n` 可能大于链表长度（题目不保证），你的代码会怎样？应该怎么防护？
