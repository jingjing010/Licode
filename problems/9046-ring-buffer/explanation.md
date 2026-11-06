# 9046. 环形缓冲区 —— 小白详细题解

> 环形缓冲区（Ring Buffer / Circular Buffer）是嵌入式面试的"必考题"，几乎所有串口驱动、日志系统、音频采集都离不开它。这道题让你从零写一个最基础的版本。

---

## 📖 第一步：先读懂题目

想象一个**圆形的停车场**，车位编号 `0 ~ capacity-1` 首尾相连：

- `push`：新来一辆车，停到"下一个空车位"（队尾 tail）。停满了就**拒绝**这辆新车。
- `pop`：最早停进来的那辆车开走（队头 head）。没车就返回 `-1`。
- 车位用到最后一个之后，**绕回 0 号车位**继续——这就是"环形"。

用示例 1（容量 3）走一遍，`[ ]` 表示空位：

| 操作 | 数组 buf[0..2] | head | tail | count | 返回 |
|---|---|---|---|---|---|
| 创建 | `[ ][ ][ ]` | 0 | 0 | 0 | null |
| push 17 | `[17][ ][ ]` | 0 | 1 | 1 | true |
| push 34 | `[17][34][ ]` | 0 | 2 | 2 | true |
| push 51 | `[17][34][51]` | 0 | **0**（绕回） | 3 | true |
| push 68 | 满了，不变 | 0 | 0 | 3 | false |
| isFull | | | | | true |
| pop | `[ ][34][51]` | 1 | 0 | 2 | 17 |
| push 85 | `[85][34][51]` | 1 | 1 | 3 | true |
| count | | | | | 3 |
| pop ×3 | 依次取出 34、51、85 | 1→2→0→1 | 1 | 0 | 34, 51, 85 |
| pop | 空了 | | | | -1 |

注意 85 写进了 **0 号位置**（物理位置在最前面），但它在逻辑上是**最后**一个，所以最后才被取出。

**容易忽略的细节：**

1. 满了以后 `push` 是**丢弃新数据**（本题），不是覆盖旧数据（覆盖旧数据见 9047）。
2. `pop` 返回 `int` 而不是 `uint8_t`，因为要用 `-1` 表示"空"，而 `uint8_t` 根本表示不了 -1。
3. `head == tail` 时可能是"空"，也可能是"满"（上表 push 51 之后 head = tail = 0 且是满的），需要额外的信息区分。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. `uint8_t` 是什么？

来自 `<stdint.h>`，表示"**正好 8 位的无符号整数**"，取值 `0 ~ 255`，正好是一个字节。嵌入式代码几乎不用 `char` / `int` 表示数据，而是用 `uint8_t`、`uint16_t`、`uint32_t`，因为 `int` 在不同单片机上可能是 16 位也可能是 32 位，而 `uint8_t` 永远是 8 位。

### 2. 结构体 + `malloc`：设计类题目的套路

```c
typedef struct {
    uint8_t* buf;    // 指向存数据的数组
    int capacity;
    int head, tail, count;
} RingBuffer;
```

`ringBufferCreate` 里要 `malloc` **两次**：一次给结构体本身，一次给数据数组 `buf`。对应地 `ringBufferFree` 也要 `free` 两次，并且**先 free(buf) 再 free(obj)**——反过来的话，`obj` 已经释放，再访问 `obj->buf` 就是使用野指针。

### 3. 取模 `%` 实现"绕回"

```c
tail = (tail + 1) % capacity;   // capacity = 3 时：0 → 1 → 2 → 0 → 1 ...
```

---

## 💡 第三步：思路一 —— head / tail + count 计数

### 思路

- `head`：下一个要**读**的位置；`tail`：下一个要**写**的位置。
- 再用 `count` 记录当前有几个元素：`count == 0` 是空，`count == capacity` 是满，完美区分了"head == tail"的两种情况。

### 代码

