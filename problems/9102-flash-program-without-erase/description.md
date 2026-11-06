# Flash 无擦除写入可行性

判断原始字节能否通过仅清位的操作变成目标字节；任何0→1都需要擦除。不同长度返回false，长度0到1024。这里只检查位规则，不模拟控制器对齐与编程次数约束。

## 约束与接口

只实现函数，输入输出由平台处理。

```c
bool canProgramFlash(const uint8_t* before,size_t beforeSize,const uint8_t* after,size_t afterSize);
```

## 示例 1

输入：
```text
[255]
[0]
```
输出：
```text
true
```

## 示例 2

输入：
```text
[0]
[1]
```
输出：
```text
false
```

## 自定义输入格式

按顺序每行一个参数：before、after。数组使用 `[1,2]`，字符串使用双引号。数组长度由平台自动传入。

本题在主机上模拟固件逻辑；实际移植时需根据芯片手册接入外设和临界区。
