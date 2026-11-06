ADC 采到的传感器信号（温度、电压、电流、电位器位置）总是带着噪声，读数会在真实值附近来回跳动。最简单有效的软件滤波是**滑动平均**（Moving Average）：每次采到一个新值，就输出**最近 N 个采样值的平均**。N 越大越平滑，但对真实变化的反应也越慢。

请你实现滑动平均滤波器 `MovingAvg`：

- `MovingAvg* movingAvgCreate(int windowSize)`：创建窗口大小为 `windowSize` 的滤波器，初始没有任何采样值。
- `uint16_t movingAvgUpdate(MovingAvg* obj, uint16_t sample)`：输入一个新的采样值，返回滤波输出：**最近 `min(已输入个数, windowSize)` 个采样值的平均值**，按**四舍五入**取整（小数部分 `>= 0.5` 进位）。
- `void movingAvgReset(MovingAvg* obj)`：清空所有历史采样值（例如传感器重新上电后），之后的行为和刚创建时一样。
- `void movingAvgFree(MovingAvg* obj)`：释放内存。

### 示例 1

```
输入：
["MovingAvg","update","update","update","update","update"]
[[3],[10],[11],[30],[40],[45]]
输出：
[null,10,11,17,27,38]
解释：窗口大小 3。
update(10)：窗口 [10]，平均 10
update(11)：窗口 [10,11]，平均 10.5 → 四舍五入 11
update(30)：窗口 [10,11,30]，平均 17
update(40)：窗口 [11,30,40]（10 被挤出），平均 27
update(45)：窗口 [30,40,45]，平均 38.33 → 38
```

### 示例 2

```
输入：
["MovingAvg","update","update","reset","update","update"]
[[2],[100],[1],[],[7],[8]]
输出：
[null,100,51,null,7,8]
解释：(100+1)/2 = 50.5 → 51；reset 后历史清空，7 → 7，(7+8)/2 = 7.5 → 8。
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
["MovingAvg","update","update"]
[[3],[10],[11]]
```

第 1 行是操作名数组，第 2 行是参数数组：`MovingAvg` 为 `[windowSize]`，`update` 为 `[sample]`，`reset` 为空 `[]`。
输出每个操作的返回值：`update` 输出整数，其它输出 `null`。
