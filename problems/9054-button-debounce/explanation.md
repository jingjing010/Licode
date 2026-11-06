# 9054. 按键消抖状态机 —— 小白详细题解

> 新手做的第一个单片机项目往往是"按一下灯亮、再按一下灯灭"，然后发现：按一下，灯闪了好几下。罪魁祸首就是**按键抖动**。这道题用最典型的"计数消抖"解决它，并且把它写成一个规范的状态机。

---

## 📖 第一步：先读懂题目

示波器上看，按下一个按键时电平大概是这样的：

```
松开 0 ________|‾|_|‾‾|_|‾‾‾‾‾‾‾‾‾‾‾‾‾‾  按下 1
               ←抖动几毫秒→ ←稳定→
```

消抖的规则一句话：**新电平要连续出现 stableCount 次才算数**。

示例 1（stableCount = 3）逐个采样：

| 下标 | 采样 | 稳定状态 | 计数 cnt | 说明 |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 和稳定状态相同 |
| 1 | 1 | 0 | 1 | 不同，开始计数 |
| 2 | 0 | 0 | **0** | 又相同了 → 抖动，清零 |
| 3 | 1 | 0 | 1 | |
| 4 | 1 | 0 | 2 | |
| 5 | 1 | 0→**1** | 3 → 清零 | 达到 3 次，**事件 [5,1]** |
| 6 | 1 | 1 | 0 | 相同 |
| 7 | 0 | 1 | 1 | |
| 8 | 1 | 1 | **0** | 抖动，清零 |
| 9 | 0 | 1 | 1 | |
| 10 | 0 | 1 | 2 | |
| 11 | 0 | 1→**0** | 3 → 清零 | **事件 [11,0]** |

**容易忽略的细节：**

1. 初始稳定状态是 0，所以一开始就是 0 的采样不会产生事件。
2. 事件的下标是**第 stableCount 个**采样的下标，不是变化开始的下标。
3. `stableCount = 1` 时不消抖，每次电平变化都立即产生事件。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 返回 n 行 2 列的二维数组

```c
res[n] = (int*)malloc(sizeof(int) * 2);   // 每个事件一行，2 个元素
res[n][0] = (int)i;                        // 下标
res[n][1] = stable;                        // 新状态
cols[n] = 2;                               // 这一行有 2 列
```

事件数最多和采样数一样多（stableCount = 1 且电平每次都变），所以按 `len + 1` 申请足够。

### 2. `enum` + `switch` 状态机

```c
typedef enum { RELEASED, PRESS_CHECK, PRESSED, RELEASE_CHECK } KeyState;
```

每个 `case` 处理"在这个状态下收到一个采样该怎么办"。**每个 case 结尾一定要写 `break;`**，否则会"贯穿"到下一个 case 继续执行。

### 3. `++cnt >= stableCount`

前置 `++` 先加 1 再比较，等价于：

```c
cnt = cnt + 1;
if (cnt >= stableCount) { /* ... */ }
```

---

## 💡 第三步：思路一 —— 稳定状态 + 计数器

### 代码

```c
int** debounce(const uint8_t* samples, size_t len, uint16_t stableCount,
               int* returnSize, int** returnColumnSizes) {
    int** res = (int**)malloc(sizeof(int*) * (len + 1));
    int* cols = (int*)malloc(sizeof(int) * (len + 1));
    int n = 0;

    uint8_t stable = 0;       // 当前认可的稳定状态，初始为松开
    uint16_t cnt = 0;         // 连续"与稳定状态不同"的采样个数

    for (size_t i = 0; i < len; i++) {
        if (samples[i] == stable) {          // 和稳定状态一样：之前的变化是抖动
            cnt = 0;
            continue;
        }
        cnt++;                               // 不一样：计数
        if (cnt >= stableCount) {            // 连续够了：确认状态改变
            stable = samples[i];
            cnt = 0;
            res[n] = (int*)malloc(sizeof(int) * 2);
            res[n][0] = (int)i;
            res[n][1] = stable;
            cols[n] = 2;
            n++;
        }
    }

    *returnSize = n;
    *returnColumnSizes = cols;
    return res;
}
```

### 复杂度分析

- 时间 **O(len)**，空间 O(事件数)。

---

## 🚀 第四步：思路二 —— 四状态的 enum + switch 状态机

### 为什么要这样写？

思路一已经是最优复杂度了。但真实项目里按键往往还要支持**长按、双击、连发**等功能，这时把过程拆成明确的状态更好扩展：

| 状态 | 含义 | 采样 = 1 | 采样 = 0 |
|---|---|---|---|
| RELEASED | 稳定松开 | → PRESS_CHECK，cnt = 1（够数则直接确认） | 保持 |
| PRESS_CHECK | 疑似按下，确认中 | cnt++，够数 → PRESSED，产生事件 | 抖动 → RELEASED |
| PRESSED | 稳定按下 | 保持 | → RELEASE_CHECK，cnt = 1（够数则直接确认） |
| RELEASE_CHECK | 疑似松开，确认中 | 抖动 → PRESSED | cnt++，够数 → RELEASED，产生事件 |

