# 138. 随机链表的复制 —— 小白详细题解

> 复制一条普通链表很简单，难就难在每个结点还多了一根"随便乱指"的 `random` 指针。这道题能让你真正分清楚"**结点本身**"和"**结点里的值**"。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 给你一条链表，每个结点除了 `next`，还有一个 `random` 指针，可能指向链表里任意一个结点，也可能是 `NULL`。请你**照着它一模一样地再造一条**：新链表的结点必须全部是新 `malloc` 的，新结点的 `next`、`random` 也必须指向**新链表里**对应的结点。

示例 1：`[[7,null],[13,0],[11,4],[10,2],[1,0]]`，每一对是 `[值, random 指向的下标]`：

| 下标 | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| val | 7 | 13 | 11 | 10 | 1 |
| next 指向 | 1 | 2 | 3 | 4 | NULL |
| random 指向 | NULL | 0 | 4 | 2 | 0 |

复制后，新链表的第 2 个结点（11）的 `random` 必须指向**新链表**的第 4 个结点（1），而不是原链表的那个结点 1。

**几个需要注意的细节：**

1. 什么叫"深拷贝"？就是**完全独立的一份**：改动新链表不会影响原链表。所以新链表里**不能出现任何原链表的结点**，`random` 也不能指向原链表。
2. `random` 可能指向**自己**（比如 `[[1,0]]`），也可能指向**后面还没复制到的结点**——这就是难点：复制第 2 个结点时，它的 `random` 要指向第 4 个结点的副本，可那个副本还没造出来！
3. 链表可能为空，返回 `NULL`。
4. 值可能重复（示例 3 三个结点都是 3），所以**不能用值来找对应结点**。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 新的结构体 `struct Node`

```c
struct Node {
    int val;
    struct Node *next;
    struct Node *random;
};
```

和 `ListNode` 一样，只是多了一个指针成员。系统已经定义好了，你直接用。

### 2. `malloc` 新结点并初始化所有成员

```c
struct Node* c = (struct Node*)malloc(sizeof(struct Node));
c->val = 7;
c->next = NULL;      // malloc 出来的内存里是随机垃圾值，指针成员一定要赋值
c->random = NULL;
```

### 3. 指针数组

```c
struct Node** arr = (struct Node**)malloc(sizeof(struct Node*) * n);
arr[i] = p;          // 第 i 个格子存一个结点的地址
```

`struct Node**` 是"指向 `struct Node*` 的指针"，用来当作"装结点指针的数组"。

### 4. "对应关系"的关键

`random` 存的是**地址**。原结点的 `random` 指向原链表的某个结点 X，我们需要的是"X 的副本"的地址。所以核心问题是：**给一个原结点，怎么快速找到它的副本？**

---

## 💡 第三步：思路一 —— 用两个数组记录"原结点 ↔ 新结点"

### 思路

把原链表的结点按顺序编号 0, 1, 2, …：

1. 遍历原链表，把每个原结点存进数组 `old[i]`，同时 `malloc` 一个副本存进 `cp[i]`（先只填 `val`）
2. 把副本按顺序串起来：`cp[i]->next = cp[i+1]`
3. 处理 `random`：原结点 `old[i]->random` 指向某个原结点 X，在 `old` 数组里找到 X 的下标 `j`，那么 `cp[i]->random = cp[j]`

第 3 步"找下标"用最简单的线性查找，每次 O(n)，总共 O(n²)。本题 n ≤ 1000，n² = 10⁶，完全够快。

### 手动模拟（示例 2：`[[1,1],[2,1]]`）

| 步骤 | 操作 | 结果 |
|---|---|---|
| 1 | old = [A, B]（A 值 1，B 值 2），造副本 cp = [A', B'] | A'.val = 1，B'.val = 2 |
| 2 | 串起来 | A' → B' → NULL |
| 3 | A.random = B，B 在 old 中下标 1 | A'.random = cp[1] = B' |
| 4 | B.random = B，下标 1 | B'.random = cp[1] = B' |

输出 `[[1,1],[2,1]]`。

### 代码

```c
struct Node* copyRandomList(struct Node* head) {
    // 1. 数一数有多少个结点
    int n = 0;
    for (struct Node* p = head; p != NULL; p = p->next) n++;
    if (n == 0) return NULL;                 // 空链表

    // 2. old[i] 存原链表第 i 个结点，cp[i] 存它的副本
    struct Node** old = (struct Node**)malloc(sizeof(struct Node*) * n);
    struct Node** cp = (struct Node**)malloc(sizeof(struct Node*) * n);
    int i = 0;
    for (struct Node* p = head; p != NULL; p = p->next) {
        old[i] = p;
        cp[i] = (struct Node*)malloc(sizeof(struct Node));
        cp[i]->val = p->val;                 // 先只复制值
        cp[i]->next = NULL;
        cp[i]->random = NULL;
        i++;
    }

    // 3. 把副本按顺序串起来
    for (i = 0; i + 1 < n; i++) {
        cp[i]->next = cp[i + 1];
    }

    // 4. 处理 random：找到原结点 random 指向的下标 j，副本就指向 cp[j]
    for (i = 0; i < n; i++) {
        if (old[i]->random == NULL) continue;    // 指向 NULL 的不用管
        for (int j = 0; j < n; j++) {
            if (old[j] == old[i]->random) {      // 比较的是地址，值可能重复
                cp[i]->random = cp[j];
                break;
            }
        }
    }

    struct Node* newHead = cp[0];
    free(old);                               // 两个辅助数组用完释放（结点本身不能释放）
    free(cp);
    return newHead;
}
```

