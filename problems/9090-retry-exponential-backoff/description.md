# 带上限的指数退避

第attempt次退避=min(base*2^attempt,cap)。base与cap为0..INT_MAX，attempt0..100；返回毫秒数。

## 约束与接口

只实现函数，输入输出由平台处理。

```c
int retryDelay(int base,int attempt,int cap);
```

## 示例 1

输入：
```text
10
0
1000
```
输出：
```text
10
```

## 示例 2

输入：
```text
10
4
1000
```
输出：
```text
160
```

## 自定义输入格式

按顺序每行一个参数：base、attempt、cap。数组使用 `[1,2]`，字符串使用双引号。数组长度由平台自动传入。

本题在主机上模拟固件逻辑；实际移植时需根据芯片手册接入外设和临界区。
