# 9044. 固定大小内存池 —— 小白详细题解

> "你们项目里为什么不用 malloc？那用什么？" —— 答案通常就是**内存池**。这道题带你实现一个 O(1) 分配、O(1) 释放、零碎片的固定块内存池，并学会嵌入式里非常经典的技巧：**把空闲链表藏在空闲块自己的内存里**。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 有一排编号 `0 ~ n-1`、大小相同的"格子"。`alloc` 借出一个空格子（告诉我编号），`release` 还回一个格子。借的顺序由"空闲链表"决定：**从链表头借，还回来也插到链表头**。

拿示例 2 来说（`blockCount = 3`）：

| 操作 | 空闲链表（头 → 尾） | 已分配 | 输出 |
|---|---|---|---|
| 创建 | 0 → 1 → 2 | — | null |
| alloc | 1 → 2 | {0} | 0 |
| alloc | 2 | {0, 1} | 1 |
| release(0) | **0** → 2 | {1} | true |
| alloc | 2 | {0, 1} | 0 |
| freeCount | 2 | {0, 1} | 1 |

**几个需要注意的细节：**

1. 还回来的块插在**头部**，所以下一次 `alloc` 会先拿到它（后进先出）。这样做有个好处：刚释放的块很可能还在 CPU Cache 里，再次使用更快。
2. `release` 要拒绝两种非法请求：**编号越界**（示例 3 的 `5`）和**重复释放**（示例 3 第二次释放 `0`）。
3. `release` 一个合法但**从没分配过**的块（比如刚创建就 `release(0)`），它本来就是空闲的，也算重复释放，返回 `false`。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 为什么嵌入式系统不爱用 malloc？

| 问题 | 说明 |
|---|---|
| 执行时间不确定 | malloc 要在空闲区里搜索合适大小的块，耗时取决于堆的状态，实时系统无法保证截止时间 |
| 内存碎片 | 反复申请/释放不同大小的内存后，总空闲量够，却找不到一块连续的大内存 |
| 难以排查 | 内存泄漏、重复释放在 MCU 上往往表现为几天后随机死机 |
| 线程安全 | 在中断里调用 malloc 通常是不允许的 |

固定大小内存池把这些问题全解决了：每块一样大 → **没有碎片**；用链表管理 → **O(1)、时间确定**；还能检查非法释放。

### 2. 力扣风格的"设计类"写法

C 语言没有"类"，力扣用 **结构体 + 一组函数** 模拟：

```c
typedef struct {
    int freeHead;      // 成员变量放在结构体里
    /* 其他成员 */
} MemoryPool;

MemoryPool* memoryPoolCreate(int blockSize, int blockCount);   // 相当于构造函数：malloc 一个结构体并初始化
int memoryPoolAlloc(MemoryPool* obj);                           // 成员函数：第一个参数是"this"指针
void memoryPoolFree(MemoryPool* obj);                           // 相当于析构函数：释放所有内存
```

访问成员用 `obj->freeHead`（等价于 `(*obj).freeHead`）。

### 3. 用"下标"代替"指针"做链表

链表不一定要用 `struct Node* next`。所有块都在同一个数组里，可以直接用**编号**当"指针"：`next[i]` 表示块 `i` 后面是哪个块，`-1` 表示链表结束。这样每个"指针"只需要一个 `int`（甚至 `uint16_t`），而且序列化、调试都更方便。

---

## 💡 第三步：思路一 —— 独立的 next 数组

### 思路

- `next[i]`：空闲链表中块 `i` 的下一个块，`-1` 表示没有
- `freeHead`：空闲链表的头，`-1` 表示没有空闲块
- `used[i]`：块 `i` 是否已分配，用来检查重复释放
- **alloc**：取出 `freeHead`，`freeHead = next[freeHead]`
- **release(i)**：检查合法后，`next[i] = freeHead; freeHead = i;`（头插法）

### 手动模拟（示例 3：`blockCount = 2`）

| 操作 | 检查 | freeHead | next | used | 输出 |
|---|---|---|---|---|---|
| 创建 | | 0 | [1, -1] | [F, F] | null |
| alloc | 有空闲块 | 1 | [1, -1] | [**T**, F] | 0 |
| release(0) | 合法且已分配 | **0** | [**1**, -1] | [**F**, F] | true |
| release(0) | used[0] 是 F → 重复释放 | 0 | 不变 | 不变 | false |
| release(5) | 越界 | 0 | 不变 | 不变 | false |
| freeCount | | | | | 2 |

### 代码