要加"长按 2 秒"，只需在 PRESSED 状态里再计时就行，其他状态不用动。

### 代码

```c
typedef enum { RELEASED, PRESS_CHECK, PRESSED, RELEASE_CHECK } KeyState;

static void addEvent(int** res, int* cols, int* n, int idx, int state) {
    res[*n] = (int*)malloc(sizeof(int) * 2);
    res[*n][0] = idx;
    res[*n][1] = state;
    cols[*n] = 2;
    (*n)++;
}

int** debounce(const uint8_t* samples, size_t len, uint16_t stableCount,
               int* returnSize, int** returnColumnSizes) {
    int** res = (int**)malloc(sizeof(int*) * (len + 1));
    int* cols = (int*)malloc(sizeof(int) * (len + 1));
    int n = 0;
    KeyState st = RELEASED;
    uint16_t cnt = 0;

    for (size_t i = 0; i < len; i++) {
        uint8_t s = samples[i];
        switch (st) {
        case RELEASED:
            if (s == 1) { st = PRESS_CHECK; cnt = 0; }   // 疑似按下，下面接着计数
            else break;
            /* fall through：本次采样也要计入 */
        case PRESS_CHECK:
            if (s == 0) { st = RELEASED; break; }        // 抖动，回到松开
            if (++cnt >= stableCount) {                  // 确认按下
                st = PRESSED;
                addEvent(res, cols, &n, (int)i, 1);
            }
            break;
        case PRESSED:
            if (s == 0) { st = RELEASE_CHECK; cnt = 0; } // 疑似松开
            else break;
            /* fall through */
        case RELEASE_CHECK:
            if (s == 1) { st = PRESSED; break; }         // 抖动，回到按下
            if (++cnt >= stableCount) {                  // 确认松开
                st = RELEASED;
                addEvent(res, cols, &n, (int)i, 0);
            }
            break;
        }
    }

    *returnSize = n;
    *returnColumnSizes = cols;
    return res;
}
```

> 💬 这里**故意**利用了 switch 的"贯穿"（fall through）：从 RELEASED 进入 PRESS_CHECK 时，当前这个采样也要算作第 1 次。故意贯穿时一定要写注释说明，否则别人会以为你忘了写 `break`。

### 复杂度分析

- 时间 **O(len)**，空间 O(事件数)。

### 🔌 嵌入式实战：多按键一起消抖

在 1ms 定时器中断里调用，每个按键一个结构体：

```c
typedef struct {
    uint8_t  stable;     // 稳定状态
    uint8_t  cnt;        // 计数
} Key;

static Key keys[4];

void key_scan_1ms(void) {                         // 在 SysTick 中断里调用
    for (int k = 0; k < 4; k++) {
        uint8_t raw = !HAL_GPIO_ReadPin(KEY_PORT, KEY_PIN[k]);   // 低电平有效，取反
        if (raw == keys[k].stable) { keys[k].cnt = 0; continue; }
        if (++keys[k].cnt >= 20) {                // 20ms 消抖
            keys[k].stable = raw;
            keys[k].cnt = 0;
            event_post(k, raw);                   // 发事件给主循环处理
        }
    }
}
```

另一个经典技巧是**移位寄存器消抖**：`hist = (hist << 1) | raw;`，当 `hist == 0xFF`（连续 8 次为 1）认为按下、`hist == 0x00` 认为松开，一个字节就搞定。

---

## ⚠️ 第五步：小白常见错误

1. **抖动时计数不清零** → 抖动中的 1 断断续续累积起来也会触发按下，相当于没消抖。
2. **用 `delay_ms(20)` 消抖** → 读到变化后延时 20ms 再读一次：简单但会卡死 CPU 20ms，其他任务全停，真实项目里不推荐。
3. **翻转后没清零 cnt** → 下一次变化少数几个采样就会触发。
4. **事件下标记成变化开始的位置** → 题目要求记录确认时刻（第 stableCount 个采样）。
5. **switch 漏写 break** → 状态被"一口气"推进好几步。思路二中故意的贯穿要写注释。

---

## 📊 第六步：方法对比

| 方法 | 时间 | 可扩展性 | 说明 |
|---|---|---|---|
| 延时再读 | 阻塞 | 差 | 入门写法，会卡住 CPU |
| 稳定状态 + 计数器 | O(len) | 一般 | 代码最短 |
| 四状态状态机 | O(len) | 好 | 方便扩展长按、双击 |
| 移位寄存器 | O(len) | 一般 | 消抖时间固定为 8 个采样周期 |

---

## 🔗 举一反三

- **9055. 表驱动状态机**：试着把本题的四状态状态机改写成"状态 × 输入"的转移表。
- **9056. 软件定时器**：按键扫描通常放在 1ms 的周期定时器里执行。
- **思考题**：在思路二的基础上增加"长按"事件：按下状态保持 1000 个采样后产生事件 `[下标, 2]`，状态机要怎么改？
