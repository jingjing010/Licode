# 9055. 表驱动状态机：交通灯控制器 —— 小白详细题解

> 状态机是嵌入式软件的"骨架"。面试官常问："状态机有哪几种写法？`switch-case` 和表驱动各有什么优缺点？"这道题代码很短，重点是理解**把逻辑变成数据**的思想。

---

## 📖 第一步：先读懂题目

状态机三要素：

- **状态**：系统现在处于什么情况（红灯、绿灯、黄灯、黄闪）
- **事件**：发生了什么（定时到、检测到故障、故障恢复）
- **转移**：在某状态下发生某事件后，变成什么状态

题目把"转移"写成了一张表，`table[当前状态][事件] = 新状态`，`-1` 表示忽略。

示例 1 逐步查表：

| 第几个事件 | 当前状态 | 事件 | 查 table[cur][e] | 新状态 |
|---|---|---|---|---|
| 0 | 0 红 | 0 定时 | table[0][0] = 1 | 1 绿 |
| 1 | 1 绿 | 0 定时 | table[1][0] = 2 | 2 黄 |
| 2 | 2 黄 | 0 定时 | table[2][0] = 0 | 0 红 |
| 3 | 0 红 | 0 定时 | 1 | 1 绿 |
| 4 | 1 绿 | 1 故障 | table[1][1] = 3 | 3 黄闪 |
| 5 | 3 黄闪 | 0 定时 | table[3][0] = **-1** | 3（忽略，不变） |
| 6 | 3 黄闪 | 2 恢复 | table[3][2] = 0 | 0 红 |

输出 `[1,2,0,1,3,3,0]`。

**容易忽略的细节：**

1. `-1` 时状态**不变**，不是变成 -1，也不是回到初始状态。
2. 输出的是"处理完每个事件**之后**"的状态，不包含初始状态。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 先看看 `switch-case` 写法（对比用）

如果只写交通灯，最直观的写法是嵌套 `switch`：

```c
// 示意：switch-case 状态机，状态和事件一多就很长
switch (state) {
case RED:
    if (event == TIMEOUT) state = GREEN;
    else if (event == FAULT) state = FLASH;
    break;
case GREEN:
    if (event == TIMEOUT) state = YELLOW;
    else if (event == FAULT) state = FLASH;
    break;
// ... YELLOW、FLASH 同理
}
```

问题：每加一个状态或事件，就要改一堆代码；逻辑分散在各个 `case` 里，很难一眼看出"完整的转移关系"。

### 2. 表驱动：把逻辑变成数据

```c
// 示意：真实项目里通常这样定义（常量表放在 Flash 中）
enum { RED, GREEN, YELLOW, FLASH, STATE_NUM };
enum { EV_TIMEOUT, EV_FAULT, EV_RECOVER, EVENT_NUM };

static const int8_t fsm_table[STATE_NUM][EVENT_NUM] = {
    /*            TIMEOUT  FAULT  RECOVER */
    /* RED    */ { GREEN,  FLASH,  -1   },
    /* GREEN  */ { YELLOW, FLASH,  -1   },
    /* YELLOW */ { RED,    FLASH,  -1   },
    /* FLASH  */ { -1,     -1,     RED  },
};
```

状态转移只需要一行：`next = fsm_table[state][event];`。改需求只改表，不改代码。

### 3. `int** table` 是什么？

本题的表是从输入读进来的，大小运行时才知道，所以用 `int**`（指针数组，每个元素指向一行）。访问方式和二维数组一样：`table[s][e]`。

---

## 💡 第三步：思路一 —— 直接查二维表

### 代码

```c
int* runStateMachine(int** table, int stateCount, int eventCount, int initState,
                     const int* events, int eventsSize, int* returnSize) {
    int* res = (int*)malloc(sizeof(int) * eventsSize);
    int cur = initState;                         // 当前状态

    for (int i = 0; i < eventsSize; i++) {
        int next = table[cur][events[i]];        // 查表：当前状态 + 事件 → 新状态
        if (next != -1) {                        // -1 表示忽略该事件
            cur = next;
        }
        res[i] = cur;                            // 记录处理完这个事件后的状态
    }

    *returnSize = eventsSize;
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n)**：每个事件一次查表。
- **空间复杂度 O(1)**（结果数组不算）。

---

## 🚀 第四步：思路二 —— 稀疏转移列表（表中大部分是 -1 时）

### 为什么需要？

真实系统中，大多数"状态 × 事件"组合是没有意义的（表里大部分是 -1）。如果有 50 个状态、20 个事件，二维表要 1000 项，可能只有 60 项有用。这时工程上常改用**转移列表**：只记录有效的转移。

```c
typedef struct {
    int from;    // 当前状态
    int event;   // 事件
    int to;      // 新状态
} Transition;
```

为了查得快，按 `from` 分组存放，并记录每个状态的转移在列表中的起止位置（类似"压缩稀疏行 CSR"）。查找时只需扫描当前状态那一小段。

### 代码

```c
typedef struct {
    int event;   // 事件
    int to;      // 新状态
} Transition;

