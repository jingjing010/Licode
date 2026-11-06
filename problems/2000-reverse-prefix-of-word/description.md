# 反转单词前缀

反转word开头到第一次出现ch（含ch）的前缀，ch不存在则保持原字符串。word只含小写字母，长度1到250。 自定义输入第二行使用字符的ASCII整数，例如d写100。

## 约束与接口

返回数组/字符串由调用方释放；不要返回局部数组。

```c
char* reversePrefix(char* word,char ch);
```

## 示例 1

输入：
```text
"abcdefd"
100
```
输出：
```text
"dcbaefd"
```

## 示例 2

输入：
```text
"xyxzxe"
122
```
输出：
```text
"zxyxxe"
```

## 自定义输入格式

按顺序每行一个参数：word、ch。数组使用 `[1,2]`，字符串使用双引号。数组长度由平台自动传入。
