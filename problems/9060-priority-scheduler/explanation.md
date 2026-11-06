# 9060. 优先级任务调度模拟 —— 小白详细题解

> "RTOS 是怎么决定下一个运行哪个任务的？为什么 FreeRTOS 找最高优先级任务是 O(1) 的？"这道题先用最朴素的方法把调度规则模拟出来，再带你实现 RTOS 内核里真正使用的"**就绪位图 + 每优先级就绪队列**"。

---

## 📖 第一步：先读懂题目

把 CPU 想成一个只有一个窗口的办事大厅：

- 任务 = 来办事的人，`arrive` 是到达时间，`burst` 是要办多久，`priority` 是 VIP 等级。
- 每一拍，窗口叫"在场的人里 VIP 等级最高"的那位办 1 拍。
- 办到一半来了更高等级的人，当前的人**立即让出窗口**（抢占），等高等级的办完再继续。

示例 1：

| 拍 | 已就绪且未完成（剩余拍数） | 选中 | 理由 |
|---|---|---|---|
| 0 | 任务 0(3) | 0 | 只有它 |
| 1 | 0(2)、**1(2)** | 1 | 优先级 3 > 1，抢占 |
| 2 | 0(2)、1(1)、2(1) | 1 | 3 最高，任务 1 完成 |
| 3 | 0(2)、2(1) | 2 | 2 > 1，任务 2 完成 |
| 4 | 0(2) | 0 | |
| 5 | 0(1) | 0 | 全部完成 |

**容易忽略的细节：**

1. **数字越大优先级越高**（FreeRTOS 风格）。uC/OS 恰好相反（数字越小越高），看清题意。
2. 同优先级时**不轮转**，先到的一直运行到完成（相当于 FreeRTOS 关闭了时间片）。
3. 中间没有任务可运行时要输出 `-1`，不能跳过。
4. 结果长度是"最后一个任务完成时的拍数"，不是 `sum(burst)`（中间可能有空闲）。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 结果数组开多大？

最坏情况：先空闲到最晚到达的任务，再把所有任务依次运行完。所以长度不超过 `max(arrive) + sum(burst)`，按这个申请就够了。

### 2. 位运算：就绪位图

用一个 `uint32_t` 的 32 个比特分别表示"优先级 0~31 有没有就绪任务"：

```c
readyMask |= 1u << p;      // 优先级 p 有任务就绪：把第 p 位置 1
readyMask &= ~(1u << p);   // 优先级 p 没有就绪任务了：把第 p 位清 0
```

### 3. `__builtin_clz`：数前导零

GCC 内建函数 `__builtin_clz(x)` 返回 `x` 的二进制表示中**最高位的 1 前面有几个 0**（x 不能为 0）：

| x（二进制） | `__builtin_clz(x)` | `31 - clz` = 最高的 1 在第几位 |
|---|---|---|
| `0...0001` | 31 | 0 |
| `0...1010` | 28 | 3 |
| `1000...0` | 0 | 31 |

在 ARM Cortex-M3/M4 上它会被编译成**一条** `CLZ` 指令，这就是 FreeRTOS `configUSE_PORT_OPTIMISED_TASK_SELECTION` 选项的原理。

### 4. `qsort` 与比较函数

```c
qsort(数组, 元素个数, 每个元素大小, 比较函数);
```

比较函数返回负数表示 a 应排在 b 前面。因为比较函数只能拿到两个元素，需要额外的数据（`arrive` 数组）时，可以先存到一个 `static` 全局指针里。

---

## 💡 第三步：思路一 —— 逐拍扫描所有任务

### 思路

完全按题意：每一拍遍历所有任务，找出"已到达、未完成、且按规则最优"的那个。

### 代码

