# 令牌桶请求限速：题解

## 📖 先读懂题目

times是非递减毫秒时间戳（0..10^6）。时刻0有capacity个令牌，此后每interval毫秒补1个，上限capacity。每个请求有令牌则接受并消耗，输出1，否则0。同一时刻依输入顺序处理。容量1..100，interval1..1000，最多1000个请求。

| 示例 | 输入参数 | 返回结果 |
|---|---|---|
| 1 | `[0,0,0,10,20] / 2 / 10` | `[1,1,0,1,1]` |
| 2 | `[0,1,2,3,4] / 1 / 2` | `[1,0,1,0,1]` |

## 🧰 需要的 C 语言知识

数组形参是指针，不能用`sizeof(指针)`推算元素个数，要使用单独传入的长度。下标从0开始，最后一个有效下标是长度减1。

返回数组需要申请独立内存，并把有效元素数写入`*returnSize`。调用方释放结果，因此不能返回函数内的局部数组。输入数组长度与输出长度不一定相同。

## 💡 推导与实现

初始桶满，按固定时间栅格补令牌，每次请求消耗一个；多余令牌丢弃，但补充时间的余数仍要保留。

先按定义手工处理第一个示例，再确认每一步保存的状态足够决定下一步。循环结束时只返回题目要求的结果，不返回尚未处理的中间状态。

```c
int *tokenBucket(int *times, int timesSize, int capacity, int interval, int *returnSize) {
    int *out = malloc((timesSize + 1) * sizeof(int)), tokens = capacity, last = 0;
    for (int i = 0; i < timesSize; ++i) {
        int add = (times[i] - last) / interval;
        last += add * interval;
        tokens = tokens + add > capacity ? capacity : tokens + add;
        out[i] = tokens > 0;
        if (tokens)
            --tokens;
    }
    *returnSize = timesSize;
    return out;
}
```

## 📊 复杂度与取舍

| 方法 | 代价 | 用途 |
|---|---|---|
| 上述实现 | 时间 O(n)，输出空间 O(n) | 正式提交 |

## ⚠️ 常见错误

- 循环写成`i <= 长度`，访问数组末尾之后的内存。
- 只返回指针却忘记设置`*returnSize`，平台无法知道输出多少元素。
- 忽略题面约束与特殊边界，直接把某个正常样例的结论推广到所有输入。
- 先用int乘法再转换到64位；溢出已经发生，转换无法补救。

## 🔗 举一反三

尝试把同一处理过程改成逐个输入的流式接口，思考需要保留哪些状态。用空边界、最小值、最大值和重复值检查自己的实现。
