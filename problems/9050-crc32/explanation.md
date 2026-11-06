# 9050. CRC-32 校验 —— 小白详细题解

> CRC-32 是"最出名"的 CRC：以太网、ZIP、PNG、Bootloader 固件校验都在用它。会了 9048、9049，这道题只多了一个新参数——**输出异或 xorout**。

---

## 📖 第一步：先读懂题目

和 CRC-16/MODBUS 对比一下参数：

| 参数 | CRC-16/MODBUS | CRC-32（本题） |
|---|---|---|
| width | 16 | 32 |
| poly | 0x8005 | 0x04C11DB7 |
| 反转后的多项式（右移算法用） | 0xA001 | **0xEDB88320** |
| init | 0xFFFF | 0xFFFFFFFF |
| refin / refout | 是 / 是 | 是 / 是 |
| xorout | 0 | **0xFFFFFFFF** |

所以算法几乎和 9049 一模一样：右移、异或 `0xEDB88320`，只是最后要 `crc ^ 0xFFFFFFFF`（也就是 `~crc`，按位取反）。

**为什么初值和 xorout 都是全 1？**

- 初值全 1：如果初值是 0，数据开头多几个 `0x00` 字节，CRC 不会变化（0 除以任何数还是 0），就检测不出"开头多了/少了几个零字节"的错误。
- xorout 全 1：同理防止"末尾多了零字节"检测不出来。

**容易忽略的细节：**

1. 结果可能超过 `2^31`（示例 1 就是 3421780262），必须用**无符号**类型，打印时用 `%u`。
2. 空数组：`0xFFFFFFFF ^ 0xFFFFFFFF = 0`。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 无符号常量后缀 `u`

```c
uint32_t crc = 0xFFFFFFFFu;
```

`u` 表示这是个无符号常量。不加 `u` 时 `0xFFFFFFFF` 在 32 位 int 平台上也会被当作 `unsigned int`，但养成加 `u` 的习惯可以避免在 16 位 MCU（int 只有 16 位）上出问题。

### 2. `~` 按位取反

`~crc` 和 `crc ^ 0xFFFFFFFFu` 对 `uint32_t` 来说完全等价。

### 3. `static` 全局变量

```c
static uint32_t crc32_table[256];
```

`static` 修饰全局变量表示"**只在本文件可见**"，防止和别的文件里同名的变量冲突。它存放在 `.bss` 段，程序启动时自动清零。

---

## 💡 第三步：思路一 —— 逐位右移算法

### 代码

```c
uint32_t crc32(const uint8_t* buf, size_t len) {
    uint32_t crc = 0xFFFFFFFFu;                       // init
    for (size_t i = 0; i < len; i++) {
        crc ^= buf[i];                                // 字节异或到低 8 位
        for (int b = 0; b < 8; b++) {
            if (crc & 1u) {                           // 最低位为 1
                crc = (crc >> 1) ^ 0xEDB88320u;       // 右移并异或反转多项式
            } else {
                crc >>= 1;
            }
        }
    }
    return crc ^ 0xFFFFFFFFu;                         // xorout
}
```

### 复杂度分析

- 时间 **O(8 × len)**：2×10⁵ 字节约 160 万次循环，完全没问题。空间 O(1)。

---

## 🚀 第四步：思路二 —— 256 项查表法

### 为什么能优化？

固件镜像动辄几百 KB，在 MCU 上逐位计算可能要几十毫秒，查表可以快好几倍。原理和 9049 完全一样：

```
crc = (crc >> 8) ^ table[(crc ^ byte) & 0xFF];
```

| crc 的部分 | 去向 |
|---|---|
| 低 8 位 | 与数据字节异或，作为查表下标 |
| 高 24 位 | 右移 8 位后与表项异或 |

### 代码

```c
static uint32_t crc32_table[256];
static bool crc32_table_ready = false;

static void crc32_init_table(void) {
    for (uint32_t i = 0; i < 256; i++) {
        uint32_t c = i;                               // 把 i 当作 crc 的低 8 位
        for (int b = 0; b < 8; b++) {                 // 执行 8 次右移算法
            c = (c & 1u) ? (c >> 1) ^ 0xEDB88320u : (c >> 1);
        }
        crc32_table[i] = c;
    }
    crc32_table_ready = true;
}

uint32_t crc32(const uint8_t* buf, size_t len) {
    if (!crc32_table_ready) crc32_init_table();      // 只在第一次调用时建表
    uint32_t crc = 0xFFFFFFFFu;
    for (size_t i = 0; i < len; i++) {
        crc = (crc >> 8) ^ crc32_table[(crc ^ buf[i]) & 0xFFu];
    }
    return crc ^ 0xFFFFFFFFu;
}
```

### 复杂度分析

- 时间 **O(len)**；表占 256 × 4 = 1KB。

### 🔌 嵌入式实战：分块计算（流式 CRC）

OTA 升级时固件是一包一包收到的，不可能等全部收完再算。把 init / xorout 拆出来，就能分块累加：

```c
uint32_t crc32_update(uint32_t crc, const uint8_t* p, size_t n) {
    for (size_t i = 0; i < n; i++)
        crc = (crc >> 8) ^ crc32_table[(crc ^ p[i]) & 0xFFu];
    return crc;
}

/* 用法 */
uint32_t c = 0xFFFFFFFFu;                 // init
c = crc32_update(c, pkt1, len1);          // 每收到一包就累加
c = crc32_update(c, pkt2, len2);
uint32_t result = c ^ 0xFFFFFFFFu;        // 全部收完再做 xorout
```

注意：STM32 的硬件 CRC 外设默认算的是**不反射**的 CRC-32/MPEG-2（同一个多项式但 refin/refout = 否、xorout = 0），结果和本题不同。想用硬件算出标准 CRC-32，需要打开外设的输入/输出反转功能（部分型号支持）并在最后取反。

---

## ⚠️ 第五步：小白常见错误

1. **忘了最后异或 0xFFFFFFFF** → 示例 1 会得到 `0x340BC6D9`，正好是正确答案按位取反。
2. **用 `int` / `%d` 打印** → 超过 2³¹ 的结果显示成负数。
3. **右移时用了有符号类型** → 算术右移高位补 1，结果全错。
4. **分块计算时每块都重新初始化 / 都做 xorout** → 只有第一块之前 init 一次、全部结束后 xorout 一次。
5. **建表时把 `c` 写成 `uint8_t`** → 表项只剩低 8 位。

---

## 📊 第六步：方法对比

| 方法 | 每字节 | 额外空间 | 说明 |
|---|---|---|---|
| 逐位右移 | 8 次循环 | 0 | Bootloader 空间紧张时用 |
| 半字节查表（16 项） | 2 次查表 | 64 字节 | 空间与速度的折中 |
| 256 项查表 | 1 次查表 | 1KB | zlib 等库的基础做法 |
| Slicing-by-8 | 每 8 字节 8 次查表 | 8KB | PC 上的高速实现 |

---

## 🔗 举一反三

- **9048 / 9049**：同一套框架下的 8 位、16 位 CRC。
- **思考题 1**：Python 的 `zlib.crc32(b"123456789")` 返回什么？用它验证你的实现。
- **思考题 2**：实现半字节查表版本：表只有 16 项，每个字节先处理低 4 位，再处理高 4 位。
