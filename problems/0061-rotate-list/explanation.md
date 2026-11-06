# 61. 旋转链表 —— 小白详细题解

> 看起来要"转很多圈"，其实只要找对**新的尾巴**，剪一刀就完事了。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 每"旋转一次"，就把链表的**最后一个结点**搬到最前面。一共旋转 `k` 次，返回新的头结点。

用示例 1（`[1,2,3,4,5]`，`k = 2`）看看：

```
原链表：     1 -> 2 -> 3 -> 4 -> 5
旋转 1 次：  5 -> 1 -> 2 -> 3 -> 4      （5 搬到最前面）
旋转 2 次：  4 -> 5 -> 1 -> 2 -> 3      （4 搬到最前面）
```

观察结果：旋转 `k` 次 = **把最后 `k` 个结点整体搬到最前面**。

```
1 -> 2 -> 3 | 4 -> 5        在第 n-k = 3 个结点后面"剪开"
4 -> 5 -> 1 -> 2 -> 3       后半段接到前半段前面
```

**几个需要注意的细节：**

1. `k` 最大是 `2×10^9`，而链表最多 500 个结点。旋转 `n` 次（`n` 为长度）链表会**变回原样**，所以真正有效的次数是 `k % n`。示例 2 中 `n = 3, k = 4`，`4 % 3 = 1`，只需要旋转 1 次。
2. 空链表（`head == NULL`）要直接返回 `NULL`，此时**不能**计算 `k % n`（`n = 0` 时取模会崩溃）。
3. `k % n == 0` 时链表不变，直接返回 `head`。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 结构体指针和 `->`

```c
struct ListNode {
    int val;                 // 结点里存的数
    struct ListNode *next;   // 指向下一个结点，最后一个结点的 next 是 NULL
};
```

`p->next` 等价于 `(*p).next`。遍历链表的固定写法：

```c
for (struct ListNode* p = head; p != NULL; p = p->next) { /* 处理 p->val */ }
```

### 2. 取模运算 `%` 不能对 0 做

`k % n` 中如果 `n == 0`，程序会直接崩溃（除零错误）。所以一定要**先判空**再取模。

### 3. "剪断"链表就是把某个结点的 `next` 设成 `NULL`

链表的结尾由 `next == NULL` 决定。想在结点 `p` 后面剪开：先用变量记住 `p->next`（后半段的头），再写 `p->next = NULL`。

---

## 💡 第三步：思路一 —— 先断开再拼接

### 思路

1. 遍历一遍，求出长度 `n`，顺便找到尾结点 `tail`
2. `k = k % n`，如果 `k == 0` 直接返回
3. 从 `head` 出发走 `n - k - 1` 步，到达**新的尾结点** `newTail`（也就是第 `n-k` 个结点）
4. `newHead = newTail->next`；把 `newTail->next = NULL`（剪断）；再让 `tail->next = head`（拼接）

### 手动模拟（示例 1：`[1,2,3,4,5]`，`k = 2`）

| 步骤 | 操作 | 结果 |
|---|---|---|
| 1 | 求长度、找尾 | n = 5，tail = 结点 5 |
| 2 | k = 2 % 5 | k = 2 |
| 3 | 从 1 走 5-2-1 = 2 步 | newTail = 结点 3 |
| 4 | newHead = 结点 4；3->next = NULL | 1->2->3 和 4->5 |
| 5 | tail(5)->next = head(1) | 4->5->1->2->3 |

### 代码

