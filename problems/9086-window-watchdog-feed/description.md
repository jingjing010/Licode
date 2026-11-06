# 窗口看门狗喂狗判定

给定自上次喂狗以来的elapsed及允许闭区间[minimum,maximum]，返回当前是否允许喂狗。参数为uint32_t，minimum≤maximum。实际芯片窗口边界以手册为准。

## 约束与接口

只实现函数，输入输出由平台处理。

```c
bool watchdogCanFeed(uint32_t elapsed,uint32_t minimum,uint32_t maximum);
```

## 示例 1

输入：
```text
0
10
20
```
输出：
```text
false
```

## 示例 2

输入：
```text
1
10
20
```
输出：
```text
false
```

## 自定义输入格式

按顺序每行一个参数：elapsed、minimum、maximum。数组使用 `[1,2]`，字符串使用双引号。数组长度由平台自动传入。

本题在主机上模拟固件逻辑；实际移植时需根据芯片手册接入外设和临界区。
