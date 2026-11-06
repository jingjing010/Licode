给你一个字符数组 `letters`，该数组按**非递减顺序**排序，以及一个字符 `target`。`letters` 里**至少有两个不同**的字符。

返回 `letters` 中大于 `target` 的最小的字符。如果不存在这样的字符，则返回 `letters` 的第一个字符。

### 示例 1

```
输入：letters = ["c","f","j"], target = "a"
输出："c"
解释：letters 中字典上比 'a' 大的最小字符是 'c'。
```

### 示例 2

```
输入：letters = ["c","f","j"], target = "c"
输出："f"
解释：letters 中字典顺序上大于 'c' 的最小字符是 'f'。
```

### 示例 3

```
输入：letters = ["x","x","y","y"], target = "z"
输出："x"
解释：letters 中没有一个字符在字典上大于 'z'，所以我们返回 letters[0]。
```

### 提示

- `2 <= letters.length <= 10^4`
- `letters[i]` 是一个小写字母
- `letters` 按**非递减顺序**排序
- `letters` 最少包含两个不同的字母
- `target` 是一个小写字母

### 函数说明

```c
char nextGreatestLetter(char* letters, int lettersSize, char target);
```

- `letters`：字符数组首地址（注意它**不是**字符串，不保证以 `'\0'` 结尾，请用 `lettersSize` 控制长度），`lettersSize`：字符个数
- `target`：目标字符
- 返回值：一个字符

### 自定义输入格式

```
["c","f","j"]
"a"
```

第 1 行是字符数组 `letters`，第 2 行是字符 `target`（带双引号）。输出的字符会带双引号。