```c
struct ListNode* rotateRight(struct ListNode* head, int k) {
    // 空链表或只有一个结点：怎么转都一样
    if (head == NULL || head->next == NULL) return head;

    // 1. 求长度 n，并找到尾结点 tail
    int n = 1;
    struct ListNode* tail = head;
    while (tail->next != NULL) {
        tail = tail->next;
        n++;
    }

    // 2. 只有 k % n 次旋转是"有效"的
    k = k % n;
    if (k == 0) return head;                // 转了整数圈，链表不变

    // 3. 找到新的尾结点：第 n-k 个结点，从 head 走 n-k-1 步
    struct ListNode* newTail = head;
    for (int i = 0; i < n - k - 1; i++) {
        newTail = newTail->next;
    }

    // 4. 剪断 + 拼接
    struct ListNode* newHead = newTail->next;   // 后半段的头就是新的头
    newTail->next = NULL;                       // 新尾巴后面剪断
    tail->next = head;                          // 原来的尾巴接上原来的头
    return newHead;
}
```

### 复杂度分析

- **时间复杂度 O(n)**：求长度一遍，找新尾巴最多再走一遍。
- **空间复杂度 O(1)**：只用了几个指针变量。

---

## 🚀 第四步：思路二 —— 先连成环，再剪开（代码更短）

### 思路

把尾结点和头结点连起来，链表就变成了一个**环**。旋转只是"换一个地方剪开这个环"：

```
1 -> 2 -> 3 -> 4 -> 5
^                   |
+-------------------+      连成环后，在 3 和 4 之间剪开 → 4->5->1->2->3
```

步骤：求长度并找尾 → `tail->next = head` 成环 → 走 `n-k-1` 步到新尾 → 新头 = 新尾的 next → 新尾的 next = NULL。

### 代码

```c
struct ListNode* rotateRight(struct ListNode* head, int k) {
    if (head == NULL || head->next == NULL || k == 0) return head;

    // 求长度并找到尾结点
    int n = 1;
    struct ListNode* tail = head;
    while (tail->next != NULL) {
        tail = tail->next;
        n++;
    }

    k %= n;
    if (k == 0) return head;

    tail->next = head;                     // 首尾相连，形成一个环

    // 新的尾结点是第 n-k 个结点
    struct ListNode* newTail = head;
    for (int i = 0; i < n - k - 1; i++) newTail = newTail->next;

    struct ListNode* newHead = newTail->next;
    newTail->next = NULL;                  // 在新尾巴处剪开环
    return newHead;
}
```

### 复杂度分析

- **时间复杂度 O(n)**，**空间复杂度 O(1)**。和思路一本质相同，只是拼接的时机不同。

> 💬 如果你忘了 `newTail->next = NULL`，环就没有被剪开，输出会无限长（判题程序会提示"链表可能有环"）。

---

## ⚠️ 第五步：小白常见错误

1. **老老实实转 k 次**：每次把尾结点搬到前面要 O(n)，转 `2×10^9` 次必然超时。一定要先 `k %= n`。
2. **空链表时做 `k % n`**：`n = 0` 时除零崩溃。先判断 `head == NULL`。
3. **新尾巴的步数算错**：新尾巴是第 `n-k` 个结点，从 `head`（第 1 个）出发只需走 `n-k-1` 步。多走一步结果就整体错位。
4. **成环后忘记剪开**：`tail->next = head` 之后必须 `newTail->next = NULL`，否则链表首尾相连，输出死循环。
5. **`k % n == 0` 时还去成环**：这时 `newTail` 会走到原来的尾结点，如果代码没处理好就会出错。提前 `return head` 最稳妥。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 逐次旋转 k 次 | O(n·k) | O(1) | ⭐ | 会超时，不可取 |
| 先断开再拼接 | O(n) | O(1) | ⭐⭐ | 思路清楚 |
| 先成环再剪开 | O(n) | O(1) | ⭐⭐ | 代码最短，推荐 |

---

## 🔗 举一反三

- **189. 轮转数组**：同样的问题换成数组，可以用"三次反转"做到 O(1) 空间。
- **19. 删除链表的倒数第 N 个结点**：同样需要定位"倒数第 k 个"，可以用快慢指针一次遍历。
- **思考题**：如果要求"向左"旋转 `k` 个位置，新的尾结点是第几个？
