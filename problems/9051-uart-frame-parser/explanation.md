# 9051. UART 帧解析 —— 小白详细题解

> "串口收到的数据怎么拆包？"——这是嵌入式面试和实际项目中最常见的问题之一。标准答案就是**状态机**。这道题把"帧头 + 长度 + 数据 + 校验"这种最典型的私有协议完整走一遍。

---

## 📖 第一步：先读懂题目

串口收到的是一串**没有分隔符**的字节，比如示例 1：

```
AA 55 02 10 20 32 00 AA 55 01 07 08
```

按协议切开：

| 字节 | 含义 |
|---|---|
| AA 55 | 帧头 |
| 02 | LEN = 2 |
| 10 20 | 数据 16, 32 |
| 32 | 校验 = 2 + 16 + 32 = 50 = 0x32 ✔ |
| 00 | 噪声，丢弃 |
| AA 55 | 帧头 |
| 01 | LEN = 1 |
| 07 | 数据 7 |
| 08 | 校验 = 1 + 7 = 8 ✔ |

输出 `[[16,32],[7]]`。

示例 3 的关键：`AA AA 55 ...`。第一个 AA 之后不是 55，而是又一个 AA。这时候**不能**回到"等待帧头 1"然后把第二个 AA 丢掉——第二个 AA 很可能才是真正的帧头。所以规则 2 规定"收到 AA 仍停留在等待帧头 2"。

**容易忽略的细节：**

1. 数据段里可以出现 `0xAA 0x55`，按 LEN 收满就行，不能当作新帧头。
2. `LEN = 0` 是合法的，此时 `CHK = 0`，对应输出一个空数组 `[]`。
3. 校验是**低 8 位**的和：255 个 0xFF 加起来远超 255，要取 `& 0xFF`。
4. 校验失败后**不回退**：从校验字节的下一个字节重新找帧头（题目规则 5）。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. `enum` 定义状态

```c
enum { ST_HEAD1, ST_HEAD2, ST_LEN, ST_DATA, ST_CHK };   // 依次等于 0,1,2,3,4
```

比直接写数字 0~4 可读得多，`switch` 里一眼就知道是哪个状态。

### 2. 返回二维数组：`int** f(..., int* returnSize, int** returnColumnSizes)`

- 返回值 `int**`：一个"指针数组"，每个元素指向一帧数据（每帧单独 `malloc`）。
- `*returnSize`：一共几帧。
- `*returnColumnSizes`：另一个数组，记录每帧的长度——因为每行长度不同，调用者必须知道每行有多长。

```c
int** frames = (int**)malloc(sizeof(int*) * maxFrames);  // 行指针数组
int* sizes = (int*)malloc(sizeof(int) * maxFrames);       // 每行长度
...
*returnSize = cnt;
*returnColumnSizes = sizes;     // 注意：是给 *returnColumnSizes 赋值，不是给 returnColumnSizes
```

### 3. 最多有几帧？

最短的有效帧是 `AA 55 00 00`（4 字节），所以帧数不会超过 `len / 4`，按 `len / 4 + 1` 申请就够了。

### 4. `uint8_t` 自动取低 8 位

`uint8_t sum` 累加时溢出会自动回绕（模 256），正好等于 `& 0xFF`。

---

## 💡 第三步：思路一 —— 下标扫描（整段数据一次性处理）

### 思路

数据已经全部在数组里，可以用下标 `i` 往前扫：

1. 找到 `AA`；跳过后面连续的 `AA`；下一个必须是 `55`，否则继续找。
2. 读 LEN，算出校验字节的位置 `end = 帧头2位置 + 2 + LEN`；如果 `end` 超出数组，说明帧不完整，结束。
3. 校验正确就记录数据。然后从 `end + 1` 继续。

### 代码

