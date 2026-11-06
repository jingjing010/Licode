# 146. LRU 缓存 —— 小白详细题解

> 面试最高频的设计题之一。它考的不是某个算法，而是**把两种数据结构组合起来**：哈希表负责"快速找到"，双向链表负责"快速调整顺序"。

---

## 📖 第一步：先读懂题目

**LRU** = Least Recently Used，"最近最少使用"。想象你的书桌只能放 `capacity` 本书：

- 每次**看**（get）或**放**（put）一本书，就把它挪到最顺手的位置（"最近使用"）
- 桌子满了还要放新书时，把**最久没碰过**的那本收走（"逐出"）

用示例走一遍（capacity = 2，左边是最近使用，右边是最久未使用）：

| 操作 | 返回 | 缓存（左新右旧） | 说明 |
|---|---|---|---|
| LRUCache(2) | null | 空 | |
| put(1, 1) | null | [1] | |
| put(2, 2) | null | [2, 1] | |
| get(1) | 1 | [1, 2] | 1 被使用，挪到最左边 |
| put(3, 3) | null | [3, 1] | 满了，逐出最右边的 2 |
| get(2) | -1 | [3, 1] | 2 已被逐出 |
| put(4, 4) | null | [4, 3] | 满了，逐出最右边的 1 |
| get(1) | -1 | [4, 3] | |
| get(3) | 3 | [3, 4] | |
| get(4) | 4 | [4, 3] | |

**几个需要注意的细节：**

1. `get` 命中时也算"使用"，要把它挪到最新的位置。
2. `put` 一个**已存在**的 key：更新值，并挪到最新位置，**不会**逐出别人（数量没变）。
3. 只有 `put` **新 key** 且缓存已满时才逐出。
4. 要求 get 和 put 都是 **O(1)**：最多 2×10⁵ 次操作、容量 3000，每次操作都扫描一遍缓存会太慢。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. C 语言怎么写"类"？

C 没有类，力扣用"结构体 + 函数"来模拟：

```c
typedef struct {
    int capacity;     // 成员变量都放在结构体里
    // ...你需要的其他成员
} LRUCache;

LRUCache* lRUCacheCreate(int capacity);      // 构造函数：malloc 一个对象并初始化
int lRUCacheGet(LRUCache* obj, int key);     // 成员函数：第一个参数 obj 相当于 this
```

判题程序会先调用 `lRUCacheCreate` 得到 `obj`，之后每次 get/put 都把这个 `obj` 传给你。所以**所有状态都必须存在 `obj` 指向的结构体里**，不能用全局变量（多组数据时会互相干扰）。

### 2. 双向链表 + 哨兵结点

每个结点有 `prev` 和 `next` 两个指针。只要拿到结点 `x` 的指针，就能 O(1) 把它从链表中摘掉：

```c
x->prev->next = x->next;    // 前一个直接连到后一个
x->next->prev = x->prev;    // 后一个直接连回前一个
```

在链表两端各放一个**不存数据的哨兵结点** `head` 和 `tail`，这样任何真实结点都一定有前驱和后继，摘除和插入时**不用判断 NULL**。

```
head <-> [最近使用] <-> ... <-> [最久未使用] <-> tail
```

### 3. 为什么要哈希表？

链表能 O(1) 调整顺序，但**找某个 key 在哪**需要从头遍历，O(n)。所以再加一个"key → 结点指针"的哈希表，一步找到结点。

### ❌ 朴素做法为什么不行

```c
// ❌ 用数组存 (key, value, 最后使用时间)……
// get：遍历数组找 key —— O(capacity)
// put 满了：遍历数组找时间最小的 —— O(capacity)
// 2×10^5 次操作 × 3000 = 6×10^8，会超时
```

---

## 💡 第三步：思路一 —— 数组当哈希表 + 双向链表

### 思路

本题 `0 <= key <= 10000`，范围很小！所以"哈希表"可以直接用一个数组 `map[10001]`：`map[key]` 存这个 key 对应的链表结点指针，不存在就是 `NULL`。这叫**直接寻址表**，是最简单的哈希表。

- **get(key)**：`x = map[key]`；为空返回 -1；否则把 `x` 摘下来插到表头，返回 `x->val`
- **put(key, value)**：
  - `map[key]` 存在：更新值，挪到表头
  - 不存在：如果已满，摘掉表尾结点（`tail.prev`），并把 `map[它的key]` 清空、`free` 掉；然后新建结点插到表头，记入 `map`

### 手动模拟（示例前 5 步，capacity = 2）

| 操作 | 链表（head 到 tail） | map 中非空的 key |
|---|---|---|
| put(1,1) | (1,1) | 1 |
| put(2,2) | (2,2) (1,1) | 1, 2 |
| get(1) → 1 | (1,1) (2,2) | 1, 2 |
| put(3,3) | 满了，删表尾 (2,2)；插入后：(3,3) (1,1) | 1, 3 |
| get(2) → -1 | 不变 | 1, 3 |