```c
int* prioritySchedule(const uint8_t* priority, const uint32_t* arrive, const uint16_t* burst,
                      size_t n, int* returnSize) {
    uint32_t maxArrive = 0, total = 0;
    for (size_t i = 0; i < n; i++) {
        if (arrive[i] > maxArrive) maxArrive = arrive[i];
        total += burst[i];
    }
    int* res = (int*)malloc(sizeof(int) * (maxArrive + total + 1));   // 时间线长度上限
    int* remain = (int*)malloc(sizeof(int) * n);                      // 每个任务还剩几拍
    for (size_t i = 0; i < n; i++) remain[i] = burst[i];

    size_t done = 0;
    int t = 0;
    while (done < n) {
        int best = -1;
        for (size_t i = 0; i < n; i++) {
            if (arrive[i] > (uint32_t)t || remain[i] == 0) continue;  // 没到或已完成
            if (best == -1
                || priority[i] > priority[best]                                     // 优先级更高
                || (priority[i] == priority[best] && arrive[i] < arrive[best])) {   // 同级先到
                best = (int)i;                     // 编号从小到大遍历，完全相同时保留小编号
            }
        }
        res[t++] = best;                           // 没有可运行任务时 best = -1
        if (best != -1 && --remain[best] == 0) done++;
    }

    free(remain);
    *returnSize = t;
    return res;
}
```

### 复杂度分析

- 时间 **O(T × n)**，T 是时间线长度（≤ 10⁵），n ≤ 500，约 5×10⁷ 次简单操作，可以通过。
- 空间 O(T + n)。

---

## 🚀 第四步：思路二 —— 就绪位图 + 每优先级 FIFO 队列（RTOS 的做法）

### 为什么能优化？

思路一每拍都把 n 个任务全看一遍。真实 RTOS 里调度发生得非常频繁（每次中断、每次任务阻塞都可能触发），必须做到 **O(1)**。观察：

1. **同一优先级内**，谁先运行只看 (到达时间, 编号)。如果任务按这个顺序进入该优先级的队列，那么**队头就是该优先级里应该运行的任务**，而且被抢占后它仍然在队头（没出队）。
2. 要在 32 个优先级里找"最高的非空队列"，用 32 位位图 + `CLZ` 指令一步得到。

| 数据结构 | 作用 |
|---|---|
| `order[]` | 任务按 (arrive, 编号) 排好序，按时间依次"到达" |
| `queue[p]` | 优先级 p 的就绪队列（FIFO） |
| `readyMask` | 第 p 位为 1 ⇔ `queue[p]` 非空 |

每一拍：

1. 把 `arrive == t` 的任务放进各自优先级的队尾，置位图。
2. 位图为 0 → 空闲，输出 -1。
3. 否则 `p = 31 - __builtin_clz(readyMask)`，运行 `queue[p]` 的队头 1 拍；做完就出队，队列空了就清位图。

### 代码

```c
static const uint32_t* g_arrive;                 // 给 qsort 比较函数用

static int cmpArrive(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b;
    if (g_arrive[x] != g_arrive[y]) return g_arrive[x] < g_arrive[y] ? -1 : 1;
    return x - y;                                // 同时到达：编号小的在前
}

int* prioritySchedule(const uint8_t* priority, const uint32_t* arrive, const uint16_t* burst,
                      size_t n, int* returnSize) {
    uint32_t maxArrive = 0, total = 0;
    for (size_t i = 0; i < n; i++) {
        if (arrive[i] > maxArrive) maxArrive = arrive[i];
        total += burst[i];
    }
    int* res = (int*)malloc(sizeof(int) * (maxArrive + total + 1));

    int* order = (int*)malloc(sizeof(int) * n);  // 1. 按 (到达时间, 编号) 排序
    for (size_t i = 0; i < n; i++) order[i] = (int)i;
    g_arrive = arrive;
    qsort(order, n, sizeof(int), cmpArrive);

    int* queue[32];                              // 2. 每个优先级一个队列
    int head[32], tail[32], cnt[32] = {0};
    for (size_t i = 0; i < n; i++) cnt[priority[i]]++;
    for (int p = 0; p < 32; p++) {
        queue[p] = (int*)malloc(sizeof(int) * (cnt[p] + 1));
        head[p] = tail[p] = 0;
    }
    int* remain = (int*)malloc(sizeof(int) * n);
    for (size_t i = 0; i < n; i++) remain[i] = burst[i];

    uint32_t readyMask = 0;                      // 就绪位图
    size_t next = 0, done = 0;                   // next：下一个将要到达的任务在 order 中的位置
    int t = 0;
    while (done < n) {
        while (next < n && arrive[order[next]] <= (uint32_t)t) {   // 3. 本拍到达的任务入队
            int id = order[next++];
            int p = priority[id];
            queue[p][tail[p]++] = id;
            readyMask |= 1u << p;
        }
        if (readyMask == 0) {                    // 4. 没有就绪任务：空闲
            res[t++] = -1;
            continue;
        }
        int p = 31 - __builtin_clz(readyMask);   // 5. O(1) 找到最高优先级
        int id = queue[p][head[p]];              //    该优先级队头就是要运行的任务
        res[t++] = id;
        if (--remain[id] == 0) {                 // 6. 运行完：出队
            head[p]++;
            done++;
            if (head[p] == tail[p]) readyMask &= ~(1u << p);   // 队列空了，清掉这一位
        }
    }

    for (int p = 0; p < 32; p++) free(queue[p]);
    free(order);
    free(remain);
    *returnSize = t;
    return res;
}
```

