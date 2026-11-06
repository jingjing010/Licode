# 将标题首字母大写

标题由英文字母单词和单空格组成，无首尾空格。长度1或2的单词全小写，其他单词仅首字母大写，返回新标题。长度1到100。

## 约束与接口

返回数组/字符串由调用方释放；不要返回局部数组。

```c
char* capitalizeTitle(char* title);
```

## 示例 1

输入：
```text
"capiTalIze tHe titLe"
```
输出：
```text
"Capitalize The Title"
```

## 示例 2

输入：
```text
"First leTTeR of EACH Word"
```
输出：
```text
"First Letter of Each Word"
```

## 自定义输入格式

按顺序每行一个参数：s。数组使用 `[1,2]`，字符串使用双引号。数组长度由平台自动传入。