### 代码

```c
#define MAX_KEY 10001            // key 的范围是 0 ~ 10000

// 双向链表结点
typedef struct DNode {
    int key;                     // 存 key 是为了逐出时能把 map[key] 清空
    int val;
    struct DNode* prev;
    struct DNode* next;
} DNode;

typedef struct {
    int capacity;                // 容量
    int size;                    // 当前存了几个
    DNode head;                  // 哨兵：head.next 是最近使用的
    DNode tail;                  // 哨兵：tail.prev 是最久未使用的
    DNode* map[MAX_KEY];         // map[key] = 对应的结点，不存在为 NULL
} LRUCache;

// 把结点 x 从链表中摘下来
static void removeNode(DNode* x) {
    x->prev->next = x->next;
    x->next->prev = x->prev;
}

// 把结点 x 插到表头（head 后面），表示"最近使用"
static void addToFront(LRUCache* obj, DNode* x) {
    x->prev = &obj->head;
    x->next = obj->head.next;
    obj->head.next->prev = x;
    obj->head.next = x;
}

LRUCache* lRUCacheCreate(int capacity) {
    // calloc 会把内存全部清零，map 里的指针一开始都是 NULL
    LRUCache* obj = (LRUCache*)calloc(1, sizeof(LRUCache));
    obj->capacity = capacity;
    obj->size = 0;
    obj->head.next = &obj->tail;     // 空链表：head <-> tail
    obj->tail.prev = &obj->head;
    return obj;
}

int lRUCacheGet(LRUCache* obj, int key) {
    DNode* x = obj->map[key];
    if (x == NULL) return -1;        // 不存在
    removeNode(x);                   // 用过了：挪到表头
    addToFront(obj, x);
    return x->val;
}

void lRUCachePut(LRUCache* obj, int key, int value) {
    DNode* x = obj->map[key];
    if (x != NULL) {                 // 已存在：更新值并挪到表头
        x->val = value;
        removeNode(x);
        addToFront(obj, x);
        return;
    }
    if (obj->size == obj->capacity) {    // 满了：逐出表尾（最久未使用）
        DNode* old = obj->tail.prev;
        removeNode(old);
        obj->map[old->key] = NULL;       // 别忘了从"哈希表"里删掉
        free(old);
        obj->size--;
    }
    x = (DNode*)malloc(sizeof(DNode));   // 新建结点放到表头
    x->key = key;
    x->val = value;
    addToFront(obj, x);
    obj->map[key] = x;
    obj->size++;
}

void lRUCacheFree(LRUCache* obj) {
    DNode* p = obj->head.next;
    while (p != &obj->tail) {            // 释放所有真实结点
        DNode* next = p->next;
        free(p);
        p = next;
    }
    free(obj);                           // 再释放缓存对象本身
}
```

### 复杂度分析

- **时间复杂度**：get、put 都是 **O(1)**。
- **空间复杂度 O(capacity + 10⁴)**：链表最多 capacity 个结点，外加一个 10001 大小的数组。

> 💬 `head`、`tail` 直接放在结构体里（不是指针），所以写 `&obj->head` 取它们的地址。`obj` 是 `calloc` 出来的，在 `lRUCacheFree` 之前一直有效，所以这些地址是安全的。

---

## 🚀 第四步：思路二 —— 通用哈希表（链地址法）+ 双向链表

### 思路

如果 key 的范围很大（比如任意 `int`），就不能开 `map[key]` 这么大的数组了。这时需要一个真正的哈希表：

- 准备 `BUCKETS` 个"桶"（数组），用哈希函数把 key 映射到某个桶
- 多个 key 落到同一个桶时，用一条单链表串起来（**链地址法**）
- 为了省事，让双向链表的结点自己多带一个 `hnext` 指针，同时充当哈希桶链表的结点

除了"查找/删除 map 里的 key"换成在桶里操作，其余逻辑和思路一完全相同。

### 代码

