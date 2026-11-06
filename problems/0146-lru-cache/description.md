请你设计并实现一个满足 [LRU (最近最少使用) 缓存](https://baike.baidu.com/item/LRU) 约束的数据结构。

实现 `LRUCache` 类：

- `LRUCache(int capacity)` 以 **正整数** 作为容量 `capacity` 初始化 LRU 缓存
- `int get(int key)` 如果关键字 `key` 存在于缓存中，则返回关键字的值，否则返回 `-1` 。
- `void put(int key, int value)` 如果关键字 `key` 已经存在，则变更其数据值 `value` ；如果不存在，则向缓存中插入该组 `key-value` 。如果插入操作导致关键字数量超过 `capacity` ，则应该 **逐出** 最久未使用的关键字。

函数 `get` 和 `put` 必须以 `O(1)` 的平均时间复杂度运行。

### 示例 1

```
输入：
["LRUCache","put","put","get","put","get","put","get","get","get"]
[[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]

输出：
[null,null,null,1,null,-1,null,-1,3,4]

解释：
LRUCache lRUCache = new LRUCache(2);
lRUCache.put(1, 1); // 缓存是 {1=1}
lRUCache.put(2, 2); // 缓存是 {1=1, 2=2}
lRUCache.get(1);    // 返回 1
lRUCache.put(3, 3); // 该操作会使得关键字 2 作废，缓存是 {1=1, 3=3}
lRUCache.get(2);    // 返回 -1 (未找到)
lRUCache.put(4, 4); // 该操作会使得关键字 1 作废，缓存是 {4=4, 3=3}
lRUCache.get(1);    // 返回 -1 (未找到)
lRUCache.get(3);    // 返回 3
lRUCache.get(4);    // 返回 4
```

### 提示

- `1 <= capacity <= 3000`
- `0 <= key <= 10000`
- `0 <= value <= 10^5`
- 最多调用 `2 * 10^5` 次 `get` 和 `put`

### 函数说明

```c
typedef struct {
    // 你自己设计需要的成员
} LRUCache;

LRUCache* lRUCacheCreate(int capacity);
int lRUCacheGet(LRUCache* obj, int key);
void lRUCachePut(LRUCache* obj, int key, int value);
void lRUCacheFree(LRUCache* obj);
```

- 这是力扣 C 语言的"设计类"写法：用结构体保存数据，每个方法的第一个参数 `obj` 是指向这个结构体的指针
- `lRUCacheCreate`：用 `malloc`/`calloc` 创建并初始化一个容量为 `capacity` 的缓存，返回它的指针
- `lRUCacheGet`：`key` 存在则返回对应的值（并把它记为最近使用），否则返回 `-1`
- `lRUCachePut`：插入或更新 `key` 的值（并把它记为最近使用），超出容量时逐出最久未使用的 `key`
- `lRUCacheFree`：释放 `lRUCacheCreate` 以及之后申请的所有内存
- `struct` 里的成员由你自己决定（模板中是空的，需要你补充），也可以在它前面定义自己的结构体（比如链表结点）

### 自定义输入格式

```
["LRUCache","put","put","get","put","get","put","get","get","get"]
[[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]
```

第 1 行是操作名数组，第 2 行是每个操作对应的参数数组。第一个操作必须是 `"LRUCache"`，参数是 `[capacity]`；`get` 的参数是 `[key]`，`put` 的参数是 `[key,value]`。
输出每个操作的返回值组成的数组（不带空格），没有返回值的操作输出 `null`，例如 `[null,null,null,1,null,-1,null,-1,3,4]`。
