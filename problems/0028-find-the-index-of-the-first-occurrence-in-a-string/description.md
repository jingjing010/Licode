# 找出字符串中第一个匹配项的下标

给定小写字符串haystack与needle，返回needle首次出现的下标，不存在返回−1。长度1到10^4。

## 约束与接口

只实现函数，输入输出由平台处理。

```c
int strStr(char* haystack,char* needle);
```

## 示例 1

输入：
```text
"sadbutsad"
"sad"
```
输出：
```text
0
```

## 示例 2

输入：
```text
"leetcode"
"leeto"
```
输出：
```text
-1
```

## 自定义输入格式

按顺序每行一个参数：haystack、needle。数组使用 `[1,2]`，字符串使用双引号。数组长度由平台自动传入。
