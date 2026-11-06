给你两个单词 `word1` 和 `word2`， *请返回将 `word1` 转换成 `word2` 所使用的最少操作数* 。

你可以对一个单词进行如下三种操作：

- 插入一个字符
- 删除一个字符
- 替换一个字符

### 示例 1

```
输入：word1 = "horse", word2 = "ros"
输出：3
解释：
horse -> rorse (将 'h' 替换为 'r')
rorse -> rose (删除 'r')
rose -> ros (删除 'e')
```

### 示例 2

```
输入：word1 = "intention", word2 = "execution"
输出：5
解释：
intention -> inention (删除 't')
inention -> enention (将 'i' 替换为 'e')
enention -> exention (将 'n' 替换为 'x')
exention -> exection (将 'n' 替换为 'c')
exection -> execution (插入 'u')
```

### 提示

- `0 <= word1.length, word2.length <= 500`
- `word1` 和 `word2` 由小写英文字母组成

### 函数说明

```c
int minDistance(char* word1, char* word2);
```

- `word1`、`word2`：以 `'\0'` 结尾的字符串（可能是空串）
- 返回值：把 `word1` 变成 `word2` 的最少操作数

### 自定义输入格式

```
"horse"
"ros"
```

第 1 行是 `word1`，第 2 行是 `word2`，都带双引号（空串写作 `""`）。
