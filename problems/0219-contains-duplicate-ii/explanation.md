# 存在重复元素 II：题解

## 📖 先读懂题目

判断是否存在不同下标i,j，值相同且|i−j|≤k。1 ≤ n ≤ 10^5，0 ≤ k ≤ 10^5。

| 示例 | 输入参数 | 返回结果 |
|---|---|---|
| 1 | `[1,2,3,1] / 3` | `true` |
| 2 | `[1,2,3,1,2,3] / 2` | `false` |

## 🧰 需要的 C 语言知识

数组形参是指针，不能用`sizeof(指针)`推算元素个数，要使用单独传入的长度。下标从0开始，最后一个有效下标是长度减1。

整数除法会向零截断。乘法中间结果可能大于最终答案，要在乘法发生之前转换为更宽的整数类型。布尔函数使用`true`与`false`表达判断结果。

## 💡 推导与实现

把数值和原始下标一起排序。同一值内按下标递增后，最小距离必然出现在相邻两项之间。

先按定义手工处理第一个示例，再确认每一步保存的状态足够决定下一步。循环结束时只返回题目要求的结果，不返回尚未处理的中间状态。

```c
typedef struct {
    int value, index;
} Entry;
static int cmpEntry(const void *a, const void *b) {
    const Entry *x = a, *y = b;
    if (x->value != y->value)
        return (x->value > y->value) - (x->value < y->value);
    return (x->index > y->index) - (x->index < y->index);
}
bool containsNearbyDuplicate(int *nums, int numsSize, int k) {
    Entry *a = malloc(numsSize * sizeof(Entry));
    for (int i = 0; i < numsSize; ++i) {
        a[i].value = nums[i];
        a[i].index = i;
    }
    qsort(a, numsSize, sizeof(Entry), cmpEntry);
    bool found = false;
    /* 相同值的原下标排序后，只需检查相邻下标差。 */
    for (int i = 1; i < numsSize; ++i)
        if (a[i].value == a[i - 1].value && a[i].index - a[i - 1].index <= k) {
            found = true;
            break;
        }
    free(a);
    return found;
}
```

## 📊 复杂度与取舍

| 方法 | 代价 | 用途 |
|---|---|---|
| 上述实现 | 时间 O(n log n)，空间 O(n) | 正式提交 |

## ⚠️ 常见错误

- 循环写成`i <= 长度`，访问数组末尾之后的内存。
- 忽略题面约束与特殊边界，直接把某个正常样例的结论推广到所有输入。
- 先用int乘法再转换到64位；溢出已经发生，转换无法补救。
- 直接复制main函数或打印调试信息，导致与平台自动生成的输入输出冲突。

## 🔗 举一反三

尝试把同一处理过程改成逐个输入的流式接口，思考需要保留哪些状态。用空边界、最小值、最大值和重复值检查自己的实现。
