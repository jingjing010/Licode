# 347. 前 K 个高频元素 —— 小白详细题解

> 两步走：**先计数，再选前 k 名**。第二步用排序、堆、桶都可以，桶排序能做到线性时间。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 数一数每个数出现了几次，把出现次数**最多的 k 个数**交出来，顺序随便。

示例 1：`nums = [1,1,1,2,2,3], k = 2`

| 数值 | 1 | 2 | 3 |
|---|---|---|---|
| 出现次数 | 3 | 2 | 1 |

次数前 2 名是 1（3 次）和 2（2 次），答案 `[1,2]`（写成 `[2,1]` 也对）。

**几个需要注意的细节：**

1. 返回的是**数值**，不是次数。
2. 题目保证答案唯一，不会出现"第 k 名和第 k+1 名次数一样"的情况。
3. 数值可能是**负数**（最小 -10⁴），不能直接拿来当数组下标。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 下标偏移：用数组代替哈希表

数值范围是 `[-10000, 10000]`，一共 20001 种。把每个数**加上 10000** 就变成了 `[0, 20000]`，可以直接当下标：

```c
#define OFFSET 10000
static int cnt[2 * OFFSET + 1];   // cnt[v + OFFSET] = v 出现的次数
cnt[nums[i] + OFFSET]++;
```

`static` 让这个 2 万大小的数组放在静态区，而不是栈上。但 `static` 数组在多次调用之间会**保留上次的值**，所以每次进函数都要 `memset` 清零。

### 2. 结构体数组 + `qsort`

```c
typedef struct {
    int val;      // 数值
    int freq;     // 出现次数
} Pair;

static int cmpFreqDesc(const void* a, const void* b) {
    const Pair* x = (const Pair*)a;
    const Pair* y = (const Pair*)b;
    return y->freq - x->freq;          // 次数多的排前面（次数 ≤ 10^5，不会溢出）
}
```

`x->freq` 等价于 `(*x).freq`，是通过结构体指针访问成员的写法。

---

## 💡 第三步：思路一 —— 计数 + 按次数排序

### 思路

1. 用计数数组统计每个数的次数；
2. 把出现过的数做成 `(val, freq)` 数组；
3. 按 `freq` 从大到小排序，取前 k 个的 `val`。

### 代码

```c
#define OFFSET 10000
#define RANGE (2 * OFFSET + 1)

typedef struct {
    int val;
    int freq;
} Pair;

static int cmpFreqDesc(const void* a, const void* b) {
    const Pair* x = (const Pair*)a;
    const Pair* y = (const Pair*)b;
    return y->freq - x->freq;                 // 次数从大到小
}

int* topKFrequent(int* nums, int numsSize, int k, int* returnSize) {
    static int cnt[RANGE];
    memset(cnt, 0, sizeof(cnt));              // static 数组每次都要清零
    for (int i = 0; i < numsSize; i++) {
        cnt[nums[i] + OFFSET]++;              // 1. 计数
    }

    Pair* pairs = (Pair*)malloc(sizeof(Pair) * RANGE);
    int m = 0;                                // 不同数值的个数
    for (int v = 0; v < RANGE; v++) {
        if (cnt[v] > 0) {                     // 2. 收集出现过的数
            pairs[m].val = v - OFFSET;        //    记得减回偏移量
            pairs[m].freq = cnt[v];
            m++;
        }
    }

    qsort(pairs, m, sizeof(Pair), cmpFreqDesc);   // 3. 按次数排序

    int* res = (int*)malloc(sizeof(int) * k);
    for (int i = 0; i < k; i++) {
        res[i] = pairs[i].val;
    }
    free(pairs);
    *returnSize = k;
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n + U + d log d)**：U = 20001 是值域大小，d 是不同数值的个数（d ≤ 20001）。
- **空间复杂度 O(U)**。

严格说排序这一步是 O(d log d)，进阶要求"优于 O(n log n)"，下面用桶排序把它也变成线性的。

---

## 🚀 第四步：思路二 —— 计数 + 桶排序

### 思路

一个数出现的次数最多是 n。准备 n+1 个"桶"，**第 c 号桶装所有出现了 c 次的数**。然后从 n 号桶往 1 号桶倒，倒满 k 个就停。

每个桶里可能有好几个数，用"数组模拟链表"串起来：`head[c]` 是桶 c 的第一个数，`nxt[v]` 是和 v 同一个桶的下一个数，`-1` 表示没有了。

### 手动模拟（示例 1：`[1,1,1,2,2,3], k = 2`）

| 桶号（次数） | 6 | 5 | 4 | 3 | 2 | 1 |
|---|---|---|---|---|---|---|
| 桶里的数 | | | | 1 | 2 | 3 |

从 6 号桶往下倒：6、5、4 号桶空；3 号桶倒出 1；2 号桶倒出 2；凑够 2 个，停。答案 `[1,2]` ✅

### 代码

```c
#define OFFSET 10000
#define RANGE (2 * OFFSET + 1)

