# 9056. 软件定时器 —— 小白详细题解

> "硬件定时器不够用怎么办？"——答案就是软件定时器。这道题让你实现一个最小的软件定时器框架，它是 RTOS 定时器服务、裸机调度器的基础，面试时经常被要求"现场设计一个"。

---

## 📖 第一步：先读懂题目

想象你有 `maxTimers` 个"倒计时器"：

- `start(id, period, repeat)`：把第 id 个倒计时器拨到 `period`，开始倒数。
- `tick()`：所有在跑的倒计时器都减 1，**减到 0 的就"响铃"**。周期定时器响完自动重新拨到 `period`；单次定时器响完就停。
- `stop(id)`：把它关掉。

示例 1 逐拍模拟：

| tick 次数 | 定时器 0（周期 2，重复）剩余 | 定时器 1（周期 3，单次）剩余 | 触发 |
|---|---|---|---|
| 启动时 | 2 | 3 | |
| 1 | 1 | 2 | [] |
| 2 | 0 → 触发，重装 2 | 1 | [0] |
| 3 | 1 | 0 → 触发，停止 | [1] |
| 4 | 0 → 触发，重装 2 | 已停止 | [0] |
| 5 | 1 | | [] |
| 6 | 0 → 触发 | | [0] |

**容易忽略的细节：**

1. `start` 一个**正在运行**的定时器，是**重新开始计时**（以最后一次为准），不是忽略。
2. 同一拍可能有多个定时器触发，结果要**按编号从小到大**——按 id 顺序遍历自然就是有序的，不用排序。
3. 周期定时器重装后，下一次在 `period` 拍之后触发，所以周期 1 的定时器每拍都触发。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 结构体数组

每个定时器有 4 个属性，用结构体打包：

```c
typedef struct {
    bool running;        // 是否在运行
    bool repeat;         // 是否周期性
    uint32_t period;     // 周期（节拍数）
    uint32_t remaining;  // 还剩几拍触发
} SoftTimer;
```

再用 `SoftTimer* timers` 指向一个 `maxTimers` 长的数组，`timers[id]` 就是第 id 个定时器。

### 2. `calloc`：申请并清零

```c
obj->timers = (SoftTimer*)calloc(maxTimers, sizeof(SoftTimer));
```

`calloc(个数, 每个的大小)` 和 `malloc` 的区别是**会把内存全部清零**，于是所有定时器的 `running` 一开始都是 `false`，省去一个初始化循环。

### 3. 用指针简化代码

```c
SoftTimer* t = &obj->timers[id];
t->remaining = period;          // 比 obj->timers[id].remaining = period 短很多
```

### 4. 这个 tick 函数在真实系统里在哪调用？

通常在 1ms 的 SysTick 中断里调用 `tick`，但**回调函数（比如点灯）不应该在中断里执行**。常见做法是中断里只记录"哪些定时器到期了"，主循环再去执行回调——这和本题"tick 返回触发列表"的设计一致。

---

## 💡 第三步：思路一 —— 倒计时（remaining 每拍减 1）

### 代码

```c
typedef struct {
    bool running;
    bool repeat;
    uint32_t period;
    uint32_t remaining;     // 还剩几拍
} SoftTimer;

typedef struct {
    SoftTimer* timers;      // 定时器数组
    int n;                  // 定时器个数
} TimerManager;

TimerManager* timerManagerCreate(int maxTimers) {
    TimerManager* obj = (TimerManager*)malloc(sizeof(TimerManager));
    obj->timers = (SoftTimer*)calloc(maxTimers, sizeof(SoftTimer));  // 全部清零：都处于停止状态
    obj->n = maxTimers;
    return obj;
}

void timerManagerStart(TimerManager* obj, int id, int period, bool repeat) {
    SoftTimer* t = &obj->timers[id];
    t->running = true;
    t->repeat = repeat;
    t->period = (uint32_t)period;
    t->remaining = (uint32_t)period;   // 重新开始计时（覆盖原来的进度）
}

void timerManagerStop(TimerManager* obj, int id) {
    obj->timers[id].running = false;
}

int* timerManagerTick(TimerManager* obj, int* returnSize) {
    int* fired = (int*)malloc(sizeof(int) * obj->n);   // 最多全部触发
    int m = 0;
    for (int id = 0; id < obj->n; id++) {               // 按 id 从小到大，结果自然有序
        SoftTimer* t = &obj->timers[id];
        if (!t->running) continue;                      // 停止的跳过
        t->remaining--;                                 // 倒数一拍
        if (t->remaining == 0) {                        // 到点了
            fired[m++] = id;
            if (t->repeat) {
                t->remaining = t->period;               // 周期定时器：重新装填
            } else {
                t->running = false;                     // 单次定时器：停止
            }
        }
    }
    *returnSize = m;
    return fired;
}

void timerManagerFree(TimerManager* obj) {
    free(obj->timers);
    free(obj);
}
```

### 复杂度分析

- `start` / `stop`：O(1)。
- `tick`：O(maxTimers)，每拍要扫描并修改所有定时器。

---

