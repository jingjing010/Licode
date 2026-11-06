# 215. 数组中的第K个最大元素 —— 小白详细题解

> 一道题串起三种重要工具：**排序（qsort）**、**堆**、**快速选择**。面试最爱问"能不能比排序更快"。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 把数组从大到小排好，第 k 个是谁？

示例 2：`nums = [3,2,3,1,2,4,5,5,6], k = 4`

| 从大到小排第几 | 1 | 2 | 3 | **4** | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| 数值 | 6 | 5 | 5 | **4** | 3 | 3 | 2 | 2 | 1 |

答案是 4。

**几个需要注意的细节：**

1. **重复的数要分别算**：两个 5 占了第 2、3 名，而不是并列第 2。
2. k 从 **1** 开始数。第 1 大就是最大值。
3. 函数可以修改 `nums` 的内容（比如原地排序）。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. `qsort` 和比较函数

`<stdlib.h>` 自带快速排序：

```c
int cmpDesc(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b;   // void* 先转成 int* 再取值
    return (x < y) - (x > y);                     // 从大到小：x 大时返回负数
}
qsort(nums, numsSize, sizeof(int), cmpDesc);
```

比较函数返回**负数**表示 a 排在 b 前面，**正数**表示 a 排在 b 后面，0 表示相等。

> 💬 不要写 `return y - x;`，两个数相差很大时（比如 INT_MAX 和 -1）会溢出。本题数据范围小不会出问题，但养成好习惯。

### 2. 交换两个数

```c
int t = a[i]; a[i] = a[j]; a[j] = t;
```

### 3. 堆（用数组存一棵完全二叉树）

下标从 0 开始时，结点 `i` 的父结点是 `(i - 1) / 2`，左孩子是 `2*i + 1`，右孩子是 `2*i + 2`。**小根堆**要求每个结点都 ≤ 它的孩子，所以堆顶 `heap[0]` 是最小值。

---

## 💡 第三步：思路一 —— 排序（最容易想到）

### 代码

```c
static int cmpDesc(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b;
    return (x < y) - (x > y);        // 从大到小
}

int findKthLargest(int* nums, int numsSize, int k) {
    qsort(nums, numsSize, sizeof(int), cmpDesc);
    return nums[k - 1];              // 第 k 大在下标 k-1
}
```

### 复杂度分析

- **时间复杂度 O(n log n)**：n = 10⁵ 时很快就能过，但题目要求 O(n)。
- **空间复杂度 O(log n)**：qsort 递归用的栈空间。

---

## 🚀 第四步：思路二 —— 大小为 k 的小根堆

### 思路

我们只关心**前 k 大**。维护一个最多装 k 个数的小根堆，它装的是"目前为止最大的 k 个数"：

- 堆没满：直接放进去；
- 堆满了：新数比堆顶（这 k 个里最小的）大，就把堆顶换成新数，再调整堆。

扫完后，堆顶就是"最大的 k 个数里最小的那个"，也就是第 k 大。

### 手动模拟（示例 1：`[3,2,1,5,6,4], k = 2`）

| 新数 | 操作 | 堆里的数 | 堆顶 |
|---|---|---|---|
| 3 | 堆没满，放入 | {3} | 3 |
| 2 | 堆没满，放入 | {2,3} | 2 |
| 1 | 1 ≤ 堆顶 2，丢弃 | {2,3} | 2 |
| 5 | 5 > 2，替换堆顶 | {3,5} | 3 |
| 6 | 6 > 3，替换堆顶 | {5,6} | 5 |
| 4 | 4 ≤ 5，丢弃 | {5,6} | **5** ✅ |

### 代码

```c
// 把 heap[i] 往下沉，直到它不比孩子大
static void siftDown(int* heap, int size, int i) {
    while (1) {
        int smallest = i;
        int l = 2 * i + 1, r = 2 * i + 2;
        if (l < size && heap[l] < heap[smallest]) smallest = l;
        if (r < size && heap[r] < heap[smallest]) smallest = r;
        if (smallest == i) break;                 // 已经比两个孩子都小
        int t = heap[i]; heap[i] = heap[smallest]; heap[smallest] = t;
        i = smallest;
    }
}

// 把 heap[i] 往上浮，直到它不比父结点小
static void siftUp(int* heap, int i) {
    while (i > 0) {
        int p = (i - 1) / 2;
        if (heap[p] <= heap[i]) break;
        int t = heap[i]; heap[i] = heap[p]; heap[p] = t;
        i = p;
    }
}

int findKthLargest(int* nums, int numsSize, int k) {
    int* heap = (int*)malloc(sizeof(int) * k);
    int size = 0;
    for (int i = 0; i < numsSize; i++) {
        if (size < k) {
            heap[size] = nums[i];                 // 放到末尾再上浮
            siftUp(heap, size);
            size++;
        } else if (nums[i] > heap[0]) {
            heap[0] = nums[i];                    // 替换掉最小的
            siftDown(heap, size, 0);
        }
    }
    int ans = heap[0];
    free(heap);
    return ans;
}
```

