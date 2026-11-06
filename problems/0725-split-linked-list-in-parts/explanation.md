# 725. 分隔链表 —— 小白详细题解

> 本题的难点不在算法，而在于两件事：**算清楚每段多长**，以及**返回一个"链表指针数组"**。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 把链表按顺序切成 `k` 段，各段长度尽量平均（最多差 1），**长的在前，短的在后**。段数不够分时，后面的段就是空的。

算每段长度：设链表长度为 `n`，

- 每段至少 `n / k` 个结点
- 还剩 `n % k` 个结点，分给**前** `n % k` 段，每段多 1 个

| 示例 | n | k | n / k | n % k | 各段长度 |
|---|---|---|---|---|---|
| 示例 1 | 3 | 5 | 0 | 3 | 1, 1, 1, 0, 0 |
| 示例 2 | 10 | 3 | 3 | 1 | 4, 3, 3 |

```
示例 2：1 -> 2 -> 3 -> 4 | 5 -> 6 -> 7 | 8 -> 9 -> 10
              第 0 段         第 1 段        第 2 段
```

**几个需要注意的细节：**

1. 返回的数组长度**永远是 `k`**，即使有些段是空的（`NULL`）。
2. 每段的最后一个结点要**切断**（`next = NULL`），否则第 0 段会一直连到链表末尾。
3. 空链表时 `k` 段全是 `NULL`。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 返回"链表指针数组"：`struct ListNode**`

```c
struct ListNode** parts = (struct ListNode**)malloc(sizeof(struct ListNode*) * k);
parts[0] = head;     // 每个元素都是一个 struct ListNode*，即某一段的头指针
parts[4] = NULL;     // 空段用 NULL 表示
```

注意 `sizeof(struct ListNode*)`（指针的大小），不是 `sizeof(struct ListNode)`（结点的大小）。

### 2. `*returnSize`

C 语言的函数只能返回一个值，数组的长度要通过指针参数"带出去"：

```c
*returnSize = k;     // 告诉调用者：返回的数组有 k 个元素
```

忘记写这一行，判题程序就不知道数组有多长，输出会是空的或乱码。

### 3. 切断链表

走到某段的最后一个结点 `cur` 时：

```c
struct ListNode* next = cur->next;   // 先记住下一段的头
cur->next = NULL;                    // 切断
cur = next;                          // 去下一段
```

---

## 💡 第三步：思路一 —— 先把结点存进数组，再按下标切

### 思路

1. 把所有结点指针存进数组 `nodes[0..n-1]`
2. 用变量 `start` 表示当前段的起始下标，第 `i` 段长度为 `len`：
   - `parts[i] = len > 0 ? nodes[start] : NULL`
   - 如果 `len > 0`，把这一段最后一个结点 `nodes[start + len - 1]` 的 `next` 设为 `NULL`
   - `start += len`

### 代码

```c
struct ListNode** splitListToParts(struct ListNode* head, int k, int* returnSize) {
    // 1. 把结点指针存进数组（最多 1000 个）
    struct ListNode* nodes[1000];
    int n = 0;
    for (struct ListNode* p = head; p != NULL; p = p->next) nodes[n++] = p;

    struct ListNode** parts = (struct ListNode**)malloc(sizeof(struct ListNode*) * k);
    int start = 0;                              // 当前段的起始下标
    for (int i = 0; i < k; i++) {
        int len = n / k + (i < n % k ? 1 : 0);  // 前 n%k 段多一个
        if (len == 0) {
            parts[i] = NULL;                    // 空段
        } else {
            parts[i] = nodes[start];                 // 这一段的头
            nodes[start + len - 1]->next = NULL;     // 这一段的尾巴切断
        }
        start += len;
    }
    *returnSize = k;                            // 别忘了！
    return parts;
}
```

### 复杂度分析

- **时间复杂度 O(n + k)**，**空间复杂度 O(n)**（指针数组，不算返回值）。

---

## 🚀 第四步：思路二 —— 直接在链表上走（最优）

### 思路

1. 遍历一遍求出长度 `n`
2. `cur` 从 `head` 出发，对第 `i` 段：
   - `parts[i] = cur`（空段时 `cur` 恰好是 `NULL`）
   - 算出长度 `size`，让 `cur` 再走 `size - 1` 步到达这一段的最后一个结点
   - 切断，`cur` 移到下一段的开头

### 手动模拟（示例 2：n = 10，k = 3）

| 段 i | size | parts[i] | cur 走到 | 切断后 cur |
|---|---|---|---|---|
| 0 | 4 | 1 | 4 | 5 |
| 1 | 3 | 5 | 7 | 8 |
| 2 | 3 | 8 | 10 | NULL |

### 代码

```c
struct ListNode** splitListToParts(struct ListNode* head, int k, int* returnSize) {
    // 1. 求链表长度
    int n = 0;
    for (struct ListNode* p = head; p != NULL; p = p->next) n++;

    int base = n / k;          // 每段的基本长度
    int extra = n % k;         // 前 extra 段要多 1 个
    struct ListNode** parts = (struct ListNode**)malloc(sizeof(struct ListNode*) * k);

    struct ListNode* cur = head;
    for (int i = 0; i < k; i++) {
        parts[i] = cur;                              // 这一段的头（空段时 cur 是 NULL）
        int size = base + (i < extra ? 1 : 0);       // 这一段的长度
        for (int j = 0; j < size - 1; j++) {
            cur = cur->next;                         // 走到这一段的最后一个结点
        }
        if (size > 0) {
            struct ListNode* next = cur->next;       // 记住下一段的头
            cur->next = NULL;                        // 切断
            cur = next;
        }
    }
    *returnSize = k;
    return parts;
}
```

> 💬 为什么空段时 `cur` 一定是 `NULL`？`size == 0` 说明 `base == 0` 且 `i >= extra`，也就是说前面的段已经把 `n` 个结点全部分完了。

### 复杂度分析

- **时间复杂度 O(n + k)**：求长度一遍，切分一遍，外加 `k` 次循环。
- **空间复杂度 O(1)**（不算返回的数组）。

---

## ⚠️ 第五步：小白常见错误

1. **忘记 `*returnSize = k`**：判题程序拿到的长度是 0，输出 `[]`。
2. **`malloc` 用了 `sizeof(struct ListNode)`**：虽然分配得更多不会出错，但说明没搞清楚数组元素是**指针**。
3. **没有切断**：第 0 段会一直连到链表末尾，输出 `[[1,2,3,4,5,6,7,8,9,10],[5,6,7,8,9,10],[8,9,10]]`。
4. **多出来的结点分给了后面的段**：题目要求"前面的段长度大于等于后面的"，`i < extra` 的段才多 1 个。
5. **`size == 0` 时还去访问 `cur->next`**：此时 `cur` 是 `NULL`，会崩溃。要先判断 `size > 0`。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 存数组按下标切 | O(n + k) | O(n) | ⭐ | 下标计算直观 |
| 直接在链表上走 | O(n + k) | O(1) | ⭐⭐ | **推荐** |

---

## 🔗 举一反三

- **61. 旋转链表**：同样要先求长度、再找到"切断点"。
- **86. 分隔链表**（同名不同题）：按值把链表分成两部分。
- **思考题**：如果要求**短的段在前、长的段在后**，长度公式要怎么改？
