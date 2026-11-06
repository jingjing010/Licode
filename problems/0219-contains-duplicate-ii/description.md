# 存在重复元素 II

判断是否存在不同下标i,j，值相同且|i−j|≤k。1 ≤ n ≤ 10^5，0 ≤ k ≤ 10^5。

## 约束与接口

只实现函数，输入输出由平台处理。

```c
bool containsNearbyDuplicate(int* nums,int numsSize,int k);
```

## 示例 1

输入：
```text
[1,2,3,1]
3
```
输出：
```text
true
```

## 示例 2

输入：
```text
[1,2,3,1,2,3]
2
```
输出：
```text
false
```

## 自定义输入格式

按顺序每行一个参数：nums、k。数组使用 `[1,2]`，字符串使用双引号。数组长度由平台自动传入。
