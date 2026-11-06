# 9047. 覆盖式日志缓冲区 —— 小白详细题解

> 9046 的环形缓冲区满了就"拒收"，这道题满了就"挤掉最旧的"。两者只差一个分支，但用途完全不同：前者用于通信（数据一个都不能乱），后者用于日志/黑匣子（只关心最近发生了什么）。

---

## 📖 第一步：先读懂题目

把缓冲区想成一个**只能挂 3 张照片的相框墙**：挂满之后再来一张新照片，就把**最早挂上去的那张**摘下来，新照片挂在那个位置。

示例 1（容量 3）：

| 操作 | 物理数组 buf[0..2] | 最旧位置 head | count | 从旧到新 |
|---|---|---|---|---|
| write 1 | `[1][ ][ ]` | 0 | 1 | 1 |
| write 2 | `[1][2][ ]` | 0 | 2 | 1, 2 |
| getAll | | | | **[1,2]** |
| write 3 | `[1][2][3]` | 0 | 3 | 1, 2, 3 |
| write 4 | `[4][2][3]` | **1** | 3 | 2, 3, 4 |
| write 5 | `[4][5][3]` | **2** | 3 | 3, 4, 5 |
| getAll | | | | **[3,4,5]** |

注意物理数组是 `[4][5][3]`，但逻辑顺序要从 head=2 开始读：3 → 4 → 5。

**容易忽略的细节：**

1. `getAll` **不删除**数据，连续调用两次结果相同。
2. 输出顺序是**从旧到新**，不是数组下标顺序。
3. 缓冲区为空时 `getAll` 返回空数组 `[]`，`*returnSize` 必须设成 0。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. `int32_t`

`<stdint.h>` 中"正好 32 位的有符号整数"。日志值最大 `10^9`，用 `int32_t` 存足够（最大约 `2.1 × 10^9`）。

### 2. 返回数组的函数：`int* f(..., int* returnSize)`

C 函数只能返回一个值，所以数组的**长度**通过指针参数 `returnSize` "带出去"：

```c
int* res = (int*)malloc(sizeof(int) * (count + 1));   // +1：count 为 0 时也申请到有效内存
*returnSize = count;                                  // 告诉调用者数组有多长
return res;
```

数组必须用 `malloc` 申请。如果写成局部数组 `int res[1000]; return res;`，函数返回后这块栈内存就失效了。

### 3. 逻辑下标 → 物理下标

第 `i` 旧的元素（i 从 0 开始）在 `buf[(head + i) % capacity]`。这个公式是所有环形结构的核心。

---

## 💡 第三步：思路一 —— 普通数组，满了整体左移（最朴素）

### 思路

像排队一样：数组 `buf[0]` 永远是最旧的。没满就追加到末尾；满了就把 `buf[1..cap-1]` 整体左移一格（挤掉 `buf[0]`），新值放到最后。`getAll` 直接按下标顺序复制。

| 操作（容量 3） | buf |
|---|---|
| write 1, 2, 3 | `[1][2][3]` |
| write 4 | 左移 → `[2][3][ ]`，追加 → `[2][3][4]` |
| write 5 | 左移 → `[3][4][ ]`，追加 → `[3][4][5]` |

### 代码

```c
typedef struct {
    int32_t* buf;     // buf[0] 永远是最旧的一条
    int capacity;
    int count;
} LogBuffer;

LogBuffer* logBufferCreate(int capacity) {
    LogBuffer* obj = (LogBuffer*)malloc(sizeof(LogBuffer));
    obj->buf = (int32_t*)malloc(sizeof(int32_t) * capacity);
    obj->capacity = capacity;
    obj->count = 0;
    return obj;
}

void logBufferWrite(LogBuffer* obj, int32_t value) {
    if (obj->count == obj->capacity) {
        // 满了：把 buf[1..cap-1] 搬到 buf[0..cap-2]，挤掉最旧的 buf[0]
        memmove(obj->buf, obj->buf + 1, sizeof(int32_t) * (obj->capacity - 1));
        obj->count--;
    }
    obj->buf[obj->count++] = value;   // 追加到末尾
}

int* logBufferGetAll(LogBuffer* obj, int* returnSize) {
    int* res = (int*)malloc(sizeof(int) * (obj->count + 1));
    for (int i = 0; i < obj->count; i++) {
        res[i] = obj->buf[i];          // 下标顺序就是从旧到新
    }
    *returnSize = obj->count;
    return res;
}

int logBufferCount(LogBuffer* obj) {
    return obj->count;
}

void logBufferFree(LogBuffer* obj) {
    free(obj->buf);
    free(obj);
}
```

> 💬 `memmove` 和 `memcpy` 的区别：源和目标内存**重叠**时必须用 `memmove`（这里正是重叠的），`memcpy` 的结果是未定义的。

### 复杂度分析

