# 416. 分割等和子集 —— 小白详细题解

> 0-1 背包的入门题。关键一步是把"分成两个和相等的子集"**转化**成"能不能凑出总和的一半"。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 把一堆正整数分成两组（每个数必须分到某一组），问能不能让两组的和**一样大**？

拿示例 1 `nums = [1,5,11,5]` 来说：总和是 22，分成 `[1,5,5]`（和 11）和 `[11]`（和 11），可以。

**关键转化：**

- 两组和相等 ⟺ 每组都是 `sum / 2`
- 所以只要能**选出一些数，和恰好是 `sum / 2`**，剩下的数自动就是另一组
- 如果 `sum` 是奇数，不可能平分，直接 `false`

| nums | sum | target = sum/2 | 能凑出 target 吗？ | 答案 |
|---|---|---|---|---|
| [1,5,11,5] | 22 | 11 | 11 ✅ | true |
| [1,2,3,5] | 11 | 奇数 | — | false |
| [2,2,3,5] | 12 | 6 | 2+2=4，2+3=5，3+2… 都凑不出 6 ❌ | false |

---

## 🧰 第二步：这道题需要的 C 语言知识

1. **`calloc` 申请 bool 数组**：全部初始化为 `false`。
2. **二维数组的 malloc**：先申请"行指针数组"，再给每一行申请空间（和 118 题杨辉三角一样）。
3. **倒序循环** `for (int j = target; j >= x; j--)`：这是 0-1 背包一维写法的灵魂，下文会解释。

---

## 💡 第三步：思路一 —— 二维动态规划

### 思路

`dp[i][j]`：只用**前 i 个数**，能否选出一些数使和**恰好为 j**。

对第 i 个数 `x = nums[i-1]`，只有两种选择：

- **不选**它：`dp[i-1][j]`
- **选**它（要求 `j >= x`）：`dp[i-1][j - x]`

```
dp[i][j] = dp[i-1][j] || (j >= x && dp[i-1][j - x])，   dp[0][0] = true
```

### 手动模拟（示例 1：`[1,5,11,5]`，target = 11，只列出为 true 的 j）

| 用了前 i 个数 | 新加入的数 | 能凑出的和 j |
|---|---|---|
| 0 | — | {0} |
| 1 | 1 | {0, 1} |
| 2 | 5 | {0, 1, 5, 6} |
| 3 | 11 | {0, 1, 5, 6, **11**} |
| 4 | 5 | {0, 1, 5, 6, 10, **11**} |

`dp[4][11] = true`。

### 代码

```c
bool canPartition(int* nums, int numsSize) {
    int sum = 0;
    for (int i = 0; i < numsSize; i++) sum += nums[i];
    if (sum % 2 != 0) return false;          // 奇数不可能平分
    int target = sum / 2;

    // dp[i][j]：前 i 个数能否凑出和 j。共 (numsSize+1) 行，每行 target+1 列
    bool** dp = (bool**)malloc(sizeof(bool*) * (numsSize + 1));
    for (int i = 0; i <= numsSize; i++) {
        dp[i] = (bool*)calloc(target + 1, sizeof(bool));
    }
    dp[0][0] = true;                         // 一个数都不选，和为 0

    for (int i = 1; i <= numsSize; i++) {
        int x = nums[i - 1];                 // 第 i 个数
        for (int j = 0; j <= target; j++) {
            dp[i][j] = dp[i - 1][j];                         // 不选 x
            if (j >= x && dp[i - 1][j - x]) dp[i][j] = true; // 选 x
        }
    }

    bool ans = dp[numsSize][target];
    for (int i = 0; i <= numsSize; i++) free(dp[i]);
    free(dp);
    return ans;
}
```

### 复杂度分析

- **时间复杂度 O(n × target)**：最多 200 × 10000 = 2×10⁶。
- **空间复杂度 O(n × target)**。

---

## 🚀 第四步：思路二 —— 一维数组 + 倒序遍历

### 思路

观察思路一：第 i 行只依赖第 i-1 行。所以可以只用**一行** `dp[j]`，表示"目前为止能否凑出 j"，每处理一个数就原地更新：

```
dp[j] = dp[j] || dp[j - x]
```

### ❓ 为什么 j 必须**倒序**？

假设 `x = 5`，如果 j **从小到大**更新：

- 先算 `dp[5] = dp[5] || dp[0]` → true（用了一次 5）
- 再算 `dp[10] = dp[10] || dp[5]` → true，但这里的 `dp[5]` 是**刚刚被这个 5 更新过的**，相当于 5 被用了**两次**！

**从大到小**更新时，计算 `dp[j]` 用到的 `dp[j - x]` 还没被本轮修改，仍然是"上一行"的值，保证每个数只用一次。

### 代码

```c
bool canPartition(int* nums, int numsSize) {
    int sum = 0;
    for (int i = 0; i < numsSize; i++) sum += nums[i];
    if (sum % 2 != 0) return false;           // 奇数不可能平分
    int target = sum / 2;

    // dp[j]：用目前处理过的数，能否凑出和 j
    bool* dp = (bool*)calloc(target + 1, sizeof(bool));
    dp[0] = true;                             // 什么都不选，和为 0

    for (int i = 0; i < numsSize; i++) {
        int x = nums[i];
        // 倒序！保证 dp[j - x] 还是"没用 x 之前"的状态，每个数只用一次
        for (int j = target; j >= x; j--) {
            if (dp[j - x]) dp[j] = true;
        }
        if (dp[target]) break;                // 已经能凑出，提前结束
    }

    bool ans = dp[target];
    free(dp);
    return ans;
}
```

### 复杂度分析

- **时间复杂度 O(n × target)**。
- **空间复杂度 O(target)**。

---

## ⚠️ 第五步：小白常见错误

1. **忘记判断 sum 是奇数** → `target = sum / 2` 会向下取整，`[1,2]` 的 target 变成 1，能凑出来，错误地返回 true。
2. **一维写法正序遍历 j** → 一个数被用了多次，变成了"完全背包"。`[1,2,5]`（sum = 8，target = 4）正序时 1 可以用 4 次，错误地返回 true。
3. **`dp[0]` 忘记设为 true** → 什么都凑不出来，永远返回 false。
4. **暴力枚举所有子集** → 2²⁰⁰ 种，根本算不完。
5. **dp 数组开成 `target` 而不是 `target + 1`** → 访问 `dp[target]` 越界。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 |
|---|---|---|---|
| 暴力枚举子集 | O(2ⁿ) | O(n) | ❌ 超时 |
| 二维 DP | O(n × target) | O(n × target) | ⭐⭐ 好理解 |
| 一维 DP（倒序） | O(n × target) | O(target) | ⭐⭐⭐ 推荐 |

---

## 🔗 举一反三

- **494. 目标和**：给每个数加正负号，转化后也是 0-1 背包（求方案数）。
- **1049. 最后一块石头的重量 II**：尽量把石头分成两堆重量接近的，和本题几乎一样。
- **322. 零钱兑换**：完全背包，内层循环是**正序**的——对比一下和本题的区别。
