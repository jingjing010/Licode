和 WiFi / 4G 模块打交道时，经常要在模块返回的一大段文本里找关键字：有没有 `"OK"`？有没有 `"ERROR"`？`"+IPD,"` 后面跟着的是收到的数据……这就是 `strstr` 的工作。

请你实现 `my_strstr(haystack, needle)`：在字符串 `haystack` 中查找字符串 `needle` **第一次出现**的位置，返回指向该位置的指针；找不到返回 `NULL`。如果 `needle` 是空串，返回 `haystack`。

> **不要调用库函数 `strstr` / `strncmp` / `memcmp` / `strchr` 等**，请自己用指针完成。

判题程序把返回的指针换算成下标输出：返回 `NULL` 输出 `-1`，否则输出 `返回值 - haystack`。

### 示例 1

```
输入：haystack = "AT+CSQ\n+CSQ: 23,0\nOK", needle = "OK"
输出：18
解释："AT+CSQ" 占下标 0~5，\n 是下标 6（算 1 个字符），"+CSQ: 23,0" 占下标 7~16，\n 是下标 17，"OK" 从下标 18 开始。
```

### 示例 2

```
输入：haystack = "aaab", needle = "ab"
输出：2
解释：下标 0、1 开始都只能匹配一个 'a'，下标 2 开始匹配成功。
```

### 示例 3

```
输入：haystack = "+CME ERROR: 10", needle = "OK"
输出：-1
```

### 提示

- `0 <= strlen(haystack), strlen(needle) <= 10^4`
- 字符串由可打印 ASCII 字符和换行符 `\n` 组成

### 函数说明

```c
char* my_strstr(const char* haystack, const char* needle);
```

- 返回值：指向 `haystack` 中第一次匹配位置的指针；找不到返回 `NULL`；`needle` 为空串时返回 `haystack`
- 和标准库一样，返回类型是 `char*`（不带 `const`），返回前需要做一次类型转换

### 自定义输入格式

```
"aaab"
"ab"
```

两行，分别为带双引号的 `haystack` 和 `needle`（支持 `\n`、`\"`、`\\` 转义）。输出为下标或 `-1`。
