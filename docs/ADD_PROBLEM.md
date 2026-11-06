# 如何添加一道新题

每道题是 `problems/` 下的一个文件夹，命名为 `四位题号-英文slug`，例如 `problems/0020-valid-parentheses/`。
以 `problems/0001-two-sum/` 为**标准范例**，新题请严格对照它的格式与质量。

## 文件清单

| 文件 | 作用 |
|---|---|
| `meta.json` | 题目元数据（见下） |
| `description.md` | 题目描述（Markdown），展示给用户 |
| `template.c` | 给用户的初始代码：力扣同款函数签名 + 空函数体（必须能编译通过，可以有警告） |
| `solution.c` | 参考答案（用于自检，不直接展示） |
| `driver.c` | 只包含 `main()`：读输入 → 调用用户函数 → 打印输出 |
| `prelude.c` | 可选。需要在用户代码之前出现的定义，如 `struct ListNode` |
| `explanation.md` | **给小白的详细题解**（重点！） |
| `gen.py` | 测试数据生成脚本（推荐，见下文），由 `tools/build.py` 调用 |
| `tests/1.in, 1.out, 2.in, 2.out ...` | 测试数据。前 `samples` 个是公开样例，必须与描述中的示例一致。有 `gen.py` 时由工具自动生成，不要手写 |

## meta.json

```json
{
  "id": 20,
  "slug": "valid-parentheses",
  "title": "有效的括号",
  "difficulty": "简单",          // 简单 / 中等 / 困难
  "tags": ["栈", "字符串"],
  "lists": ["hot100"],            // 所属题单：hot100（力扣热题 100）/ embedded（嵌入式 C），可为空 []
  "leetcode": "https://leetcode.cn/problems/valid-parentheses/",   // 嵌入式原创题写 ""
  "time_limit_ms": 1000,
  "samples": 3,                   // 前几个测试点是公开样例
  "hints": ["渐进式提示1（很轻）", "提示2", "提示3（接近答案）"]
}
```

## 判题时的代码拼接顺序

```
常用头文件 (stdio/stdlib/string/stdbool/limits/math/ctype/stdint)
prelude.c
用户代码 (solution.c / 用户提交)
problems/_common/oj_lib.c   ← 输入输出工具函数，全部以 oj_ 开头
driver.c                    ← main()
```

因此 `driver.c` 可以直接调用用户函数和 `oj_lib.c` 中的工具：

- 读取：`oj_read_int()`、`oj_read_ll()`、`oj_read_bool()`、`oj_read_int_array(&n)`、`oj_read_int_matrix(&rows,&colSizes)`、
  `oj_read_string()`、`oj_read_string_array(&n)`、`oj_read_char_array(&n)`、`oj_read_list()`、`oj_read_tree()`
  `oj_read_char_matrix(&rows,&cols)`（`[["1","0"],["0","1"]]`，每行是 `'\0'` 结尾的 `char*`）、`oj_read_string_matrix(&rows,&colSizes)`
- 输出：`oj_print_int(x)`、`oj_print_bool(b)`、`oj_print_double(x,位数)`、`oj_print_int_array(a,n)`、`oj_print_int_matrix(...)`、
  `oj_print_string(s)`、`oj_print_string_array(a,n)`、`oj_print_char_array(s,n)`、`oj_print_list(head)`、`oj_print_tree(root)`、
  `oj_print_char_matrix(g,rows,cols)`、`oj_print_string_matrix(m,rows,colSizes)`、`oj_print_quoted(s)`（不换行）
- 规范化（答案顺序任意时）：`oj_sort_int_matrix(m,rows,colSizes,每行内部是否也排序)`、`oj_sort_string_array(a,n)`、
  `oj_sort_string_matrix(m,rows,colSizes,每行内部是否也排序)`
- 其他：`oj_cmp_int`、`oj_cmp_str`（qsort 比较函数）、`oj_next_line()`（读下一行原始文本，读完返回 NULL）、`oj_fail(msg)`

> [!IMPORTANT]
> `oj_lib.c` 是所有题共用的，**不要为了某一道题修改它**。题目专用的工具函数写在该题的 `driver.c` 里（放在 `main` 前面，命名以 `drv_` 开头，加 `static`）。
> 编译器是 MinGW gcc 8.1（Windows msvcrt）：打印 `long long` 用 `oj_print_int` 或 `%lld`（会有格式警告，但运行正确），**不要用 `%zu`**。
- 链表题：在 `prelude.c` 中写

  ```c
  #define OJ_HAS_LISTNODE
  struct ListNode {
      int val;
      struct ListNode *next;
  };
  ```

- 二叉树题：`#define OJ_HAS_TREENODE` + `struct TreeNode { int val; struct TreeNode *left; struct TreeNode *right; };`

