设备运行时会不断产生日志（错误码、事件编号……），但 MCU 的 RAM 很小，不可能全部保存。常见做法是开一块固定大小的**覆盖式环形缓冲区**：空间满了以后，新日志直接**覆盖最旧的那条**。这样缓冲区里永远保存着"最近的 N 条"日志，设备死机重启后（或者通过调试口）就能把它们读出来分析问题——很多芯片的"黑匣子（crash log）"就是这么实现的。

请你实现 `LogBuffer`：

- `LogBuffer* logBufferCreate(int capacity)`：创建一个最多保存 `capacity` 条日志的缓冲区，初始为空。
- `void logBufferWrite(LogBuffer* obj, int32_t value)`：写入一条日志。如果缓冲区**已满**，则**覆盖最旧的一条**。
- `int* logBufferGetAll(LogBuffer* obj, int* returnSize)`：按**从旧到新**的顺序返回当前保存的全部日志（**不删除**它们）。
- `int logBufferCount(LogBuffer* obj)`：返回当前保存的日志条数。
- `void logBufferFree(LogBuffer* obj)`：释放内存。

### 示例 1

```
输入：
["LogBuffer","write","write","getAll","write","write","write","getAll","count"]
[[3],[1],[2],[],[3],[4],[5],[],[]]
输出：
[null,null,null,[1,2],null,null,null,[3,4,5],3]
解释：
容量为 3。写入 1、2 后还没满，getAll 返回 [1,2]。
写入 3 后满了：[1,2,3]；写入 4 覆盖最旧的 1：[2,3,4]；写入 5 覆盖最旧的 2：[3,4,5]。
```

### 示例 2

```
输入：
["LogBuffer","getAll","count","write","write","getAll"]
[[1],[],[],[7],[9],[]]
输出：
[null,[],0,null,null,[9]]
解释：容量为 1，刚创建时为空；写入 9 时覆盖了 7，只剩最新的一条。
```

### 提示

- `1 <= capacity <= 1000`
- `0 <= value <= 10^9`
- 操作总次数不超过 `10^4`，所有 `getAll` 返回的元素总数不超过 `5 * 10^4`
- 第一个操作一定是 `LogBuffer`

### 函数说明

```c
typedef struct {
    // 自己设计
} LogBuffer;

LogBuffer* logBufferCreate(int capacity);
void logBufferWrite(LogBuffer* obj, int32_t value);
int* logBufferGetAll(LogBuffer* obj, int* returnSize);
int logBufferCount(LogBuffer* obj);
void logBufferFree(LogBuffer* obj);
```

- `logBufferGetAll` 返回 `malloc` 申请的数组（日志为空时也可以返回长度为 0 的数组），由判题程序 `free`

### 自定义输入格式

```
["LogBuffer","write","getAll"]
[[3],[1],[]]
```

第 1 行是操作名数组，第 2 行是参数数组：`LogBuffer` 为 `[capacity]`，`write` 为 `[value]`，其它为空 `[]`。
输出每个操作的返回值：`getAll` 输出数组，`count` 输出整数，其它输出 `null`。
