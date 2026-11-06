设计一个算法收集某些股票的每日报价，并返回该股票当日价格的 **跨度** 。

当日股票价格的 **跨度** 被定义为股票价格小于或等于今天价格的最大连续日数（从今天开始往回数，包括今天）。

- 例如，如果未来 7 天股票的价格是 `[100,80,60,70,60,75,85]`，那么股票跨度将是 `[1,1,1,2,1,4,6]` 。

实现 `StockSpanner` 类：

- `StockSpanner()` 初始化类对象。
- `int next(int price)` 给出今天的股价 `price` ，返回该股票当日价格的 **跨度** 。

### 示例 1

```
输入：
["StockSpanner","next","next","next","next","next","next","next"]
[[],[100],[80],[60],[70],[60],[75],[85]]

输出：
[null,1,1,1,2,1,4,6]

解释：
StockSpanner stockSpanner = new StockSpanner();
stockSpanner.next(100); // 返回 1
stockSpanner.next(80);  // 返回 1
stockSpanner.next(60);  // 返回 1
stockSpanner.next(70);  // 返回 2
stockSpanner.next(60);  // 返回 1
stockSpanner.next(75);  // 返回 4 ，因为截至今天的最后 4 个股价 (包括今天的股价 75) 都小于或等于今天的股价。
stockSpanner.next(85);  // 返回 6
```

### 提示

- `1 <= price <= 10^5`
- 最多调用 `next` 方法 `10^4` 次

### 函数说明

```c
typedef struct {
    // 你自己设计需要的成员
} StockSpanner;

StockSpanner* stockSpannerCreate();
int stockSpannerNext(StockSpanner* obj, int price);
void stockSpannerFree(StockSpanner* obj);
```

- 这是力扣 C 语言的"设计类"写法：用结构体保存数据，每个方法的第一个参数 `obj` 是指向这个结构体的指针
- `stockSpannerCreate`：用 `malloc` 创建并初始化一个 `StockSpanner`，返回它的指针
- `stockSpannerNext`：传入今天的价格，返回今天的跨度
- `stockSpannerFree`：释放 `stockSpannerCreate` 以及之后申请的所有内存
- `struct` 里的成员由你自己决定（模板中是空的，需要你补充）

### 自定义输入格式

```
["StockSpanner","next","next","next","next","next","next","next"]
[[],[100],[80],[60],[70],[60],[75],[85]]
```

第 1 行是操作名数组，第 2 行是每个操作对应的参数数组（没有参数写 `[]`）。第一个操作必须是 `"StockSpanner"`。
输出每个操作的返回值组成的数组（不带空格），没有返回值的操作输出 `null`，例如 `[null,1,1,1,2,1,4,6]`。
