# RTC BCD 时间增加分钟

hourBcd为合法24小时BCD，minuteBcd为合法分钟BCD，delta为0..10^6。增加分钟并按24小时回绕，返回[小时BCD,分钟BCD]。输入输出以十进制整数显示，例如0x23输入35。

## 约束与接口

返回数组/字符串由调用方释放；不要返回局部数组。

```c
int* addBcdMinutes(int hourBcd,int minuteBcd,int delta,int* returnSize);
```

## 示例 1

输入：
```text
35
89
1
```
输出：
```text
[0,0]
```

## 示例 2

输入：
```text
18
48
90
```
输出：
```text
[20,0]
```

## 自定义输入格式

按顺序每行一个参数：hourBcd、minuteBcd、delta。数组使用 `[1,2]`，字符串使用双引号。数组长度由平台自动传入。

本题在主机上模拟固件逻辑；实际移植时需根据芯片手册接入外设和临界区。
