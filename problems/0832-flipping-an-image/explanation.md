# 832. 翻转图像 —— 小白详细题解

> 一道纯模拟题，重点练习两件事：**双指针反转数组**，以及力扣返回二维数组时的 **`returnColumnSizes`** 写法。

---

## 📖 第一步：先读懂题目

对每一行做两件事：

1. **水平翻转**：把这一行倒过来，`[1,1,0]` → `[0,1,1]`
2. **反转**：0 变 1，1 变 0，`[0,1,1]` → `[1,0,0]`

拿示例 1 来说：

| 行 | 原来 | 翻转后 | 再反转 |
|---|---|---|---|
| 0 | [1,1,0] | [0,1,1] | [1,0,0] |
| 1 | [1,0,1] | [1,0,1] | [0,1,0] |
| 2 | [0,0,0] | [0,0,0] | [1,1,1] |

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 返回二维数组的三件套

```c
int** flipAndInvertImage(int** image, int imageSize, int* imageColSize,
                         int* returnSize, int** returnColumnSizes)
```

返回一个二维数组时，调用者需要知道：**有几行**、**每行有几列**。所以你要做三件事：

| 你要做的事 | 写法 |
|---|---|
| 返回矩阵本身 | `return image;`（原地修改后直接返回原矩阵也可以） |
| 告诉调用者有几行 | `*returnSize = imageSize;` |
| 告诉调用者每行几列 | `*returnColumnSizes = malloc(...)`，再逐个填写 |

`returnColumnSizes` 的类型是 `int**`——它是"一个 `int*` 变量的地址"。你要 `malloc` 一个 `int` 数组，把它的地址**写进** `*returnColumnSizes`：

```c
*returnColumnSizes = (int*)malloc(sizeof(int) * imageSize);   // 申请数组
for (int i = 0; i < imageSize; i++) {
    (*returnColumnSizes)[i] = imageColSize[i];                // 注意括号！
}
```

> ⚠️ `(*returnColumnSizes)[i]` 的括号不能省。`*returnColumnSizes[i]` 会被理解成 `*(returnColumnSizes[i])`，意思完全不同，会写到错误的地方。

### 2. 0/1 互换的三种写法

```c
x = 1 - x;      // 1-0=1, 1-1=0
x = !x;         // !0 = 1, !1 = 0
x ^= 1;         // 异或：0^1=1, 1^1=0
```

---

## 💡 第三步：思路一 —— 老老实实分两步

### 思路

对每一行：

1. 用**双指针**反转：`l` 从左、`r` 从右，交换 `row[l]` 和 `row[r]`，然后 `l++`、`r--`，直到相遇。
2. 再把整行每个数 `^= 1`。

### 代码

```c
int** flipAndInvertImage(int** image, int imageSize, int* imageColSize, int* returnSize, int** returnColumnSizes) {
    for (int i = 0; i < imageSize; i++) {
        int* row = image[i];             // 第 i 行
        int n = imageColSize[i];         // 这一行的长度

        // 第 1 步：双指针反转这一行
        int l = 0, r = n - 1;
        while (l < r) {
            int t = row[l];              // 交换 row[l] 和 row[r]
            row[l] = row[r];
            row[r] = t;
            l++;
            r--;
        }
        // 第 2 步：每个数 0/1 互换
        for (int j = 0; j < n; j++) {
            row[j] ^= 1;
        }
    }

    // 告诉调用者：结果有几行、每行几列
    *returnSize = imageSize;
    *returnColumnSizes = (int*)malloc(sizeof(int) * imageSize);
    for (int i = 0; i < imageSize; i++) {
        (*returnColumnSizes)[i] = imageColSize[i];
    }
    return image;                        // 原地修改，直接返回原矩阵
}
```

### 复杂度分析

- **时间复杂度 O(n²)**：每个元素被交换一次、取反一次。
- **空间复杂度 O(1)**（不算返回的列数数组）。

---

## 🚀 第四步：思路二 —— 交换的同时取反（一遍搞定）

### 思路

翻转后位置 `l` 的值是原来的 `row[r]`，再取反就是 `row[r] ^ 1`。所以交换时直接写入取反后的值即可：

```
row[l] = 原 row[r] ^ 1
row[r] = 原 row[l] ^ 1
```

当行长是**奇数**时，最后 `l == r` 指向中间那个数，它不用交换（翻转后还在原位），但**仍然要取反**。

> 💡 有趣的观察：如果 `row[l] != row[r]`（一个 0 一个 1），交换再取反后……和原来一模一样！只有 `row[l] == row[r]` 时才真的会变。

### 手动模拟（`[1,1,0]`）

| 步骤 | l | r | 操作 | 行 |
|---|---|---|---|---|
| 1 | 0 | 2 | row[0] = 0^1 = 1, row[2] = 1^1 = 0 | [1,1,0] |
| 2 | 1 | 1 | l == r，中间取反 row[1] = 1^1 = 0 | [1,0,0] |

### 代码

```c
int** flipAndInvertImage(int** image, int imageSize, int* imageColSize, int* returnSize, int** returnColumnSizes) {
    for (int i = 0; i < imageSize; i++) {
        int* row = image[i];
        int l = 0, r = imageColSize[i] - 1;
        while (l < r) {
            int t = row[l];
            row[l] = row[r] ^ 1;         // 交换 + 取反
            row[r] = t ^ 1;
            l++;
            r--;
        }
        if (l == r) row[l] ^= 1;         // 奇数长度：中间元素只取反
    }

    *returnSize = imageSize;
    *returnColumnSizes = (int*)malloc(sizeof(int) * imageSize);
    for (int i = 0; i < imageSize; i++) {
        (*returnColumnSizes)[i] = imageColSize[i];
    }
    return image;
}
```

### 复杂度分析

- **时间复杂度 O(n²)**，但每行只走一半。
- **空间复杂度 O(1)**。

---

## ⚠️ 第五步：小白常见错误

1. **没设置 `*returnSize` 或 `*returnColumnSizes`** → 调用者不知道矩阵多大，输出为空 `[]` 或程序崩溃。
2. **写成 `*returnColumnSizes[i] = ...`** → 运算符优先级问题，必须写 `(*returnColumnSizes)[i]`。
3. **反转循环写成 `for (j = 0; j < n; j++) 交换 row[j] 和 row[n-1-j]`** → 走完整行等于交换了两次，又换回去了！只能走一半（`l < r`）。
4. **思路二忘了处理奇数长度的中间元素** → `[[1,1,0]]` 中间的 1 没取反，结果 `[1,1,0]` 而不是 `[1,0,0]`。
5. **用 `~x` 取反** → `~` 是按位取反，`~0 = -1`、`~1 = -2`，不是 0/1 互换。要用 `x ^ 1`、`1 - x` 或 `!x`。

---

## 📊 第六步：两种方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 先翻转再取反 | O(n²) | O(1) | ⭐ | 按题意直写，最不容易错 |
| 交换同时取反 | O(n²) | O(1) | ⭐⭐ | 少走一遍，注意中间元素 |

---

## 🔗 举一反三

- **344. 反转字符串**：双指针反转的最基础练习。
- **48. 旋转图像**：矩阵顺时针旋转 90° = 先转置再每行反转。
- **867. 转置矩阵**：同样要返回二维数组，练习 `returnColumnSizes`。
