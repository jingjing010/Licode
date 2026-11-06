# 278. 第一个错误的版本 —— 小白详细题解

> 这道题是"二分找边界"的标准模板题，同时它有一个经典陷阱：**`(lo + hi) / 2` 会溢出**。很多人第一次提交就栽在这里。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 有 `n` 个版本，从某个版本开始全都坏了（后面的版本都基于它，所以也全坏）。你有一个"检测器" `isBadVersion(v)`，问它"版本 v 坏了吗"。请用**尽量少的提问次数**找出第一个坏版本。

拿示例 1 `n = 5, bad = 4` 来说：

| 版本号 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| isBadVersion | false | false | false | **true** | true |

版本状态一定是"**一段 false，接着一段 true**"，我们要找的就是**第一个 true** 的位置。

**几个需要注意的细节：**

1. 版本号从 **1** 开始，不是 0。
2. 你拿不到 `bad`，只能通过调用 `isBadVersion` 去"问"。
3. `n` 最大是 `2^31 - 1 = 2147483647`，也就是 `int` 的最大值。
4. 本 OJ 限制调用次数（n 最大时 64 次），一个一个问肯定不行。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. "预定义 API" 是什么？

```c
// The API isBadVersion is defined for you.
// bool isBadVersion(int version);
```

这两行是**注释**，告诉你：系统已经写好了 `isBadVersion` 函数，你**直接调用**就行，不用（也不能）自己再写一遍。`bool` 类型来自 `<stdbool.h>`，取值 `true` / `false`。

### 2. int 溢出 —— 本题的头号陷阱

`int` 能表示的最大值是 `2147483647`（`INT_MAX`）。如果 `lo = 2000000000, hi = 2147483647`：

```c
int mid = (lo + hi) / 2;          // ❌ lo + hi = 4147483647 超过 INT_MAX，溢出成负数！
int mid2 = lo + (hi - lo) / 2;    // ✅ hi - lo 不会溢出，结果正确
```

C 语言里**有符号整数溢出是"未定义行为"**，实际效果通常是"绕一圈"变成负数，然后你会拿一个负数版本号去调用 `isBadVersion`。

另一种安全写法是先转成 `long long`：`int mid = (int)(((long long)lo + hi) / 2);`。

---

## 💡 第三步：思路一 —— 从 1 开始挨个问（会超出调用次数）

### 思路

从版本 1 开始，一个一个问，第一个返回 `true` 的就是答案。

### 手动模拟（`n = 5, bad = 4`）

| 问的版本 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| 结果 | false | false | false | **true** → 返回 4 |

### 代码

```c
// ❌ 思路正确，但 n 很大时要问上亿次：超出本题调用上限，在力扣上也会超时
int firstBadVersion(int n) {
    for (int v = 1; v < n; v++) {
        if (isBadVersion(v)) {
            return v;            // 第一个坏版本
        }
    }
    return n;                    // 前面都没坏，那第 n 个一定是坏的
}
```

### 复杂度分析

- **时间复杂度 O(n)**：`n = 2^31-1` 时最多要问 21 亿次。
- **空间复杂度 O(1)**。

---

## 🚀 第四步：思路二 —— 二分查找（标准答案）

### 思路

序列是 `false false ... false true true ... true`，具有**单调性**。随便问中间一个版本 `mid`：

- `isBadVersion(mid) == true`：mid 坏了，第一个坏版本**在 mid 或者 mid 左边**，保留 mid：`hi = mid`
- `isBadVersion(mid) == false`：mid 是好的，第一个坏版本**一定在 mid 右边**：`lo = mid + 1`

### 区间定义与循环条件

- 区间：**闭区间 `[lo, hi]`**，含义是"答案一定在这里面"。初始 `lo = 1, hi = n`（题目保证 n 一定是坏的，所以答案就在 `[1, n]` 里）。
- 循环条件：`while (lo < hi)`。`lo == hi` 时只剩一个候选，就是答案，**不需要再问**。
- 中点：`mid = lo + (hi - lo) / 2`，向下取整，保证 `lo <= mid < hi`，所以 `hi = mid` 一定会让区间变小，不会死循环。

