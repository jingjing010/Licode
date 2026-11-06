给你一个单链表的头节点 `head` ，请你判断该链表是否为回文链表。如果是，返回 `true` ；否则，返回 `false` 。

### 示例 1

```
1 -> 2 -> 2 -> 1
```

```
输入：head = [1,2,2,1]
输出：true
```

### 示例 2

```
1 -> 2
```

```
输入：head = [1,2]
输出：false
```

### 提示

- 链表中节点数目在范围 `[1, 10^5]` 内
- `0 <= Node.val <= 9`

**进阶：** 你能否用 `O(n)` 时间复杂度和 `O(1)` 空间复杂度解决此题？

### 函数说明

```c
struct ListNode {
    int val;
    struct ListNode *next;
};

bool isPalindrome(struct ListNode* head);
```

- `struct ListNode` 已由系统定义，**不要**在代码里重复定义
- `head`：链表的头指针（至少有 1 个结点）
- 返回值：是回文链表返回 `true`，否则返回 `false`

### 自定义输入格式

```
[1,2,2,1]
```

只有 1 行：链表各结点的值。输出 `true` 或 `false`。
