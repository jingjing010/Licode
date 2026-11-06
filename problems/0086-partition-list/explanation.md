# 分隔链表：题解

## 📖 先读懂题目

把链表拆成小于x与大于等于x的两条链，各自保持原顺序，最后把小链接到大链。两个哑结点让空链与普通链使用同一套连接逻辑。大链尾必须指向NULL，否则旧next可能形成环。

### 示例1

输入：
```text
[1,4,3,2,5,2]
3
```
输出：
```text
[1,2,2,4,3,5]
```

### 示例2

输入：
```text
[2,1]
2
```
输出：
```text
[1,2]
```


## 🧰 C 语言知识

数组参数传入的是指针，长度单独传递。字符串结尾的`'\0'`不是普通数据，动态结果必须多留一个字节。链表通过`next`连接，断开或拼接前要确定后继仍可找到。返回数组时同时设置`*returnSize`。

## 💡 解题步骤

1. 想象把一队人分成两队：「矮于 x 的」一队，「不矮于 x 的」另一队，每个人按原来的顺序排进自己的队，最后两队接起来。
2. 准备两个哑结点 smallDummy、largeDummy，以及各自的尾指针。遍历原链表，把每个结点接到对应链表的尾巴上。
3. 最后 smallTail->next = largeDummy.next，并且一定要 largeTail->next = NULL，否则可能形成环。

## 可直接提交的 C 代码

```c
struct ListNode* partition(struct ListNode* head, int x) {
    struct ListNode smallDummy, largeDummy;
    struct ListNode* small = &smallDummy;
    struct ListNode* large = &largeDummy;
    for (struct ListNode* p = head; p != NULL; p = p->next) {
        if (p->val < x) {
            small->next = p;
            small = p;
        } else {
            large->next = p;
            large = p;
        }
    }
    large->next = NULL;
    small->next = largeDummy.next;
    return smallDummy.next;
}
```

## 📊 复杂度

时间 O(n)，空间 O(1)。先用题面样例逐步跟踪变量，再检查最短输入与重复值，不应仅凭一个正常样例判断算法正确。

## ⚠️ 常见错误

- 把数组边界`i < n`误写成`i <= n`。
- 忘记返回数组的有效长度，或字符串结尾缺少`'\0'`。
- 把题目中的严格比较写成允许相等，或把有重数的元素当作集合。
- 返回局部数组地址，函数退出后该内存不再有效。

## 🔗 举一反三

改变输入长度为1、重复值、边界整数，手工验证每一步保存的状态。思考能否在输入逐个到达时保留相同的状态完成计算。
