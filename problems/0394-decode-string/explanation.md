# 394. 字符串解码 —— 小白详细题解

> 括号一嵌套，就要想到**栈**或者**递归**。这道题两种写法都很经典，还能顺便练会 C 语言里"会自动变长的字符串"。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> `k[xxx]` 表示把 `xxx` 重复 `k` 遍。括号可以套括号，从里往外展开就行。

| 编码 | 展开过程 | 结果 |
|---|---|---|
| `3[a]2[bc]` | `aaa` + `bcbc` | `aaabcbc` |
| `3[a2[c]]` | 里层 `2[c]` = `cc` → `3[acc]` | `accaccacc` |
| `abc3[cd]xyz` | `abc` + `cdcdcd` + `xyz` | `abccdcdcdxyz` |

**几个需要注意的细节：**

1. **数字可能是多位数**，比如 `100[a]`，要把 `1`、`0`、`0` 拼成 100，而不是只看一位。
2. 括号外面也可以有普通字母（示例 4 的 `abc` 和 `xyz`）。
3. 输入很短（≤ 30），但输出可能很长（`300[300[a]]` 有 9 万个字符），**不能开固定大小的小数组**。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 字符转数字、拼多位数

```c
int k = 0;
while (s[i] >= '0' && s[i] <= '9') {
    k = k * 10 + (s[i] - '0');    // '7' - '0' == 7；"123" → 1 → 12 → 123
    i++;
}
```

### 2. 会自动变长的字符串：`realloc`

C 的字符串长度是固定的，结果有多长事先不知道，我们自己做一个"动态字符串"：

```c
typedef struct {
    char* buf;   // 字符数据，始终以 '\0' 结尾
    int len;     // 当前长度（不含 '\0'）
    int cap;     // 已申请的容量
} Str;
```

追加内容前检查容量，不够就用 `realloc` **翻倍**扩容。`realloc(p, newSize)` 会申请一块更大的内存，把旧内容复制过去，并释放旧内存，返回新地址。

> 💬 为什么翻倍而不是每次 +1？每次 +1 的话，追加 n 个字符要复制 1+2+...+n ≈ n²/2 次；翻倍的话总复制量不超过 2n。

### 3. `memcpy`

`memcpy(dst, src, n)` 把 `src` 开始的 n 个字节复制到 `dst`。比逐个字符复制写起来更短。

---

## 💡 第三步：思路一 —— 递归

### 思路

观察 `k[...]` 里面的 `...`：它本身就是一个**格式完全相同**的编码串！所以可以写一个函数 `decode`，从位置 `pos` 开始解码，**遇到 `]` 或字符串结束就返回**：

- 遇到字母：直接追加到结果；
- 遇到数字：读出完整的 k，跳过 `[`，**递归调用 decode** 解出括号里的内容，跳过 `]`，把它重复 k 次追加到结果。

`pos` 要在递归调用之间共享（里层读到哪了，外层要接着读），所以传指针 `int* pos`。

### 手动模拟（`s = "3[a2[c]]"`）

| 层 | 读到 | 动作 | 这一层的结果 |
|---|---|---|---|
| 1 | `3[` | k=3，进入第 2 层 | `` |
| 2 | `a` | 追加 | `a` |
| 2 | `2[` | k=2，进入第 3 层 | `a` |
| 3 | `c` | 追加 | `c` |
| 3 | `]` | 返回 `c` | |
| 2 | | `c` 重复 2 次 | `acc` |
| 2 | `]` | 返回 `acc` | |
| 1 | | `acc` 重复 3 次 | `accaccacc` ✅ |

### 代码

```c
typedef struct {
    char* buf;
    int len;
    int cap;
} Str;

static Str newStr(void) {
    Str d;
    d.cap = 16;
    d.len = 0;
    d.buf = (char*)malloc(d.cap);
    d.buf[0] = '\0';
    return d;
}

// 在 d 末尾追加 src 的前 n 个字符
static void append(Str* d, const char* src, int n) {
    while (d->len + n + 1 > d->cap) {          // +1 给 '\0' 留位置
        d->cap *= 2;
        d->buf = (char*)realloc(d->buf, d->cap);
    }
    memcpy(d->buf + d->len, src, n);
    d->len += n;
    d->buf[d->len] = '\0';
}

// 从 s[*pos] 开始解码，结果追加到 out；遇到 ']' 或结尾时停止
static void decode(const char* s, int* pos, Str* out) {
    while (s[*pos] != '\0' && s[*pos] != ']') {
        char c = s[*pos];
        if (c >= '0' && c <= '9') {
            int k = 0;
            while (s[*pos] >= '0' && s[*pos] <= '9') {   // 读完整的多位数
                k = k * 10 + (s[*pos] - '0');
                (*pos)++;
            }
            (*pos)++;                          // 跳过 '['
            Str inner = newStr();
            decode(s, pos, &inner);            // 递归解码括号里的内容
            (*pos)++;                          // 跳过 ']'
            for (int i = 0; i < k; i++) {
                append(out, inner.buf, inner.len);
            }
            free(inner.buf);
        } else {
            append(out, &c, 1);                // 普通字母
            (*pos)++;
        }
    }
}

char* decodeString(char* s) {
    Str out = newStr();
    int pos = 0;
    decode(s, &pos, &out);
    return out.buf;                            // buf 是 malloc 出来的，可以直接返回
}
```