### 复杂度分析

- **时间复杂度 O(n log k)**：每个数最多做一次 O(log k) 的调整。k 很小时非常快。
- **空间复杂度 O(k)**。

---

## 🚀 第五步：思路三 —— 快速选择（平均 O(n)）

### 思路

回忆快速排序：选一个基准数 `pivot`，把数组分成"比它大 / 等于它 / 比它小"三段。分完之后：

- 如果第 k 大落在"比它大"那段 → 只需要在那段里继续找；
- 如果落在"等于它"那段 → 答案就是 `pivot`；
- 否则 → 去"比它小"那段找（k 要减去前两段的长度）。

快排要递归两边，快速选择**只走一边**，平均下来总工作量是 n + n/2 + n/4 + ... ≈ 2n，即 O(n)。

> ⚠️ **为什么要三路分区？** 如果数组是 10⁵ 个相同的数，普通的两路分区每次只能排除一个数，会退化成 O(n²)。三路分区把所有"等于 pivot"的数一次性归到中间，直接命中。
>
> ⚠️ **为什么要随机选 pivot？** 如果总选第一个数，遇到已经排好序的数组也会退化成 O(n²)。

### 代码

```c
int findKthLargest(int* nums, int numsSize, int k) {
    int lo = 0, hi = numsSize - 1;        // 在 nums[lo..hi] 里找第 k 大
    while (1) {
        // 随机选基准。Windows 上 rand() 最大只有 32767，拼两次扩大范围
        int r = lo + (int)(((long long)rand() * 32768 + rand()) % (hi - lo + 1));
        int pivot = nums[r];
        // 三路分区（从大到小）：[lo, lt) > pivot，[lt, i) == pivot，(gt, hi] < pivot
        int lt = lo, i = lo, gt = hi;
        while (i <= gt) {
            if (nums[i] > pivot) {
                int t = nums[i]; nums[i] = nums[lt]; nums[lt] = t;
                lt++; i++;
            } else if (nums[i] < pivot) {
                int t = nums[i]; nums[i] = nums[gt]; nums[gt] = t;
                gt--;                     // 换过来的数还没看过，i 不动
            } else {
                i++;
            }
        }
        int bigger = lt - lo;             // 比 pivot 大的个数
        int equal = gt - lt + 1;          // 等于 pivot 的个数
        if (k <= bigger) {
            hi = lt - 1;                  // 答案在"更大"段
        } else if (k <= bigger + equal) {
            return pivot;                 // 答案就是 pivot
        } else {
            k -= bigger + equal;          // 去"更小"段找第 k' 大
            lo = gt + 1;
        }
    }
}
```

### 复杂度分析

- **时间复杂度：平均 O(n)**，最坏 O(n²)（随机化后几乎不可能发生）。
- **空间复杂度 O(1)**：用循环代替递归，原地分区。

> 💬 本题数值范围只有 [-10⁴, 10⁴]，还可以用**计数排序**：开一个 20001 大小的计数数组，从大到小累加到 k 为止，严格 O(n + 值域)。

---

## ⚠️ 第六步：小白常见错误

1. **返回 `nums[k]`** → 下标从 0 开始，第 k 大是 `nums[k - 1]`。
2. **从小到大排序后返回 `nums[k - 1]`** → 那是第 k **小**。从小到大排序要返回 `nums[n - k]`。
3. **去重了** → 题目说的是"排序后的第 k 个"，重复的数要分别计数。
4. **堆用成了大根堆** → 大根堆装 k 个数时堆顶是最大值，不是第 k 大。找第 k 大要用**小根堆**。
5. **快速选择用两路分区 + 固定 pivot** → 全相同或已排序的 10⁵ 个数会超时。
6. **三路分区里和 `gt` 交换后 `i++`** → 换过来的 `nums[i]` 还没比较过，不能跳过。

---

## 📊 第七步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| qsort 排序 | O(n log n) | O(log n) | ⭐ | 先写对 |
| 小根堆 | O(n log k) | O(k) | ⭐⭐⭐ | 数据流/k 很小时最好 |
| 快速选择（三路 + 随机） | 平均 O(n) | O(1) | ⭐⭐⭐⭐ | 题目要求，面试高频 |
| 计数排序 | O(n + 值域) | O(值域) | ⭐⭐ | 值域小时的捷径 |

---

## 🔗 举一反三

- **347. 前 K 个高频元素**：先统计频率，再对频率做"第 k 大"。
- **703. 数据流中的第 K 大元素**：数据不断到来，只能用堆。
- **973. 最接近原点的 K 个点**：同样是 top-k，比较的是距离。
- **思考题**：如果要找第 k **小**，小根堆版本要怎么改？
