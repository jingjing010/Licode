# 15. 三数之和 —— 小白详细题解

> "两数之和"的升级版。难点不在找，而在**去重**。核心套路：**排序 + 固定一个数 + 双指针**。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 从数组里挑 3 个**不同位置**的数，让它们加起来等于 0。把所有这样的组合找出来，但**内容相同的组合只能算一次**。

拿示例 1 `nums = [-1,0,1,2,-1,-4]` 来说：

| 选的下标 | 对应的数 | 和 |
|---|---|---|
| 0, 1, 2 | -1, 0, 1 | 0 ✅ |
| 1, 2, 4 | 0, 1, -1 | 0 ✅（内容和上一行一样，都是 {-1,0,1}） |
| 0, 3, 4 | -1, 2, -1 | 0 ✅ |

去掉重复后只剩两组：`[-1,-1,2]` 和 `[-1,0,1]`。

**几个需要注意的细节：**

1. **返回的是数值，不是下标**（和"两数之和"不一样）。
2. **"不重复"指内容不重复**：`[-1,0,1]` 和 `[0,1,-1]` 是同一个三元组，只能出现一次。
3. 同一个**值**可以用多次，只要来自**不同位置**：`[-1,-1,2]` 用了两个 -1，因为数组里本来就有两个 -1。示例 3 `[0,0,0]` 同理。
4. 可能一组答案都没有，此时返回空数组，`*returnSize = 0`。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 返回"二维数组"的三件套

```c
int** threeSum(int* nums, int numsSize, int* returnSize, int** returnColumnSizes)
```

| 你要做的 | 代码 |
|---|---|
| 返回值：行指针数组 | `int** res = malloc(sizeof(int*) * 容量);` |
| 每一行：3 个 int | `res[cnt] = malloc(sizeof(int) * 3);` |
| 告诉调用者有几行 | `*returnSize = cnt;` |
| 告诉调用者每行几列 | `cols[cnt] = 3;` 最后 `*returnColumnSizes = cols;` |

### 2. 事先不知道有多少个答案：用 `realloc` 动态扩容

答案个数无法提前知道（最多可能有上万个）。做法是先申请一个小容量，**满了就翻倍**：

```c
int cap = 16, cnt = 0;
int** res = (int**)malloc(sizeof(int*) * cap);
...
if (cnt == cap) {                                  // 装满了
    cap *= 2;                                      // 容量翻倍
    res = (int**)realloc(res, sizeof(int*) * cap); // realloc 会保留原来的内容
}
```

### 3. 排序比较函数

```c
int cmp(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b;
    return (x > y) - (x < y);      // 写 x - y 在本题也不会溢出，但养成好习惯
}
qsort(nums, numsSize, sizeof(int), cmp);
```

---

## 💡 第三步：思路一 —— 排序 + 三重循环（最朴素）

### 思路

1. 先**排序**。排序后相同的值挨在一起，而且每个三元组都会按"从小到大"的顺序被找到，方便去重。
2. 三重循环枚举 `i < j < k`。
3. **去重**：在每一层循环里，如果当前值和这一层**上一次**用过的值相同，就跳过。比如排序后是 `[-1,-1,0,1]`，第一层用过 `-1` 了，第二个 `-1` 再当第一个数只会找到一模一样的组合。

### 代码

