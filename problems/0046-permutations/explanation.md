# 46. 全排列 —— 小白详细题解

> 这是**回溯算法**的第一课。回溯 = 「做选择 → 递归 → 撤销选择」，学会这个模板，后面的子集、组合、N 皇后都是它的变形。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 给你几个**互不相同**的数，把它们所有可能的**排队方式**都列出来。

`[1,2,3]` 排队：第 1 个位置有 3 种选法，第 2 个位置剩 2 种，第 3 个位置剩 1 种，一共 3 × 2 × 1 = **6** 种。

把选择过程画成一棵「决策树」：

| 第 1 位 | 第 2 位 | 第 3 位 | 得到的排列 |
|---|---|---|---|
| 1 | 2 | 3 | [1,2,3] |
| 1 | 3 | 2 | [1,3,2] |
| 2 | 1 | 3 | [2,1,3] |
| 2 | 3 | 1 | [2,3,1] |
| 3 | 1 | 2 | [3,1,2] |
| 3 | 2 | 1 | [3,2,1] |

**几个需要注意的细节：**

1. n 个数的全排列有 **n!** 个，n ≤ 6 时最多 720 个。
2. 顺序任意，本 OJ 会排序后再比较，你不用管输出顺序。
3. 数字互不相同，所以不用考虑去重。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 返回二维数组：`int**` + `returnSize` + `returnColumnSizes`

```c
int** permute(int* nums, int numsSize, int* returnSize, int** returnColumnSizes)
```

| 参数 | 你要做什么 |
|---|---|
| 返回值 `int**` | `malloc` 一个「行指针数组」，每一行再 `malloc` 一个 `int` 数组 |
| `*returnSize` | 写入一共有多少行 |
| `*returnColumnSizes` | `malloc` 一个 `int` 数组记录每行长度，**把它的地址写进 `*returnColumnSizes`** |

`returnColumnSizes` 是 `int**`（指针的指针），因为你要在函数里**修改调用者的一个 `int*` 变量**。和 `*returnSize = 6` 改一个 `int` 是同一个道理。

```c
*returnColumnSizes = (int*)malloc(sizeof(int) * total);  // 让调用者的指针指向新数组
(*returnColumnSizes)[i] = numsSize;                      // 括号不能省！
```

> ❓ 为什么要括号？`[]` 的优先级比 `*` 高，`*returnColumnSizes[i]` 会被理解成 `*(returnColumnSizes[i])`，访问到错误的内存。

### 2. 递归时通过指针「带出」结果

递归函数里要往结果里加一行，并让计数 `+1`。计数器必须用**指针**传进去（`int* cnt`），否则递归里改的只是副本。

---

## 💡 第三步：思路一 —— 回溯 + used 数组

### 思路

用 `path[]` 存「正在排的这一队」，`depth` 表示已经排了几个人，`used[i]` 表示 `nums[i]` 是否已经在队里。

1. 如果 `depth == n`：队排满了，把 `path` **复制**一份存进结果。
2. 否则，枚举每个没用过的 `nums[i]`：
   - **做选择**：`used[i] = true`，`path[depth] = nums[i]`
   - **递归**：去排第 `depth + 1` 个位置
   - **撤销选择**：`used[i] = false`（这样回到上一层后，`nums[i]` 还能被放到别的位置）

### 手动模拟（`[1,2,3]` 的前几步）

| 动作 | path | used |
|---|---|---|
| 选 1 | [1] | T F F |
| 选 2 | [1,2] | T T F |
| 选 3，满了，记录 [1,2,3] | [1,2,3] | T T T |
| 撤销 3 | [1,2] | T T F |
| 撤销 2 | [1] | T F F |
| 选 3 | [1,3] | T F T |
| 选 2，满了，记录 [1,3,2] | [1,3,2] | T T T |

### 代码

