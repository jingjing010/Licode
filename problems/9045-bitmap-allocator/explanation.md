# 9045. 位图分配器 —— 小白详细题解

> 9044 的内存池一次只能借一个块。如果要一次借**连续的好几块**呢？空闲链表就不好用了。这道题介绍嵌入式和操作系统里另一种经典的资源管理方式：**位图**——用 1 个 bit 记录 1 个块的状态，4096 个块只需要 512 字节。你会同时练到位运算的"读、置位、清零"三件套。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 一排编号 `0 ~ n-1` 的格子，每个格子要么空、要么被占。`alloc(count)` 从左往右找**第一段**连续 `count` 个空格子，全部占上，返回起点；`release(start, count)` 把一段被占的格子还回来，但要拒绝越界和"还了没借的格子"。

拿示例 2 来说（`blockCount = 8`，位图从左到右写块 0 ~ 7）：

| 操作 | 位图（块 0 → 7） | 输出 | 说明 |
|---|---|---|---|
| 创建 | 00000000 | null | |
| alloc(2) | **11**000000 | 0 | |
| alloc(2) | 11**11**0000 | 2 | |
| alloc(2) | 1111**11**00 | 4 | |
| release(2, 2) | 11**00**1100 | true | 块 2、3 都是已分配的，合法 |
| alloc(1) | 11**1**01100 | 2 | 编号最小的空闲块是 2 |
| alloc(3) | 11101100 | -1 | 空闲块 3、6、7 不连续 |
| usedCount | | 5 | |

**几个需要注意的细节：**

1. **首次适应**：返回**编号最小**的可行起点，而不是"最合适"的空隙。
2. 总空闲数够了也不一定能分配，必须**连续**（示例 2 最后的 alloc(3)）。这就是"外部碎片"。
3. `release` 要么全部释放、要么什么都不改。示例 3 中重复释放块 0、越界释放 30~49 都返回 `false`。
4. `count` 可能比 `blockCount` 还大，这时直接返回 `-1`。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 用 `uint32_t` 数组存位图

第 `i` 个块存放在第 `i / 32` 个 `uint32_t` 的第 `i % 32` 位：

```
块号:      31 ......... 1 0 | 63 ........ 33 32 | ...
bits[0]:   bit31 ...... b1 b0   bits[1]: bit31 .. b1 b0
```

因为 32 是 2 的幂，`i / 32` 可以写成 `i >> 5`，`i % 32` 可以写成 `i & 31`（见 9042、9043）。

需要的 `uint32_t` 个数是 `(n + 31) / 32`（向上取整）：`n = 40` 时需要 2 个，`n = 32` 时需要 1 个。

### 2. 位运算三件套

| 操作 | 代码 | 原理 |
|---|---|---|
| 读第 i 位 | `(bits[i >> 5] >> (i & 31)) & 1u` | 右移到最低位，再取出来 |
| 置 1 | `bits[i >> 5] \|= 1u << (i & 31)` | 和 1 做或，结果一定是 1 |
| 清 0 | `bits[i >> 5] &= ~(1u << (i & 31))` | 和 0 做与，结果一定是 0；其他位和 1 做与，保持不变 |

注意用 `1u`（无符号）：`1 << 31` 是有符号溢出，属于未定义行为。

### 3. `calloc`：分配并清零

`calloc(个数, 每个的大小)` 分配的内存全部是 0，正好对应"初始全部空闲"。用 `malloc` 的话还要自己 `memset`。

### 4. 设计类题目的写法

和 9044 一样：结构体保存状态，`Create` 相当于构造函数，`Free` 负责释放结构体和它的成员。

---

## 💡 第三步：思路一 —— 用 bool 数组模拟（最朴素）

### 思路

先不考虑省内存，用 `bool used[n]` 表示每个块的状态，把算法逻辑写对：

- **alloc(count)**：从左往右扫，`run` 记录"到当前为止连续空闲块的个数"。遇到已分配的块 `run = 0`；遇到空闲块 `run++`，一旦 `run == count`，起点就是 `i - count + 1`。
- **release(start, count)**：先检查范围，再检查每一块都是已分配的，最后统一清零。
- **usedCount**：维护一个计数器，分配时加、释放时减，O(1) 返回。

### 手动模拟（示例 2 中的 alloc(3)，位图 11101100）

| i | 块 i | run |
|---|---|---|
| 0 | 1 | 0 |
| 1 | 1 | 0 |
| 2 | 1 | 0 |
| 3 | 0 | 1 |
| 4 | 1 | **0**（被打断） |
| 5 | 1 | 0 |
| 6 | 0 | 1 |
| 7 | 0 | 2 |
| 结束 | | 没有达到 3，返回 -1 |

### 代码

