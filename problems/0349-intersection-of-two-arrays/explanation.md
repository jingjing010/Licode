# 349. 两个数组的交集 —— 小白详细题解

> 找两个数组的公共元素，并且**去重**。这道题可以用三种经典方法做：暴力、哈希（标记数组）、排序 + 双指针。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 找出**两个数组都有**的数字，每个数字在答案里**只写一次**，顺序随意。

示例 2：`nums1 = [4,9,5]`，`nums2 = [9,4,9,8,4]`

| 数字 | 在 nums1 中？ | 在 nums2 中？ | 在交集中？ |
|---|---|---|---|
| 4 | ✅ | ✅（出现 2 次） | ✅ |
| 9 | ✅ | ✅（出现 2 次） | ✅ |
| 5 | ✅ | ❌ | ❌ |
| 8 | ❌ | ✅ | ❌ |

答案 `[4,9]`（或 `[9,4]`）。

**几个需要注意的细节：**

1. 结果**不能有重复**：示例 1 中 2 在两个数组里都出现了多次，但答案只有一个 `2`。
2. 交集可能为空，此时返回长度为 0 的数组，`*returnSize = 0`。
3. 数值范围很小：**0 ~ 1000**，这一点可以利用。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 返回数组的套路（同 1. 两数之和）

```c
int* res = (int*)malloc(sizeof(int) * 最大可能长度);
*returnSize = 实际长度;
return res;
```

交集的长度不会超过较短数组的长度，所以申请 `min(nums1Size, nums2Size)` 个就够。

### 2. 用 `bool` 数组当"集合"

数值只在 0~1000 之间，那么 `bool seen[1001]` 中 `seen[x] = true` 就表示"x 出现过"。查询和修改都是 O(1)，这就是最简单的**哈希表**。

```c
bool seen[1001] = {false};   // 一定要初始化！
```

### 3. `qsort` 排序

```c
int cmpInt(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b;
    return (x > y) - (x < y);      // x<y 返回 -1，x==y 返回 0，x>y 返回 1
}
qsort(nums, numsSize, sizeof(int), cmpInt);
```

`qsort` 需要一个比较函数，参数是 `const void*`，要先转成 `const int*` 再取值。

---

## 💡 第三步：思路一 —— 暴力枚举

### 思路

对 `nums1` 中的每个数 `x`：

1. 先看 `x` 是不是已经在答案里了（去重），在就跳过；
2. 再到 `nums2` 里找 `x`，找到就把 `x` 加入答案。

### 代码

```c
int* intersection(int* nums1, int nums1Size, int* nums2, int nums2Size, int* returnSize) {
    int* res = (int*)malloc(sizeof(int) * nums1Size);   // 答案最多 nums1Size 个
    int k = 0;                                          // 答案中已有的元素个数

    for (int i = 0; i < nums1Size; i++) {
        int x = nums1[i];

        // 1. 去重：x 已经在答案里就跳过
        bool already = false;
        for (int t = 0; t < k; t++) {
            if (res[t] == x) {
                already = true;
                break;
            }
        }
        if (already) {
            continue;
        }

        // 2. 在 nums2 中查找 x
        for (int j = 0; j < nums2Size; j++) {
            if (nums2[j] == x) {
                res[k++] = x;                           // 找到了，加入答案
                break;                                  // 找到一个就够了
            }
        }
    }

    *returnSize = k;
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n × (m + k))**：n、m 是两个数组长度，k 是答案长度。本题最多约 200 万次比较，能通过。
- **空间复杂度 O(1)**（不计答案）。

---

## 🚀 第四步：思路二 —— 标记数组（哈希，最优）

### 思路

1. 遍历 `nums1`，用 `in1[x] = true` 标记出现过的数；
2. 遍历 `nums2`，如果 `in1[x]` 为真，说明 `x` 在两个数组中都有，加入答案；
3. **加入后立刻把 `in1[x]` 改为 `false`**，这样 `nums2` 后面再遇到 `x` 就不会重复加入。

### 手动模拟（示例 2）

第 1 步后：`in1[4] = in1[9] = in1[5] = true`。

| nums2[j] | in1[x] | 操作 | 答案 |
|---|---|---|---|
| 9 | true | 加入，in1[9] = false | [9] |
| 4 | true | 加入，in1[4] = false | [9,4] |
| 9 | false | 跳过（已加入过） | [9,4] |
| 8 | false | 跳过 | [9,4] |
| 4 | false | 跳过（已加入过） | [9,4] |

### 代码

```c
int* intersection(int* nums1, int nums1Size, int* nums2, int nums2Size, int* returnSize) {
    bool in1[1001] = {false};                 // in1[x] 表示 x 在 nums1 中出现过（且还没加入答案）
    for (int i = 0; i < nums1Size; i++) {
        in1[nums1[i]] = true;
    }

    int minSize = nums1Size < nums2Size ? nums1Size : nums2Size;
    int* res = (int*)malloc(sizeof(int) * minSize);   // 交集不会比短的数组更长
    int k = 0;

    for (int j = 0; j < nums2Size; j++) {
        int x = nums2[j];
        if (in1[x]) {                         // x 在两个数组里都有
            res[k++] = x;
            in1[x] = false;                   // 关掉标记，防止重复加入
        }
    }

    *returnSize = k;
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n + m)**：两个数组各扫一遍。
- **空间复杂度 O(V)**：V = 1001 是值域大小。