### 复杂度分析

- **时间复杂度 O(输出长度)**：每个输出字符只被复制常数次（加上嵌套层数的因子）。
- **空间复杂度 O(输出长度)**：递归深度最多 15 层（输入只有 30 个字符）。

---

## 🚀 第四步：思路二 —— 两个栈（不用递归）

### 思路

把递归"手动"改成栈：

- `cur`：当前这一层已经解出的字符串；`k`：正在读的数字。
- 遇到 **数字**：`k = k * 10 + 数字`。
- 遇到 **`[`**：要进入新的一层了。把 `cur` 和 `k` **压栈保存**，然后 `cur` 清空、`k` 清零。
- 遇到 **`]`**：这一层结束。弹出上一层的字符串 `prev` 和次数 `times`，把 `cur` 重复 `times` 次接到 `prev` 后面，`cur = prev`。
- 遇到 **字母**：追加到 `cur`。

### 手动模拟（`s = "3[a2[c]]"`）

| 字符 | 动作 | 栈（字符串, 次数） | cur | k |
|---|---|---|---|---|
| `3` | 读数字 | | `` | 3 |
| `[` | 压栈 | (``, 3) | `` | 0 |
| `a` | 追加 | (``, 3) | `a` | 0 |
| `2` | 读数字 | (``, 3) | `a` | 2 |
| `[` | 压栈 | (``, 3) (`a`, 2) | `` | 0 |
| `c` | 追加 | (``, 3) (`a`, 2) | `c` | 0 |
| `]` | 弹出 (`a`,2)：`a` + `cc` | (``, 3) | `acc` | 0 |
| `]` | 弹出 (``,3)：`` + `acc`×3 | | `accaccacc` ✅ | 0 |

### 代码

```c
typedef struct {
    char* buf;
    int len;
    int cap;
} Str;

static Str newStr(void) {
    Str d;
    d.cap = 16;
    d.len = 0;
    d.buf = (char*)malloc(d.cap);
    d.buf[0] = '\0';
    return d;
}

static void append(Str* d, const char* src, int n) {
    while (d->len + n + 1 > d->cap) {
        d->cap *= 2;
        d->buf = (char*)realloc(d->buf, d->cap);
    }
    memcpy(d->buf + d->len, src, n);
    d->len += n;
    d->buf[d->len] = '\0';
}

char* decodeString(char* s) {
    int n = strlen(s);
    Str* strStack = (Str*)malloc(sizeof(Str) * (n + 1));   // 每层进入前的字符串
    int* numStack = (int*)malloc(sizeof(int) * (n + 1));   // 每层的重复次数
    int top = 0;
    Str cur = newStr();
    int k = 0;
    for (int i = 0; i < n; i++) {
        char c = s[i];
        if (c >= '0' && c <= '9') {
            k = k * 10 + (c - '0');               // 多位数
        } else if (c == '[') {
            strStack[top] = cur;                  // 保存当前层
            numStack[top] = k;
            top++;
            cur = newStr();                       // 开始新的一层
            k = 0;
        } else if (c == ']') {
            top--;
            Str prev = strStack[top];             // 回到上一层
            int times = numStack[top];
            for (int t = 0; t < times; t++) {
                append(&prev, cur.buf, cur.len);  // 把这一层重复 times 次接上去
            }
            free(cur.buf);
            cur = prev;
        } else {
            append(&cur, &c, 1);                  // 普通字母
        }
    }
    free(strStack);
    free(numStack);
    return cur.buf;
}
```

### 复杂度分析

- **时间复杂度 O(输出长度)**，**空间复杂度 O(输出长度)**，和递归一样，只是把系统调用栈换成了自己的数组。

---

## ⚠️ 第五步：小白常见错误

1. **只读一位数字**：`k = s[i] - '0'` → `10[a]` 会被当成 `1` 和 `0[a]`。
2. **结果用固定大小数组** `char res[1000]` → `300[300[a]]` 有 90000 个字符，直接越界。
3. **忘了给 `'\0'` 留位置**：扩容条件写成 `len + n > cap`，刚好填满时 `buf[len] = '\0'` 越界一个字节。
4. **`realloc` 的返回值没接住**：`realloc(d->buf, d->cap);` 不赋值回去，旧指针可能已经失效。
5. **`[` 之后 `k` 不清零** → 下一个数字会接在旧数字后面，`2[a]3[b]` 的 3 会变成 23。
6. **返回局部数组** `char res[100005]; return res;` → 函数返回后这块内存就无效了，必须 `malloc`。

---

## 📊 第六步：两种方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 递归 | O(输出长度) | O(输出长度) | ⭐⭐ | 代码贴近题意，推荐先写 |
| 双栈 | O(输出长度) | O(输出长度) | ⭐⭐⭐ | 理解"递归 = 栈"的好练习 |

---

## 🔗 举一反三

- **20. 有效的括号**：最基础的括号 + 栈。
- **224. 基本计算器**：遇到 `(` 保存当前结果和符号，遇到 `)` 弹出合并，和本题双栈写法一模一样。
- **726. 原子的数量**：`(OH)2` 这类化学式，同样是"括号 + 倍数"。
- **思考题**：如果只要求输出解码后字符串的**长度**（可能非常大，比如 10¹⁸），能不能不真的展开？
