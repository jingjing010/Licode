设计一个支持 `push` ，`pop` ，`top` 操作，并能在常数时间内检索到最小元素的栈。

实现 `MinStack` 类:

- `MinStack()` 初始化堆栈对象。
- `void push(int val)` 将元素 `val` 推入堆栈。
- `void pop()` 删除堆栈顶部的元素。
- `int top()` 获取堆栈顶部的元素。
- `int getMin()` 获取堆栈中的最小元素。

### 示例 1

```
输入：
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]

输出：
[null,null,null,null,-3,null,0,-2]

解释：
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin();   --> 返回 -3.
minStack.pop();
minStack.top();      --> 返回 0.
minStack.getMin();   --> 返回 -2.
```

### 提示

- `-2^31 <= val <= 2^31 - 1`
- `pop`、`top` 和 `getMin` 操作总是在 **非空栈** 上调用
- `push`, `pop`, `top`, and `getMin` 最多被调用 `3 * 10^4` 次

### 函数说明

```c
typedef struct {
    // 你自己设计需要的成员
} MinStack;

MinStack* minStackCreate();
void minStackPush(MinStack* obj, int val);
void minStackPop(MinStack* obj);
int minStackTop(MinStack* obj);
int minStackGetMin(MinStack* obj);
void minStackFree(MinStack* obj);
```

- 这是力扣 C 语言的"设计类"写法：用结构体保存数据，每个方法的第一个参数 `obj` 是指向这个结构体的指针
- `minStackCreate`：用 `malloc` 创建并初始化一个 `MinStack`，返回它的指针
- `minStackFree`：释放 `minStackCreate` 以及之后申请的所有内存
- `struct` 里的成员由你自己决定（模板中是空的，需要你补充）

### 自定义输入格式

```
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]
```

第 1 行是操作名数组，第 2 行是每个操作对应的参数数组（没有参数写 `[]`）。第一个操作必须是 `"MinStack"`。
输出每个操作的返回值组成的数组（不带空格），没有返回值的操作输出 `null`。