```c
typedef struct {
    uint8_t* buf;    // 数据数组
    int capacity;    // 容量
    int head;        // 下一个要读的位置
    int tail;        // 下一个要写的位置
    int count;       // 当前元素个数
} RingBuffer;

RingBuffer* ringBufferCreate(int capacity) {
    RingBuffer* obj = (RingBuffer*)malloc(sizeof(RingBuffer));   // 结构体本身
    obj->buf = (uint8_t*)malloc(capacity);                       // 数据数组，每个元素 1 字节
    obj->capacity = capacity;
    obj->head = 0;
    obj->tail = 0;
    obj->count = 0;
    return obj;
}

bool ringBufferPush(RingBuffer* obj, uint8_t data) {
    if (obj->count == obj->capacity) {          // 满了：丢弃新数据
        return false;
    }
    obj->buf[obj->tail] = data;                 // 写到队尾
    obj->tail = (obj->tail + 1) % obj->capacity; // 队尾后移，到头就绕回 0
    obj->count++;
    return true;
}

int ringBufferPop(RingBuffer* obj) {
    if (obj->count == 0) {                      // 空了
        return -1;
    }
    int v = obj->buf[obj->head];                // 读队头
    obj->head = (obj->head + 1) % obj->capacity; // 队头后移
    obj->count--;
    return v;
}

int ringBufferCount(RingBuffer* obj) {
    return obj->count;
}

bool ringBufferIsFull(RingBuffer* obj) {
    return obj->count == obj->capacity;
}

void ringBufferFree(RingBuffer* obj) {
    free(obj->buf);     // 先释放数据数组
    free(obj);          // 再释放结构体
}
```

### 复杂度分析

- 每个操作都是 **O(1)**，空间 O(capacity)。

---

## 🚀 第四步：思路二 —— 不要 count，"牺牲一个格子"

### 为什么要换？

思路一有个隐患：真实项目中 `push` 在**中断**里调用，`pop` 在**主循环**里调用，两边都会修改 `count`。`count++` 在 CPU 上其实是"读 → 加 1 → 写回"三步，如果主循环执行 `count--` 到一半被中断打断，就会丢失一次修改——这叫**竞态条件**。

解决办法之一：**去掉 count**，让中断只改 `tail`、主循环只改 `head`，每个变量只有一个"写者"，就不会冲突（单生产者单消费者无锁队列，SPSC）。

可是没有 count，怎么区分空和满？经典做法是**多开一个格子并且永远不用满它**：

- 数组大小 `size = capacity + 1`
- **空**：`head == tail`
- **满**：`(tail + 1) % size == head`（tail 再走一步就追上 head 了）

| 操作（capacity=3，size=4） | head | tail | 判断 |
|---|---|---|---|
| 初始 | 0 | 0 | head == tail → 空 |
| push ×3 | 0 | 3 | (3+1)%4 == 0 == head → 满 |
| pop | 1 | 3 | 不满 |
| push | 1 | 0 | (0+1)%4 == 1 == head → 满 |

### 代码

```c
typedef struct {
    uint8_t* buf;
    int size;           // 数组实际大小 = capacity + 1
    volatile int head;  // 只有读者（主循环）修改
    volatile int tail;  // 只有写者（中断）修改
} RingBuffer;

RingBuffer* ringBufferCreate(int capacity) {
    RingBuffer* obj = (RingBuffer*)malloc(sizeof(RingBuffer));
    obj->size = capacity + 1;                    // 多开一个格子
    obj->buf = (uint8_t*)malloc(obj->size);
    obj->head = 0;
    obj->tail = 0;
    return obj;
}

bool ringBufferIsFull(RingBuffer* obj) {
    return (obj->tail + 1) % obj->size == obj->head;   // tail 再走一步就撞上 head
}

bool ringBufferPush(RingBuffer* obj, uint8_t data) {
    if (ringBufferIsFull(obj)) return false;
    obj->buf[obj->tail] = data;                  // 先写数据
    obj->tail = (obj->tail + 1) % obj->size;     // 再移动 tail（顺序不能反！）
    return true;
}

int ringBufferPop(RingBuffer* obj) {
    if (obj->head == obj->tail) return -1;       // 空
    int v = obj->buf[obj->head];                 // 先读数据
    obj->head = (obj->head + 1) % obj->size;     // 再移动 head
    return v;
}

int ringBufferCount(RingBuffer* obj) {
    return (obj->tail - obj->head + obj->size) % obj->size;  // 加 size 防止出现负数
}

void ringBufferFree(RingBuffer* obj) {
    free(obj->buf);
    free(obj);
}
```

