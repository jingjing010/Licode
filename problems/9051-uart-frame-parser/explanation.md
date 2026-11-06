# 9051. UART 帧解析 —— 小白详细题解

> 几乎每个嵌入式项目都要和别的设备"对话"：上位机发命令、GPS 模块报位置、蓝牙模块透传数据……串口只给你一个个字节，**把字节流切成一帧帧**是驱动工程师的基本功，也是面试官最爱让你现场手写的题目之一。

---

## 📖 第一步：先读懂题目

一帧长这样：

```
AA 55 | LEN | DATA[0] ... DATA[LEN-1] | CHK
帧头     长度      数据（LEN 个字节）       校验 = (LEN + 数据之和) & 0xFF
```

为什么要这么设计？

- **帧头 AA 55**：让接收方知道"一帧从这里开始"。两个字节比一个字节更不容易被数据"冒充"。
- **LEN**：知道数据有多长，才知道什么时候结束。
- **CHK**：线路干扰会把某些位翻转，校验不对就丢弃。

示例 3 `[170,170,85,1,3,4,170,85,3,1,2]` 逐字节走一遍：

| 下标 | 字节 | 在做什么 | 说明 |
|---|---|---|---|
| 0 | AA | 找帧头 | 看到 AA，期待下一个是 55 |
| 1 | AA | 期待 55 | 不是 55，但它**自己是 AA**，继续期待 55 |
| 2 | 55 | 期待 55 | 帧头找到了！ |
| 3 | 01 | 读长度 | LEN = 1，sum = 1 |
| 4 | 03 | 读数据 | 数据 [3]，sum = 4，读够了 |
| 5 | 04 | 读校验 | 4 == 4，**有效帧 [3]** |
| 6~7 | AA 55 | 找帧头 | 帧头 |
| 8 | 03 | 读长度 | LEN = 3 |
| 9~10 | 01 02 | 读数据 | 只读到 2 个，字节流就结束了 → 半截帧丢弃 |

**容易忽略的细节：**

1. `AA AA 55`：第二个 AA 才是帧头的开始，不能因为第一个 AA 后面不是 55 就把第二个 AA 也跳过。
2. 校验失败后**不回头**：从 CHK 的下一个字节继续找。真实设备上字节是一个个从中断送来的，读过的字节已经没了，没法回头。
3. `LEN = 0` 是合法的（比如"心跳包"），输出空数组 `[]`。
4. 数据里出现 `AA 55` 很正常（数据是任意字节），只要还在读数据，就把它当数据。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 返回二维数组：`int** f(..., int* returnSize, int** returnColumnSizes)`

每帧长度不同，所以要"锯齿数组"：

```c
int** res  = (int**)malloc(sizeof(int*) * 最大帧数);   // 每个元素指向一帧的数据
int*  cols = (int*)malloc(sizeof(int) * 最大帧数);     // 每帧的长度
res[n]  = data;        // data 是这一帧 malloc 出来的数组
cols[n] = frameLen;
*returnSize = n;                // 一共几帧
*returnColumnSizes = cols;      // 注意是 *returnColumnSizes，把数组地址"带出去"
```

最大帧数怎么估计？最短的帧是 `AA 55 00 CHK` 共 4 字节，所以最多 `len / 4 + 1` 帧。

### 2. `enum`：给状态起名字

```c
typedef enum { WAIT_AA, WAIT_55, READ_LEN, READ_DATA, READ_CHK } ParseState;
```

`enum` 本质上就是整数常量 0、1、2……，但写成名字后代码一眼就能看懂，调试器里也能直接显示状态名。

### 3. `uint8_t` 自动取模

`uint8_t sum; sum = sum + c;` 超过 255 会自动回绕（只保留低 8 位），恰好就是 `& 0xFF`。

---

## 💡 第三步：思路一 —— 下标扫描（一次拿到完整数据时）

### 思路

如果整段数据都在数组里（例如 DMA 一次收完一整块），可以直接用下标 `i` 往后扫：

