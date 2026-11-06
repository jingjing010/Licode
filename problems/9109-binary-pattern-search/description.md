# 二进制缓冲区查找

返回pattern在data中首次匹配的字节下标，不存在返回−1，空pattern返回0。两个长度0到1024，可包含零字节。

## 约束与接口

只实现函数，输入输出由平台处理。

```c
int findBinaryPattern(const uint8_t* data,size_t len,const uint8_t* pattern,size_t patternSize);
```

## 示例 1

输入：
```text
[1,0,2,0,3]
[0,2]
```
输出：
```text
1
```

## 示例 2

输入：
```text
[0,1]
[2]
```
输出：
```text
-1
```

## 自定义输入格式

按顺序每行一个参数：data、pattern。数组使用 `[1,2]`，字符串使用双引号。数组长度由平台自动传入。

本题在主机上模拟固件逻辑；实际移植时需根据芯片手册接入外设和临界区。
