ADC 采样到的电压、温度、电流等信号总会带有随机噪声。最简单有效的软件滤波就是**滑动平均（Moving Average）**：每来一个新采样值，就输出"最近 N 个采样值的平均"，读数会平稳很多。

请实现滑动平均滤波器 `MovingAvg`：

- `MovingAvg* movingAvgCreate(int windowSize)`：创建窗口大小为 `windowSize` 的滤波器，初始没有任何采样。
- `uint16_t movingAvgUpdate(MovingAvg* obj, uint16_t sample)`：输入一个新采样值，返回**最近 `min(已输入个数, windowSize)` 个采样值**的平均值，按**四舍五入**取整（`.5` 进位）。
- `void movingAvgReset(MovingAvg* obj)`：清空所有历史采样（例如传感器重新上电后），之后就像刚创建时一样。
- `void movingAvgFree(MovingAvg* obj)`：释放内存。

也就是说，在窗口还没填满之前，只对已有的采样值求平均。

### 示例 1

```
输入：
["MovingAvg","update","update","update","update","update"]
[[3],[10],[11],[30],[40],[45]]
输出：
[null,10,11,17,27,38]
解释：
窗口大小 3。
update(10)：[10] → 10
update(11)：[10,11] → 21/2 = 10.5 → 四舍五入 11
update(30)：[10,11,30] → 51/3 = 17
update(40)：[11,30,40] → 81/3 = 27（10 被挤出窗口）
update(45)：[30,40,45] → 115/3 = 38.33 → 38
```

### 示例 2

```
输入：
["MovingAvg","update","update","reset","update","update"]
[[2],[100],[1],[],[7],[8]]
输出：
[null,100,51,null,7,8]
解释：
update(100) → 100；update(1)：(100+1)/2 = 50.5 → 51。
reset 后历史清空：update(7) → 7；update(8)：(7+8)/2 = 7.5 → 8。
```

### 提示

- `1 <= windowSize <= 1000`
- `0 <= sample <= 65535`
- 操作总次数不超过 `2 * 10^4`
- 第一个操作一定是 `MovingAvg`

### 函数说明

```c
typedef struct {
    // 自己设计
} MovingAvg;

MovingAvg* movingAvgCreate(int windowSize);
uint16_t movingAvgUpdate(MovingAvg* obj, uint16_t sample);
void movingAvgReset(MovingAvg* obj);
void movingAvgFree(MovingAvg* obj);
```

### 自定义输入格式

```
["MovingAvg","update","reset"]
[[3],[10],[]]
```

第 1 行是操作名数组，第 2 行是参数数组：`MovingAvg` 为 `[windowSize]`，`update` 为 `[sample]`，`reset` 为空 `[]`。
输出每个操作的返回值：`update` 输出整数，其它输出 `null`。
