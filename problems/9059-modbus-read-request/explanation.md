# 9059. Modbus 读寄存器请求帧 —— 小白详细题解

> 工业现场的设备基本都"说 Modbus"。作为主机去读一台电表的电压，第一步就是**拼出这 8 个字节**。这道题考的是协议文档阅读能力、字节序和 CRC 的综合运用——都是嵌入式通信的基本功。

---

## 📖 第一步：先读懂题目

### 一帧请求长什么样？

示例 2：读 17 号从机、从地址 107 开始的 3 个寄存器：

| 字节 | 含义 | 十六进制 | 十进制 |
|---|---|---|---|
| 0 | 从机地址 17 | 11 | 17 |
| 1 | 功能码"读保持寄存器" | 03 | 3 |
| 2 | 起始地址 107 的高字节 | 00 | 0 |
| 3 | 起始地址 107 的低字节 | 6B | 107 |
| 4 | 数量 3 的高字节 | 00 | 0 |
| 5 | 数量 3 的低字节 | 03 | 3 |
| 6 | CRC 0x8776 的**低**字节 | 76 | 118 |
| 7 | CRC 0x8776 的**高**字节 | 87 | 135 |

### 字节序：大端 vs 小端

- **大端（Big-Endian）**：高字节在前。Modbus 的地址、数量、寄存器数据都是大端。
- **小端（Little-Endian）**：低字节在前。Modbus 的 **CRC 偏偏是小端**。

这个"不一致"是 Modbus 最出名的坑，很多新手调了半天设备不回应，就是 CRC 字节顺序反了。

### 参数检查

| 条件 | 原因 |
|---|---|
| 从机地址 1 ~ 247 | 0 是广播（从机不回应），248 ~ 255 保留 |
| 数量 1 ~ 125 | 响应帧里数据字节数用 1 个字节表示，125 × 2 = 250 ≤ 255 |
| 起始地址 + 数量 ≤ 65536 | 寄存器地址只有 16 位 |

**容易忽略的细节：**

1. 起始地址 65535、数量 1 是合法的（65535 + 1 = 65536，正好不越界）。
2. `startAddr + quantity` 在 `uint16_t` 下会**溢出回绕**（65535 + 2 = 1），必须先转成 32 位再加。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 拆分 16 位数

```c
uint16_t x = 0x1234;
uint8_t hi = (uint8_t)(x >> 8);      // 0x12：右移 8 位，高字节移到低位
uint8_t lo = (uint8_t)(x & 0xFF);    // 0x34：与 0xFF 只保留低 8 位
```

### 2. 整数提升与溢出

`uint16_t` 参与运算时会先提升为 `int`，所以 `startAddr + quantity` 在 32 位机器上其实不会溢出。但在 **16 位单片机**（int 只有 16 位，如 MSP430、部分 8051）上就会溢出。显式写 `(uint32_t)startAddr + quantity` 才能保证到处都正确。

### 3. `size_t` 返回值

返回"写了多少字节"是 C 库的常见风格（类似 `snprintf` 返回写入长度），返回 0 表示失败，调用者可以直接 `if (n == 0)` 判断。

---

## 💡 第三步：思路一 —— 逐字节填写 + 逐位 CRC

### 代码

```c
static uint16_t crc16Modbus(const uint8_t* buf, size_t len) {
    uint16_t crc = 0xFFFF;                                   // 初值
    for (size_t i = 0; i < len; i++) {
        crc ^= buf[i];
        for (int b = 0; b < 8; b++) {                        // 右移算法，多项式反转为 0xA001
            if (crc & 1) crc = (uint16_t)((crc >> 1) ^ 0xA001);
            else crc >>= 1;
        }
    }
    return crc;
}

size_t modbusBuildReadRequest(uint8_t slave, uint16_t startAddr, uint16_t quantity, uint8_t* frame) {
    if (slave < 1 || slave > 247) return 0;                  // 从机地址非法
    if (quantity < 1 || quantity > 125) return 0;            // 数量非法
    if ((uint32_t)startAddr + quantity > 65536u) return 0;   // 地址越界（先转 32 位防溢出）

    frame[0] = slave;                                        // 从机地址
    frame[1] = 0x03;                                         // 功能码：读保持寄存器
    frame[2] = (uint8_t)(startAddr >> 8);                    // 起始地址：高字节在前
    frame[3] = (uint8_t)(startAddr & 0xFF);
    frame[4] = (uint8_t)(quantity >> 8);                     // 数量：高字节在前
    frame[5] = (uint8_t)(quantity & 0xFF);

    uint16_t crc = crc16Modbus(frame, 6);                    // 对前 6 字节算 CRC
    frame[6] = (uint8_t)(crc & 0xFF);                        // CRC：低字节在前！
    frame[7] = (uint8_t)(crc >> 8);
    return 8;
}
```

### 复杂度分析

- O(1)：固定 6 个字节 × 8 位。

---

## 🚀 第四步：思路二 —— 封装字节序工具函数 + 查表 CRC

### 为什么要这样写？

