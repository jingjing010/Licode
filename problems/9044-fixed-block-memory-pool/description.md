很多嵌入式系统**禁止使用 `malloc`**：它的执行时间不确定、会产生内存碎片、出错时难以排查。常见的替代方案是**固定大小内存池**：启动时一次性准备 `blockCount` 个大小都为 `blockSize` 字节的内存块，运行时只在这些块里分配和回收。FreeRTOS 的消息缓冲、LwIP 的 `memp`、uC/OS 的 `OSMemGet/OSMemPut` 都是这种设计。

请你设计 `MemoryPool`，用**空闲链表**管理所有空闲块，块用编号 `0 ~ blockCount-1` 表示：

- `MemoryPool* memoryPoolCreate(int blockSize, int blockCount)`：创建内存池，申请 `blockSize * blockCount` 字节的内存。初始时空闲链表为 `0 → 1 → 2 → … → blockCount-1`
- `int memoryPoolAlloc(MemoryPool* obj)`：取出空闲链表**头部**的块，返回它的编号；没有空闲块时返回 `-1`
- `bool memoryPoolRelease(MemoryPool* obj, int index)`：释放编号为 `index` 的块，把它插回空闲链表的**头部**，返回 `true`。如果 `index` 越界，或者这个块当前本来就是空闲的（**重复释放**），什么都不做并返回 `false`
- `int memoryPoolFreeCount(MemoryPool* obj)`：返回当前空闲块的个数
- `void memoryPoolFree(MemoryPool* obj)`：销毁内存池，释放所有内存

> 换句话说，`alloc` 总是优先返回**最近一次被释放、且当前仍空闲**的块；如果没有这样的块，就返回编号最小的、从未被分配过的块。所有操作都应该是 **O(1)** 的。
>
> 面试里这个操作常被叫作 `PoolFree(index)`，这里命名为 `release`，是为了不和力扣 C 语言约定的销毁函数 `memoryPoolFree` 重名。

### 示例 1

```
输入：
["MemoryPool","alloc","alloc","alloc","freeCount"]
[[16,2],[],[],[],[]]
输出：
[null,0,1,-1,0]
解释：只有 2 个块，第 3 次分配失败。
```

### 示例 2

```
输入：
["MemoryPool","alloc","alloc","release","alloc","freeCount"]
[[8,3],[],[],[0],[],[]]
输出：
[null,0,1,true,0,1]
解释：空闲链表 0→1→2。分配 0、1 后剩 2；释放 0 插回头部，链表变成 0→2；再分配得到 0；剩 1 个空闲块（2）。
```

### 示例 3

```
输入：
["MemoryPool","alloc","release","release","release","freeCount"]
[[4,2],[],[0],[0],[5],[]]
输出：
[null,0,true,false,false,2]
解释：第二次释放块 0 是重复释放，返回 false；块 5 不存在，返回 false。
```

### 提示

- `4 <= blockSize <= 64`，且 `blockSize` 是 4 的倍数
- `1 <= blockCount <= 1000`
- `-1000 <= index <= 2000`
- 操作总数不超过 `10^4`，第一个操作一定是 `"MemoryPool"`

### 函数说明

```c
typedef struct {
    /* 你自己定义的成员 */
} MemoryPool;

MemoryPool* memoryPoolCreate(int blockSize, int blockCount);
int memoryPoolAlloc(MemoryPool* obj);
bool memoryPoolRelease(MemoryPool* obj, int index);
int memoryPoolFreeCount(MemoryPool* obj);
void memoryPoolFree(MemoryPool* obj);
```

判题程序会按顺序调用这些函数：构造函数输出 `null`，`alloc` / `freeCount` 输出整数，`release` 输出 `true`/`false`。最后调用 `memoryPoolFree`。

### 自定义输入格式

```
["MemoryPool","alloc","alloc","release","alloc","freeCount"]
[[8,3],[],[],[0],[],[]]
```

第 1 行是操作名数组（`"MemoryPool"`、`"alloc"`、`"release"`、`"freeCount"`），第 2 行是对应的参数数组。