### 复杂度分析

- **时间复杂度 O(n²)**：第 4 步对每个结点都线性查找一次。n = 1000 时约 10⁶ 次，很快。
- **空间复杂度 O(n)**：两个辅助数组（返回的新链表不算）。

> 💬 如果用哈希表存"原结点地址 → 副本地址"，第 4 步可以变成 O(1) 查找，总时间 O(n)。但 C 语言要自己写哈希表。下面有一个更巧妙、连哈希表都不需要的办法。

---

## 🚀 第四步：思路二 —— 把副本"插"在原结点后面（O(1) 额外空间）

### 思路

思路一的难点是"从原结点找到副本"。如果我们**把每个副本直接放在原结点的正后方**：

```
原来：A -> B -> C
插入：A -> A' -> B -> B' -> C -> C'
```

那么"A 的副本"就是 `A->next`，一步就找到了！分三趟：

1. **插入副本**：每个原结点后面插一个副本
2. **设置 random**：`A'->random = A->random->next`（A 的 random 指向 X，X 的副本就是 `X->next`）；原结点 random 为 `NULL` 时副本也是 `NULL`
3. **拆开**：把交织在一起的链表拆成原链表和新链表，原链表恢复原样

### 手动模拟（示例 2：A(1) 和 B(2)，A.random = B，B.random = B）

| 步骤 | 链表状态 | 说明 |
|---|---|---|
| 1 插入 | A → A' → B → B' → NULL | |
| 2 random | A'.random = A.random->next = B->next = B' | |
| | B'.random = B.random->next = B->next = B' | |
| 3 拆开 | 原：A → B → NULL；新：A' → B' → NULL | 原链表恢复 |

### 代码

```c
struct Node* copyRandomList(struct Node* head) {
    if (head == NULL) return NULL;

    // 第 1 趟：在每个原结点后面插入它的副本，变成 A -> A' -> B -> B'
    for (struct Node* p = head; p != NULL; p = p->next->next) {
        struct Node* c = (struct Node*)malloc(sizeof(struct Node));
        c->val = p->val;
        c->random = NULL;
        c->next = p->next;       // 副本接上原来的下一个结点
        p->next = c;             // 原结点指向副本
    }

    // 第 2 趟：设置副本的 random。p 是原结点，p->next 是它的副本
    for (struct Node* p = head; p != NULL; p = p->next->next) {
        if (p->random != NULL) {
            p->next->random = p->random->next;   // 原 random 指向 X，X 的副本是 X->next
        }
    }

    // 第 3 趟：拆成两条链表，并恢复原链表
    struct Node* newHead = head->next;
    for (struct Node* p = head; p != NULL; p = p->next) {
        struct Node* c = p->next;                 // p 的副本
        p->next = c->next;                        // 原结点跳过副本，指回下一个原结点
        c->next = (c->next != NULL) ? c->next->next : NULL;   // 副本指向下一个副本
    }
    return newHead;
}
```

**第 3 趟要小心的地方**：循环里 `p = p->next` 时，`p->next` 已经被改成了"下一个原结点"，所以 `p` 每次正好跳到下一个原结点。

### 复杂度分析

- **时间复杂度 O(n)**：三趟遍历。
- **空间复杂度 O(1)**：除了新链表本身，只用了几个指针。

---

## ⚠️ 第五步：小白常见错误

1. **新结点的 `random` 直接抄原结点的**：`c->random = p->random;` → 新链表的 `random` 指向了原链表，不是深拷贝（判题程序会报错）。
2. **用值来找对应结点**：比如"random 指向值为 3 的结点，就在新链表里找值为 3 的"——示例 3 中三个结点的值都是 3，会找错。必须用**地址/下标**对应。
3. **思路二忘了恢复原链表**：只把副本拆出来，原结点的 `next` 还指着副本。题目要求原链表保持原样。
4. **思路二第 2 趟写成 `p->next->random = p->random;`**：漏了 `->next`，指向的是原结点而不是副本。
5. **`malloc` 后没给 `random` 赋初值**：`random` 是垃圾值，原结点 `random` 为 `NULL` 时副本却指向了野指针。
6. **思路二把三趟合成一趟**：插入副本还没完成时，`p->random->next` 可能还不是副本（后面的结点还没插），结果错误。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 两个数组 + 线性查找下标 | O(n²) | O(n) | ⭐ | 思路最直观，本题数据范围内能过 |
| 哈希表（原结点 → 副本） | O(n) | O(n) | ⭐⭐ | 通用做法，C 语言需自己写哈希表 |
| 副本插在原结点后面 | O(n) | O(1) | ⭐⭐⭐ | **最优**，面试加分 |

> 🎯 **学习建议**：思路二在纸上画三行：插入后、设置 random 后、拆开后，每一行把所有箭头都画出来，三趟循环的含义就一目了然了。

---

## 🔗 举一反三

- **133. 克隆图**：同样是"复制带指针的结构"，用哈希表记录"原结点 → 副本"。
- **1485. 克隆含随机指针的二叉树**：本题的二叉树版本。
- **思考题**：思路一里如果把"线性查找下标"换成"给每个原结点的 `val` 临时改成它的下标，查完再改回来"，能不能做到 O(n)？这样做有什么风险？