```c
// depth：已经排好了几个位置；path：当前排列；used[i]：nums[i] 是否已用
void backtrack(int* nums, int n, int depth, int* path, bool* used,
               int** res, int* cnt) {
    if (depth == n) {                                   // 排满了，记录答案
        res[*cnt] = (int*)malloc(sizeof(int) * n);
        for (int i = 0; i < n; i++) res[*cnt][i] = path[i];   // 必须复制，path 之后还会被改
        (*cnt)++;
        return;
    }
    for (int i = 0; i < n; i++) {
        if (used[i]) continue;          // 已经在队里了，跳过
        used[i] = true;                 // 做选择
        path[depth] = nums[i];
        backtrack(nums, n, depth + 1, path, used, res, cnt);  // 排下一个位置
        used[i] = false;                // 撤销选择
    }
}

int** permute(int* nums, int numsSize, int* returnSize, int** returnColumnSizes) {
    int total = 1;
    for (int i = 2; i <= numsSize; i++) total *= i;     // n! 个排列

    int** res = (int**)malloc(sizeof(int*) * total);
    int path[6];                                        // n 最大是 6
    bool used[6] = {false};
    int cnt = 0;
    backtrack(nums, numsSize, 0, path, used, res, &cnt);

    *returnSize = cnt;
    *returnColumnSizes = (int*)malloc(sizeof(int) * total);
    for (int i = 0; i < cnt; i++) (*returnColumnSizes)[i] = numsSize;   // 每行长度都是 n
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n · n!)**：一共 n! 个排列，每个复制需要 O(n)。
- **空间复杂度 O(n)**：递归深度 n，加上 `path` 和 `used`（结果本身不算）。

---

## 🚀 第四步：思路二 —— 原地交换（不用 used 数组）

### 思路

把数组分成两半：`nums[0..depth-1]` 是已经排好的，`nums[depth..n-1]` 是还没用的。

排第 `depth` 个位置时，依次把 `nums[depth..n-1]` 中的每一个**交换**到 `depth` 位置上，递归排下一位，回来后**再换回去**（撤销）。

这样「没用过的数」永远在数组右半边，不需要 `used[]`。

### 代码

```c
void swap(int* a, int* b) {
    int t = *a; *a = *b; *b = t;
}

void backtrack(int* nums, int n, int depth, int** res, int* cnt) {
    if (depth == n) {
        res[*cnt] = (int*)malloc(sizeof(int) * n);
        memcpy(res[*cnt], nums, sizeof(int) * n);   // 当前 nums 就是一个排列
        (*cnt)++;
        return;
    }
    for (int i = depth; i < n; i++) {
        swap(&nums[depth], &nums[i]);               // 让 nums[i] 坐到第 depth 个位置
        backtrack(nums, n, depth + 1, res, cnt);
        swap(&nums[depth], &nums[i]);               // 换回来（撤销）
    }
}

int** permute(int* nums, int numsSize, int* returnSize, int** returnColumnSizes) {
    int total = 1;
    for (int i = 2; i <= numsSize; i++) total *= i;
    int** res = (int**)malloc(sizeof(int*) * total);
    int cnt = 0;
    backtrack(nums, numsSize, 0, res, &cnt);
    *returnSize = cnt;
    *returnColumnSizes = (int*)malloc(sizeof(int) * total);
    for (int i = 0; i < cnt; i++) (*returnColumnSizes)[i] = numsSize;
    return res;
}
```

> 💬 `memcpy(目标, 源, 字节数)`：一次性复制一整块内存，等价于写一个 for 循环逐个赋值。

### 复杂度分析

- **时间复杂度 O(n · n!)**，**空间复杂度 O(n)**（递归栈），省掉了 `used` 和 `path`。

---

## ⚠️ 第五步：小白常见错误

1. **直接把 `path` 存进结果**：`res[cnt] = path;` 所有行都指向同一块内存，最后全变成同一个排列。必须 `malloc` 新数组再复制。
2. **忘记撤销 `used[i] = false`**：第一个排列 `[1,2,3]` 之后所有数都被标记为已用，只能得到 1 个答案。
3. **`*returnColumnSizes[i] = n` 少了括号**：运算符优先级问题，会写到错误的内存，通常直接崩溃。
4. **计数器按值传递**：`void backtrack(..., int cnt)` 里 `cnt++` 不会影响外面，最后 `returnSize` 还是 0。要传 `&cnt`，函数里用 `(*cnt)++`。
5. **`*cnt++` 写法**：`*cnt++` 等于 `*(cnt++)`，是把**指针**往后移，不是把计数加 1。要写 `(*cnt)++`。

---

## 📊 第六步：两种方法对比

| 方法 | 时间复杂度 | 额外空间 | 难度 | 建议 |
|---|---|---|---|---|
| used 数组回溯 | O(n · n!) | O(n) | ⭐⭐ | 通用模板，必须掌握 |
| 原地交换 | O(n · n!) | O(n) 递归栈 | ⭐⭐⭐ | 更省空间，但输出不是字典序 |

> 🎯 **学习建议**：把思路一的「做选择 → 递归 → 撤销选择」背成肌肉记忆，它是所有回溯题的骨架。

---

## 🔗 举一反三

- **47. 全排列 II**：数组里有重复数字，要先排序，再跳过「和前一个相同且前一个没用过」的数。
- **78. 子集**、**39. 组合总和**：同样的回溯框架，只是「选择列表」和「记录答案的时机」不同。
- **51. N 皇后**：每一行选一列，本质上是一个带限制条件的全排列。
- **思考题**：如果只要求输出第 k 个排列（第 60 题），还需要把所有排列都生成出来吗？
