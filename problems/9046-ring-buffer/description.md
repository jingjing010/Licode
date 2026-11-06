单片机的串口（UART）每收到一个字节就会触发一次**接收中断**。中断服务函数（ISR）必须尽快返回，所以通常只把收到的字节塞进一个**环形缓冲区**（Ring Buffer，也叫循环队列 / FIFO），主循环再慢慢从里面取出来解析。

请你实现一个容量固定的字节环形缓冲区 `RingBuffer`：

- `RingBuffer* ringBufferCreate(int capacity)`：创建一个最多能存放 `capacity` 个字节的缓冲区，初始为空。
- `bool ringBufferPush(RingBuffer* obj, uint8_t data)`：把一个字节写入队尾。如果缓冲区**已满**，则**丢弃这个新字节**（缓冲区内容不变）并返回 `false`；否则写入成功返回 `true`。
- `int ringBufferPop(RingBuffer* obj)`：从队头取出最早写入的那个字节并返回（`0 ~ 255`）。如果缓冲区**为空**，返回 `-1`。
- `int ringBufferCount(RingBuffer* obj)`：返回缓冲区中当前存放的字节数。
- `bool ringBufferIsFull(RingBuffer* obj)`：缓冲区已满返回 `true`，否则返回 `false`。
- `void ringBufferFree(RingBuffer* obj)`：释放缓冲区占用的全部内存。

数据必须**先进先出**（FIFO）：先 `push` 进去的字节先被 `pop` 出来。

### 示例 1

```
输入：
["RingBuffer","push","push","push","push","isFull","pop","push","count","pop","pop","pop","pop"]
[[3],[17],[34],[51],[68],[],[],[85],[],[],[],[],[]]
输出：
[null,true,true,true,false,true,17,true,3,34,51,85,-1]
解释：
容量为 3。依次写入 17、34、51 后缓冲区已满，再写 68 失败（68 被丢弃），isFull 返回 true。
pop 取出最早的 17，腾出一个位置，于是 85 写入成功，此时有 3 个字节：34、51、85。
接下来依次 pop 出 34、51、85，最后缓冲区为空，pop 返回 -1。
```

### 示例 2

```
输入：
["RingBuffer","pop","push","isFull","count","pop","isFull"]
[[1],[],[255],[],[],[],[]]
输出：
[null,-1,true,true,1,255,false]
解释：容量为 1。一开始为空，pop 返回 -1；写入 255 后满了；取出 255 后又变回非满。
```

### 提示

- `1 <= capacity <= 1000`
- `0 <= data <= 255`
- 操作总次数不超过 `2 * 10^4`
- 第一个操作一定是 `RingBuffer`

### 函数说明

```c
typedef struct {
    // 自己设计
} RingBuffer;

RingBuffer* ringBufferCreate(int capacity);
bool ringBufferPush(RingBuffer* obj, uint8_t data);
int ringBufferPop(RingBuffer* obj);
int ringBufferCount(RingBuffer* obj);
bool ringBufferIsFull(RingBuffer* obj);
void ringBufferFree(RingBuffer* obj);
```

- `ringBufferCreate` 要用 `malloc` 申请结构体（以及存放数据的数组）并返回指针
- `ringBufferFree` 由判题程序在最后调用，负责释放内存

### 自定义输入格式

```
["RingBuffer","push","pop"]
[[3],[17],[]]
```

第 1 行是操作名数组，第 2 行是每个操作对应的参数数组（`RingBuffer` 的参数是 `[capacity]`，`push` 的参数是 `[data]`，其它操作参数为空 `[]`）。
输出每个操作的返回值：`RingBuffer` 输出 `null`，布尔值输出 `true` / `false`，整数直接输出。
