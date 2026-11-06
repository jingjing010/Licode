# 9052. 滑动平均滤波 —— 小白详细题解

> ADC 读数乱跳？第一反应就是"取最近几次的平均"。滑动平均是嵌入式里用得最多的软件滤波，这道题教你写出 O(1) 的版本，并顺带掌握整数四舍五入这个小技巧。

---

## 📖 第一步：先读懂题目

想象一个只能装 N 个球的**透明管子**：每次从右边塞进一个新球（新采样值），满了以后最左边的旧球就被挤出去。每塞一次，输出管子里所有球的平均值。

示例 1（窗口 3）：

| update | 窗口内容 | 和 | 个数 | 平均 | 四舍五入 |
|---|---|---|---|---|---|
| 10 | [10] | 10 | 1 | 10 | 10 |
| 11 | [10, 11] | 21 | 2 | 10.5 | **11** |
| 30 | [10, 11, 30] | 51 | 3 | 17 | 17 |
| 40 | [11, 30, 40] | 81 | 3 | 27 | 27 |
| 45 | [30, 40, 45] | 115 | 3 | 38.33 | 38 |

**容易忽略的细节：**

1. 窗口还没装满时，除以的是**实际个数**，不是窗口大小（第 2 次 update 除以 2，不是除以 3）。
2. 要**四舍五入**，C 的整数除法是直接截断的（`21 / 2 = 10`）。
3. `reset` 之后要从头开始算，包括"个数"也要清零。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 整数四舍五入

对非负整数 `a`、正整数 `b`，`a / b` 四舍五入的写法：

```c
(a + b / 2) / b
```

原理：先加上"半个 b"，原本小数部分 ≥ 0.5 的就会跨过下一个整数。例如 `21 / 2`：`(21 + 1) / 2 = 11`；`115 / 3`：`(115 + 1) / 3 = 38`。

> b 为奇数时 `b / 2` 向下取整，例如 b = 3 时加的是 1 而不是 1.5，但对整数 a 来说，`a/3` 的小数部分只可能是 0、0.33、0.67，加 1 后的判断结果完全一样。

单片机上很多没有浮点运算单元（FPU），所以嵌入式代码**尽量用整数运算**代替 `round()`。

### 2. 累加和的类型

窗口最大 1000，每个值最大 65535，和最大约 `6.5 × 10^7`，超出 `uint16_t`，但在 `uint32_t`（最大约 `4.29 × 10^9`）范围内。**先估算最大值再选类型**是嵌入式的好习惯。

### 3. `uint16_t` 返回值

ADC 一般是 12 位（0 ~ 4095）或 16 位，所以采样值和输出都用 `uint16_t`。平均值不会超过最大的采样值，返回 `uint16_t` 不会溢出。

---

## 💡 第三步：思路一 —— 每次把窗口重新加一遍

### 思路

用环形数组存最近 N 个值（满了就覆盖最旧的，和 9047 一样），每次 update 后把数组里现有的 `count` 个值全部加起来再除。

### 代码

```c
typedef struct {
    uint16_t* buf;     // 环形数组
    int size;          // 窗口大小
    int pos;           // 下一个写入位置
    int count;         // 当前有几个值
} MovingAvg;

MovingAvg* movingAvgCreate(int windowSize) {
    MovingAvg* obj = (MovingAvg*)malloc(sizeof(MovingAvg));
    obj->buf = (uint16_t*)malloc(sizeof(uint16_t) * windowSize);
    obj->size = windowSize;
    obj->pos = 0;
    obj->count = 0;
    return obj;
}

uint16_t movingAvgUpdate(MovingAvg* obj, uint16_t sample) {
    obj->buf[obj->pos] = sample;                    // 写入（满了就覆盖最旧的）
    obj->pos = (obj->pos + 1) % obj->size;
    if (obj->count < obj->size) obj->count++;

    uint32_t sum = 0;
    for (int i = 0; i < obj->count; i++) {          // 窗口里的值全部加一遍
        sum += obj->buf[i];
    }
    return (uint16_t)((sum + obj->count / 2) / obj->count);   // 四舍五入
}

void movingAvgReset(MovingAvg* obj) {
    obj->pos = 0;
    obj->count = 0;
}

void movingAvgFree(MovingAvg* obj) {
    free(obj->buf);
    free(obj);
}
```

> 💬 为什么直接加 `buf[0..count-1]` 是对的？没满时数据正好存在前 count 个位置；满了以后 count = size，整个数组都是窗口内容。平均值和顺序无关，不需要从最旧的开始加。

### 复杂度分析

- `update`：**O(windowSize)**。最坏 2×10⁴ × 1000 = 2×10⁷ 次加法，能过，但在 MCU 的 1kHz 采样中断里每次加 1000 个数就太浪费了。

---

## 🚀 第四步：思路二 —— 维护累加和，O(1) 更新

### 为什么能优化？

