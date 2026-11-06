给你一个字符串数组，请你将 **字母异位词** 组合在一起。可以按任意顺序返回结果列表。

**字母异位词** 是由重新排列源单词的所有字母得到的一个新单词。

### 示例 1

```
输入：strs = ["eat","tea","tan","ate","nat","bat"]
输出：[["ate","eat","tea"],["bat"],["nat","tan"]]
解释：
在 strs 中没有字符串可以通过重新排列来形成 "bat"。
字符串 "nat" 和 "tan" 是字母异位词，因为它们可以重新排列以形成彼此。
字符串 "ate"，"eat" 和 "tea" 是字母异位词，因为它们可以重新排列以形成彼此。
```

### 示例 2

```
输入：strs = [""]
输出：[[""]]
```

### 示例 3

```
输入：strs = ["a"]
输出：[["a"]]
```

### 提示

- `1 <= strs.length <= 10^4`
- `0 <= strs[i].length <= 100`
- `strs[i]` 仅包含小写字母

### 函数说明

```c
char*** groupAnagrams(char** strs, int strsSize, int* returnSize, int** returnColumnSizes);
```

- `strs`：字符串数组，`strs[i]` 是以 `'\0'` 结尾的字符串；`strsSize`：字符串个数
- 返回值：用 `malloc` 申请的"二维字符串数组"，第 `g` 组是 `char**`，里面放这一组的字符串（可以直接使用 `strs[i]` 这个指针）
- `*returnSize`：返回的组数
- `*returnColumnSizes`：你需要 `malloc` 一个长度为 `*returnSize` 的 `int` 数组，第 `g` 个元素写第 `g` 组有几个字符串，再把它的地址写进 `*returnColumnSizes`

### 自定义输入格式

```
["eat","tea","tan","ate","nat","bat"]
```

只有 1 行，是字符串数组 `strs`。（组的顺序、组内字符串的顺序都任意，判题时会先把每组内部按字典序排序，再把所有组按字典序排序后输出）