```c
typedef struct {
    bool* used;       // used[i]：块 i 是否已分配
    int blockCount;
    int usedCount;    // 已分配的块数
} BitmapAllocator;

BitmapAllocator* bitmapAllocatorCreate(int blockCount) {
    BitmapAllocator* obj = (BitmapAllocator*)malloc(sizeof(BitmapAllocator));
    obj->used = (bool*)calloc(blockCount, sizeof(bool));   // 全部清零：初始都空闲
    obj->blockCount = blockCount;
    obj->usedCount = 0;
    return obj;
}

int bitmapAllocatorAlloc(BitmapAllocator* obj, int count) {
    if (count < 1 || count > obj->blockCount) return -1;
    int run = 0;                                   // 当前连续空闲块的个数
    for (int i = 0; i < obj->blockCount; i++) {
        if (obj->used[i]) {
            run = 0;                               // 被已分配的块打断
        } else {
            run++;
            if (run == count) {                    // 找到了：起点是 i - count + 1
                int start = i - count + 1;
                for (int j = start; j <= i; j++) obj->used[j] = true;
                obj->usedCount += count;
                return start;
            }
        }
    }
    return -1;                                     // 没有足够长的连续空闲段
}

bool bitmapAllocatorRelease(BitmapAllocator* obj, int start, int count) {
    // 1. 范围检查
    if (start < 0 || count < 1 || start + count > obj->blockCount) return false;
    // 2. 先全部检查一遍：有任何一块是空闲的就拒绝，保证"要么全改，要么不改"
    for (int i = start; i < start + count; i++) {
        if (!obj->used[i]) return false;
    }
    // 3. 再统一释放
    for (int i = start; i < start + count; i++) obj->used[i] = false;
    obj->usedCount -= count;
    return true;
}

int bitmapAllocatorUsedCount(BitmapAllocator* obj) {
    return obj->usedCount;
}

void bitmapAllocatorFree(BitmapAllocator* obj) {
    free(obj->used);
    free(obj);
}
```

### 复杂度分析

- **时间复杂度**：alloc O(n)，release O(count)，usedCount O(1)。
- **空间复杂度 O(n) 字节**：每个块用了一个 `bool`（1 字节 = 8 bit），比位图多用 8 倍内存。

---

## 🚀 第四步：思路二 —— 真正的位图 + 整字跳过

### 思路

1. 把 `bool used[n]` 换成 `uint32_t bits[(n + 31) / 32]`，用位运算读写——内存降到 1/8。
2. **整字跳过**：扫描时如果当前块正好是一个字的开头（`i % 32 == 0`），并且这个字是 `0xFFFFFFFF`（32 块全被占用），就可以一次跳过 32 块，`run` 清零。在内存比较满的时候能显著加快 alloc。

### 代码

```c
typedef struct {
    uint32_t* bits;   // 位图：第 i 块在 bits[i >> 5] 的第 (i & 31) 位，1 表示已分配
    int blockCount;
    int used;
} BitmapAllocator;

static bool bm_test(const BitmapAllocator* obj, int i) {
    return (obj->bits[i >> 5] >> (i & 31)) & 1u;
}

static void bm_set(BitmapAllocator* obj, int i) {
    obj->bits[i >> 5] |= 1u << (i & 31);
}

static void bm_clear(BitmapAllocator* obj, int i) {
    obj->bits[i >> 5] &= ~(1u << (i & 31));
}

BitmapAllocator* bitmapAllocatorCreate(int blockCount) {
    BitmapAllocator* obj = (BitmapAllocator*)malloc(sizeof(BitmapAllocator));
    obj->bits = (uint32_t*)calloc((blockCount + 31) / 32, sizeof(uint32_t));   // 向上取整
    obj->blockCount = blockCount;
    obj->used = 0;
    return obj;
}

int bitmapAllocatorAlloc(BitmapAllocator* obj, int count) {
    if (count < 1 || count > obj->blockCount) return -1;
    int run = 0;
    int i = 0;
    while (i < obj->blockCount) {
        // 整字跳过：从字的开头开始、并且 32 块全满
        if ((i & 31) == 0 && obj->bits[i >> 5] == 0xFFFFFFFFu) {
            run = 0;
            i += 32;
            continue;
        }
        if (bm_test(obj, i)) {
            run = 0;
        } else if (++run == count) {
            int start = i - count + 1;
            for (int j = start; j <= i; j++) bm_set(obj, j);
            obj->used += count;
            return start;
        }
        i++;
    }
    return -1;
}

bool bitmapAllocatorRelease(BitmapAllocator* obj, int start, int count) {
    if (start < 0 || count < 1 || start + count > obj->blockCount) return false;
    for (int i = start; i < start + count; i++) {
        if (!bm_test(obj, i)) return false;        // 有空闲块：重复释放或释放了别人的块
    }
    for (int i = start; i < start + count; i++) bm_clear(obj, i);
    obj->used -= count;
    return true;
}

int bitmapAllocatorUsedCount(BitmapAllocator* obj) {
    return obj->used;
}

void bitmapAllocatorFree(BitmapAllocator* obj) {
    free(obj->bits);
    free(obj);
}
```