相邻两次的窗口只差两个数：**进来一个新值、出去一个旧值**。所以：

```
新的和 = 旧的和 + 新值 - 被挤出去的旧值
```

被挤出去的旧值在哪？满了以后，`buf[pos]` 正好是最旧的那个（马上要被覆盖），覆盖之前先把它从 sum 里减掉。

| update（窗口 3） | 写入前 buf[pos] | sum 变化 | sum |
|---|---|---|---|
| 10 | 未满 | +10 | 10 |
| 11 | 未满 | +11 | 21 |
| 30 | 未满 | +30 | 51 |
| 40 | 10（最旧） | -10 +40 | 81 |
| 45 | 11 | -11 +45 | 115 |

### 代码

```c
typedef struct {
    uint16_t* buf;
    int size;
    int pos;           // 下一个写入位置；满了时也是最旧值的位置
    int count;
    uint32_t sum;      // 窗口内所有值的和
} MovingAvg;

MovingAvg* movingAvgCreate(int windowSize) {
    MovingAvg* obj = (MovingAvg*)malloc(sizeof(MovingAvg));
    obj->buf = (uint16_t*)malloc(sizeof(uint16_t) * windowSize);
    obj->size = windowSize;
    obj->pos = 0;
    obj->count = 0;
    obj->sum = 0;
    return obj;
}

uint16_t movingAvgUpdate(MovingAvg* obj, uint16_t sample) {
    if (obj->count == obj->size) {
        obj->sum -= obj->buf[obj->pos];             // 满了：先减掉即将被覆盖的最旧值
    } else {
        obj->count++;                               // 没满：个数 +1
    }
    obj->buf[obj->pos] = sample;
    obj->sum += sample;                             // 加上新值
    obj->pos = (obj->pos + 1) % obj->size;
    return (uint16_t)((obj->sum + (uint32_t)obj->count / 2) / (uint32_t)obj->count);
}

void movingAvgReset(MovingAvg* obj) {
    obj->pos = 0;
    obj->count = 0;
    obj->sum = 0;                                   // 别忘了 sum 也要清零
}

void movingAvgFree(MovingAvg* obj) {
    free(obj->buf);
    free(obj);
}
```

### 复杂度分析

- `update`：**O(1)**，空间 O(windowSize)。

### 🔌 嵌入式实战：窗口取 2 的幂，用移位代替除法

很多 MCU（如 Cortex-M0）没有硬件除法指令，除法要几十个周期。把窗口固定为 2 的幂（如 16），且只在窗口满了之后使用结果，就能用移位：

```c
#define N_SHIFT 4                          // 窗口 16 = 2^4
static uint16_t win[1 << N_SHIFT];
static uint32_t sum;
static uint8_t  idx;

uint16_t adc_filter(uint16_t x) {
    sum += x - win[idx];                   // 进一个、出一个（无符号回绕结果依然正确）
    win[idx] = x;
    idx = (idx + 1) & ((1 << N_SHIFT) - 1);
    return (uint16_t)((sum + (1u << (N_SHIFT - 1))) >> N_SHIFT);   // 四舍五入除以 16
}
```

如果连数组的 RAM 都不想花，还可以用**一阶低通（指数滑动平均）**：`y += (x - y) >> k`，只需要一个变量。

---

## ⚠️ 第五步：小白常见错误

1. **没满时除以 windowSize** → 示例 1 第一次会输出 `10/3 = 3`。
2. **直接用 `sum / count`** → 截断而不是四舍五入，示例 1 第 2 次输出 10。
3. **sum 用 `uint16_t`** → 几个大值相加就溢出。
4. **先覆盖 `buf[pos]` 再减** → 减掉的是新值而不是旧值，sum 越算越错。
5. **reset 只清 count 不清 sum** → reset 后第一次输出就带着历史数据。
6. **用 `round((double)sum / count)`** → 结果虽然对，但在没有 FPU 的 MCU 上浮点运算要靠软件模拟，又慢又占 Flash。

---

## 📊 第六步：方法对比

| 方法 | update 时间 | 空间 | 说明 |
|---|---|---|---|
| 每次重新求和 | O(N) | O(N) | 最直观 |
| 维护累加和 | O(1) | O(N) | 标准写法 |
| 2 的幂窗口 + 移位 | O(1)，无除法 | O(N) | 适合没有除法器的 MCU |
| 一阶低通 `y += (x-y)>>k` | O(1) | O(1) | 不是严格的滑动平均，但最省资源 |

---

## 🔗 举一反三

- **9053. 中值滤波**：滑动平均对"毛刺"（偶尔一个特别大的值）很敏感，中值滤波可以直接把毛刺剔除。
- **9047. 覆盖式日志缓冲区**：本题的环形数组就是它。
- **力扣 346. 数据流中的移动平均值**：同一道题的通用版本。
- **思考题**：如果 sum 用 `uint32_t`、窗口大小 100000、采样值都是 65535，会溢出吗？应该怎么办？
