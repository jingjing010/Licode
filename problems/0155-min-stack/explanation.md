# 155. 最小栈 —— 小白详细题解

> 第一道"设计类"题：不再是写一个函数，而是用结构体设计一个**数据结构**。核心技巧是"**用空间换时间**，把每一步的最小值记下来"。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 做一个栈，除了普通的压栈、弹栈、看栈顶，还要能**随时立刻**说出栈里最小的数是多少。

走一遍示例：

| 操作 | 栈（底→顶） | 返回 |
|---|---|---|
| `MinStack()` | 空 | null |
| `push(-2)` | -2 | null |
| `push(0)` | -2, 0 | null |
| `push(-3)` | -2, 0, -3 | null |
| `getMin()` | -2, 0, -3 | **-3** |
| `pop()` | -2, 0 | null |
| `top()` | -2, 0 | **0** |
| `getMin()` | -2, 0 | **-2** |

**几个需要注意的细节：**

1. 最小值会随着 `pop` **变回去**：弹出 -3 后，最小值又变成了 -2。
2. 值的范围是整个 int（`-2^31` 到 `2^31 - 1`），**不能**用某个特殊值（比如 `INT_MAX`）当"空"的标记去参与运算后再比较。
3. 题目保证 `pop`、`top`、`getMin` 时栈不为空，不用处理空栈。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 力扣 C 语言的"设计类"写法

```c
typedef struct {
    int* data;     // 成员自己设计
    int top;
} MinStack;

MinStack* minStackCreate() { ... }        // 相当于构造函数
void minStackPush(MinStack* obj, int val) { ... }   // 相当于 obj.push(val)
void minStackFree(MinStack* obj) { ... }  // 相当于析构函数
```

C 没有"类"，所以用**结构体保存数据**，每个"方法"都是普通函数，第一个参数 `obj` 指向要操作的那个结构体。`obj->top` 就是 `(*obj).top`。

### 2. 在 `Create` 里必须 `malloc`

```c
MinStack* minStackCreate() {
    MinStack s;          // ❌ 局部变量，函数返回后就没了
    return &s;
}
```

要用 `malloc(sizeof(MinStack))` 在堆上创建，才能在函数返回后继续使用。

### 3. 用 `realloc` 让数组自动扩容

操作最多 3×10⁴ 次，可以直接开这么大；但更通用的做法是：先开 16 个，满了就 `realloc` 成两倍。

```c
if (obj->top == obj->cap) {
    obj->cap *= 2;
    obj->data = (int*)realloc(obj->data, sizeof(int) * obj->cap);
}
```

---

## 💡 第三步：思路一 —— 普通栈，`getMin` 时遍历

### 思路

`push`/`pop`/`top` 用数组模拟；`getMin` 时把栈里所有数扫一遍找最小值。

### 代码

```c
typedef struct {
    int* data;    // 栈数组
    int top;      // 元素个数
    int cap;      // 容量
} MinStack;

MinStack* minStackCreate() {
    MinStack* obj = (MinStack*)malloc(sizeof(MinStack));
    obj->cap = 16;
    obj->top = 0;
    obj->data = (int*)malloc(sizeof(int) * obj->cap);
    return obj;
}

void minStackPush(MinStack* obj, int val) {
    if (obj->top == obj->cap) {                 // 满了就扩容
        obj->cap *= 2;
        obj->data = (int*)realloc(obj->data, sizeof(int) * obj->cap);
    }
    obj->data[obj->top++] = val;
}

void minStackPop(MinStack* obj) {
    obj->top--;
}

int minStackTop(MinStack* obj) {
    return obj->data[obj->top - 1];
}

int minStackGetMin(MinStack* obj) {
    int m = obj->data[0];
    for (int i = 1; i < obj->top; i++) {        // 每次都扫一遍
        if (obj->data[i] < m) m = obj->data[i];
    }
    return m;
}

void minStackFree(MinStack* obj) {
    free(obj->data);
    free(obj);
}
```

### 复杂度分析

- `push`/`pop`/`top` 是 O(1)，但 **`getMin` 是 O(n)**，不满足题目"常数时间"的要求。本题数据量小，这样也能通过，但面试官想要的不是它。

---

## 🚀 第四步：思路二 —— 辅助栈记录"到这里为止的最小值"

### 思路

只用一个变量 `min` 记最小值行不行？不行：弹出最小值之后，**不知道第二小的是谁**。

