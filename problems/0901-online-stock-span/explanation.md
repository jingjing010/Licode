# 901. 股票价格跨度 —— 小白详细题解

> 一道"设计类 + 单调栈"的题。数据是**一个一个**来的（在线），我们要边接收边回答。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 每天告诉你一个股价，你要立刻回答：**从今天往回数，连续有几天的价格都 ≤ 今天**（今天自己也算）。

示例：

| 第几天 | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| 价格 | 100 | 80 | 60 | 70 | 60 | 75 | 85 |
| 往回数，遇到第一个**更贵**的是哪天 | 无 | 0 | 1 | 1 | 3 | 1 | 0 |
| 跨度 | 1 | 1 | 1 | 2 | 1 | **4** | 6 |

第 5 天价格 75：往回看 60、70、60 都 ≤ 75，再往回 80 > 75 停下，所以跨度 = 3 + 1（今天）= **4**。

**几个需要注意的细节：**

1. "小于**或等于**"：相等的价格也算进跨度。
2. 跨度至少是 1（今天自己）。
3. 只能往回看**连续**的天数，中间被一个更贵的打断就停。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 设计类题目的写法

力扣 C 语言用"结构体 + 一组函数"模拟面向对象：

```c
typedef struct {
    int* price;     // 成员由你自己定义
    int top;
} StockSpanner;

StockSpanner* stockSpannerCreate() {                 // 相当于构造函数
    StockSpanner* obj = (StockSpanner*)malloc(sizeof(StockSpanner));
    obj->top = 0;                                    // 一定要初始化！
    return obj;
}
```

- `typedef struct {...} StockSpanner;`：以后可以直接用 `StockSpanner` 当类型名。
- `obj->top` 等价于 `(*obj).top`：通过指针访问结构体成员。
- 结构体必须用 `malloc` 放在堆上，返回局部变量的地址是错的。

### 2. 动态扩容 `realloc`

不知道会调用多少次 `next` 时，可以先开小数组，满了就翻倍：

```c
if (obj->top == obj->cap) {
    obj->cap *= 2;
    obj->price = (int*)realloc(obj->price, sizeof(int) * obj->cap);   // 旧数据会被保留
}
```

（本题最多 10⁴ 次调用，直接开 10⁴ 大小的数组也可以。）

### 3. `Free` 要释放干净

结构体里 `malloc` 的数组要先 `free`，最后再 `free(obj)`。顺序反了就访问不到成员了。

---

## 💡 第三步：思路一 —— 记下所有价格，每次往回数

### 思路

把每天的价格都存进数组。`next(price)` 时，从昨天开始往回走，只要价格 ≤ 今天就继续，遇到更贵的就停。

### 手动模拟（第 5 天，price = 75）

| 往回看第几天 | 价格 | ≤ 75 吗？ | 跨度 |
|---|---|---|---|
| 今天 | 75 | | 1 |
| 4 | 60 | ✅ | 2 |
| 3 | 70 | ✅ | 3 |
| 2 | 60 | ✅ | 4 |
| 1 | 80 | ❌ 停 | **4** |

### 代码

```c
typedef struct {
    int* prices;   // 所有历史价格
    int n;         // 已经有几天
} StockSpanner;

StockSpanner* stockSpannerCreate() {
    StockSpanner* obj = (StockSpanner*)malloc(sizeof(StockSpanner));
    obj->prices = (int*)malloc(sizeof(int) * 10000);   // 最多调用 10^4 次
    obj->n = 0;
    return obj;
}

int stockSpannerNext(StockSpanner* obj, int price) {
    int j = obj->n - 1;                        // 从昨天开始往回看
    while (j >= 0 && obj->prices[j] <= price) {
        j--;                                   // 不比今天贵，继续往回
    }
    int span = obj->n - j;                     // j 是第一个更贵的那天（或 -1）
    obj->prices[obj->n++] = price;             // 把今天记下来
    return span;
}

void stockSpannerFree(StockSpanner* obj) {
    free(obj->prices);
    free(obj);
}
```

### 复杂度分析

- **时间复杂度**：单次 `next` 最坏 O(n)，总共 O(n²)。价格一直上涨时，每次都要数回第 0 天，10⁴ 次约 5×10⁷ 步，本题勉强能过。
- **空间复杂度 O(n)**。

---

## 🚀 第四步：思路二 —— 单调栈（跳着往回数）

### 为什么能优化？

