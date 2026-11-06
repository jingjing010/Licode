# 9052. 滑动平均滤波 —— 小白详细题解

> ADC 读数跳来跳去怎么办？先上一个滑动平均。这是嵌入式里最常用的软件滤波器，面试常问"怎么做到 O(1) 更新"、"整数除法怎么四舍五入"、"和一阶低通滤波有什么区别"。

---

## 📖 第一步：先读懂题目

想象一个只能装 N 个数的"窗口"沿着采样序列往前滑，每次输出窗口里所有数的平均值：

示例 1（N = 3）：

| 第几次 update | 新值 | 窗口内容 | 和 | 个数 | 平均 | 四舍五入 |
|---|---|---|---|---|---|---|
| 1 | 10 | [10] | 10 | 1 | 10 | 10 |
| 2 | 11 | [10, 11] | 21 | 2 | 10.5 | **11** |
| 3 | 30 | [10, 11, 30] | 51 | 3 | 17 | 17 |
| 4 | 40 | [11, 30, 40] | 81 | 3 | 27 | 27 |
| 5 | 45 | [30, 40, 45] | 115 | 3 | 38.33 | 38 |

**容易忽略的细节：**

1. 窗口**没填满之前**，除数是"已有的个数"，不是 N（第 2 次是除以 2）。
2. 要**四舍五入**，直接 `sum / cnt` 是向下取整，10.5 会变成 10。
3. `reset` 后要从头开始，之前的数据一个都不能算进去。
4. 和最大是 `1000 × 65535 ≈ 6.5 × 10^7`，超过了 `uint16_t`，要用 `uint32_t`。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 整数除法的四舍五入

C 的整数除法 `a / b`（都非负时）是**向下取整**。四舍五入的技巧是先加上除数的一半：

```c
avg = (sum + cnt / 2) / cnt;
```

例：`sum = 21, cnt = 2` → `(21 + 1) / 2 = 11` ✔；`sum = 115, cnt = 3` → `(115 + 1) / 3 = 38` ✔。

### 2. 整数类型宽度

| 类型 | 范围 | 用途 |
|---|---|---|
| `uint16_t` | 0 ~ 65535 | 单个采样值（12 位 ADC 只用到 0~4095） |
| `uint32_t` | 0 ~ 约 42.9 亿 | 累加和 |

如果把 sum 定义成 `uint16_t`，加几个大数就溢出回绕，平均值会突然变得很小。

### 3. 为什么嵌入式里不用 `float`？

很多 MCU（如 Cortex-M0/M3）**没有浮点运算单元**，一次浮点除法要几十上百个时钟周期。能用整数解决的滤波器就用整数。

---

## 💡 第三步：思路一 —— 保存窗口，每次重新求和

### 思路

用一个环形数组保存最近 N 个值（满了就覆盖最旧的，和 9047 一样），每次 `update` 时把窗口里的值全部加一遍再除。

### 代码

```c
typedef struct {
    uint16_t* buf;   // 环形数组，保存最近的采样
    int size;        // 窗口大小 N
    int pos;         // 下一个写入位置
    int cnt;         // 当前有效个数（<= size）
} MovingAvg;

MovingAvg* movingAvgCreate(int windowSize) {
    MovingAvg* obj = (MovingAvg*)malloc(sizeof(MovingAvg));
    obj->buf = (uint16_t*)malloc(sizeof(uint16_t) * windowSize);
    obj->size = windowSize;
    obj->pos = 0;
    obj->cnt = 0;
    return obj;
}

uint16_t movingAvgUpdate(MovingAvg* obj, uint16_t sample) {
    obj->buf[obj->pos] = sample;                    // 写入（满了就覆盖最旧的）
    obj->pos = (obj->pos + 1) % obj->size;
    if (obj->cnt < obj->size) obj->cnt++;

    uint32_t sum = 0;
    for (int i = 0; i < obj->cnt; i++) {            // 窗口没满时，有效数据在 buf[0..cnt-1]
        sum += obj->buf[i];                         // 满了以后整个数组都是有效数据
    }
    return (uint16_t)((sum + obj->cnt / 2) / obj->cnt);   // 四舍五入
}

void movingAvgReset(MovingAvg* obj) {
    obj->pos = 0;
    obj->cnt = 0;
}

void movingAvgFree(MovingAvg* obj) {
    free(obj->buf);
    free(obj);
}
```

> 💬 为什么可以直接加 `buf[0..cnt-1]`？窗口没满时，数据是从下标 0 开始依次写的；满了以后整个数组都是有效数据。平均值和顺序无关，所以不需要按从旧到新的顺序加。

### 复杂度分析

- `update`：**O(N)**；空间 O(N)。

---

## 🚀 第四步：思路二 —— 维护累加和，O(1) 更新

