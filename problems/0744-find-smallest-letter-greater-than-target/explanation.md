# 744. 寻找比目标字母大的最小字母 —— 小白详细题解

> 这是"找第一个 **>** target"的二分模板题（注意是严格大于）。另外它还会帮你搞清楚 C 语言里 `char` 到底是什么。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 一排按字母顺序排好的字母（可能有重复），找出**第一个比 target 大**的字母。如果一个都没有，就返回第一个字母（相当于"绕回开头"）。

拿 `letters = ["c","f","j"]` 来说：

| target | 比它大的字母 | 答案 | 理由 |
|---|---|---|---|
| "a" | c, f, j | "c" | 最小的是 c |
| "c" | f, j | "f" | c **不比** c 大，所以不能选 c |
| "j" | 无 | "c" | 没有比 j 大的，返回 letters[0] |

**几个需要注意的细节：**

1. 是**严格大于**，等于不算。示例 2 中 target = "c"，答案是 "f" 而不是 "c"。
2. 可能有重复字母，比如 `["x","x","y","y"]`。
3. 找不到时返回 `letters[0]`，不是返回空。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. `char` 本质上是一个小整数

在 C 语言里，`'a'` 其实就是整数 97（ASCII 码），`'b'` 是 98……`'z'` 是 122。所以字母可以**直接用 `<`、`>` 比较**，字母顺序就是数值大小顺序：

```c
char a = 'c', b = 'f';
if (a < b) printf("c 在 f 前面\n");   // 成立，因为 99 < 102
```

### 2. 单引号 vs 双引号

- `'c'` 是一个**字符**（`char` 类型，就是一个整数）
- `"c"` 是一个**字符串**（`char*` 类型，内存里是 `'c'` 和 `'\0'` 两个字节）

函数参数 `char target` 是字符，返回值 `char` 也是字符。题面里写的 `"a"` 只是力扣的显示格式。

### 3. `char* letters` 不是字符串

这里 `letters` 是一个"字符数组"，长度由 `lettersSize` 给出，**不要**用 `strlen(letters)` 求长度（不保证有 `'\0'` 结尾）。

---

## 💡 第三步：思路一 —— 从左到右扫（O(n)）

### 代码

```c
char nextGreatestLetter(char* letters, int lettersSize, char target) {
    for (int i = 0; i < lettersSize; i++) {
        if (letters[i] > target) {
            return letters[i];   // 第一个比 target 大的
        }
    }
    return letters[0];           // 没有比 target 大的，绕回开头
}
```

### 复杂度分析

- **时间复杂度 O(n)**，**空间复杂度 O(1)**。n ≤ 10⁴ 能过，但没有利用"有序"。

---

## 🚀 第四步：思路二 —— 二分查找"第一个 > target"

### 思路

数组有序，所有字母分成两部分：

```
letters:      x  x  y  y        target = 'x'
<= target?    是 是 否 否
                    ↑ 第一个 "否" 就是答案
```

左边一段 `<= target`，右边一段 `> target`。找右边那段的第一个——这正是"找第一个满足条件的位置"模板，条件是 `letters[mid] > target`。

### 区间定义与循环条件

- 区间：**左闭右开 `[lo, hi)`**，`lo = 0, hi = lettersSize`。答案可能是 `lettersSize`（表示一个都没找到）。
- `while (lo < hi)`。
- `letters[mid] <= target`：mid 不够大，答案在右边：`lo = mid + 1`
- `letters[mid] > target`：mid 可能就是答案，保留：`hi = mid`
- 结束后若 `lo == lettersSize`，说明没有比 target 大的，返回 `letters[0]`。

### 手动模拟（`letters = ["c","f","j"], target = 'c'`）

| 轮次 | lo | hi | mid | letters[mid] | <= 'c' ? | 操作 |
|---|---|---|---|---|---|---|
| 1 | 0 | 3 | 1 | 'f' | 否 | hi = 1 |
| 2 | 0 | 1 | 0 | 'c' | 是 | lo = 1 |
| 结束 | 1 | 1 | | | | 返回 letters[1] = 'f' ✅ |

### 代码

```c
char nextGreatestLetter(char* letters, int lettersSize, char target) {
    int lo = 0, hi = lettersSize;        // 左闭右开 [lo, hi)
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;    // 防溢出写法
        if (letters[mid] <= target) {
            lo = mid + 1;                // 不够大，答案在右边
        } else {
            hi = mid;                    // 够大了，mid 可能是答案
        }
    }
    // lo 是第一个 > target 的下标；等于 lettersSize 说明没有，绕回开头
    return lo < lettersSize ? letters[lo] : letters[0];
}
```

> `条件 ? A : B` 是三目运算符：条件成立取 A，否则取 B。

也可以写成取模的形式：`return letters[lo % lettersSize];`——`lo == lettersSize` 时 `lo % lettersSize == 0`。

### 复杂度分析

- **时间复杂度 O(log n)**，**空间复杂度 O(1)**。

---

## ⚠️ 第五步：小白常见错误

1. **条件写成 `letters[mid] < target`** → 这是在找"第一个 >= target"，target 本身在数组里时会返回 target（示例 2 会错误地返回 'c'）。
2. **`hi` 初始化成 `lettersSize - 1`** → 用左闭右开写法时，找不到的情况就判断不出来了。
3. **忘记处理"找不到"** → `lo == lettersSize` 时直接返回 `letters[lo]`，越界读取。
4. **用 `strlen(letters)` 求长度** → letters 不一定以 `'\0'` 结尾，结果不可靠。
5. **返回 `"c"` 这样的字符串** → 返回类型是 `char`，应该返回字符本身。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 顺序扫描 | O(n) | O(1) | ⭐ | 最直观 |
| 二分查找 | O(log n) | O(1) | ⭐⭐ | 练习"第一个 > target"模板 |

> 🎯 **学习建议**：对比 35 题（第一个 `>=` target）和本题（第一个 `>` target），它们只差在 `<` 和 `<=` 一个符号上。34 题就是把这两个组合起来。

---

## 🔗 举一反三

- **35. 搜索插入位置**：第一个 `>=` target。
- **34. 在排序数组中查找元素的第一个和最后一个位置**：第一个 `>=` target 和第一个 `>` target 再减 1。
- **思考题**：如果要找"**小于** target 的最大字母"（找不到就返回最后一个），代码要怎么改？