看第 6 天 price = 85：思路一要一天一天地看 75、60、70、60、80。
可是第 5 天的 75 已经算过跨度 4 了——意思是"75 往前的 3 天都 ≤ 75"。既然 85 ≥ 75，那这 4 天**整块都 ≤ 85**，可以一步跳过！

所以我们用栈保存 `(价格, 跨度)`：

1. 今天的跨度先设为 1。
2. 只要栈顶价格 ≤ 今天：弹出栈顶，把它的跨度**加到今天**上（相当于一口气跳过那么多天）。
3. 把 `(今天价格, 今天跨度)` 压栈。

被弹出的天数永远不会再被用到：以后的日子要么被今天挡住，要么连今天一起跳过。所以栈里的价格从底到顶**严格递减**。

### 手动模拟（栈里写成 `价格(跨度)`）

| 天 | price | 弹出 | 今天跨度 | 栈（底→顶） |
|---|---|---|---|---|
| 0 | 100 | | 1 | 100(1) |
| 1 | 80 | | 1 | 100(1) 80(1) |
| 2 | 60 | | 1 | 100(1) 80(1) 60(1) |
| 3 | 70 | 60(1) | 1+1 = 2 | 100(1) 80(1) 70(2) |
| 4 | 60 | | 1 | 100(1) 80(1) 70(2) 60(1) |
| 5 | 75 | 60(1)、70(2) | 1+1+2 = **4** | 100(1) 80(1) 75(4) |
| 6 | 85 | 75(4)、80(1) | 1+4+1 = **6** | 100(1) 85(6) |

输出 `[null,1,1,1,2,1,4,6]` ✅

### 代码

```c
typedef struct {
    int* price;   // 栈：价格
    int* span;    // 栈：对应的跨度
    int top;      // 栈里元素个数
} StockSpanner;

StockSpanner* stockSpannerCreate() {
    StockSpanner* obj = (StockSpanner*)malloc(sizeof(StockSpanner));
    obj->price = (int*)malloc(sizeof(int) * 10000);   // 最多 10^4 次 next，栈不会更深
    obj->span = (int*)malloc(sizeof(int) * 10000);
    obj->top = 0;
    return obj;
}

int stockSpannerNext(StockSpanner* obj, int price) {
    int span = 1;                                   // 今天自己
    // 栈顶那天不比今天贵：它和它"罩着"的天数整块并入今天
    while (obj->top > 0 && obj->price[obj->top - 1] <= price) {
        obj->top--;
        span += obj->span[obj->top];
    }
    obj->price[obj->top] = price;                   // 今天入栈
    obj->span[obj->top] = span;
    obj->top++;
    return span;
}

void stockSpannerFree(StockSpanner* obj) {
    free(obj->price);
    free(obj->span);
    free(obj);
}
```

### 复杂度分析

- **时间复杂度**：每天最多入栈一次、出栈一次，n 次调用总共 O(n)，**均摊每次 O(1)**。
- **空间复杂度 O(n)**：价格一直下降时栈里有 n 个元素。

---

## ⚠️ 第五步：小白常见错误

1. **弹栈条件写成 `<`** → 相等的价格也应该算进跨度。`[5,5,5]` 正确答案是 `[1,2,3]`，用 `<` 会得到 `[1,1,1]`。
2. **只存价格不存跨度** → 弹出时不知道这一天"罩着"多少天，跨度会算少。
3. **弹出时只 `span++`** → 应该加上弹出元素的跨度 `span += obj->span[...]`，而不是 1。
4. **`stockSpannerCreate` 里忘了 `obj->top = 0`** → `malloc` 的内存是垃圾值，`top` 可能是个随机大数，直接崩溃。
5. **在 `Free` 里先 `free(obj)` 再 `free(obj->price)`** → `obj` 已经被释放，再访问它的成员是未定义行为。
6. **把结构体定义成局部变量再返回地址** → `StockSpanner s; return &s;` 函数返回后这块内存就失效了。

---

## 📊 第六步：方法对比

| 方法 | 单次 next 时间 | 总时间 | 空间 | 难度 |
|---|---|---|---|---|
| 存所有价格往回数 | 最坏 O(n) | O(n²) | O(n) | ⭐ |
| 单调栈 | 均摊 O(1) | O(n) | O(n) | ⭐⭐ |

---

## 🔗 举一反三

- **739. 每日温度**：往**后**找第一个更大的数，同样是单调栈。
- **84. 柱状图中最大的矩形**：往左右找第一个更小的数。
- **155. 最小栈**：另一道"设计类 + 栈"的经典题。
- **思考题**：如果跨度定义改成"价格**严格小于**今天的连续天数"，代码要改哪一个字符？