### 为什么能优化？

窗口每滑动一步，只有**一个值进来、一个值出去**，中间的值都没变。所以不必重新求和：

```
新和 = 旧和 + 新进来的值 - 被挤出去的值
```

被挤出去的值是谁？窗口满时，`buf[pos]` 正好是**最旧的那个**（即将被覆盖），先把它从 sum 里减掉再覆盖即可。

| update | 被挤出 | sum 变化 | sum |
|---|---|---|---|
| 10 | - | +10 | 10 |
| 11 | - | +11 | 21 |
| 30 | - | +30 | 51 |
| 40 | 10 | +40 −10 | 81 |
| 45 | 11 | +45 −11 | 115 |

### 代码

```c
typedef struct {
    uint16_t* buf;
    int size;
    int pos;         // 下一个写入位置；窗口满时它也是最旧数据的位置
    int cnt;
    uint32_t sum;    // 窗口内所有值的和
} MovingAvg;

MovingAvg* movingAvgCreate(int windowSize) {
    MovingAvg* obj = (MovingAvg*)malloc(sizeof(MovingAvg));
    obj->buf = (uint16_t*)malloc(sizeof(uint16_t) * windowSize);
    obj->size = windowSize;
    obj->pos = 0;
    obj->cnt = 0;
    obj->sum = 0;
    return obj;
}

uint16_t movingAvgUpdate(MovingAvg* obj, uint16_t sample) {
    if (obj->cnt == obj->size) {
        obj->sum -= obj->buf[obj->pos];    // 窗口满：减去即将被覆盖的最旧值
    } else {
        obj->cnt++;                        // 窗口未满：个数 +1
    }
    obj->buf[obj->pos] = sample;
    obj->sum += sample;                    // 加上新值
    obj->pos = (obj->pos + 1) % obj->size;
    return (uint16_t)((obj->sum + (uint32_t)obj->cnt / 2) / (uint32_t)obj->cnt);
}

void movingAvgReset(MovingAvg* obj) {
    obj->pos = 0;
    obj->cnt = 0;
    obj->sum = 0;                          // 别忘了清零累加和
}

void movingAvgFree(MovingAvg* obj) {
    free(obj->buf);
    free(obj);
}
```

### 🔌 嵌入式实战

- **窗口取 2 的幂**（8、16、32）：窗口填满后除法可以换成右移 `(sum + N/2) >> 3`，在没有硬件除法器的 MCU 上快很多。
- **更省内存的一阶低通（指数平均 EMA）**：不需要保存窗口，只要一个变量：

  ```c
  // alpha = 1/8：新值占 1/8 权重。用整数实现时通常让 y 多保留几位小数
  static uint32_t y_q3;                 // y × 8
  uint16_t ema_update(uint16_t x) {
      y_q3 += x - (y_q3 >> 3);          // y = y + (x - y) / 8
      return (uint16_t)(y_q3 >> 3);
  }
  ```

  代价是"老数据永远不会完全消失"，阶跃响应是指数曲线而不是直线。
- 滑动平均对**偶发的尖峰干扰**（如继电器动作时的毛刺）效果一般，一个尖峰会影响后面 N 个输出。这种场景用中值滤波更好（见 9053）。

### 复杂度分析

- `update`：**O(1)**；空间 O(N)。

---

## ⚠️ 第五步：小白常见错误

1. **窗口没满时除以 N** → 示例 1 第一次输出会是 10/3 = 3。
2. **直接 `sum / cnt`** → 向下取整，示例 1 第 2 次得到 10 而不是 11。
3. **`sum` 用 `uint16_t`** → 窗口里几个大值相加就溢出。
4. **先覆盖再减旧值** → 减掉的是刚写进去的新值，sum 越算越错。
5. **`reset` 只清 cnt 不清 sum**（思路二） → reset 后第一次输出就带着旧数据。

---

## 📊 第六步：方法对比

| 方法 | update 时间 | 内存 | 说明 |
|---|---|---|---|
| 每次重新求和 | O(N) | N 个采样 | 最直观 |
| 维护累加和 | O(1) | N 个采样 + 1 个和 | 实际项目标准写法 |
| 一阶低通 EMA | O(1) | 1 个变量 | 最省内存，但不是严格的"最近 N 个" |

---

## 🔗 举一反三

- **9047. 覆盖式日志缓冲区**：本题保存窗口的就是一个覆盖式环形缓冲区。
- **9053. 中值滤波**：对付尖峰干扰的滤波器。
- **力扣 346. 数据流中的移动平均值**：同一题的通用版本。
- **思考题**：如果长期运行的浮点版本 `sum += new - old`，会不会因为舍入误差越积越大？整数版本有没有这个问题？
