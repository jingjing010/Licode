# 摇杆中心死区

输入value为int16范围，threshold0..32767。|value|≤threshold输出0，否则向0方向减去threshold。

## 约束与接口

只实现函数，输入输出由平台处理。

```c
int applyDeadband(int value,int threshold);
```

## 示例 1

输入：
```text
10
5
```
输出：
```text
5
```

## 示例 2

输入：
```text
-10
5
```
输出：
```text
-5
```

## 自定义输入格式

按顺序每行一个参数：value、threshold。数组使用 `[1,2]`，字符串使用双引号。数组长度由平台自动传入。

本题在主机上模拟固件逻辑；实际移植时需根据芯片手册接入外设和临界区。