```c
typedef struct {
    uint8_t* mem;        // 真正的内存：blockCount 个块，每块 blockSize 字节
    int* next;           // next[i]：空闲链表中块 i 的下一个块，-1 表示结束
    bool* used;          // used[i]：块 i 是否已经分配出去
    int blockSize;
    int blockCount;
    int freeHead;        // 空闲链表头，-1 表示没有空闲块
    int freeCount;       // 空闲块个数
} MemoryPool;

MemoryPool* memoryPoolCreate(int blockSize, int blockCount) {
    MemoryPool* obj = (MemoryPool*)malloc(sizeof(MemoryPool));
    obj->mem = (uint8_t*)malloc((size_t)blockSize * blockCount);
    obj->next = (int*)malloc(sizeof(int) * blockCount);
    obj->used = (bool*)calloc(blockCount, sizeof(bool));   // calloc 会清零：全部未分配
    obj->blockSize = blockSize;
    obj->blockCount = blockCount;

    // 初始链表 0 -> 1 -> 2 -> 直到最后一块：块 i 的下一个是 i + 1，最后一块指向 -1
    for (int i = 0; i < blockCount; i++) {
        obj->next[i] = (i + 1 < blockCount) ? i + 1 : -1;
    }
    obj->freeHead = 0;
    obj->freeCount = blockCount;
    return obj;
}

int memoryPoolAlloc(MemoryPool* obj) {
    if (obj->freeHead == -1) return -1;     // 没有空闲块
    int idx = obj->freeHead;                // 取出链表头
    obj->freeHead = obj->next[idx];         // 头指针后移
    obj->used[idx] = true;
    obj->freeCount--;
    return idx;
}

bool memoryPoolRelease(MemoryPool* obj, int index) {
    // 越界，或者这个块本来就是空闲的（重复释放）
    if (index < 0 || index >= obj->blockCount || !obj->used[index]) return false;
    obj->next[index] = obj->freeHead;       // 头插法：新块指向原来的头
    obj->freeHead = index;                  // 新块成为新的头
    obj->used[index] = false;
    obj->freeCount++;
    return true;
}

int memoryPoolFreeCount(MemoryPool* obj) {
    return obj->freeCount;
}

void memoryPoolFree(MemoryPool* obj) {
    // 先释放成员指向的内存，最后释放结构体本身
    free(obj->mem);
    free(obj->next);
    free(obj->used);
    free(obj);
}
```

### 复杂度分析

- **时间复杂度**：创建 O(n)，`alloc` / `release` / `freeCount` 都是 **O(1)**。
- **空间复杂度 O(n)**：除了块本身，还需要 `next` 和 `used` 两个数组。

---

## 🚀 第四步：思路二 —— 侵入式空闲链表（嵌入式经典写法）

### 思路

观察一下：**空闲块里面存的数据，根本没人用**。那为什么还要单独开一个 `next` 数组？直接把"下一个空闲块的编号"**写在空闲块自己的前 4 个字节里**！

```
mem: [ 块0 | 块1 | 块2 | 块3 ]
       ↓      ↓      ↓      ↓
     next=1 next=2 next=3 next=-1     ← 空闲时，块的开头存的是链表指针
```

- 块被分配出去后，用户会覆盖这 4 个字节——没关系，它已经不在空闲链表里了。
- 块被释放时，我们重新在开头写入 `next`，把它挂回链表。

这就是 uC/OS 的 `OS_MEM`、LwIP 的 `memp` 采用的做法，**额外开销为 0**（`used[]` 只是为了检测重复释放；很多真实实现为了省内存连这个都不要）。这也是本题要求 `blockSize >= 4` 且是 4 的倍数的原因：每个块至少放得下一个 `int`，并且块的起始地址都是 4 字节对齐的（见 9042），用 `int*` 访问不会出现非对齐访问。

### 代码

