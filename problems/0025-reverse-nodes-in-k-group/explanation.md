# 25. K 个一组翻转链表 —— 小白详细题解

> 困难题，但其实是"**206. 反转链表**"的分段版。只要把"反转一段"和"把这一段接回去"两件事分开想清楚，就不难。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 从头开始，每 `k` 个结点分成一组，每组**内部倒序**。最后不满 `k` 个的那组**保持原样**。

示例 1、2（`head = [1,2,3,4,5]`）：

| k | 分组 | 每组翻转后 | 结果 |
|---|---|---|---|
| 2 | (1,2) (3,4) (5) | (2,1) (4,3) (5) 不满 2 个不动 | `[2,1,4,3,5]` |
| 3 | (1,2,3) (4,5) | (3,2,1) (4,5) 不满 3 个不动 | `[3,2,1,4,5]` |

**几个需要注意的细节：**

1. **最后不足 k 个的部分不翻转**，这是和"全部翻转"最大的区别。
2. `k = 1` 时什么都不变；`k = n` 时就是整个链表反转。
3. 必须真正调整结点（改 `next`），不能只改 `val`——判题程序会检查。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 指针数组

```c
struct ListNode** arr = (struct ListNode**)malloc(sizeof(struct ListNode*) * n);
arr[i] = p;          // 第 i 个元素存的是一个结点的地址
arr[i]->next = ...;  // 通过地址修改那个结点
```

### 2. 反转链表（第 206 题）的核心四步

```c
struct ListNode* next = cur->next;   // 备份
cur->next = prev;                    // 掉头
prev = cur;                          // prev 前进
cur = next;                          // cur 前进
```

本题就是把它限制在"一段 k 个结点"里做。

---

## 💡 第三步：思路一 —— 存进数组，分段翻转后重新连接

### 思路

数组可以随意下标访问，翻转一段非常方便：

1. 把所有结点指针按顺序存进数组 `arr`
2. 对每个完整的段 `[i, i+k-1]`，在数组里把这一段**左右交换**倒过来
3. 最后按数组顺序重新连 `next`：`arr[j]->next = arr[j+1]`，最后一个指向 `NULL`

注意：我们在数组里交换的是**指针**，结点的 `val` 没有动，符合题意。

### 手动模拟（示例 2：k = 3）

| 步骤 | arr（显示结点的值） |
|---|---|
| 存数组 | [1, 2, 3, 4, 5] |
| 翻转段 [0, 2] | [**3, 2, 1**, 4, 5] |
| 段 [3, 5] 不完整（只有 2 个） | 不动 |
| 重新连接 | 3 -> 2 -> 1 -> 4 -> 5 |

### 代码

```c
struct ListNode* reverseKGroup(struct ListNode* head, int k) {
    // 1. 统计结点个数
    int n = 0;
    for (struct ListNode* p = head; p != NULL; p = p->next) n++;
    if (n == 0) return head;

    // 2. 把结点指针按顺序存进数组
    struct ListNode** arr = (struct ListNode**)malloc(sizeof(struct ListNode*) * n);
    int idx = 0;
    for (struct ListNode* p = head; p != NULL; p = p->next) arr[idx++] = p;

    // 3. 每个完整的 k 段，在数组里左右对调（i + k <= n 保证这一段是完整的）
    for (int i = 0; i + k <= n; i += k) {
        int l = i, r = i + k - 1;
        while (l < r) {
            struct ListNode* t = arr[l];   // 交换的是指针，不是 val
            arr[l] = arr[r];
            arr[r] = t;
            l++;
            r--;
        }
    }

    // 4. 按数组顺序重新连接
    for (int i = 0; i + 1 < n; i++) {
        arr[i]->next = arr[i + 1];
    }
    arr[n - 1]->next = NULL;               // 最后一个结点指向 NULL

    struct ListNode* newHead = arr[0];
    free(arr);
    return newHead;
}
```

### 复杂度分析

- **时间复杂度 O(n)**：存数组、翻转、重连各一遍。
- **空间复杂度 O(n)**：指针数组。

---

## 🚀 第四步：思路二 —— 原地分段翻转（O(1) 空间）

### 思路

进阶要求 O(1) 额外空间，就要直接在链表上一段一段地翻转。对每一段，记住 4 个关键结点：

```
prev -> start -> ... -> end -> next
        └──── 这 k 个要翻转 ────┘
```

- `prev`：这一段**前面**的结点（第一段的 prev 是哑结点 `dummy`）
- `start`：这一段的第一个结点（翻转后变成最后一个）
- `end`：这一段的最后一个结点（翻转后变成第一个）
- `next`：这一段**后面**的结点