1. `buf[i] == AA && buf[i+1] == 55` → 帧头。否则 `i++`。
2. 读 `LEN = buf[i+2]`，帧尾位置 `end = i + 3 + LEN`（CHK 的下标）。`end` 超出数组 → 半截帧，结束。
3. 计算校验，有效就保存；然后 `i = end + 1`（不回头）。

因为第 1 步是 `i++` 一格一格挪，`AA AA 55` 时 i 会自然停在第二个 AA 上。

### 代码

```c
int** parseFrames(const uint8_t* buf, size_t len, int* returnSize, int** returnColumnSizes) {
    size_t maxFrames = len / 4 + 1;                  // 最短帧 4 字节
    int** res = (int**)malloc(sizeof(int*) * maxFrames);
    int* cols = (int*)malloc(sizeof(int) * maxFrames);
    int n = 0;

    size_t i = 0;
    while (i + 1 < len) {
        if (buf[i] != 0xAA || buf[i + 1] != 0x55) {  // 不是帧头，往后挪一格
            i++;
            continue;
        }
        if (i + 2 >= len) break;                     // 连 LEN 都没收到
        int frameLen = buf[i + 2];
        size_t end = i + 3 + frameLen;               // CHK 所在下标
        if (end >= len) break;                       // 半截帧，丢弃

        uint8_t sum = (uint8_t)frameLen;
        for (size_t k = i + 3; k < end; k++) {
            sum = (uint8_t)(sum + buf[k]);           // 累加数据
        }
        if (sum == buf[end]) {                       // 校验通过：保存数据部分
            int* data = (int*)malloc(sizeof(int) * (frameLen + 1));
            for (int k = 0; k < frameLen; k++) {
                data[k] = buf[i + 3 + k];
            }
            res[n] = data;
            cols[n] = frameLen;
            n++;
        }
        i = end + 1;                                 // 不论是否有效，都从 CHK 后面继续
    }

    *returnSize = n;
    *returnColumnSizes = cols;
    return res;
}
```

### 复杂度分析

- 每个字节最多被访问常数次，时间 **O(len)**，空间 O(len)（结果）。

---

## 🚀 第四步：思路二 —— 逐字节状态机（真实驱动的写法）

### 为什么要换？

思路一需要"往后看"（`buf[i+1]`、`buf[end]`），前提是数据都已经到了。可真实的串口是**每收到一个字节触发一次中断**，中断里只有"当前这一个字节"。这时就要用**状态机**：把"解析进行到哪一步"记在状态变量里，每来一个字节推进一步。

状态转移图：

```
           AA                55                 LEN(>0)
 WAIT_AA ------> WAIT_55 ---------> READ_LEN ------------> READ_DATA
    ^    <------  |  ^ AA(保持)        |  LEN==0               | 读满 LEN 个
    |    其他字节  +--+                 v                       v
    +------------------------------ READ_CHK <-----------------+
               （校验完，不论对错）
```

### 代码

