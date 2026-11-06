# PWM 软启动爬坡

占空比采用千分比0..1000。每tick向target靠近step且不越过，返回ticks拍后值。step0..1000，ticks0..10^6。

## 约束与接口

只实现函数，输入输出由平台处理。

```c
int pwmRamp(int initial,int target,int step,int ticks);
```

## 示例 1

输入：
```text
0
1000
10
5
```
输出：
```text
50
```

## 示例 2

输入：
```text
1000
0
30
100
```
输出：
```text
0
```

## 自定义输入格式

按顺序每行一个参数：initial、target、step、ticks。数组使用 `[1,2]`，字符串使用双引号。数组长度由平台自动传入。

本题在主机上模拟固件逻辑；实际移植时需根据芯片手册接入外设和临界区。