int* topKFrequent(int* nums, int numsSize, int k, int* returnSize) {
    static int cnt[RANGE];
    static int nxt[RANGE];                    // nxt[v]：同一桶里 v 后面的那个数（下标形式）
    memset(cnt, 0, sizeof(cnt));
    for (int i = 0; i < numsSize; i++) {
        cnt[nums[i] + OFFSET]++;              // 1. 计数
    }

    // 2. 建桶：head[c] 是出现 c 次的第一个数（下标形式），-1 表示桶空
    int* head = (int*)malloc(sizeof(int) * (numsSize + 1));
    for (int c = 0; c <= numsSize; c++) head[c] = -1;
    for (int v = 0; v < RANGE; v++) {
        if (cnt[v] > 0) {
            nxt[v] = head[cnt[v]];            // 头插法：v 接到桶的最前面
            head[cnt[v]] = v;
        }
    }

    // 3. 从次数最多的桶开始倒，凑够 k 个为止
    int* res = (int*)malloc(sizeof(int) * k);
    int m = 0;
    for (int c = numsSize; c >= 1 && m < k; c--) {
        for (int v = head[c]; v != -1 && m < k; v = nxt[v]) {
            res[m++] = v - OFFSET;            // 减回偏移量得到真实数值
        }
    }
    free(head);
    *returnSize = m;
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n + U)**：计数 O(n)，建桶 O(U)，倒桶 O(n + U)。
- **空间复杂度 O(n + U)**。

> 💬 如果数值范围很大（比如 ±10⁹），计数数组开不下，就需要自己写哈希表来计数，后面的桶排序不变。

---

## ⚠️ 第五步：小白常见错误

1. **负数直接当下标** → `cnt[-3]` 越界。必须加偏移量 `OFFSET`。
2. **`static` 数组不清零** → 判题时函数只调用一次看不出问题，但在力扣上多组数据会互相污染。
3. **返回次数而不是数值** → `res[i] = pairs[i].freq` 是错的。
4. **忘了减回偏移量** → 返回的是 `v` 而不是 `v - OFFSET`，所有答案都大了 10000。
5. **`head` 只开 `numsSize` 个** → 一个数可能出现 `numsSize` 次，桶号最大是 `numsSize`，要开 `numsSize + 1` 个。
6. **在栈上开 `int cnt[20001]` 还嫌不够又开几个大数组** → 栈空间有限（Windows 默认 1MB），大数组用 `static` 或 `malloc`。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 计数 + qsort | O(n + d log d) | O(U) | ⭐⭐ | 最直观 |
| 计数 + 小根堆（大小 k） | O(n + d log k) | O(U + k) | ⭐⭐⭐ | k 很小时好用 |
| 计数 + 桶排序 | O(n + U) | O(n + U) | ⭐⭐⭐ | 满足进阶要求 |

---

## 🔗 举一反三

- **215. 数组中的第K个最大元素**：堆和快速选择的写法可以直接搬过来，比较的对象换成次数。
- **451. 根据字符出现频率排序**：同样是"计数 + 按次数排序"，字符只有 128 种。
- **692. 前K个高频单词**：次数相同时要按字典序，需要自定义比较函数。
- **思考题**：如果数据是一个**数据流**（数不断到来，随时要回答前 k 高频），该怎么设计？
