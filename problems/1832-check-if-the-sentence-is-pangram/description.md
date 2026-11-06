# 判断句子是否为全字母句

输入仅含小写英文字母的句子，判断是否每个英文字母至少出现一次。长度1到1000。

## 约束与接口

只实现函数，输入输出由平台处理。

```c
bool checkIfPangram(char* sentence);
```

## 示例 1

输入：
```text
"thequickbrownfoxjumpsoverthelazydog"
```
输出：
```text
true
```

## 示例 2

输入：
```text
"leetcode"
```
输出：
```text
false
```

## 自定义输入格式

按顺序每行一个参数：s。数组使用 `[1,2]`，字符串使用双引号。数组长度由平台自动传入。