```c
typedef enum { WAIT_AA, WAIT_55, READ_LEN, READ_DATA, READ_CHK } ParseState;

int** parseFrames(const uint8_t* buf, size_t len, int* returnSize, int** returnColumnSizes) {
    size_t maxFrames = len / 4 + 1;
    int** res = (int**)malloc(sizeof(int*) * maxFrames);
    int* cols = (int*)malloc(sizeof(int) * maxFrames);
    int n = 0;

    ParseState st = WAIT_AA;     // 当前状态
    uint8_t frameLen = 0;        // 本帧长度
    uint8_t sum = 0;             // 校验累加值
    int got = 0;                 // 已收到的数据字节数
    int* data = NULL;            // 本帧数据

    for (size_t i = 0; i < len; i++) {
        uint8_t c = buf[i];      // 模拟"中断里收到一个字节"
        switch (st) {
        case WAIT_AA:
            if (c == 0xAA) st = WAIT_55;
            break;
        case WAIT_55:
            if (c == 0x55) st = READ_LEN;            // 帧头完整
            else if (c != 0xAA) st = WAIT_AA;        // 是 AA 就继续等 55，否则重新找
            break;
        case READ_LEN:
            frameLen = c;
            sum = c;                                 // 校验从 LEN 开始累加
            got = 0;
            data = (int*)malloc(sizeof(int) * (frameLen + 1));
            st = (frameLen == 0) ? READ_CHK : READ_DATA;   // 没有数据就直接读校验
            break;
        case READ_DATA:
            data[got++] = c;
            sum = (uint8_t)(sum + c);
            if (got == frameLen) st = READ_CHK;      // 数据收齐
            break;
        case READ_CHK:
            if (c == sum) {                          // 校验通过
                res[n] = data;
                cols[n] = frameLen;
                n++;
            } else {
                free(data);                          // 校验失败，丢弃
            }
            data = NULL;
            st = WAIT_AA;                            // 回到起点找下一帧
            break;
        }
    }
    free(data);                                      // 半截帧的数据也要释放

    *returnSize = n;
    *returnColumnSizes = cols;
    return res;
}
```

### 复杂度分析

- 时间 **O(len)**，每个字节只处理一次、绝不回头；状态只占几个字节，非常适合放进中断。

### 🔌 嵌入式实战：中断 + 环形缓冲 + 状态机

真实项目里通常分成两层：

```c
void USART1_IRQHandler(void) {              // 中断：只负责把字节塞进环形缓冲区（9046）
    ring_push(&rx_ring, USART1->DR);
}

void main_loop(void) {
    int c;
    while ((c = ring_pop(&rx_ring)) >= 0) { // 主循环：取一个字节喂一次状态机
        parser_feed(&parser, (uint8_t)c);   // 收到完整帧时在内部回调 on_frame()
    }
}
```

另外，真实协议通常还会加一个**超时复位**：如果在 READ_DATA 状态下超过 N 毫秒没收到新字节（对方掉线、半截帧），就强制回到 WAIT_AA，避免一个坏掉的 LEN 让解析器"卡"很久。

---

## ⚠️ 第五步：小白常见错误

1. **WAIT_55 收到 AA 时回到 WAIT_AA** → `AA AA 55 ...` 的帧被漏掉（示例 3 会输出 `[]`）。
2. **校验失败后回到帧头的下一个字节重新扫描** → 和题意不符；而且在中断驱动的真实场景里根本做不到。
3. **校验和只加数据、忘了加 LEN** → 题目定义 `CHK = (LEN + 数据之和) & 0xFF`。
4. **用 `int sum` 比较时不 `& 0xFF`** → 数据之和超过 255 时永远对不上。
5. **`LEN = 0` 时进入 READ_DATA** → 下一个字节（其实是 CHK）被当作数据，整帧错位。
6. **`*returnColumnSizes = cols` 写成 `returnColumnSizes = &cols`** → 只改了函数内部的局部指针，调用者拿不到。

---

## 📊 第六步：方法对比

| 方法 | 时间 | 需要整段数据 | 能否放进中断 | 适用 |
|---|---|---|---|---|
| 下标扫描 | O(len) | 是 | 否 | DMA 整块接收、离线解析日志 |
| 逐字节状态机 | O(len) | 否 | 能 | 串口中断逐字节接收（最常见） |

---

## 🔗 举一反三

- **9046. 环形缓冲区**：中断和主循环之间传递字节的"管道"。
- **9055. 表驱动状态机**：本题的 switch-case 状态机也可以改写成查表。
- **9049. CRC-16/MODBUS**：把本题的累加和换成 CRC，检错能力强得多。
- **思考题**：如果数据里出现 `AA 55` 会误导"中途接入"的接收方，有的协议会做**字节填充**（转义），比如数据中的 `AA` 发送为 `AA 00`。接收方的状态机要怎么改？