## 🚀 第四步：思路二 —— 记录"到期时刻"（绝对时间）

### 为什么要换？

思路一每拍都要**修改**每个定时器的 `remaining`。换个角度：维护一个全局时间 `now`（每拍 +1），每个定时器只记录**到期的绝对时刻** `expire = now + period`。tick 时只需**比较** `now == expire`，不用逐个减 1。

这样做的好处：

- 如果定时器按到期时间排好序（链表或堆），tick 只要看最前面那个有没有到期，大多数拍可以 O(1) 返回——这就是 FreeRTOS、Linux 内核定时器的思路。
- 可以随时算出"距离最近一个定时器到期还有多久"，配合低功耗模式让 CPU 一直睡到那个时刻（tickless）。

### ⚠️ 时间回绕问题

`now` 是 `uint32_t`，1ms 一拍的话约 49.7 天就会溢出回到 0。如果写 `if (now >= expire)`，回绕时会出错。经典的安全写法是：

```c
if ((int32_t)(now - expire) >= 0) { /* 已到期 */ }
```

无符号减法在回绕时依然得到正确的"差值"，再转成有符号数判断正负。本题中 `now` 不会溢出，用 `==` 判断就够了，但面试时一定要能说出这个坑。

### 代码

```c
typedef struct {
    bool running;
    bool repeat;
    uint32_t period;
    uint32_t expire;        // 到期的绝对时刻
} SoftTimer;

typedef struct {
    SoftTimer* timers;
    int n;
    uint32_t now;           // 全局时间（已经过的节拍数）
} TimerManager;

TimerManager* timerManagerCreate(int maxTimers) {
    TimerManager* obj = (TimerManager*)malloc(sizeof(TimerManager));
    obj->timers = (SoftTimer*)calloc(maxTimers, sizeof(SoftTimer));
    obj->n = maxTimers;
    obj->now = 0;
    return obj;
}

void timerManagerStart(TimerManager* obj, int id, int period, bool repeat) {
    SoftTimer* t = &obj->timers[id];
    t->running = true;
    t->repeat = repeat;
    t->period = (uint32_t)period;
    t->expire = obj->now + (uint32_t)period;      // 从现在起 period 拍后到期
}

void timerManagerStop(TimerManager* obj, int id) {
    obj->timers[id].running = false;
}

int* timerManagerTick(TimerManager* obj, int* returnSize) {
    int* fired = (int*)malloc(sizeof(int) * obj->n);
    int m = 0;
    obj->now++;                                    // 时间前进一拍
    for (int id = 0; id < obj->n; id++) {
        SoftTimer* t = &obj->timers[id];
        if (t->running && t->expire == obj->now) { // 只比较，不修改
            fired[m++] = id;
            if (t->repeat) {
                t->expire += t->period;            // 下一次到期时刻
            } else {
                t->running = false;
            }
        }
    }
    *returnSize = m;
    return fired;
}

void timerManagerFree(TimerManager* obj) {
    free(obj->timers);
    free(obj);
}
```

> 💬 `t->expire += t->period` 而不是 `t->expire = now + period`：两者在本题中相同；但在真实系统里，如果某次 tick 处理被延迟，前者能保证周期定时器"不累积误差"。

### 复杂度分析

- 本写法 `tick` 仍是 O(maxTimers)（为了按 id 输出，仍然扫描）；若改为按 `expire` 排序的链表，`tick` 在没有到期定时器时就是 O(1)。

---

## ⚠️ 第五步：小白常见错误

1. **重复 `start` 时没有重置 remaining** → 题目要求"重新开始计时"，以最后一次 start 为准。
2. **周期定时器触发后忘了重装** → remaining 变成 0 后再减 1，`uint32_t` 下溢成 42 亿，再也不会触发。
3. **单次定时器触发后没有停止** → 和上一条一样会下溢，或者被错误地再次触发。
4. **先判断 `remaining == 0` 再减 1** → 触发时间晚了一拍。
5. **返回数组按触发先后乱序添加后忘了排序** → 按 id 顺序遍历最简单，天然有序。
6. **在中断里直接调用耗时的回调**（真实项目） → 中断处理时间过长，影响其他中断的实时性。

---

## 📊 第六步：两种方法对比

| 方法 | tick 操作 | 能否快速得知"下一个到期时间" | 说明 |
|---|---|---|---|
| 倒计时 remaining | 每拍修改所有定时器 | 否 | 最直观，裸机小项目常用 |
| 绝对到期时刻 expire | 只比较 | 能（配合排序结构） | RTOS / 内核常用，支持 tickless 低功耗 |

---

## 🔗 举一反三

- **9060. 优先级任务调度模拟**：调度器同样是"每个 tick 做一次决策"。
- **思考题 1**：定时器有 1 万个时，每拍扫描全部太慢。了解一下**时间轮（timing wheel）**：像钟表一样按到期时间把定时器挂到不同的"槽"里。
- **思考题 2**：如果 `start` 在主循环里调用、`tick` 在中断里调用，哪些变量需要加 `volatile`？修改结构体的多个字段时需不需要关中断？