> 💡 如果数值范围很大（比如到 10^9），就不能开这么大的数组了，需要真正的哈希表，或者用下面的排序方法。

---

## 🚀 第五步：思路三 —— 排序 + 双指针

### 思路

两个数组都排好序后，用两个指针 `i`、`j` 从头往后走：

- `nums1[i] < nums2[j]`：`i` 指向的数太小，`i++`；
- `nums1[i] > nums2[j]`：`j++`；
- 相等：是公共元素。如果它和答案中最后一个数不同（去重），就加入答案；然后 `i++`、`j++`。

因为有序，相同的数挨在一起，所以只需和**答案的最后一个元素**比较就能去重。

### 代码

```c
int cmpInt(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b;
    return (x > y) - (x < y);
}

int* intersection(int* nums1, int nums1Size, int* nums2, int nums2Size, int* returnSize) {
    qsort(nums1, nums1Size, sizeof(int), cmpInt);     // 先把两个数组都排序
    qsort(nums2, nums2Size, sizeof(int), cmpInt);

    int minSize = nums1Size < nums2Size ? nums1Size : nums2Size;
    int* res = (int*)malloc(sizeof(int) * minSize);
    int i = 0, j = 0, k = 0;

    while (i < nums1Size && j < nums2Size) {
        if (nums1[i] < nums2[j]) {
            i++;                                      // nums1 当前数太小，往后走
        } else if (nums1[i] > nums2[j]) {
            j++;                                      // nums2 当前数太小，往后走
        } else {
            // 相等：公共元素。和答案最后一个不同才加入（去重）
            if (k == 0 || res[k - 1] != nums1[i]) {
                res[k++] = nums1[i];
            }
            i++;
            j++;
        }
    }

    *returnSize = k;
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n log n + m log m)**：主要是排序。
- **空间复杂度 O(log n + log m)**：排序用的栈空间（不计答案）。

---

## ⚠️ 第六步：小白常见错误

1. **结果没有去重** → 示例 1 会输出 `[2,2]`，而正确答案是 `[2]`。
2. **`bool in1[1001];` 没有初始化** → 局部数组里是垃圾值，很多数一开始就被当成"出现过"。
3. **数组开成 `in1[1000]`** → 数值可以等于 1000，`in1[1000]` 越界。要开 1001。
4. **忘记设置 `*returnSize`** → 判题程序拿不到正确的长度。
5. **双指针法中只和 `nums1[i - 1]` 比较来去重** → `i - 1` 可能越界（`i = 0` 时），而且逻辑容易错。和答案最后一个元素 `res[k - 1]` 比较更稳妥。
6. **`qsort` 的比较函数写成 `return *(int*)a > *(int*)b;`** → 只返回 0 或 1，没有负数，排序结果是错的。

---

## 📊 第七步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 适用场景 |
|---|---|---|---|
| 暴力枚举 | O(n·m) | O(1) | 数据很小 |
| 标记数组 | O(n + m) | O(值域) | 值域小，本题最优 |
| 排序 + 双指针 | O(n log n + m log m) | O(log n) | 值域大，或数组已经有序 |

---

## 🔗 举一反三

- **350. 两个数组的交集 II**：结果要保留重复次数（取两边出现次数的较小值），把 `bool` 标记换成计数即可。
- **1. 两数之和**：同样是"用哈希表快速判断某个数是否出现过"。
- **思考题**：如果两个数组都已经排好序，哪种方法最好？
