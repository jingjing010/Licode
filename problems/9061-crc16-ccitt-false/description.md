# CRC16 CCITT-FALSE

计算CRC-16/CCITT-FALSE：poly=0x1021，init=0xFFFF，refin/refout=false，xorout=0。输入0到1024字节，返回0到65535。ASCII 123456789校验值为0x29B1。

## 约束与接口

只实现函数，输入输出由平台处理。

```c
uint16_t crc16Ccitt(const uint8_t* data,size_t len);
```

## 示例 1

输入：
```text
[49,50,51,52,53,54,55,56,57]
```
输出：
```text
10673
```

## 示例 2

输入：
```text
[]
```
输出：
```text
65535
```

## 自定义输入格式

按顺序每行一个参数：data。数组使用 `[1,2]`，字符串使用双引号。数组长度由平台自动传入。

本题在主机上模拟固件逻辑；实际移植时需根据芯片手册接入外设和临界区。
