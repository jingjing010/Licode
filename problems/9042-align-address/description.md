嵌入式开发中经常要把地址或长度**对齐**到某个边界：DMA 要求缓冲区 4 字节对齐、Flash 只能按页（如 4096 字节）擦除、内存分配器把每次申请的大小向上取整到 8 字节、MPU 区域的起始地址必须是区域大小的倍数……

请你实现两个函数，`align` 一定是 **2 的幂**：

- `align_up(addr, align)`：返回**大于等于** `addr` 的最小的 `align` 的倍数（向上对齐）
- `align_down(addr, align)`：返回**小于等于** `addr` 的最大的 `align` 的倍数（向下对齐）

判题程序依次输出 `align_up(addr, align)` 和 `align_down(addr, align)`，各占一行。

### 示例 1

```
输入：addr = 13, align = 8
输出：
16
8
解释：13 两边的 8 的倍数是 8 和 16。
```

### 示例 2

```
输入：addr = 16, align = 8
输出：
16
16
解释：16 已经对齐，向上、向下对齐都是它本身。
```

### 示例 3

```
输入：addr = 536870913, align = 4
输出：
536870916
536870912
解释：536870913 = 0x20000001（STM32 SRAM 起始地址 + 1），向上对齐到 0x20000004，向下对齐到 0x20000000。
```

### 提示

- `0 <= addr <= 4294901760`（即 `0xFFFF0000`）
- `align = 2^k`，`0 <= k <= 12`（即 `1 <= align <= 4096`）

### 函数说明

```c
uintptr_t align_up(uintptr_t addr, size_t align);
uintptr_t align_down(uintptr_t addr, size_t align);
```

- `addr`：地址（用整数类型 `uintptr_t` 表示）
- `align`：对齐边界，2 的幂

### 自定义输入格式

```
13
8
```

第 1 行是 `addr`，第 2 行是 `align`，均为十进制整数。输出两行：向上对齐结果、向下对齐结果。