int* runStateMachine(int** table, int stateCount, int eventCount, int initState,
                     const int* events, int eventsSize, int* returnSize) {
    // 1. 把二维表压缩成转移列表：状态 s 的转移存放在 list[begin[s]] 到 list[begin[s+1]-1]
    Transition* list = (Transition*)malloc(sizeof(Transition) * (stateCount * eventCount + 1));
    int* begin = (int*)malloc(sizeof(int) * (stateCount + 1));
    int total = 0;
    for (int s = 0; s < stateCount; s++) {
        begin[s] = total;
        for (int e = 0; e < eventCount; e++) {
            if (table[s][e] != -1) {             // 只保存有效转移
                list[total].event = e;
                list[total].to = table[s][e];
                total++;
            }
        }
    }
    begin[stateCount] = total;

    // 2. 运行状态机：在当前状态的那一段里找匹配的事件
    int* res = (int*)malloc(sizeof(int) * eventsSize);
    int cur = initState;
    for (int i = 0; i < eventsSize; i++) {
        for (int j = begin[cur]; j < begin[cur + 1]; j++) {
            if (list[j].event == events[i]) {
                cur = list[j].to;                // 找到转移
                break;
            }
        }                                        // 没找到：忽略事件，状态不变
        res[i] = cur;
    }

    free(list);
    free(begin);
    *returnSize = eventsSize;
    return res;
}
```

> 💬 真实项目中，转移列表的每一项通常还会带一个**动作函数指针**，例如 `{RED, EV_TIMEOUT, GREEN, turn_on_green}`，转移时顺便调用 `turn_on_green()` 点亮绿灯。这就是很多嵌入式框架（如 QP、各种 FSM 库）的核心。

### 复杂度分析

- **时间复杂度 O(n × 每个状态的有效转移数)**，最坏 O(n × eventCount)。
- **空间复杂度 O(有效转移数)**：表越稀疏越省空间。

---

## ⚠️ 第五步：小白常见错误

1. **遇到 -1 时把 cur 设成 -1** → 下一次 `table[-1][e]` 直接越界崩溃。
2. **先记录再转移** → 输出的是处理事件之前的状态，整体错一位。
3. **把行列搞反写成 `table[e][cur]`** → 题目约定行是状态、列是事件。
4. **`eventCount` 从哪来？** → 本题直接作为参数传入；自己写项目时用 `sizeof(table[0]) / sizeof(table[0][0])` 计算静态二维数组的列数。
5. **switch 写法漏写 `break`** → 会"贯穿"执行到下一个 case，状态被连续改两次。这是 switch 状态机最常见的 bug，也是表驱动的优势之一。

---

## 📊 第六步：方法对比

| 写法 | 查找速度 | 空间 | 可维护性 | 适用 |
|---|---|---|---|---|
| switch-case | 快 | 代码大 | 状态多时差 | 状态少、每个状态动作复杂 |
| 二维转移表 | O(1) | 状态数 × 事件数 | 好 | 转移表比较"满" |
| 稀疏转移列表 | O(每状态转移数) | 有效转移数 | 好，还能挂动作函数 | 表很稀疏 / 需要动作回调 |

---

## 🔗 举一反三

- **9054. 按键消抖状态机**：用 `enum + switch` 写的状态机，试着把它改写成表驱动。
- **9051. UART 帧解析**：协议解析也是状态机。
- **思考题 1**：给每个状态加上"进入动作"（例如进入绿灯时点亮绿灯、启动 30 秒定时器），表结构要怎么扩展？（提示：函数指针数组 `void (*on_enter[STATE_NUM])(void)`）
- **思考题 2**：如果事件来自中断，而状态机在主循环里运行，中间需要什么数据结构缓冲事件？（提示：9046）
