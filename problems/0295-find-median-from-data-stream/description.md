**中位数** 是有序整数列表中的中间值。如果列表的大小是偶数，则没有中间值，中位数是两个中间值的平均值。

- 例如 `arr = [2,3,4]` 的中位数是 `3` 。
- 例如 `arr = [2,3]` 的中位数是 `(2 + 3) / 2 = 2.5` 。

实现 `MedianFinder` 类:

- `MedianFinder()` 初始化 `MedianFinder` 对象。
- `void addNum(int num)` 将数据流中的整数 `num` 添加到数据结构中。
- `double findMedian()` 返回到目前为止所有元素的中位数。与实际答案相差 `10^-5` 以内的答案将被接受。

### 示例 1

```
输入：
["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
[[], [1], [2], [], [3], []]

输出：
[null,null,null,1.50000,null,2.00000]

解释：
MedianFinder medianFinder = new MedianFinder();
medianFinder.addNum(1);    // arr = [1]
medianFinder.addNum(2);    // arr = [1, 2]
medianFinder.findMedian(); // 返回 1.5 ((1 + 2) / 2)
medianFinder.addNum(3);    // arr[1, 2, 3]
medianFinder.findMedian(); // return 2.0
```

### 提示

- `-10^5 <= num <= 10^5`
- 在调用 `findMedian` 之前，数据结构中至少有一个元素
- 最多 `5 * 10^4` 次调用 `addNum` 和 `findMedian`

### 函数说明

```c
typedef struct {
    // 你自己设计需要的成员
} MedianFinder;

MedianFinder* medianFinderCreate();
void medianFinderAddNum(MedianFinder* obj, int num);
double medianFinderFindMedian(MedianFinder* obj);
void medianFinderFree(MedianFinder* obj);
```

- 这是力扣 C 语言的"设计类"写法：用结构体保存数据，每个方法的第一个参数 `obj` 是指向这个结构体的指针
- `medianFinderCreate`：用 `malloc` 创建并初始化一个 `MedianFinder`，返回它的指针
- `medianFinderFree`：释放 `medianFinderCreate` 以及之后申请的所有内存
- `struct` 里的成员由你自己决定（模板中是空的，需要你补充）

### 自定义输入格式

```
["MedianFinder","addNum","addNum","findMedian","addNum","findMedian"]
[[],[1],[2],[],[3],[]]
```

第 1 行是操作名数组，第 2 行是每个操作对应的参数数组（没有参数写 `[]`）。第一个操作必须是 `"MedianFinder"`。
输出每个操作的返回值组成的数组（不带空格），没有返回值的操作输出 `null`，`findMedian` 的返回值**保留 5 位小数**输出。
