上一题的固定大小内存池每次只能分配**一个**块。如果需要一次分配**连续的多个块**（比如一个 DMA 描述符链、一段连续的 Flash 扇区、文件系统里的连续簇），常用的方案是**位图分配器**：用 1 个 bit 表示 1 个块，`1` 表示已分配，`0` 表示空闲。管理 4096 个块只需要 512 字节的位图，FAT/ext 文件系统的空闲块管理、Linux 的 `bitmap_find_next_zero_area` 都是这种思路。

请你设计 `BitmapAllocator`，管理编号为 `0 ~ blockCount-1` 的块，初始全部空闲：

- `BitmapAllocator* bitmapAllocatorCreate(int blockCount)`：创建分配器
- `int bitmapAllocatorAlloc(BitmapAllocator* obj, int count)`：找到**编号最小**的、连续 `count` 个块都空闲的起点 `start`（首次适应，first fit），把 `start ~ start+count-1` 标记为已分配，返回 `start`；找不到返回 `-1`，什么都不改
- `bool bitmapAllocatorRelease(BitmapAllocator* obj, int start, int count)`：释放 `start ~ start+count-1` 这些块，返回 `true`。如果范围越界（`start < 0` 或 `start + count > blockCount`），或者范围内**有任何一块本来就是空闲的**（重复释放 / 释放了不属于自己的块），则什么都不改，返回 `false`
- `int bitmapAllocatorUsedCount(BitmapAllocator* obj)`：返回当前已分配的块数
- `void bitmapAllocatorFree(BitmapAllocator* obj)`：销毁分配器，释放所有内存

> 推荐用 `uint32_t` 数组作为位图（每个元素管理 32 个块），这也是真实系统的做法。

### 示例 1

```
输入：
["BitmapAllocator","alloc","alloc","usedCount","alloc"]
[[10],[3],[4],[],[4]]
输出：
[null,0,3,7,-1]
解释：位图 0000000000 → 分配 3 块得到 0：1110000000 → 分配 4 块得到 3：1111111000。
     已分配 7 块；只剩 3 个空闲块，分配 4 块失败。
```

### 示例 2

```
输入：
["BitmapAllocator","alloc","alloc","alloc","release","alloc","alloc","usedCount"]
[[8],[2],[2],[2],[2,2],[1],[3],[]]
输出：
[null,0,2,4,true,2,-1,5]
解释：分配 3 次后位图为 11111100；释放 2~3 后为 11001100；
     分配 1 块，最小的空闲块是 2：11101100；
     分配 3 块，空闲块是 3、6、7，没有连续 3 块，失败（虽然总共有 3 个空闲块）。
```

### 示例 3

```
输入：
["BitmapAllocator","alloc","release","release","release","usedCount"]
[[40],[33],[0,33],[0,1],[30,20],[]]
输出：
[null,0,true,false,false,0]
解释：分配 33 块（跨越了两个 uint32_t）后全部释放；再次释放块 0 是重复释放，返回 false；
     30 + 20 > 40，越界，返回 false。
```

### 提示

- `1 <= blockCount <= 4096`
- `1 <= count <= 5000`
- `-5000 <= start <= 5000`
- 操作总数不超过 `5000`，第一个操作一定是 `"BitmapAllocator"`

### 函数说明

```c
typedef struct {
    /* 你自己定义的成员 */
} BitmapAllocator;

BitmapAllocator* bitmapAllocatorCreate(int blockCount);
int bitmapAllocatorAlloc(BitmapAllocator* obj, int count);
bool bitmapAllocatorRelease(BitmapAllocator* obj, int start, int count);
int bitmapAllocatorUsedCount(BitmapAllocator* obj);
void bitmapAllocatorFree(BitmapAllocator* obj);
```

判题程序会按顺序调用这些函数：构造函数输出 `null`，`alloc` / `usedCount` 输出整数，`release` 输出 `true`/`false`。最后调用 `bitmapAllocatorFree`。

### 自定义输入格式

```
["BitmapAllocator","alloc","alloc","usedCount","alloc"]
[[10],[3],[4],[],[4]]
```

第 1 行是操作名数组（`"BitmapAllocator"`、`"alloc"`、`"release"`、`"usedCount"`），第 2 行是对应的参数数组。
