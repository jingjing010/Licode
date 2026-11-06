# 将标题首字母大写：题解

## 📖 先读懂题目

标题由英文字母单词和单空格组成，无首尾空格。长度1或2的单词全小写，其他单词仅首字母大写，返回新标题。长度1到100。

| 示例 | 输入参数 | 返回结果 |
|---|---|---|
| 1 | `"capiTalIze tHe titLe"` | `"Capitalize The Title"` |
| 2 | `"First leTTeR of EACH Word"` | `"First Letter of Each Word"` |

## 🧰 需要的 C 语言知识

C字符串以`'\0'`结束，`strlen`返回有效字符数，不包含结束符。使用`ctype.h`判断字符时先转成`unsigned char`，避免负char带来未定义行为。

申请输出字符串时，要在有效字符之外多留1字节写入结束符。参考实现返回动态内存，由调用方负责释放。

## 💡 推导与实现

每个单词先转小写，长度大于2时再把首字母转大写。

先按定义手工处理第一个示例，再确认每一步保存的状态足够决定下一步。循环结束时只返回题目要求的结果，不返回尚未处理的中间状态。

```c
char *capitalizeTitle(char *title) {
    int n = (int)strlen(title);
    char *out = malloc(n + 1);
    memcpy(out, title, n + 1);
    for (int i = 0; i < n;) {
        int j = i;
        while (j < n && out[j] != ' ') {
            out[j] = (char)tolower((unsigned char)out[j]);
            ++j;
        }
        if (j - i > 2)
            out[i] = (char)toupper((unsigned char)out[i]);
        i = j + 1;
    }
    return out;
}
```

## 📊 复杂度与取舍

| 方法 | 代价 | 用途 |
|---|---|---|
| 上述实现 | 时间 O(n)，输出空间 O(n) | 正式提交 |

## ⚠️ 常见错误

- 忘记字符串末尾的`'\0'`，导致打印越过已申请内存。
- 只申请有效字符数大小的缓冲区，没有给结束符留空间。
- 忽略题面约束与特殊边界，直接把某个正常样例的结论推广到所有输入。
- 先用int乘法再转换到64位；溢出已经发生，转换无法补救。

## 🔗 举一反三

尝试把同一处理过程改成逐个输入的流式接口，思考需要保留哪些状态。用空边界、最小值、最大值和重复值检查自己的实现。