- `write`：满了以后每次要搬 capacity 个元素，**O(capacity)**。
- `getAll`：O(count)。

---

## 🚀 第四步：思路二 —— 环形缓冲区，满了只移动 head

### 为什么能优化？

思路一每写一条日志都要搬动整个数组。在 MCU 上，日志可能在中断里高频写入，这种开销不可接受。

环形缓冲区的思路：**数据不动，移动"最旧位置"这个指针**。

- 写入位置 `tail = (head + count) % capacity`（最旧位置往后数 count 个）。
- 没满：写入后 `count++`。
- 满了：tail 正好等于 head，新值**覆盖**了最旧的那条，然后 `head` 后移一格（第二旧的变成最旧的）。

### 代码

```c
typedef struct {
    int32_t* buf;
    int capacity;
    int head;     // 最旧一条的位置
    int count;    // 当前条数
} LogBuffer;

LogBuffer* logBufferCreate(int capacity) {
    LogBuffer* obj = (LogBuffer*)malloc(sizeof(LogBuffer));
    obj->buf = (int32_t*)malloc(sizeof(int32_t) * capacity);
    obj->capacity = capacity;
    obj->head = 0;
    obj->count = 0;
    return obj;
}

void logBufferWrite(LogBuffer* obj, int32_t value) {
    int tail = (obj->head + obj->count) % obj->capacity;  // 下一个写入位置
    obj->buf[tail] = value;                               // 满了时这里正好覆盖最旧的
    if (obj->count < obj->capacity) {
        obj->count++;                                     // 没满：条数 +1
    } else {
        obj->head = (obj->head + 1) % obj->capacity;      // 满了：最旧位置后移
    }
}

int* logBufferGetAll(LogBuffer* obj, int* returnSize) {
    int* res = (int*)malloc(sizeof(int) * (obj->count + 1));
    for (int i = 0; i < obj->count; i++) {
        res[i] = obj->buf[(obj->head + i) % obj->capacity];  // 逻辑第 i 个 → 物理位置
    }
    *returnSize = obj->count;
    return res;
}

int logBufferCount(LogBuffer* obj) {
    return obj->count;
}

void logBufferFree(LogBuffer* obj) {
    free(obj->buf);
    free(obj);
}
```

### 复杂度分析

- `write`：**O(1)**。
- `getAll`：O(count)，这是输出本身的代价，无法更快。

### 🔌 嵌入式实战：掉电不丢的"黑匣子"

真实项目里，日志缓冲区通常放在一段**复位时不清零**的 RAM 里（链接脚本中的 `.noinit` 段），这样看门狗复位后还能读出死机前的日志：

```c
#define LOG_MAGIC 0x4C4F4721u
typedef struct {
    uint32_t magic;                // 有效标志：上电后不等于 LOG_MAGIC 说明内容是随机值
    uint32_t wr;                   // 一共写了多少条（一直递增）
    uint32_t buf[64];
} CrashLog;
__attribute__((section(".noinit"))) static CrashLog g_log;

void log_put(uint32_t code) {
    g_log.buf[g_log.wr % 64] = code;   // wr 一直增长，取模得到位置
    g_log.wr++;                        // 条数 = min(wr, 64)，最旧的在 wr - 条数
}
```

这里用"总写入次数 wr"代替 head + count，也是一种常见写法。

---

## ⚠️ 第五步：小白常见错误

1. **满了时只覆盖不移动 head** → `getAll` 从 head 开始读，第一个读到的是**最新**的那条，顺序全乱。
2. **满了时 head 和 count 都变** → 满了以后条数不再增加，`count` 必须保持 `capacity`。
3. **`getAll` 直接按物理下标 `buf[0..count-1]` 输出** → 绕圈后顺序错误（示例 1 会输出 `[4,5,3]`）。
4. **`*returnSize` 忘了赋值** → 判题程序读到随机长度，输出乱码甚至崩溃。
5. **思路一用 `memcpy` 搬重叠内存** → 未定义行为，在某些库实现下会出错。

---

## 📊 第六步：方法对比

| 方法 | write | getAll | 说明 |
|---|---|---|---|
| 数组整体左移 | O(capacity) | O(count) | 好理解，但每次写都要搬数据 |
| 环形缓冲区覆盖 | O(1) | O(count) | 实际项目的标准做法 |

---

## 🔗 举一反三

- **9046. 环形缓冲区**：满了丢弃新数据的版本，对比一下两者的 `push` / `write` 只差哪几行。
- **9052. 滑动平均滤波**：滤波器的"最近 N 个采样值"也是用覆盖式环形缓冲区保存的。
- **思考题 1**：如果只想读出"最近的 k 条"（k < count），最旧的那条在哪个位置？
- **思考题 2**：日志在中断里写、在主循环里 `getAll`，读到一半时被中断写入一条新日志，会发生什么？应该怎么保护？