```c
int** parseFrames(const uint8_t* buf, size_t len, int* returnSize, int** returnColumnSizes) {
    int maxFrames = (int)(len / 4) + 1;                 // 最短帧 4 字节
    int** frames = (int**)malloc(sizeof(int*) * maxFrames);
    int* sizes = (int*)malloc(sizeof(int) * maxFrames);
    int cnt = 0;
    size_t i = 0;

    while (i < len) {
        if (buf[i] != 0xAA) { i++; continue; }          // 不是帧头 1，跳过
        size_t j = i + 1;
        while (j < len && buf[j] == 0xAA) j++;          // 连续的 AA，最后一个才算帧头 1
        if (j >= len) break;                            // 数据结束了
        if (buf[j] != 0x55) { i = j + 1; continue; }    // 帧头 2 不对，从下一个字节重新找
        if (j + 1 >= len) break;                        // 没有 LEN 字节
        int n = buf[j + 1];                             // LEN
        size_t end = j + 2 + (size_t)n;                 // 校验字节的下标
        if (end >= len) break;                          // 帧不完整

        uint8_t sum = (uint8_t)n;
        for (size_t k = j + 2; k < end; k++) sum = (uint8_t)(sum + buf[k]);
        if (sum == buf[end]) {                          // 校验通过，保存数据
            int* f = (int*)malloc(sizeof(int) * (n + 1));
            for (int k = 0; k < n; k++) f[k] = buf[j + 2 + k];
            frames[cnt] = f;
            sizes[cnt] = n;
            cnt++;
        }
        i = end + 1;                                    // 不回退，从校验字节之后继续
    }
    *returnSize = cnt;
    *returnColumnSizes = sizes;
    return frames;
}
```

### 复杂度分析

- **时间 O(len)**：每个字节最多被看一次。**空间 O(len)**（结果）。

### 这个写法的问题

它要求**整段数据都已经到齐**。可真实的串口是一个字节一个字节来的：中断里收到一个字节，可能这一帧的后半段要过几毫秒才到。用下标扫描就得先把数据攒起来，还要处理"上次扫到一半"的情况，非常别扭。

---

## 🚀 第四步：思路二 —— 逐字节状态机（真实项目写法）

### 思路

把"现在解析到哪一步"保存成一个**状态变量**，每来一个字节只做一件事：根据当前状态处理这个字节，并决定下一个状态。这样字节什么时候来都无所谓，非常适合放在串口接收中断里。

```
        AA              55               LEN>0            收满 LEN 个
HEAD1 ─────> HEAD2 ─────────> LEN ──────────> DATA ──────────────> CHK
  ^          │ ↺ AA             │ LEN=0                               │
  │          │ 其它             └───────────────────────────────────> │
  └──────────┴──────────────────── 校验完成（无论对错）<──────────────┘
```

### 代码

```c
enum { ST_HEAD1, ST_HEAD2, ST_LEN, ST_DATA, ST_CHK };

int** parseFrames(const uint8_t* buf, size_t len, int* returnSize, int** returnColumnSizes) {
    int maxFrames = (int)(len / 4) + 1;
    int** frames = (int**)malloc(sizeof(int*) * maxFrames);
    int* sizes = (int*)malloc(sizeof(int) * maxFrames);
    int cnt = 0;

    int state = ST_HEAD1;      // 当前状态
    uint8_t data[256];         // 正在接收的数据段（LEN 最大 255）
    int need = 0, got = 0;     // 应收字节数、已收字节数
    uint8_t sum = 0;           // 一边收一边累加校验和

    for (size_t i = 0; i < len; i++) {        // 模拟"每收到一个字节"
        uint8_t b = buf[i];
        switch (state) {
        case ST_HEAD1:
            if (b == 0xAA) state = ST_HEAD2;
            break;
        case ST_HEAD2:
            if (b == 0x55) state = ST_LEN;
            else if (b != 0xAA) state = ST_HEAD1;   // 是 AA 就留在本状态
            break;
        case ST_LEN:
            need = b;
            got = 0;
            sum = b;                                // 校验和从 LEN 开始累加
            state = (need > 0) ? ST_DATA : ST_CHK;  // LEN=0 没有数据段
            break;
        case ST_DATA:
            data[got++] = b;
            sum = (uint8_t)(sum + b);
            if (got == need) state = ST_CHK;
            break;
        case ST_CHK:
            if (b == sum) {                         // 校验正确：保存这一帧
                int* f = (int*)malloc(sizeof(int) * (need + 1));
                for (int k = 0; k < need; k++) f[k] = data[k];
                frames[cnt] = f;
                sizes[cnt] = need;
                cnt++;
            }
            state = ST_HEAD1;                       // 无论对错都重新找帧头
            break;
        }
    }
    *returnSize = cnt;
    *returnColumnSizes = sizes;
    return frames;
}
```