解决办法：再开一个同样长度的数组 `mins`，`mins[i]` 记录**从栈底到第 i 个元素为止的最小值**。

- `push(x)`：`mins[top] = min(x, mins[top-1])`（栈空时就是 x）；
- `pop()`：两个数组一起弹，`mins` 自然"退回"到上一步的最小值；
- `getMin()`：直接返回 `mins[top-1]`。

### 手动模拟

| 操作 | data | mins | getMin |
|---|---|---|---|
| push(-2) | -2 | -2 | |
| push(0) | -2, 0 | -2, **-2** | |
| push(-3) | -2, 0, -3 | -2, -2, **-3** | |
| getMin | | | -3 |
| pop | -2, 0 | -2, -2 | |
| getMin | | | **-2** ✅ |

### 代码

```c
typedef struct {
    int* data;    // 普通栈
    int* mins;    // mins[i]：data[0..i] 中的最小值
    int top;      // 元素个数
    int cap;      // 容量
} MinStack;

MinStack* minStackCreate() {
    MinStack* obj = (MinStack*)malloc(sizeof(MinStack));
    obj->cap = 16;
    obj->top = 0;
    obj->data = (int*)malloc(sizeof(int) * obj->cap);
    obj->mins = (int*)malloc(sizeof(int) * obj->cap);
    return obj;
}

void minStackPush(MinStack* obj, int val) {
    if (obj->top == obj->cap) {                         // 两个数组一起扩容
        obj->cap *= 2;
        obj->data = (int*)realloc(obj->data, sizeof(int) * obj->cap);
        obj->mins = (int*)realloc(obj->mins, sizeof(int) * obj->cap);
    }
    int m = val;
    if (obj->top > 0 && obj->mins[obj->top - 1] < m) {
        m = obj->mins[obj->top - 1];                    // 和之前的最小值比较
    }
    obj->data[obj->top] = val;
    obj->mins[obj->top] = m;
    obj->top++;
}

void minStackPop(MinStack* obj) {
    obj->top--;                                         // 两个数组共用 top，一起弹出
}

int minStackTop(MinStack* obj) {
    return obj->data[obj->top - 1];
}

int minStackGetMin(MinStack* obj) {
    return obj->mins[obj->top - 1];                     // O(1)
}

void minStackFree(MinStack* obj) {
    free(obj->data);                                    // 先释放成员，再释放结构体
    free(obj->mins);
    free(obj);
}
```

### 复杂度分析

- **所有操作都是 O(1)**（扩容的代价平摊下来也是 O(1)）。
- **空间复杂度 O(n)**：多了一个 `mins` 数组。

---

## ⚠️ 第五步：小白常见错误

1. **只用一个变量记最小值** → `pop` 掉最小值后无法恢复，示例最后一步会返回 -3 而不是 -2。
2. **`Create` 里返回局部变量的地址** → 后续操作全是野指针。
3. **`Free` 时只 `free(obj)`** → 结构体里 `malloc` 出来的数组没释放，造成内存泄漏。顺序也要注意：先 `free(obj->data)`，再 `free(obj)`，反过来就访问了已释放的内存。
4. **栈空时 push 去读 `mins[top - 1]`** → `mins[-1]` 越界。要先判断 `top > 0`。
5. **扩容时只扩了 `data` 没扩 `mins`** → `mins` 写越界，可能在很久以后才崩溃，非常难查。
6. **用 `INT_MAX` 当初始最小值再做减法之类的运算** → 值本身就可能是 `INT_MAX` 或 `INT_MIN`，相减会溢出。本题只做比较，不做加减。

---

## 📊 第六步：两种方法对比

| 方法 | push/pop/top | getMin | 额外空间 | 建议 |
|---|---|---|---|---|
| 遍历求最小 | O(1) | O(n) | O(1) | 不满足题意 |
| 辅助最小值栈 | O(1) | O(1) | O(n) | 标准解法 |

---

## 🔗 举一反三

- **232. 用栈实现队列**、**225. 用队列实现栈**：同样是设计类，练习结构体 + 函数的写法。
- **716. 最大栈**：还要支持 `popMax`，需要更复杂的结构。
- **思考题**：能不能只用**一个栈**、额外 O(1) 空间实现？（提示：栈里存"当前值与最小值的差"，注意用 `long long` 防溢出。）