### 手动模拟（`n = 5, bad = 4`）

| 轮次 | lo | hi | mid | isBadVersion(mid) | 操作 |
|---|---|---|---|---|---|
| 1 | 1 | 5 | 3 | false | lo = 4 |
| 2 | 4 | 5 | 4 | true | hi = 4 |
| 结束 | 4 | 4 | | | 返回 4 ✅ |

只问了 2 次！`n = 2^31-1` 时也只要问约 31 次。

### 代码

```c
// The API isBadVersion is defined for you.
// bool isBadVersion(int version);

int firstBadVersion(int n) {
    int lo = 1;                  // 答案在闭区间 [lo, hi] 中
    int hi = n;

    while (lo < hi) {            // 区间里还有不止一个候选
        int mid = lo + (hi - lo) / 2;   // 防溢出！不能写 (lo + hi) / 2
        if (isBadVersion(mid)) {
            hi = mid;            // mid 是坏的：答案是 mid 或在它左边
        } else {
            lo = mid + 1;        // mid 是好的：答案在它右边
        }
    }
    return lo;                   // lo == hi，就是第一个坏版本
}
```

### 另一种常见写法：记录答案的闭区间二分

```c
int firstBadVersion(int n) {
    int lo = 1, hi = n;
    int ans = n;                 // 先假设答案是 n
    while (lo <= hi) {           // 区间 [lo, hi] 非空就继续
        int mid = lo + (hi - lo) / 2;
        if (isBadVersion(mid)) {
            ans = mid;           // mid 是坏的，记下来，再去左边找更早的
            hi = mid - 1;
        } else {
            lo = mid + 1;
        }
    }
    return ans;
}
```

两种写法都对，关键是**区间定义、循环条件、更新方式三者要配套**。

### 复杂度分析

- **时间复杂度 O(log n)**：每问一次，区间减半。
- **空间复杂度 O(1)**。

---

## ⚠️ 第五步：小白常见错误

1. **`mid = (lo + hi) / 2`** → `n = 2147483647` 时 `lo + hi` 溢出变成负数，传给 `isBadVersion` 一个负数版本号（本 OJ 会直接报"参数越界"）。
2. **`while (lo < hi)` 搭配 `hi = mid - 1`** → mid 本身是坏版本时把它扔掉了，可能错过答案。
3. **`while (lo <= hi)` 搭配 `hi = mid`** → `lo == hi` 时 `mid == hi`，`hi = mid` 不变，**死循环**，调用次数爆表。
4. **`lo` 从 0 开始** → 版本号从 1 开始，`isBadVersion(0)` 是非法调用。
5. **把 `lo`、`hi` 声明成 `long long` 却直接传给 `isBadVersion`** → 能用，但要确认传入的值在 `[1, n]` 内；更简单的做法是 `int` + 防溢出中点。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 调用次数（n = 2^31-1） | 难度 | 建议 |
|---|---|---|---|---|
| 顺序询问 | O(n) | 最多约 21 亿次 | ⭐ | 只用来理解题意 |
| 二分查找 | O(log n) | 约 31 次 | ⭐⭐ | 标准答案，牢记防溢出 |

> 🎯 **学习建议**：这道题就是"找第一个满足条件的位置"模板：`lo = mid + 1` / `hi = mid`，`while (lo < hi)`，最后返回 `lo`。

---

## 🔗 举一反三

- **35. 搜索插入位置**：找第一个 `>= target` 的位置，同一个模板。
- **374. 猜数字大小**：同样是"通过 API 提问"的二分，但 API 返回三种结果。
- **69. x 的平方根**：在答案范围上二分，同样要注意乘法溢出。
- **思考题**：如果题目不保证 `n` 是坏的（可能全是好版本，此时返回 `-1`），代码要怎么改？
