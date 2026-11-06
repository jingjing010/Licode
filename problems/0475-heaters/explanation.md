# 475. 供暖器 —— 小白详细题解

> 这道题的关键是**把问题拆开**：整体的"最小半径"其实就是"每个房屋到最近供暖器的距离"中的最大值。拆开后，每个房屋只需要做一次二分查找。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 一条直线上有一些房屋和一些供暖器。所有供暖器的加热半径都一样，记为 r，位置 p 的供暖器能覆盖 `[p - r, p + r]`。问 r 最小取多少，才能让**每个房屋都被至少一个供暖器覆盖**？

拿示例 3 `houses = [1,5], heaters = [2]` 来说：

| 房屋位置 | 最近的供暖器 | 距离 |
|---|---|---|
| 1 | 2 | 1 |
| 5 | 2 | 3 |

半径至少要 3，房屋 5 才能被覆盖；半径为 3 时房屋 1 也被覆盖了。答案是 3。

所以：**答案 = 所有房屋"到最近供暖器的距离"的最大值**。

**几个需要注意的细节：**

1. 两个数组**都不一定有序**！
2. 房屋和供暖器可以在同一个位置（距离为 0）。
3. 坐标最大 `10^9`，两个坐标相减最大约 `10^9`，仍在 `int` 范围内，不会溢出。
4. 房屋可能在所有供暖器的左边或右边，这时只有一侧有供暖器。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. `qsort` 排序

```c
int cmpInt(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b;
    return (x > y) - (x < y);     // x<y 返回 -1，相等返回 0，x>y 返回 1
}
qsort(heaters, heatersSize, sizeof(int), cmpInt);
```

- `qsort` 是 `<stdlib.h>` 里的快速排序，平均 O(n log n)。
- 比较函数参数是 `const void*`（"指向任意类型的指针"），要先强制转换成 `const int*` 再取值。
- ⚠️ 不要写 `return x - y;`：当 x、y 一正一负且很大时会溢出。本题坐标都是正数，但养成好习惯。

### 2. `INT_MAX`

在 `<limits.h>` 中，表示 int 的最大值。常用来给"最小值"变量设初始值。

---

## 💡 第三步：思路一 —— 暴力枚举（会超时）

### 思路

对每个房屋，遍历所有供暖器，算出最近距离；再对所有房屋取最大值。

### 代码

```c
// ❌ 正确但太慢：3万 × 3万 = 9 亿次运算，会超时
int findRadius(int* houses, int housesSize, int* heaters, int heatersSize) {
    int ans = 0;
    for (int i = 0; i < housesSize; i++) {
        int best = INT_MAX;                      // 这个房屋到最近供暖器的距离
        for (int j = 0; j < heatersSize; j++) {
            int d = abs(houses[i] - heaters[j]);
            if (d < best) best = d;
        }
        if (best > ans) ans = best;              // 取所有房屋中的最大值
    }
    return ans;
}
```

### 复杂度分析

- **时间复杂度 O(n · m)**，n、m 都是 3×10⁴ 时约 9×10⁸，超时。
- **空间复杂度 O(1)**。

---

## 🚀 第四步：思路二 —— 排序 + 二分查找（推荐）

### 思路

暴力法慢在"对每个房屋都要扫一遍所有供暖器"。如果供暖器**排好序**，离房屋 `h` 最近的供暖器一定在 h 的"左右两边紧挨着"：

```
供暖器（已排序）:  1      4         9      15
房屋 h = 6:              ↑  h  ↑
                     左边最近=4  右边最近=9
```

用二分查找找到**第一个 >= h 的供暖器**，下标记为 `lo`：

- 右边最近的供暖器：`heaters[lo]`（如果 `lo < heatersSize`）
- 左边最近的供暖器：`heaters[lo - 1]`（如果 `lo > 0`）

两者距离取较小值，就是这个房屋需要的半径。

### 区间定义与循环条件

和 35 题"搜索插入位置"一模一样：

- **左闭右开 `[lo, hi)`**，初始 `lo = 0, hi = heatersSize`（答案可能等于 heatersSize，表示所有供暖器都在 h 左边）。
- `while (lo < hi)`；`heaters[mid] < h` 时 `lo = mid + 1`，否则 `hi = mid`。
- `mid = lo + (hi - lo) / 2`。

### 手动模拟（`houses = [1,5]`, `heaters = [2]`）

