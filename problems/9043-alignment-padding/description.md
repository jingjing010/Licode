编译器在排布结构体成员时，会在成员之间插入**填充字节**（padding），保证每个成员都落在自己对齐要求的地址上。这就是 `struct { char a; int b; char c; }` 的 `sizeof` 是 12 而不是 6 的原因。内存分配器、协议打包、DMA 描述符布局里也处处需要这种计算。

请你实现两个函数，`align` 一定是 **2 的幂**：

- `is_aligned(addr, align)`：`addr` 是否是 `align` 的倍数
- `align_padding(addr, align)`：从 `addr` 开始，至少要再跳过多少个字节，才能到达一个 `align` 的倍数。`addr` 已经对齐时返回 `0`

判题程序依次输出 `is_aligned(addr, align)`（`true` / `false`）和 `align_padding(addr, align)`，各占一行。

### 示例 1

```
输入：addr = 12, align = 4
输出：
true
0
解释：12 是 4 的倍数，已经对齐，不需要填充。
```

### 示例 2

```
输入：addr = 13, align = 4
输出：
false
3
解释：13 不是 4 的倍数；下一个 4 的倍数是 16，需要填充 16 - 13 = 3 个字节。
```

### 示例 3

```
输入：addr = 536870913, align = 8
输出：
false
7
解释：536870913 = 0x20000001，下一个 8 的倍数是 0x20000008，需要填充 7 个字节。
```

### 提示

- `0 <= addr <= 4294967295`（即 `0xFFFFFFFF`）
- `align = 2^k`，`0 <= k <= 12`（即 `1 <= align <= 4096`）

### 函数说明

```c
bool is_aligned(uintptr_t addr, size_t align);
size_t align_padding(uintptr_t addr, size_t align);
```

- `addr`：地址（用整数类型 `uintptr_t` 表示）
- `align`：对齐边界，2 的幂
- `align_padding` 的返回值满足 `0 <= 返回值 < align`

### 自定义输入格式

```
13
4
```

第 1 行是 `addr`，第 2 行是 `align`，均为十进制整数。输出两行：是否对齐、填充字节数。
