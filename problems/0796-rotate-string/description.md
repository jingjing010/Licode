# 旋转字符串

一次操作把s最左字符移到最右，判断能否经过若干次得到goal。只含小写字母，长度1到100。

## 约束与接口

只实现函数，输入输出由平台处理。

```c
bool rotateString(char* s,char* goal);
```

## 示例 1

输入：
```text
"abcde"
"cdeab"
```
输出：
```text
true
```

## 示例 2

输入：
```text
"abcde"
"abced"
```
输出：
```text
false
```

## 自定义输入格式

按顺序每行一个参数：s、goal。数组使用 `[1,2]`，字符串使用双引号。数组长度由平台自动传入。
