# 9053. 中值滤波 —— 小白详细题解

> "滑动平均和中值滤波有什么区别？各适合什么场景？"——这是嵌入式面试的高频问题。一句话：**平均值会被毛刺带偏，中位数不会**。

---

## 📖 第一步：先读懂题目

对每个位置 i，拿出它左右各 `k/2` 个邻居（加上自己共 k 个），排序后取**正中间**那个作为输出。

示例 1（k = 3，k/2 = 1），注意两端的补齐：

| i | 窗口下标 | 窗口值（越界的用端点补齐） | 排序后 | 中位数 |
|---|---|---|---|---|
| 0 | -1, 0, 1 | **10**, 10, 12 | 10 10 12 | 10 |
| 1 | 0, 1, 2 | 10, 12, 250 | 10 **12** 250 | 12 |
| 2 | 1, 2, 3 | 12, 250, 11 | 11 **12** 250 | 12 |
| 3 | 2, 3, 4 | 250, 11, 13 | 11 **13** 250 | 13 |
| 4 | 3, 4, 5 | 11, 13, **13** | 11 13 13 | 13 |

毛刺 250 一次都没被输出。如果用 3 点滑动平均，i = 2 的输出是 `(12+250+11)/3 = 91`，被严重带偏。

**容易忽略的细节：**

1. 补齐用的是**端点的值**（`signal[0]` 或 `signal[len-1]`），不是 0。
2. k 可能比 len 还大（如 len = 1，k = 51），补齐规则照样适用。
3. 输出写进调用者给的 `out` 数组，函数本身返回 `void`。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. `int16_t`

16 位有符号整数，范围 `-32768 ~ 32767`。ADC 差分输入、温度这类可能为负的信号常用它。

### 2. 有符号和无符号混用的坑

`len` 和 `k` 是 `size_t`（无符号）。计算 `i - k/2` 时如果全用 `size_t`，`0 - 1` 不会得到 -1，而是一个巨大的正数（`2^64 - 1`）。所以计算下标时先转成有符号的 `long`：

```c
long idx = (long)i - (long)(k / 2);   // 可以是负数
```

### 3. 下标钳位（clamp）

```c
if (idx < 0) idx = 0;
if (idx > (long)len - 1) idx = (long)len - 1;
```

### 4. 插入排序

k 最大 51，用插入排序最简单：把新元素从后往前和已排好的元素比较，比它大的都往后挪一格，然后放进空位。对小数组，它比 `qsort` 还快（没有函数调用开销）。

---

## 💡 第三步：思路一 —— 每个位置单独排序

### 代码

```c
static int16_t clampAt(const int16_t* signal, size_t len, long idx) {
    if (idx < 0) idx = 0;                               // 左边越界：取第一个
    if (idx > (long)len - 1) idx = (long)len - 1;       // 右边越界：取最后一个
    return signal[idx];
}

void medianFilter(const int16_t* signal, size_t len, size_t k, int16_t* out) {
    long h = (long)(k / 2);                             // 半窗宽
    int16_t* win = (int16_t*)malloc(sizeof(int16_t) * k);
    for (size_t i = 0; i < len; i++) {
        int n = 0;
        for (long j = (long)i - h; j <= (long)i + h; j++) {
            int16_t v = clampAt(signal, len, j);
            int p = n++;                                // 插入排序：从末尾往前找位置
            while (p > 0 && win[p - 1] > v) {
                win[p] = win[p - 1];                    // 比 v 大的往后挪
                p--;
            }
            win[p] = v;
        }
        out[i] = win[h];                                // 正中间就是中位数
    }
    free(win);
}
```

### 复杂度分析

- 每个位置插入排序 O(k²)，总共 **O(len × k²)** ≈ 10⁴ × 2601 ≈ 2.6×10⁷，可以通过。
- 空间 O(k)。

---

## 🚀 第四步：思路二 —— 维护有序窗口，每步 O(k)

### 为什么能优化？

窗口从 i 移到 i+1 时，只是**移出**最左边的 `signal[i-h]`、**移进** `signal[i+h+1]`，其余 k-1 个值不变。如果一直保持窗口有序，就不需要每次重新排序：

1. 在有序数组里找到要移出的值，它的位置变成一个"空位"。
2. 把新值放进空位，再像插入排序一样往左或往右挪到正确位置。

示例 1 从 i=1 到 i=2：

| 步骤 | 有序窗口 |
|---|---|
| i=1 的窗口 | [10, 12, 250] |
| 移出 10，留下空位 | [_, 12, 250] |
| 放入 11：比右边 12 小，停在原位 | [11, 12, 250] → 中位数 12 |

