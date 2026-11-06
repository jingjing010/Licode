串口命令行、AT 指令、NMEA（GPS）报文都长这样：`"SET,LED,1"`、`"$GPGGA,123519,4807.038,N"`。解析它们的第一步就是**按分隔符切开**。

在没有（或不想用）`malloc` 的单片机上，最常见的做法是**原地分割**：不复制任何字符，而是直接在原字符串上把分隔符改成 `'\0'`，再用一个指针数组记录每个子串的起始地址。C 标准库的 `strtok` 就是这么做的。

请你实现 `split_string(str, delim, tokens, maxTokens)`：

- 把 `str` 按字符 `delim` 分割，**连续的分隔符视为一个**，开头和结尾的分隔符忽略——也就是说**不产生空子串**
- 第 `i` 个子串的起始地址存入 `tokens[i]`，子串必须以 `'\0'` 结尾（把它后面的分隔符改成 `'\0'`）
- 最多切出 `maxTokens` 个子串：切出第 `maxTokens` 个后**立即停止**，`str` 剩余的部分不必处理
- 返回切出的子串个数

> **不要调用 `malloc` / `strtok` / `strchr` 等**。`tokens[i]` 必须指向 `str` 内部（原地分割），判题程序会检查。

判题程序调用 `split_string(str, delim, tokens, maxTokens)`，按顺序输出返回的所有子串。

### 示例 1

```
输入：str = "SET,LED,1", delim = ",", maxTokens = 8
输出：["SET","LED","1"]
解释：把两个 ',' 改成 '\0'，内存变成 S E T \0 L E D \0 1 \0，tokens 依次指向 'S'、'L'、'1' 三个位置。
```

### 示例 2

```
输入：str = "  hello   world ", delim = " ", maxTokens = 8
输出：["hello","world"]
解释：开头、结尾和中间连续的空格都被跳过，不产生空子串。
```

### 示例 3

```
输入：str = "a,b,c,d", delim = ",", maxTokens = 2
输出：["a","b"]
解释：切出 2 个子串后立即停止。
```

### 提示

- `0 <= strlen(str) <= 10^5`，`str` 由可打印 ASCII 字符组成
- `delim` 是一个可打印 ASCII 字符
- `1 <= maxTokens <= 10^5`，`tokens` 数组的长度恰好为 `maxTokens`

### 函数说明

```c
int split_string(char* str, char delim, char* tokens[], int maxTokens);
```

- `str`：要分割的字符串，函数会**修改**它
- `delim`：分隔符
- `tokens`：输出参数，存放各子串的起始地址
- `maxTokens`：`tokens` 数组的容量
- 返回值：子串个数（`0 ~ maxTokens`）

### 自定义输入格式

```
"SET,LED,1"
","
8
```

第 1 行是带双引号的 `str`，第 2 行是带双引号的分隔符（只取第一个字符），第 3 行是 `maxTokens`。输出为子串数组。