```c
// ❌ 会超时：n = 3000 时三重循环约 4.5×10^9 次，仅用于理解思路
int cmpInt(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b;
    return (x > y) - (x < y);
}

int** threeSum(int* nums, int numsSize, int* returnSize, int** returnColumnSizes) {
    qsort(nums, numsSize, sizeof(int), cmpInt);       // 1. 排序
    int cap = 16, cnt = 0;
    int** res = (int**)malloc(sizeof(int*) * cap);
    int* cols = (int*)malloc(sizeof(int) * cap);

    for (int i = 0; i < numsSize; i++) {
        if (i > 0 && nums[i] == nums[i - 1]) continue;              // 第一个数去重
        for (int j = i + 1; j < numsSize; j++) {
            if (j > i + 1 && nums[j] == nums[j - 1]) continue;      // 第二个数去重
            for (int k = j + 1; k < numsSize; k++) {
                if (k > j + 1 && nums[k] == nums[k - 1]) continue;  // 第三个数去重
                if (nums[i] + nums[j] + nums[k] == 0) {
                    if (cnt == cap) {                               // 容量不够就翻倍
                        cap *= 2;
                        res = (int**)realloc(res, sizeof(int*) * cap);
                        cols = (int*)realloc(cols, sizeof(int) * cap);
                    }
                    res[cnt] = (int*)malloc(sizeof(int) * 3);
                    res[cnt][0] = nums[i];
                    res[cnt][1] = nums[j];
                    res[cnt][2] = nums[k];
                    cols[cnt] = 3;
                    cnt++;
                }
            }
        }
    }
    *returnSize = cnt;
    *returnColumnSizes = cols;
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n³)**：n = 3000 时约 4.5×10⁹ 次，必然超时。
- **空间复杂度 O(log n)**：排序（返回值不算）。

---

## 🚀 第四步：思路二 —— 排序 + 双指针（O(n²)）

### 思路

固定第一个数 `nums[i]` 后，问题变成：

> 在 `nums[i+1 .. n-1]` 里找两个数，和为 `-nums[i]`。

这是**有序数组上的两数之和**，可以用**左右双指针**在 O(n) 内解决：

- `l` 从 `i+1` 开始（最小），`r` 从 `n-1` 开始（最大）。
- 三数之和 `sum < 0`：太小了，只能让 `l` 右移（换一个更大的数）。
- `sum > 0`：太大了，只能让 `r` 左移（换一个更小的数）。
- `sum == 0`：找到一组！记录后 `l`、`r` 同时向中间走，并**跳过相同的值**。

> ❓ **为什么双指针不会漏掉答案？** 当 `sum < 0` 时，`nums[l]` 和当前最大的 `nums[r]` 搭配都不够大，和其他更小的 `nums[r']` 搭配就更不够了，所以 `nums[l]` 可以安全地扔掉。`sum > 0` 同理。

**两个小优化：**

- 如果 `nums[i] > 0`，后面的数都 ≥ `nums[i]` > 0，三个正数加起来不可能是 0，直接 `break`。
- `nums[i] == nums[i-1]` 时跳过，避免第一个数重复。

### 手动模拟（示例 1 排序后：`[-4,-1,-1,0,1,2]`）

| i | nums[i] | l | r | sum | 操作 |
|---|---|---|---|---|---|
| 0 | -4 | 1 (-1) | 5 (2) | -3 | 太小，l++ |
| 0 | -4 | 2 (-1) | 5 (2) | -3 | 太小，l++ |
| 0 | -4 | 3 (0) | 5 (2) | -2 | 太小，l++ |
| 0 | -4 | 4 (1) | 5 (2) | -1 | 太小，l++ → l == r 结束 |
| 1 | -1 | 2 (-1) | 5 (2) | 0 | ✅ 记录 [-1,-1,2]，l++, r-- |
| 1 | -1 | 3 (0) | 4 (1) | 0 | ✅ 记录 [-1,0,1]，l++, r-- → 结束 |
| 2 | -1 | | | | 和 nums[1] 相同，**跳过** |
| 3 | 0 | 4 (1) | 5 (2) | 3 | 太大，r-- → 结束 |

`i` 只需要走到 `n - 3`（后面至少要留两个数给 `l` 和 `r`），所以到这里外层循环就结束了。

### 代码

```c
int cmpInt(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b;
    return (x > y) - (x < y);
}

int** threeSum(int* nums, int numsSize, int* returnSize, int** returnColumnSizes) {
    qsort(nums, numsSize, sizeof(int), cmpInt);        // 1. 排序

    int cap = 16, cnt = 0;                             // 动态数组：容量 / 已有个数
    int** res = (int**)malloc(sizeof(int*) * cap);
    int* cols = (int*)malloc(sizeof(int) * cap);

    for (int i = 0; i < numsSize - 2; i++) {           // 2. 固定第一个数
        if (nums[i] > 0) break;                        //    最小的数都 > 0，不可能凑出 0
        if (i > 0 && nums[i] == nums[i - 1]) continue; //    第一个数去重

        int l = i + 1, r = numsSize - 1;               // 3. 在右边用双指针找另外两个数
        while (l < r) {
            int sum = nums[i] + nums[l] + nums[r];     // 最大 3×10^5，不会溢出
            if (sum < 0) {
                l++;                                   // 太小，左指针右移换个大的
            } else if (sum > 0) {
                r--;                                   // 太大，右指针左移换个小的
            } else {
                // 4. 找到一组，存起来（容量不够先扩容）
                if (cnt == cap) {
                    cap *= 2;
                    res = (int**)realloc(res, sizeof(int*) * cap);
                    cols = (int*)realloc(cols, sizeof(int) * cap);
                }
                res[cnt] = (int*)malloc(sizeof(int) * 3);
                res[cnt][0] = nums[i];
                res[cnt][1] = nums[l];
                res[cnt][2] = nums[r];
                cols[cnt] = 3;
                cnt++;

                // 5. 跳过和当前 nums[l]、nums[r] 相同的值，避免重复
                while (l < r && nums[l] == nums[l + 1]) l++;
                while (l < r && nums[r] == nums[r - 1]) r--;
                l++;
                r--;
            }
        }
    }

    *returnSize = cnt;
    *returnColumnSizes = cols;
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n²)**：排序 O(n log n)，外层 n 次 × 双指针 O(n)。n = 3000 时约 4.5×10⁶ 次，非常快。
- **空间复杂度 O(log n)**：排序用的栈空间（返回值不算）。

---

## ⚠️ 第五步：小白常见错误

1. **第一个数去重写成 `nums[i] == nums[i + 1]`** → 会把 `[-1,-1,2]` 这种答案漏掉：第一个 -1 被跳过了，第二个 -1 当第一个数时，右边已经没有另一个 -1 可用。正确的是和**前一个**比较：`i > 0 && nums[i] == nums[i - 1]`。
2. **找到答案后只做了 `l++` / `r--`，没有跳过重复值** → `[-2,0,0,2,2]` 会输出两次 `[-2,0,2]`。
3. **跳过重复时没写 `l < r`** → `while (nums[l] == nums[l + 1]) l++;` 在 `[0,0,0,0]` 这种数组里会一直走到数组外面，越界。
4. **没有 `realloc`，直接开固定大小的结果数组**（比如 `malloc(sizeof(int*) * numsSize)`）→ 答案个数可能比 n 大得多（本题测试中有上万组），写越界导致崩溃。
5. **忘记排序就用双指针** → 双指针依赖"左边小、右边大"，不排序结果完全错误。
6. **`*returnColumnSizes` 没赋值，或者 `cols[cnt]` 没写 3** → 调用者读到垃圾列数，输出错乱或崩溃。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 排序 + 三重循环 | O(n³) | O(log n) | ⭐ | 会超时，用来理解去重 |
| 排序 + 双指针 | O(n²) | O(log n) | ⭐⭐ | 标准答案，必须掌握 |

> 💬 也可以"固定一个数 + 哈希表找另外两个"，同样是 O(n²)，但去重更麻烦，C 语言还要手写哈希表，不推荐。

---

## 🔗 举一反三

- **1. 两数之和**：本题固定一个数之后，剩下的就是两数之和。
- **167. 两数之和 II - 输入有序数组**：双指针的入门题。
- **16. 最接近的三数之和**：同样的双指针框架，记录和 target 的最小差距。
- **18. 四数之和**：再套一层循环，O(n³)；注意四个数相加可能溢出 `int`，要用 `long long`。
- **思考题**：如果题目要求返回**下标**而不是数值，还能先排序吗？要怎么处理？
