MCU 的硬件定时器只有几个，而应用里需要的定时任务却很多：LED 每 500ms 闪一次、串口 100ms 超时、看门狗每秒喂一次……常见的做法是用**一个**硬件定时器产生周期性的"节拍（tick）"中断（例如每 1ms 一次），再在软件里管理许多个**软件定时器**。FreeRTOS 的 `xTimerCreate`、各种裸机框架里的 `soft_timer` 都是这个思路。

请你实现软件定时器管理器 `TimerManager`：

- `TimerManager* timerManagerCreate(int maxTimers)`：创建管理器，可用的定时器编号为 `0 ~ maxTimers-1`，初始全部处于停止状态。
- `void timerManagerStart(TimerManager* obj, int id, int period, bool repeat)`：启动（或**重新启动**）编号为 `id` 的定时器：从现在起再经过 `period` 次 tick 后触发。`repeat` 为 `true` 表示**周期定时器**（触发后自动重新开始计时），为 `false` 表示**单次定时器**（触发一次后自动停止）。如果该定时器已经在运行，则丢弃原来的计时，按新参数重新开始。
- `void timerManagerStop(TimerManager* obj, int id)`：停止编号为 `id` 的定时器（若本来就是停止的，什么也不做）。
- `int* timerManagerTick(TimerManager* obj, int* returnSize)`：时间前进 1 个节拍。每个运行中的定时器剩余节拍数减 1，减到 0 的定时器在本次**触发**：周期定时器的剩余节拍重新设为 `period`，单次定时器停止。返回本次触发的所有定时器编号，按**从小到大**排列（没有则返回空数组）。
- `void timerManagerFree(TimerManager* obj)`：释放内存。

### 示例 1

```
输入：
["TimerManager","start","start","tick","tick","tick","tick","tick","tick"]
[[3],[0,2,1],[1,3,0],[],[],[],[],[],[]]
输出：
[null,null,null,[],[0],[1],[0],[],[0]]
解释：
定时器 0：周期 2 的周期定时器；定时器 1：3 个节拍后触发一次的单次定时器。
第 1 次 tick：0 剩 1，1 剩 2 → []
第 2 次 tick：0 剩 0 触发并重装为 2；1 剩 1 → [0]
第 3 次 tick：0 剩 1；1 剩 0 触发并停止 → [1]
第 4 次 tick：0 触发 → [0]；第 5 次 → []；第 6 次 → [0]
```

### 示例 2

```
输入：
["TimerManager","start","tick","start","tick","stop","tick","start","start","tick","tick","tick"]
[[2],[1,1,1],[],[0,1,0],[],[1],[],[0,2,0],[0,3,0],[],[],[]]
输出：
[null,null,[1],null,[0,1],null,[],null,null,[],[],[0]]
解释：
定时器 1 周期为 1，每次 tick 都触发。定时器 0 是 1 个节拍的单次定时器，和 1 同时触发，按编号输出 [0,1]。
stop(1) 之后没有定时器在运行，tick 返回 []。
定时器 0 先以 2 启动、马上又以 3 重新启动，以最后一次为准，所以第 3 次 tick 才触发。
```

### 提示

- `1 <= maxTimers <= 100`
- `0 <= id < maxTimers`，`1 <= period <= 1000`
- 操作总次数不超过 `10^4`，所有 `tick` 返回的编号总数不超过 `10^5`
- 第一个操作一定是 `TimerManager`

### 函数说明

```c
typedef struct {
    // 自己设计
} TimerManager;

TimerManager* timerManagerCreate(int maxTimers);
void timerManagerStart(TimerManager* obj, int id, int period, bool repeat);
void timerManagerStop(TimerManager* obj, int id);
int* timerManagerTick(TimerManager* obj, int* returnSize);
void timerManagerFree(TimerManager* obj);
```

- `timerManagerTick` 返回 `malloc` 申请的数组，由判题程序 `free`

### 自定义输入格式

```
["TimerManager","start","tick","tick"]
[[3],[0,2,1],[],[]]
```

第 1 行是操作名数组，第 2 行是参数数组：`TimerManager` 为 `[maxTimers]`，`start` 为 `[id, period, repeat]`（`repeat` 用 `1`/`0` 表示 `true`/`false`），`stop` 为 `[id]`，`tick` 为空 `[]`。
输出每个操作的返回值：`tick` 输出数组，其它输出 `null`。