> 💬 **为什么 push 要"先写数据再移动 tail"？** 如果先移动 tail，主循环可能在数据写入之前就看到"有新数据"，读到的是旧的垃圾值。
>
> 💬 **`volatile` 的作用**：告诉编译器这个变量可能被中断"偷偷"修改，每次都要从内存重新读取，不能缓存在寄存器里。

### 🔌 嵌入式实战：容量取 2 的幂

很多驱动把容量定为 2 的幂（如 256），并让 head / tail **一直往上加不取模**，用的时候再 `& (SIZE - 1)`：

```c
#define RB_SIZE 256u                              // 必须是 2 的幂
static uint8_t  rx_buf[RB_SIZE];
static volatile uint32_t rx_head, rx_tail;        // 一直递增，溢出也没关系

void USART1_IRQHandler(void) {                    // 接收中断：只管写
    uint8_t c = USART1->DR;
    if (rx_tail - rx_head < RB_SIZE) {            // 无符号相减 = 元素个数，溢出时依然正确
        rx_buf[rx_tail & (RB_SIZE - 1)] = c;      // & 代替 %，一条指令
        rx_tail++;
    }
}
```

好处：`&` 比 `%` 快得多（很多 MCU 没有硬件除法器）；`tail - head` 直接就是元素个数，也不用浪费格子。

### 复杂度分析

- 每个操作 **O(1)**，空间 O(capacity + 1)。

---

## ⚠️ 第五步：小白常见错误

1. **只用 `head == tail` 判断空和满** → 写满后 head 又等于 tail，被当成"空"，数据全丢了。
2. **忘记取模**：`obj->tail++` 不绕回 → 写到第 capacity 个时数组越界，程序崩溃或改坏别的内存。
3. **`ringBufferPop` 返回类型写成 `uint8_t`** → `-1` 变成 255，"空"和"读到 255"无法区分（示例 2 正好有 255）。
4. **`malloc(capacity)` 写成 `malloc(sizeof(capacity))`** → 只申请了 4 个字节（int 的大小），容量大一点就越界。
5. **free 顺序反了**：先 `free(obj)` 再 `free(obj->buf)` → 访问已释放的内存。
6. **思路二计算个数写成 `tail - head`** → tail 绕回后比 head 小，结果为负数，要加上 size 再取模。

---

## 📊 第六步：两种方法对比

| 方法 | 区分空/满 | 空间 | 中断安全 | 说明 |
|---|---|---|---|---|
| head + tail + count | 看 count | capacity | 需要关中断保护 count | 最直观，面试先写这个 |
| 牺牲一个格子 | `(tail+1)%size == head` | capacity + 1 | 单读单写天然安全 | 驱动层常用 |
| 2 的幂 + 自由递增下标 | `tail - head` | capacity | 单读单写天然安全 | Linux kfifo 就是这么做的 |

---

## 🔗 举一反三

- **9047. 覆盖式日志缓冲区**：满了以后不是丢弃新数据，而是**覆盖最旧的数据**。
- **9051. UART 帧解析**：从环形缓冲区里取出字节后，下一步就是按协议拆帧。
- **力扣 622. 设计循环队列**：同一道题的通用版本。
- **思考题**：如果要一次 `push` 一整块数据（`push(buf, len)`），怎样用最多两次 `memcpy` 完成？（提示：数据可能跨过数组末尾，要拆成两段。）