> 💬 最后一个字可能只用了一部分 bit（比如 `n = 40` 时 `bits[1]` 只用低 8 位），高位永远是 0，它不会等于 `0xFFFFFFFF`，所以整字跳过不会出错；扫描循环也只到 `blockCount` 为止，不会把多出来的 bit 当成可用块。

### 复杂度分析

- **时间复杂度**：alloc 最坏 O(n)，但跳过满字时只需 O(n / 32)；release O(count)；usedCount O(1)。
- **空间复杂度 O(n / 32) 个字**：4096 块只需 128 个 `uint32_t` = 512 字节。

---

## 🔌 嵌入式实战

**1. CLZ / CTZ 指令加速：** Cortex-M3 及以上有 `CLZ`（数前导 0）指令，GCC 提供 `__builtin_ctz(x)`（数末尾 0 的个数）。要找一个字里第一个空闲块，可以写 `__builtin_ctz(~word)`，一条指令代替最多 32 次循环。FreeRTOS 选择最高优先级就绪任务时（`configUSE_PORT_OPTIMISED_TASK_SELECTION`）用的就是这个技巧。

**2. 位图的其他用途：**

| 场景 | 每个 bit 表示 |
|---|---|
| RTOS 就绪表 | 某个优先级是否有就绪任务 |
| 文件系统 / Flash 管理 | 某个扇区 / 簇是否已使用 |
| 中断挂起寄存器（NVIC ISPR） | 某个中断是否挂起 |
| 事件组（Event Group） | 某个事件是否发生 |

**3. 中断安全：** "检查 + 置位"不是原子操作。如果主循环和中断都会调用 alloc，必须在临界区里执行（关中断，或者用 LDREX/STREX 实现的原子操作），否则两边可能分到同一段块。

---

## ⚠️ 第五步：小白常见错误

1. **位置计算写错**：`bits[i / 32]` 和 `i % 32` 写成 `bits[i % 32]`、`i / 32`，或者把 `>> 5` 写成 `>> 4`。用 `n = 40` 的示例 3 测一下跨字的情况。
2. **`1 << 31` 有符号溢出**：要写 `1u << (i & 31)`。
3. **清零写成 `bits[w] &= (1u << b)`**：这会把**其他所有位**清零。正确的是 `&= ~(1u << b)`。
4. **release 边检查边清零**：

   ```c
   for (int i = start; i < start + count; i++) {
       if (!bm_test(obj, i)) return false;   // ❌ 前面几块已经被清零了，状态被破坏
       bm_clear(obj, i);
   }
   ```

   必须先完整检查一遍，再统一修改。
5. **越界检查漏了**：只判断 `start + count > n`，没判断 `start < 0`，释放 `(-1, 2)` 时访问 `bits[-1 >> 5]`。
6. **位图大小没有向上取整**：`n / 32` 在 `n = 40` 时只分配了 1 个字，访问块 32 ~ 39 越界。要用 `(n + 31) / 32`。
7. **找到连续段后忘了更新 usedCount，或者 `run` 遇到已分配块时没清零**：后者会把不连续的空闲块误当成连续的。

---

## 📊 第六步：方法对比

| 方法 | alloc | release | 额外空间 | 难度 | 说明 |
|---|---|---|---|---|---|
| bool 数组 | O(n) | O(count) | n 字节 | ⭐⭐ | 先把逻辑写对 |
| uint32_t 位图 + 整字跳过 | O(n)，满时 O(n/32) | O(count) | n/8 字节 | ⭐⭐⭐ | 真实系统的做法 |
| 9044 空闲链表内存池 | O(1) | O(1) | 几乎为 0 | ⭐⭐ | 只能一次分配一个块 |

> 🎯 **学习建议**：先写思路一通过，再把 `obj->used[i]` 的读写替换成 `bm_test / bm_set / bm_clear` 三个函数——你会发现算法完全没变，变的只是"状态存在哪里"。

---

## 🔗 举一反三

- **9044. 固定大小内存池**：O(1) 分配单个块。两者各适合什么场景？
- **9001. 置位指定位**：本题 `bm_set` 的基础。
- **最佳适应（best fit）**：改成返回"能放下 count 块的**最短**空闲段"的起点。它能减少碎片吗？代价是什么？
- **思考题**：如果 `release` 只给 `start`，不给 `count`（像 `free(ptr)` 一样），分配器要额外记录什么信息？（提示：可以再开一个位图，标记每段分配的"起始块"。）
