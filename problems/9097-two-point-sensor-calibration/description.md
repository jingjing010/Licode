# 传感器两点线性标定

raw/raw0/raw1在0..65535，raw0<raw1；value0/value1在−10^6..10^6，可升可降。计算value0+trunc((raw−raw0)*(value1−value0)/(raw1−raw0))，允许外推，保证结果在int范围。

## 约束与接口

只实现函数，输入输出由平台处理。

```c
int calibrateSensor(int raw,int raw0,int raw1,int value0,int value1);
```

## 示例 1

输入：
```text
100
100
1100
-500
500
```
输出：
```text
-500
```

## 示例 2

输入：
```text
1100
100
1100
-500
500
```
输出：
```text
500
```

## 自定义输入格式

按顺序每行一个参数：raw、raw0、raw1、value0、value1。数组使用 `[1,2]`，字符串使用双引号。数组长度由平台自动传入。

本题在主机上模拟固件逻辑；实际移植时需根据芯片手册接入外设和临界区。