```c
typedef struct {
    uint8_t* mem;        // blockCount 个块连续存放
    bool* used;          // 用于检测重复释放
    int blockSize;
    int blockCount;
    int freeHead;
    int freeCount;
} MemoryPool;

// 返回块 index 开头 4 个字节的地址：空闲时这里存放"下一个空闲块的编号"
static int* pool_next(MemoryPool* obj, int index) {
    return (int*)(obj->mem + (size_t)index * obj->blockSize);
}

MemoryPool* memoryPoolCreate(int blockSize, int blockCount) {
    MemoryPool* obj = (MemoryPool*)malloc(sizeof(MemoryPool));
    obj->mem = (uint8_t*)malloc((size_t)blockSize * blockCount);
    obj->used = (bool*)calloc(blockCount, sizeof(bool));
    obj->blockSize = blockSize;
    obj->blockCount = blockCount;
    for (int i = 0; i < blockCount; i++) {
        *pool_next(obj, i) = (i + 1 < blockCount) ? i + 1 : -1;   // 把链表写进块里
    }
    obj->freeHead = 0;
    obj->freeCount = blockCount;
    return obj;
}

int memoryPoolAlloc(MemoryPool* obj) {
    if (obj->freeHead == -1) return -1;
    int idx = obj->freeHead;
    obj->freeHead = *pool_next(obj, idx);   // 从块里读出下一个空闲块
    obj->used[idx] = true;
    obj->freeCount--;
    return idx;
}

bool memoryPoolRelease(MemoryPool* obj, int index) {
    if (index < 0 || index >= obj->blockCount || !obj->used[index]) return false;
    *pool_next(obj, index) = obj->freeHead; // 在块里写入原来的链表头
    obj->freeHead = index;
    obj->used[index] = false;
    obj->freeCount++;
    return true;
}

int memoryPoolFreeCount(MemoryPool* obj) {
    return obj->freeCount;
}

void memoryPoolFree(MemoryPool* obj) {
    free(obj->mem);
    free(obj->used);
    free(obj);
}
```

> 💬 真实的内存池返回的是**指针**（`void* PoolAlloc(pool)`），释放时传指针。根据指针算编号：`index = ((uint8_t*)p - pool->mem) / blockSize`，还要检查 `p` 是否落在池的范围内、是否正好在块的边界上——这就是本题用编号来简化的部分。

### 复杂度分析

- **时间复杂度**：创建 O(n)，其余操作 **O(1)**。
- **空间复杂度**：除块本身外只有 `used[]`；去掉重复释放检测的话额外开销为 O(1)。

---

## ⚠️ 第五步：小白常见错误

1. **不检查重复释放**：同一个块释放两次，会被两次插进链表，之后两次 `alloc` 会把**同一个块**分给两个人——两段代码互相踩数据，这是内存池最常见、最难查的 bug。
2. **不检查越界**：`release(5)` 时直接写 `next[5]`，越界写坏了别的内存。
3. **`alloc` 时忘了判断 `freeHead == -1`**：没有空闲块时访问 `next[-1]`，越界读。
4. **释放时插到链表尾部**：需要遍历链表，变成 O(n)；而且分配顺序和题目要求的不一样，示例 2 第二次分配会得到 2 而不是 0。
5. **销毁时只 `free(obj)`**：成员 `mem`、`next`、`used` 指向的内存全部泄漏。必须**先释放成员，再释放结构体**；反过来先 `free(obj)` 再访问 `obj->mem` 是使用已释放内存。
6. **侵入式链表的块太小或不对齐**：`blockSize = 2` 时放不下一个 `int`；`blockSize = 6` 时第 1 个块从偏移 6 开始，用 `int*` 访问在 Cortex-M0 上会 HardFault。实际项目中要把 `blockSize` 向上对齐到 `sizeof(void*)`。

---

## 📊 第六步：两种方法对比

| 方法 | alloc / release | 额外空间 | 难度 | 说明 |
|---|---|---|---|---|
| 独立 next 数组 | O(1) | O(n) | ⭐⭐ | 思路清晰，链表和数据分开，调试方便 |
| 侵入式空闲链表 | O(1) | O(1)（不算 used） | ⭐⭐⭐ | RTOS / 协议栈的标准做法 |

> 🎯 **学习建议**：先写思路一理解"用下标做链表"，再改成思路二——你只需要把 `obj->next[i]` 换成 `*pool_next(obj, i)`，体会"空闲块的内存可以复用"这个想法。

---

## 🔗 举一反三

- **9045. 位图分配器**：另一种管理固定块的方法，用 1 个 bit 表示 1 个块，还能一次分配**连续的多个块**。
- **力扣 146. LRU 缓存**：同样是"设计类"题，用链表 + 哈希表实现 O(1)。
- **多种尺寸的内存池**：LwIP 为不同大小的对象（TCP 控制块、pbuf……）各建一个池。如果要支持 16/64/256 字节三种大小，`alloc(size)` 该怎么选池？
- **中断安全**：如果 `alloc` 在主循环里执行到一半（刚读出 `freeHead`），被中断打断，中断里也调用了 `alloc`，会发生什么？怎样用"关中断"或原子操作保护临界区？