### 代码

```c
static int16_t clampAt(const int16_t* signal, size_t len, long idx) {
    if (idx < 0) idx = 0;
    if (idx > (long)len - 1) idx = (long)len - 1;
    return signal[idx];
}

void medianFilter(const int16_t* signal, size_t len, size_t k, int16_t* out) {
    long h = (long)(k / 2);
    int16_t* win = (int16_t*)malloc(sizeof(int16_t) * k);

    int n = 0;
    for (long j = -h; j <= h; j++) {                     // 1. 建立第一个窗口（i = 0）并排好序
        int16_t v = clampAt(signal, len, j);
        int p = n++;
        while (p > 0 && win[p - 1] > v) {
            win[p] = win[p - 1];
            p--;
        }
        win[p] = v;
    }

    for (size_t i = 0; i < len; i++) {
        out[i] = win[h];                                 // 2. 输出中位数
        if (i + 1 == len) break;

        int16_t oldV = clampAt(signal, len, (long)i - h);      // 将要移出窗口的值
        int16_t newV = clampAt(signal, len, (long)i + h + 1);  // 将要移进窗口的值

        int p = 0;
        while (win[p] != oldV) p++;                      // 3. 找到 oldV，位置 p 当作空位

        while (p > 0 && win[p - 1] > newV) {             // 4a. newV 太小：左边的往右挪
            win[p] = win[p - 1];
            p--;
        }
        while (p + 1 < (int)k && win[p + 1] < newV) {    // 4b. newV 太大：右边的往左挪
            win[p] = win[p + 1];
            p++;
        }
        win[p] = newV;                                   // 5. 填入空位
    }
    free(win);
}
```

### 复杂度分析

- 每步找位置 O(k) + 挪动 O(k)，总共 **O(len × k)**，比思路一快约 k 倍。
- 空间 O(k)。

### 🔌 嵌入式实战：实时滤波怎么写

上面是"离线"处理（整段数据都已采集好，可以看到 i 右边的值）。实时采样时拿不到"未来"的数据，通常用**最近 k 个值**做中值（因果滤波），输出会延迟 k/2 个采样周期：

```c
#define K 5
static int16_t hist[K];      // 环形缓冲，保存最近 K 个采样
static uint8_t pos;

int16_t median_rt(int16_t x) {
    int16_t tmp[K];
    hist[pos] = x;
    pos = (pos + 1) % K;
    memcpy(tmp, hist, sizeof(tmp));
    for (int i = 1; i < K; i++) {              // K 很小，插入排序
        int16_t v = tmp[i];
        int j = i;
        while (j > 0 && tmp[j - 1] > v) { tmp[j] = tmp[j - 1]; j--; }
        tmp[j] = v;
    }
    return tmp[K / 2];
}
```

工程上还常把中值和平均**组合**使用："**中位值平均滤波**"（去掉最大最小值后求平均，也叫防脉冲干扰平均滤波），兼顾去毛刺和平滑。

---

## ⚠️ 第五步：小白常见错误

1. **用 `size_t` 计算 `i - k/2`** → 无符号下溢成巨大的数，访问越界直接崩溃。
2. **越界位置补 0** → 示例 1 的 i=0 会输出 `[0,10,12]` 的中位数 10（碰巧对），但信号全是负数时就错了；题目要求补端点值。
3. **在原数组 `signal` 上排序** → `signal` 是 `const`，而且会破坏后续窗口的数据。
4. **思路二找 oldV 时用二分查找却没处理重复值** → 有重复值时找到哪一个都可以，但用线性查找最不容易写错。
5. **把 `out[i] = win[h]` 写成 `win[k/2 + 1]`** → 下标从 0 开始，中间位置是 `k/2`。

---

## 📊 第六步：方法对比

| 方法 | 时间 | 空间 | 说明 |
|---|---|---|---|
| 每个位置重新排序 | O(len · k²) | O(k) | 最直观，k 很小时足够 |
| 维护有序窗口 | O(len · k) | O(k) | 本题推荐 |
| 双堆 / 平衡树 | O(len · log k) | O(k) | k 很大时才有优势，MCU 上很少用 |

---

## 🔗 举一反三

- **9052. 滑动平均滤波**：对比两者对毛刺的反应。
- **力扣 480. 滑动窗口中位数**：k 很大时的双堆解法。
- **思考题 1**：一个连续 3 个点的"宽毛刺"，k = 3 的中值滤波能去掉吗？k 至少要多大？
- **思考题 2**：中值滤波会让方波的边沿变形吗？和滑动平均相比呢？
