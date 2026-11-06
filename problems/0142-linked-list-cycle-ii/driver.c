int main(void) {
    int n;
    int* a = oj_read_int_array(&n);
    int pos = oj_read_int();
    struct ListNode* nodes = (struct ListNode*)malloc(sizeof(struct ListNode) * (n > 0 ? n : 1));
    for (int i = 0; i < n; i++) {
        nodes[i].val = a[i];
        nodes[i].next = (i + 1 < n) ? &nodes[i + 1] : NULL;
    }
    if (n > 0 && pos >= 0 && pos < n) nodes[n - 1].next = &nodes[pos];
    struct ListNode* head = n > 0 ? &nodes[0] : NULL;

    struct ListNode* ans = detectCycle(head);

    for (int i = 0; i < n; i++) {
        struct ListNode* want = (i + 1 < n) ? &nodes[i + 1] : (pos >= 0 ? &nodes[pos] : NULL);
        if (nodes[i].next != want || nodes[i].val != a[i]) {
            printf("错误：链表被修改了（本题不允许修改链表）\n");
            return 0;
        }
    }
    if (ans == NULL) {
        oj_print_int(-1);
        return 0;
    }
    for (int i = 0; i < n; i++) {
        if (ans == &nodes[i]) {
            oj_print_int(i);
            return 0;
        }
    }
    printf("错误：返回的指针不是链表中的结点\n");
    return 0;
}
