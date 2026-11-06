# EEPROM 按需写入字节数

同长度数据返回不同字节位置数，不同长度返回−1。长度0到1024，字节值0..255。

## 约束与接口

只实现函数，输入输出由平台处理。

```c
int eepromChangedBytes(const uint8_t* before,size_t beforeSize,const uint8_t* after,size_t afterSize);
```

## 示例 1

输入：
```text
[1,2,3]
[1,9,3]
```
输出：
```text
1
```

## 示例 2

输入：
```text
[0]
[255]
```
输出：
```text
1
```

## 自定义输入格式

按顺序每行一个参数：before、after。数组使用 `[1,2]`，字符串使用双引号。数组长度由平台自动传入。

本题在主机上模拟固件逻辑；实际移植时需根据芯片手册接入外设和临界区。
