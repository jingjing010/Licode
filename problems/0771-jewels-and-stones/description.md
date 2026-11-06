# 宝石与石头

jewels是互不相同的英文字母，stones是持有石头的类型序列。统计宝石数量，大小写敏感。两个字符串长度1到50。

## 约束与接口

只实现函数，输入输出由平台处理。

```c
int numJewelsInStones(char* jewels,char* stones);
```

## 示例 1

输入：
```text
"aA"
"aAAbbbb"
```
输出：
```text
3
```

## 示例 2

输入：
```text
"z"
"ZZ"
```
输出：
```text
0
```

## 自定义输入格式

按顺序每行一个参数：jewels、stones。数组使用 `[1,2]`，字符串使用双引号。数组长度由平台自动传入。