### 复杂度分析

- 排序 O(n log n)；之后每拍 O(1)（每个任务只入队、出队各一次）。总计 **O(n log n + T)**。
- 空间 O(n + T)。

### 🔌 嵌入式实战：FreeRTOS 里的对应代码

FreeRTOS 的 `tasks.c` 中：

```c
static List_t pxReadyTasksLists[configMAX_PRIORITIES];   // 每个优先级一个就绪链表
/* port 层，Cortex-M 上的实现 */
#define portGET_HIGHEST_PRIORITY(uxTopPriority, uxReadyPriorities) \
    uxTopPriority = (31UL - (uint32_t)__builtin_clz(uxReadyPriorities))
```

和本题的思路二一模一样。不同点是 FreeRTOS 默认开启**时间片轮转**：同优先级的任务每个 tick 轮换一次（把当前任务移到链表尾部），而本题是"先到先做完"。

---

## ⚠️ 第五步：小白常见错误

1. **把优先级比较写反** → 题目是数字越大越优先。
2. **空闲时直接把 t 跳到下一个任务的到达时间** → 漏掉了要输出的 `-1`。
3. **同优先级时选了编号小的而不是先到达的** → 例如 priority = [1,1]、rrive = [1,0]、urst = [1,2]，第 1 拍应继续运行先到的任务 1，而不是编号小的任务 0。要先比 arrive 再比编号。
4. **思路二中被抢占的任务出队后又重新入队到队尾** → 它就排到了同优先级后到任务的后面，违反"先到先做"。被抢占时什么都不用做，它仍在队头。
5. **对 0 调用 `__builtin_clz`** → 结果未定义！必须先判断 `readyMask != 0`。
6. **结果数组只开 `sum(burst)` 大小** → 有空闲拍时越界。

---

## 📊 第六步：方法对比

| 方法 | 每拍选任务 | 总时间 | 说明 |
|---|---|---|---|
| 逐拍扫描所有任务 | O(n) | O(T·n) | 直观，任务少时足够 |
| 堆（优先队列） | O(log n) | O((n + T) log n) | 通用，优先级范围很大时用 |
| 就绪位图 + 每优先级队列 | O(1) | O(n log n + T) | RTOS 内核的标准做法 |

---

## 🔗 举一反三

- **9056. 软件定时器**：tick 中断里既要处理定时器，也要触发调度。
- **9044. 固定大小内存池**：RTOS 创建任务时，任务控制块常从内存池里分配。
- **思考题 1**：如果同优先级要**时间片轮转**（每个任务运行 1 拍后排到同级队尾），思路二要改哪几行？
- **思考题 2**：优先级超过 32 级（例如 256 级）时，一个 32 位位图不够用了。uC/OS 用"两级位图"解决，想想它是怎么做的？
- **思考题 3**：高优先级任务等待低优先级任务持有的锁，而中优先级任务一直在运行——这就是著名的**优先级反转**（火星探路者号事故）。RTOS 用什么机制解决？