| 房屋 h | 第一个 >= h 的下标 lo | 右边距离 | 左边距离 | 该房屋需要 |
|---|---|---|---|---|
| 1 | 0（heaters[0]=2） | 2-1 = 1 | 无（lo=0） | 1 |
| 5 | 1（越界，没有） | 无 | 5-2 = 3 | 3 |

最大值是 3 ✅。

### 代码

```c
static int cmpInt(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b;
    return (x > y) - (x < y);
}

int findRadius(int* houses, int housesSize, int* heaters, int heatersSize) {
    qsort(heaters, heatersSize, sizeof(int), cmpInt);   // 只需要给供暖器排序

    int ans = 0;
    for (int i = 0; i < housesSize; i++) {
        int h = houses[i];

        // 二分：找第一个 >= h 的供暖器下标，区间 [lo, hi)
        int lo = 0, hi = heatersSize;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (heaters[mid] < h) lo = mid + 1;   // 太靠左，答案在右边
            else hi = mid;                         // heaters[mid] >= h，可能是答案
        }

        int best = INT_MAX;                        // h 到最近供暖器的距离
        if (lo < heatersSize) best = heaters[lo] - h;                    // 右边的
        if (lo > 0 && h - heaters[lo - 1] < best) best = h - heaters[lo - 1];  // 左边的
        if (best > ans) ans = best;
    }
    return ans;
}
```

### 复杂度分析

- **时间复杂度 O((n + m) log m)**：排序 O(m log m)，每个房屋二分 O(log m)。
- **空间复杂度 O(log m)**：qsort 的递归栈。

---

## 🔁 补充：思路三 —— 两个数组都排序 + 双指针

如果把房屋也排序，那么房屋从左往右走时，"最近的供暖器"也只会往右移，不会回头。用一个指针 `j` 跟着走即可：

```c
static int cmpInt(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b;
    return (x > y) - (x < y);
}

int findRadius(int* houses, int housesSize, int* heaters, int heatersSize) {
    qsort(houses, housesSize, sizeof(int), cmpInt);
    qsort(heaters, heatersSize, sizeof(int), cmpInt);
    int ans = 0, j = 0;
    for (int i = 0; i < housesSize; i++) {
        // 只要下一个供暖器离当前房屋不更远，就往右移
        while (j + 1 < heatersSize &&
               abs(heaters[j + 1] - houses[i]) <= abs(heaters[j] - houses[i])) {
            j++;
        }
        int d = abs(heaters[j] - houses[i]);
        if (d > ans) ans = d;
    }
    return ans;
}
```

时间复杂度 O(n log n + m log m)，排序之后的扫描只要 O(n + m)。

---

## ⚠️ 第五步：小白常见错误

1. **忘了排序就二分** → 题目没保证 `heaters` 有序，直接二分结果是错的。
2. **只看右边（或只看左边）的供暖器** → 比如 `heaters = [1, 10]`, 房屋在 3：右边最近是 10（距离 7），左边是 1（距离 2），答案应取 2。
3. **访问 `heaters[lo]` 前没判断 `lo < heatersSize`** → 房屋在所有供暖器右边时 `lo == heatersSize`，越界。
4. **访问 `heaters[lo - 1]` 前没判断 `lo > 0`** → 房屋在所有供暖器左边时越界读 `heaters[-1]`。
5. **最后取 min 而不是 max** → 半径要让**所有**房屋都被覆盖，取的是每个房屋需求的**最大值**。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 暴力枚举 | O(n · m) | O(1) | ⭐ | 会超时，只用于理解 |
| 排序 + 二分 | O((n + m) log m) | O(log m) | ⭐⭐ | 推荐，思路最清晰 |
| 排序 + 双指针 | O(n log n + m log m) | O(log n) | ⭐⭐ | 也很常见 |

> 🎯 **学习建议**：遇到"在一堆数里找离 x 最近的数"，第一反应是**排序 + 二分找第一个 >= x 的位置**，然后看它和它左边的那个。

---

## 🔗 举一反三

- **35. 搜索插入位置**：本题二分部分的原型。
- **658. 找到 K 个最接近的元素**：找离 x 最近的 k 个数。
- **思考题**：本题也可以"二分答案"：猜一个半径 r，检查能否覆盖所有房屋。这个检查要怎么写？复杂度是多少？