每一轮：

1. 从 `prev` 往后走 k 步找 `end`；走不到（遇到 `NULL`）说明剩下不足 k 个，**结束**
2. 把 `start..end` 这一段反转。技巧：反转时让 `prev` 的初值取 `next` 而不是 `NULL`，这样 `start` 反转后直接就接上了后面的 `next`
3. `prev->next = end`（前面接上新的头）
4. `prev = start`（`start` 现在是这一段的尾巴，是下一段的"前一个结点"）

### 手动模拟（示例 1：k = 2）

| 轮次 | prev | start | end | next | 翻转后整条链表 |
|---|---|---|---|---|---|
| 1 | dummy | 1 | 2 | 3 | dummy -> **2 -> 1** -> 3 -> 4 -> 5 |
| 2 | 1 | 3 | 4 | 5 | dummy -> 2 -> 1 -> **4 -> 3** -> 5 |
| 3 | 3 | 5 | 走 2 步遇到 NULL | - | 不足 k 个，结束 |

### 代码

```c
struct ListNode* reverseKGroup(struct ListNode* head, int k) {
    struct ListNode dummy;                // 哑结点，第一段也有"前一个结点"
    dummy.next = head;
    struct ListNode* prev = &dummy;       // 当前段前面的结点

    while (1) {
        // 1. 从 prev 往后走 k 步，找到这一段的最后一个结点 end
        struct ListNode* end = prev;
        for (int i = 0; i < k && end != NULL; i++) {
            end = end->next;
        }
        if (end == NULL) break;           // 剩下不足 k 个，保持原样，结束

        struct ListNode* start = prev->next;  // 这一段的第一个结点
        struct ListNode* next = end->next;    // 这一段后面的结点

        // 2. 反转 start..end：q 初值取 next，这样 start 反转后自动指向 next
        struct ListNode* q = next;
        struct ListNode* p = start;
        while (p != next) {
            struct ListNode* t = p->next; // 备份
            p->next = q;                  // 掉头
            q = p;
            p = t;
        }

        // 3. 把翻转好的一段接回去：前面接 end（新的段头）
        prev->next = end;
        // 4. start 成了这一段的尾巴，作为下一段的 prev
        prev = start;
    }
    return dummy.next;
}
```

### 复杂度分析

- **时间复杂度 O(n)**：每个结点被"找 end"访问一次、被反转一次。
- **空间复杂度 O(1)**：只用了几个指针。

---

## ⚠️ 第五步：小白常见错误

1. **最后不足 k 个也翻转了**：没有先检查"够不够 k 个"就直接反转，`[1,2,3,4,5], k = 2` 会得到 `[2,1,4,3,5]` 没问题，但 `k = 3` 会错误地得到 `[3,2,1,5,4]`。
2. **翻转后没有接回去**：只反转了段内部，忘了 `prev->next = end`，结果前一段还指向旧的段头 `start`，中间的结点全部丢失。
3. **`prev` 更新成了 `end`**：翻转后 `end` 在这一段的**最前面**，`start` 才在最后面。下一段的前一个结点应该是 `start`。
4. **段内反转的初值用 `NULL`**：这样 `start->next` 变成 `NULL`，这一段和后面断开，需要再手动 `start->next = next`；忘了这一步就会丢失后面所有结点。
5. **只交换 `val`**：比如把一段的值存到数组里倒序写回，违反"必须实际进行节点交换"，判题程序会报错。
6. **数组写法中最后一个结点的 `next` 没设成 `NULL`**：原来的尾结点可能被换到中间，原来中间的某个结点到了末尾却还指着别人，形成环。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 指针数组 + 分段对调 | O(n) | O(n) | ⭐⭐ | 思路简单，先 AC |
| 原地分段翻转 | O(n) | O(1) | ⭐⭐⭐⭐ | 进阶要求，面试高频 |

> 🎯 **学习建议**：思路二建议先单独写一个"反转 start 到 end 这一段"的小函数，测试通过后再写外面"找段、接回去"的循环，把复杂问题拆小。

---

## 🔗 举一反三

- **206. 反转链表**：本题的基本零件。
- **24. 两两交换链表中的节点**：本题 k = 2 的特例。
- **92. 反转链表 II**：只反转第 left 到第 right 个结点，和本题的"反转一段并接回去"一模一样。
- **思考题**：如果要求最后不足 k 个的部分**也要翻转**，代码要改哪里？
