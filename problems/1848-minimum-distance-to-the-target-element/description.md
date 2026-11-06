# 到目标元素的最小距离

返回值为target的元素下标与start的最小绝对差。保证target存在，0 ≤ start < n ≤ 1000。

## 约束与接口

只实现函数，输入输出由平台处理。

```c
int getMinDistance(int* nums,int numsSize,int target,int start);
```

## 示例 1

输入：
```text
[1,2,3,4,5]
5
3
```
输出：
```text
1
```

## 示例 2

输入：
```text
[1]
1
0
```
输出：
```text
0
```

## 自定义输入格式

按顺序每行一个参数：nums、target、start。数组使用 `[1,2]`，字符串使用双引号。数组长度由平台自动传入。
