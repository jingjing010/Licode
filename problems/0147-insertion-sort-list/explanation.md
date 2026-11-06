# 147. 对链表进行插入排序 —— 小白详细题解

> 插入排序在数组上要"挪一大片元素"，在链表上却只需要改几个指针。这道题帮你把"在链表中间插入结点"练熟。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 像理扑克牌一样排序：左手是排好的牌，每次从右手拿一张，**从左往右**找到它该放的位置插进去。

用示例 1（`[4,2,1,3]`）走一遍：

| 步骤 | 取出的结点 | 插入位置 | 已排序部分 |
|---|---|---|---|
| 开始 | - | - | 4 |
| 1 | 2 | 4 的前面（最前面） | 2 -> 4 |
| 2 | 1 | 最前面 | 1 -> 2 -> 4 |
| 3 | 3 | 2 和 4 之间 | 1 -> 2 -> 3 -> 4 |

**几个需要注意的细节：**

1. 新结点可能插到**最前面**，所以头结点会变——用**哑结点**。
2. 要在结点 `prev` 后面插入，需要找到"**最后一个值 `<=` 当前值**"的结点 `prev`。
3. 题目要求用插入排序，复杂度 O(n²) 是允许的（n ≤ 5000）。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 在结点 `prev` 后面插入结点 `node`

```
插入前：prev -> A
插入后：prev -> node -> A
```

```c
node->next = prev->next;   // 1. 新结点先指向 A（顺序不能反！）
prev->next = node;         // 2. prev 再指向新结点
```

如果先写 `prev->next = node;`，`A` 就丢了，再写 `node->next = prev->next;` 会让 `node` 指向自己。

### 2. 哑结点

```c
struct ListNode dummy;     // 栈上的假结点
dummy.next = NULL;         // 一开始已排序链表是空的
```

在 `&dummy` 后面插入，就等于插到最前面，不需要特判。最后返回 `dummy.next`。

---

## 💡 第三步：思路一 —— 逐个取出，插入新的有序链表

### 思路

1. 准备一条空的有序链表（只有哑结点 `dummy`）
2. 从原链表依次取出结点 `cur`（**先备份 `cur->next`**）
3. 从 `dummy` 开始往后找，直到 `prev->next` 为空或 `prev->next->val > cur->val`
4. 把 `cur` 插到 `prev` 后面

### 代码

```c
struct ListNode* insertionSortList(struct ListNode* head) {
    struct ListNode dummy;          // 有序链表的哑结点
    dummy.next = NULL;              // 一开始有序链表为空

    struct ListNode* cur = head;    // 原链表中待插入的结点
    while (cur != NULL) {
        struct ListNode* next = cur->next;   // 备份：插入后 cur->next 会被改掉

        // 在有序链表里找插入位置：prev 是最后一个 <= cur->val 的结点
        struct ListNode* prev = &dummy;
        while (prev->next != NULL && prev->next->val <= cur->val) {
            prev = prev->next;
        }

        // 把 cur 插到 prev 后面
        cur->next = prev->next;
        prev->next = cur;

        cur = next;                          // 处理原链表的下一个结点
    }
    return dummy.next;
}
```

### 复杂度分析

- **时间复杂度 O(n²)**：每个结点都要从头找插入位置。即使原链表**已经有序**，也要每次走到有序链表的末尾。
- **空间复杂度 O(1)**。

---

## 🚀 第四步：思路二 —— 原地插入 + lastSorted 优化

### 思路

不新建链表，而是把原链表分成"前面已排序 + 后面未排序"两部分，用 `lastSorted` 记住**已排序部分的最后一个结点**。对于下一个结点 `cur = lastSorted->next`：

- 如果 `cur->val >= lastSorted->val`：它本来就该排在最后，**不用动**，`lastSorted = cur`
- 否则：先把 `cur` 从原位置**摘下来**（`lastSorted->next = cur->next`），再从 `dummy` 开始找位置插进去

已经有序的部分可以 O(1) 跳过，原链表本来就升序时只需 O(n)。

### 手动模拟（示例 2：`[-1,5,3,4,0]`）

| cur | lastSorted | 操作 | 链表 |
|---|---|---|---|
| 5 | -1 | 5 >= -1，lastSorted = 5 | -1 5 \| 3 4 0 |
| 3 | 5 | 摘下 3，插到 -1 后面 | -1 3 5 \| 4 0 |
| 4 | 5 | 摘下 4，插到 3 后面 | -1 3 4 5 \| 0 |
| 0 | 5 | 摘下 0，插到 -1 后面 | -1 0 3 4 5 |

### 代码

```c
struct ListNode* insertionSortList(struct ListNode* head) {
    if (head == NULL) return NULL;

    struct ListNode dummy;               // 哑结点，方便插到最前面
    dummy.next = head;
    struct ListNode* lastSorted = head;  // 已排序部分的最后一个结点
    struct ListNode* cur = head->next;   // 待插入的结点

    while (cur != NULL) {
        if (cur->val >= lastSorted->val) {
            lastSorted = cur;            // 已经在正确位置，已排序部分直接变长
        } else {
            // 从头找插入位置：prev 是最后一个 <= cur->val 的结点
            struct ListNode* prev = &dummy;
            while (prev->next->val <= cur->val) {
                prev = prev->next;
            }
            lastSorted->next = cur->next;    // 1. 把 cur 从原位置摘下
            cur->next = prev->next;          // 2. cur 指向插入位置的下一个
            prev->next = cur;                // 3. prev 指向 cur
        }
        cur = lastSorted->next;          // 下一个待插入的结点
    }
    return dummy.next;
}
```

> 💬 内层 `while` 为什么不用判断 `prev->next != NULL`？因为走到这里时 `cur->val < lastSorted->val`，所以最晚走到 `lastSorted` 时一定会停下，不会越界。

### 复杂度分析

- **时间复杂度 O(n²)**（最坏），原链表已有序时只需 O(n)。
- **空间复杂度 O(1)**。

---

## ⚠️ 第五步：小白常见错误

1. **插入时两行指针顺序写反**：先 `prev->next = cur;` 再 `cur->next = prev->next;`，`cur` 指向自己，形成环。
2. **思路一中没有先备份 `cur->next`**：插入后 `cur->next` 已指向有序链表里的结点，`cur = cur->next` 会在有序链表里打转。
3. **思路二中忘记"摘下"结点**：漏了 `lastSorted->next = cur->next;`，`cur` 同时出现在两个位置，链表成环。
4. **思路二中无论是否插入都执行 `lastSorted = cur`**：插入后 `lastSorted` 应该不变，否则它不再是已排序部分的末尾。
5. **比较用 `<` 还是 `<=`**：找插入位置时用 `<=` 能保证相同的值保持原顺序（稳定排序）；用 `<` 结果也对，但不稳定。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 插入新有序链表 | O(n²) | O(1) | ⭐⭐ | 最直观 |
| 原地 + lastSorted | O(n²)，有序时 O(n) | O(1) | ⭐⭐ | **推荐** |
| 归并排序（148 题） | O(n log n) | O(log n) | ⭐⭐⭐ | 不是本题要求的算法，但更快 |

---

## 🔗 举一反三

- **148. 排序链表**：要求 O(n log n)，用归并排序。
- **21. 合并两个有序链表**：归并排序的核心步骤。
- **思考题**：数组的插入排序需要把元素一个个往后挪，链表为什么不需要？链表插入排序比数组慢在哪里？（提示：找位置）