真实的 Modbus 主机要支持很多功能码（03 读、06 写单个、10 写多个……），每个都要拼帧。把"写大端 16 位""写小端 16 位"封装成工具函数，代码更不容易出错，也更像协议文档。CRC 用查表法，在高波特率、多从机轮询时能省下不少 CPU。

### 代码

```c
static uint16_t crcTable[256];
static bool crcReady = false;

static void crcInit(void) {
    for (int i = 0; i < 256; i++) {
        uint16_t c = (uint16_t)i;
        for (int b = 0; b < 8; b++) c = (c & 1) ? (uint16_t)((c >> 1) ^ 0xA001) : (uint16_t)(c >> 1);
        crcTable[i] = c;
    }
    crcReady = true;
}

static uint16_t crc16(const uint8_t* p, size_t n) {
    if (!crcReady) crcInit();
    uint16_t crc = 0xFFFF;
    while (n--) crc = (uint16_t)((crc >> 8) ^ crcTable[(crc ^ *p++) & 0xFF]);
    return crc;
}

static uint8_t* putU16BE(uint8_t* p, uint16_t v) {   // 大端写入，返回下一个写入位置
    *p++ = (uint8_t)(v >> 8);
    *p++ = (uint8_t)v;
    return p;
}

static uint8_t* putU16LE(uint8_t* p, uint16_t v) {   // 小端写入
    *p++ = (uint8_t)v;
    *p++ = (uint8_t)(v >> 8);
    return p;
}

size_t modbusBuildReadRequest(uint8_t slave, uint16_t startAddr, uint16_t quantity, uint8_t* frame) {
    bool ok = slave >= 1 && slave <= 247
           && quantity >= 1 && quantity <= 125
           && (uint32_t)startAddr + quantity <= 65536u;
    if (!ok) return 0;

    uint8_t* p = frame;
    *p++ = slave;
    *p++ = 0x03;
    p = putU16BE(p, startAddr);                       // PDU 部分：大端
    p = putU16BE(p, quantity);
    p = putU16LE(p, crc16(frame, (size_t)(p - frame))); // CRC：小端
    return (size_t)(p - frame);                       // 指针相减 = 已写入的字节数
}
```

> 💬 `p - frame`：两个指向同一数组的指针相减，结果是它们之间相隔的**元素个数**。这里就是已经写了多少字节。

### 复杂度分析

- O(1)。

### 🔌 嵌入式实战：发送与等待响应

```c
uint8_t tx[8], rx[256];
size_t n = modbusBuildReadRequest(1, 0, 2, tx);
if (n) {
    RS485_DE_HIGH();                 // RS-485 收发器切到发送
    uart_send(tx, n);
    uart_wait_tx_complete();         // 必须等最后一个字节的停止位发完！
    RS485_DE_LOW();                  // 切回接收
    /* 接收响应：01 03 04 [4 字节数据] CRC_L CRC_H，超时则重发 */
}
```

Modbus RTU 用**帧间静默时间**（至少 3.5 个字符时间）来区分两帧，所以连续发送两帧之间要留出足够的间隔。

### ❌ 不推荐：用结构体直接 memcpy

```c
struct { uint8_t slave, func; uint16_t start, qty; } req;   // ❌
memcpy(frame, &req, 6);
```

ARM、x86 都是小端机器，`uint16_t` 在内存里低字节在前，和 Modbus 要求的大端正好相反；而且编译器可能在成员之间插入填充字节。**协议打包一定要逐字节写**。

---

## ⚠️ 第五步：小白常见错误

1. **CRC 高字节在前** → 设备认为校验失败，什么都不回。
2. **地址/数量低字节在前** → 读的是别的寄存器（地址 107 = 0x006B 会变成 0x6B00 = 27392）。
3. **`startAddr + quantity` 在 16 位下溢出** → 65535 + 2 回绕成 1，越界检查失效。
4. **对 8 个字节算 CRC** → CRC 只覆盖前 6 个字节，不包括 CRC 自己。
5. **把"40108 号寄存器"直接当地址填 40108** → Modbus 文档里的 4xxxx 是"寄存器编号"，协议里的地址 = 编号 − 40001，即 107（示例 2）。

---

## 📊 第六步：方法对比

| 方法 | CRC | 可维护性 | 说明 |
|---|---|---|---|
| 逐字节手写 + 逐位 CRC | 每字节 8 次循环 | 一般 | 代码直观，适合一次性需求 |
| 字节序工具函数 + 查表 CRC | 每字节 1 次查表 | 好 | 功能码多时推荐 |
| 结构体 memcpy | — | ❌ 错误 | 字节序和填充都有问题 |

---

## 🔗 举一反三

- **9049. CRC-16/MODBUS**：本题用到的 CRC 算法。
- **9051. UART 帧解析**：主机收到从机响应后，要从字节流里解析出响应帧。
- **思考题 1**：写出功能码 `0x06`（写单个寄存器）的请求帧：`[从机, 06, 地址H, 地址L, 值H, 值L, CRC_L, CRC_H]`。
- **思考题 2**：从机响应 `01 03 04 00 0A 01 02 CRC_L CRC_H`，两个寄存器的值分别是多少？