输入每个参数占一行，使用力扣风格的写法：数组 `[1,2,3]`、字符串 `"abc"`、整数 `9`、链表 `[1,2,4]`、树 `[3,9,20,null,null,15,7]`。
输出同样使用力扣风格（整数直接打印，布尔打印 `true/false`，数组 `[1,2]`，字符串带双引号）。
判题时会忽略每行行尾空格和末尾空行。如果答案不唯一（例如顺序任意），由 driver 先规范化（如排序）再输出。
如果答案有多种都正确且无法通过排序规范化（例如"返回任意一个峰值下标"），由 driver **检查合法性**后输出固定文本（如 `true`），
或者选择保证答案唯一的测试数据。

### 特殊题型约定

- **设计类**（LRU 缓存、最小栈、Trie……）：输入两行，第 1 行操作名 `["LRUCache","put","get"]`，第 2 行参数 `[[2],[1,1],[1]]`
  （参数为字符串时用 `[["apple"],["app"]]`，用 `oj_read_string_matrix` 读取）。
  模板使用力扣 C 语言的写法（`typedef struct {...} LRUCache; LRUCache* lRUCacheCreate(int capacity); ...`）。
  driver 输出力扣风格的结果数组，如 `[null,null,1,-1]`（布尔返回值输出 `true`/`false`）。
- **环形链表 / 相交链表 / 随机指针链表 / 最近公共祖先**等需要"结点引用"的题：按力扣的输入格式（如 `[3,2,0,-4]` + `pos`），
  在 driver 里自行构造，函数说明和"自定义输入格式"里写清楚。
- **原地修改**（返回 `void`）：driver 调用后打印被修改的参数。
- **嵌入式原创题**：`id` 用 9001 起，`leetcode` 写 `""`，`lists` 含 `"embedded"`，`slug` 用英文短横线命名；
  函数签名要贴近真实嵌入式开发（`uint8_t`/`uint16_t`/`uint32_t`、`const uint8_t* buf, size_t len` 等）。

## gen.py：生成测试数据（推荐）

```python
from genlib import *          # arr / mat / s / sarr / carr / cmat / b / tree / lines 以及随机工具

def samples():
    # 与 description.md 中的示例一一对应：(输入, 预期输出)，预期输出照抄题面
    return [
        (lines(arr([2, 7, 11, 15]), 9), "[0,1]"),
        (lines(arr([3, 2, 4]), 6), "[1,2]"),
    ]

def cases():
    # 隐藏测试点的输入（预期输出由 solution.c 自动生成）：边界情况 + 随机小数据 + 最大规模数据
    return [lines(arr(rand_arr(10**4, -10**9, 10**9)), 0), ...]
```

- 运行 `python tools/build.py 题号`：清空 `tests/` → 写入输入 → 用 `solution.c` 生成 `.out` → **核对样例输出与题面一致** → 完整自检。
- 随机种子固定为题号，重复构建结果不变。`genlib.py` 里有 `rand_arr`、`rand_sorted`、`rand_distinct`、`rand_str`、`perm`、
  `rand_tree`（随机二叉树层序）、`rand_bst(vals)` 等。
- 测试点建议 10~20 个，要覆盖：最小规模、全相同/全负数等特殊值、题目上限规模（检查 TLE）。单个输入不超过 2MB/行。
- `solution.c` 要用题目期望的最优复杂度，**生成的 .out 就是标准答案，solution 写错测试就全错了**；
  拿不准的题，在 `gen.py` 里写一个 Python 暴力解对随机小数据做交叉验证（`assert`）。

## explanation.md 要求（面向零基础小白）

参照 `0001-two-sum/explanation.md`，至少包含：

1. **📖 先读懂题目**：大白话复述 + 用表格/图示走一遍示例 + 容易忽略的细节
2. **🧰 需要的 C 语言知识**：这道题会用到的语法点（指针、malloc、`*returnSize`、字符串 `'\0'`、结构体指针等），讲清楚"为什么"
3. **💡 思路一（最朴素）**：思路 → 手动模拟表格 → 带逐行中文注释的完整代码 → 复杂度
4. **🚀 思路二（优化，如有）**：同上，讲清楚为什么能优化
5. **⚠️ 小白常见错误**：至少 4 条，具体到代码
6. **📊 方法对比表**
7. **🔗 举一反三**：相关题目/思考题

所有题解中的代码必须能在本 OJ 直接 AC（可复制粘贴提交）。`verify.py` 会自动提交 explanation.md 里**定义了 template.c 全部函数**的
` ```c ` 代码块；错误示范或示意片段请在代码里带上 `❌` 或 `...`，它们会被跳过。

## 自检

```bash
python tools/build.py 20          # 有 gen.py 的题：生成测试数据 + 核对样例 + 完整自检
python tools/verify.py --gen 20   # 没有 gen.py 的题：用 solution.c 生成 tests/*.out（请人工核对样例输出是否正确！）
python tools/verify.py 20         # 检查文件齐全、meta 合法、solution.c 全部 AC、template.c 可编译
```

Windows PowerShell 下中文乱码时先执行：`$env:PYTHONIOENCODING='utf-8'; [Console]::OutputEncoding=[Text.Encoding]::UTF8`
