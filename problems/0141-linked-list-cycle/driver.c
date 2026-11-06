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
    oj_print_bool(hasCycle(head));
    return 0;
}