### 🔌 嵌入式实战：放进串口中断

真实项目里把局部变量换成一个结构体，函数每次只吃一个字节：

```c
typedef struct {
    uint8_t state, need, got, sum;
    uint8_t data[255];
} FrameParser;

// 每收到一个字节调用一次（可以在 UART 中断里，也可以在主循环从环形缓冲区取出后调用）
// 返回 true 表示刚刚收到了一帧完整有效的数据，内容在 p->data[0 .. p->need-1]
bool parser_feed(FrameParser* p, uint8_t b);
```

工程上还有两点要加：

- **超时复位**：如果一帧收到一半就断了（比如对方掉电），状态机会卡在 DATA 状态把下一帧的帧头当数据吃掉。通常加一个"字节间超时"（例如 20ms 没收到新字节就回到 HEAD1）。
- **LEN 上限检查**：如果缓冲区只有 64 字节，收到 `LEN > 64` 应该直接判定为错误帧，否则会越界写内存。

### 复杂度分析

- **时间 O(len)**，**空间 O(1)**（不算结果）——状态机只需要几个字节的状态。

---

## ⚠️ 第五步：小白常见错误

1. **在 HEAD2 收到 AA 时回到 HEAD1** → 示例 3 的 `AA AA 55` 会被漏掉。
2. **LEN = 0 时进入 DATA 状态** → 会把校验字节当成数据收进去，后面全乱。
3. **校验和用 `int` 累加后直接和字节比较** → 和超过 255 时永远对不上，要 `& 0xFF` 或用 `uint8_t`。
4. **数据段里遇到 AA 就重新同步** → 数据里本来就可能有 AA，按 LEN 收满才对。
5. **`returnColumnSizes = sizes;`（少了 `*`）** → 只修改了函数内的局部指针，调用者拿不到列长度，直接崩溃。
6. **`data[256]` 写成 `data[255]` 后又不检查 LEN** → 本题 LEN 最大 255 正好够用，但 data 数组一定要按协议上限开。

---

## 📊 第六步：方法对比

| 方法 | 时间 | 状态空间 | 能否边收边解析 | 适用 |
|---|---|---|---|---|
| 下标扫描 | O(n) | 需要整帧数据都在内存里 | 不方便 | 离线分析、上位机解析日志 |
| 逐字节状态机 | O(n) | 几个字节 | 能 | 单片机串口接收（标准写法） |

---

## 🔗 举一反三

- **9046. 环形缓冲区**：中断把字节放进环形缓冲区，主循环取出来喂给本题的状态机。
- **9049. CRC-16/MODBUS**：把本题的"累加和"换成 CRC，检错能力会强很多。
- **9055. 表驱动状态机**：试着把本题的 `switch` 状态机改写成"状态 × 字节类别"的转移表。
- **思考题**：如果协议改成"帧尾 0x0D 0x0A 结束、没有 LEN 字段"，数据里又可能出现 0x0D 0x0A，该怎么办？（提示：字节填充 / 转义，如 SLIP、HDLC。）
