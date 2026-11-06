很多硬件对地址有**对齐**要求：DMA 的缓冲区要 4 字节对齐，Cache 行是 32 字节对齐，Flash 擦除以 4KB 扇区为单位，MPU 保护区域的起始地址要对齐到区域大小……写驱动和内存分配器时，几乎天天都要做"地址对齐"运算。

给定地址 `addr` 和对齐值 `align`（`align` 一定是 **2 的幂**），请实现两个函数：

- `align_up(addr, align)`：返回 **大于等于** `addr` 的最小的 `align` 的倍数
- `align_down(addr, align)`：返回 **小于等于** `addr` 的最大的 `align` 的倍数

如果 `addr` 本身已经是 `align` 的倍数，两个函数都返回 `addr`。

判题程序先输出 `align_up(addr, align)`，再输出 `align_down(addr, align)`，每个一行（十进制）。

### 示例 1

```
输入：addr = 13, align = 8
输出：
16
8
解释：8 的倍数中，>= 13 的最小的是 16，<= 13 的最大的是 8。
```

### 示例 2

```
输入：addr = 16, align = 8
输出：
16
16
解释：16 已经是 8 的倍数。
```

### 示例 3

```
输入：addr = 536870913, align = 4
输出：
536870916
536870912
解释：536870913 = 0x20000001（STM32 的 SRAM 起始地址 + 1）。
     向上对齐到 0x20000004，向下对齐到 0x20000000。
```

### 提示

- `0 <= addr <= 4294901760`（即 `0xFFFF0000`）
- `align = 2^k`，`0 <= k <= 12`（即 `1 <= align <= 4096`）

### 函数说明

```c
uintptr_t align_up(uintptr_t addr, size_t align);
uintptr_t align_down(uintptr_t addr, size_t align);
```

- `uintptr_t`（`<stdint.h>`）：一个足以存放指针值的无符号整数类型，专门用来对地址做算术运算
- `align`：对齐值，保证是 2 的幂

### 自定义输入格式

```
13
8
```

第 1 行是 `addr`，第 2 行是 `align`，均为十进制整数。输出两行。
