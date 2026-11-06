# Excel 表列名称

给定列号 columnNumber，1 ≤ columnNumber ≤ 2^31−1，返回 A、B、…、Z、AA 等列名。

## 约束与接口

返回数组/字符串由调用方释放；不要返回局部数组。

```c
char* convertToTitle(int columnNumber);
```

## 示例 1

输入：
```text
1
```
输出：
```text
"A"
```

## 示例 2

输入：
```text
28
```
输出：
```text
"AB"
```

## 自定义输入格式

按顺序每行一个参数：n。数组使用 `[1,2]`，字符串使用双引号。数组长度由平台自动传入。