```c
#define BUCKETS 4096             // 桶的数量，取 2 的幂方便用 & 取模

typedef struct HNode {
    int key;
    int val;
    struct HNode* prev;          // 双向链表（维护使用顺序）
    struct HNode* next;
    struct HNode* hnext;         // 同一个哈希桶里的下一个结点
} HNode;

typedef struct {
    int capacity;
    int size;
    HNode head;                  // 哨兵：head.next 最近使用
    HNode tail;                  // 哨兵：tail.prev 最久未使用
    HNode* bucket[BUCKETS];      // 哈希桶
} LRUCache;

// 哈希函数：乘一个大质数打散，再取低位（转成 unsigned 避免负数）
static unsigned int hashKey(int key) {
    return ((unsigned int)key * 2654435761u) & (BUCKETS - 1);
}

// 在哈希表中查找 key，找不到返回 NULL
static HNode* findNode(LRUCache* obj, int key) {
    for (HNode* p = obj->bucket[hashKey(key)]; p != NULL; p = p->hnext) {
        if (p->key == key) return p;
    }
    return NULL;
}

// 从哈希表中删除结点 x
static void eraseFromHash(LRUCache* obj, HNode* x) {
    unsigned int h = hashKey(x->key);
    HNode* prev = NULL;
    HNode* p = obj->bucket[h];
    while (p != x) {             // 在桶链表里找到 x
        prev = p;
        p = p->hnext;
    }
    if (prev == NULL) obj->bucket[h] = x->hnext;   // x 是桶里第一个
    else prev->hnext = x->hnext;
}

static void removeNode(HNode* x) {
    x->prev->next = x->next;
    x->next->prev = x->prev;
}

static void addToFront(LRUCache* obj, HNode* x) {
    x->prev = &obj->head;
    x->next = obj->head.next;
    obj->head.next->prev = x;
    obj->head.next = x;
}

LRUCache* lRUCacheCreate(int capacity) {
    LRUCache* obj = (LRUCache*)calloc(1, sizeof(LRUCache));   // 桶全部清零为 NULL
    obj->capacity = capacity;
    obj->head.next = &obj->tail;
    obj->tail.prev = &obj->head;
    return obj;
}

int lRUCacheGet(LRUCache* obj, int key) {
    HNode* x = findNode(obj, key);
    if (x == NULL) return -1;
    removeNode(x);
    addToFront(obj, x);
    return x->val;
}

void lRUCachePut(LRUCache* obj, int key, int value) {
    HNode* x = findNode(obj, key);
    if (x != NULL) {                     // 已存在：更新并挪到表头
        x->val = value;
        removeNode(x);
        addToFront(obj, x);
        return;
    }
    if (obj->size == obj->capacity) {    // 满了：逐出表尾
        HNode* old = obj->tail.prev;
        removeNode(old);
        eraseFromHash(obj, old);
        free(old);
        obj->size--;
    }
    x = (HNode*)malloc(sizeof(HNode));
    x->key = key;
    x->val = value;
    unsigned int h = hashKey(key);       // 插到桶链表的开头
    x->hnext = obj->bucket[h];
    obj->bucket[h] = x;
    addToFront(obj, x);
    obj->size++;
}

void lRUCacheFree(LRUCache* obj) {
    HNode* p = obj->head.next;
    while (p != &obj->tail) {
        HNode* next = p->next;
        free(p);
        p = next;
    }
    free(obj);
}
```

### 复杂度分析

- **时间复杂度**：get、put **平均 O(1)**（桶数比元素多，每个桶里平均不到 1 个结点）。
- **空间复杂度 O(capacity + BUCKETS)**。

---

## ⚠️ 第五步：小白常见错误

1. **逐出时忘了从哈希表里删除**：链表里没了，`map[key]` 却还指着已经 `free` 的结点，之后 `get` 这个 key 会访问野指针（结果错误或崩溃）。
2. **`get` 命中后没有挪到表头**：示例中 `get(1)` 之后 `put(3,3)` 应该逐出 2，如果没挪，会错误地逐出 1。
3. **`put` 已存在的 key 时也执行了逐出**：key 已存在时数量不变，只需要更新值并挪到表头。
4. **结点里不存 `key`**：逐出表尾时只拿到结点，不知道它的 key 是多少，就没法从哈希表里删掉它。
5. **用全局变量存缓存数据**：判题时虽然只有一个对象，但这是错误的设计习惯；所有状态都应该放在 `LRUCache` 结构体里。
6. **用 `malloc` 而不是 `calloc` 创建对象，又没有初始化 `map`**：`map` 里是随机的垃圾指针，`get` 一个不存在的 key 会被当成存在。
7. **不用哨兵结点**：插入/删除时要分别判断"是不是第一个""是不是最后一个"，很容易漏掉某种情况导致空指针。

---

## 📊 第六步：方法对比

| 方法 | get/put 时间 | 空间 | 适用场景 | 建议 |
|---|---|---|---|---|
| 数组遍历 + 时间戳 | O(capacity) | O(capacity) | - | ❌ 会超时 |
| 直接寻址数组 + 双向链表 | O(1) | O(capacity + key 范围) | key 范围小（本题） | **推荐先写这个** |
| 链地址哈希表 + 双向链表 | 平均 O(1) | O(capacity + 桶数) | 任意 key | 面试通用答案 |

> 🎯 **学习建议**：先把"双向链表 + 哨兵"的 `removeNode`、`addToFront` 两个小函数写熟，LRU 就只剩下"什么时候调用它们"的逻辑了。

---

## 🔗 举一反三

- **460. LFU 缓存**：按"使用次数"逐出，次数相同再按 LRU，难度更高。
- **155. 最小栈**、**232. 用栈实现队列**：其他经典设计题，同样是"结构体 + 一组函数"的写法。
- **思考题**：操作系统的页面置换、CPU 缓存、浏览器缓存都用到了 LRU 思想。如果要求"线程安全"，你的实现需要考虑什么？
