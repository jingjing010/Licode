int main(void) {
    int n;
    int* a = oj_read_int_array(&n);
    int k = oj_read_int();
    struct ListNode* nodes = (struct ListNode*)malloc(sizeof(struct ListNode) * (n > 0 ? n : 1));
    for (int i = 0; i < n; i++) {
        nodes[i].val = a[i];
        nodes[i].next = (i + 1 < n) ? &nodes[i + 1] : NULL;
    }
    struct ListNode* head = n > 0 ? &nodes[0] : NULL;

    struct ListNode* ans = reverseKGroup(head, k);

    for (int i = 0; i < n; i++) {
        if (nodes[i].val != a[i]) {
            printf("错误：修改了结点的值（本题只能交换结点，不能修改 val）\n");
            return 0;
        }
    }
    char* seen = (char*)calloc(n > 0 ? n : 1, 1);
    int cnt = 0;
    for (struct ListNode* p = ans; p; p = p->next) {
        uintptr_t off = (uintptr_t)p - (uintptr_t)nodes;
        if ((uintptr_t)p < (uintptr_t)nodes || off % sizeof(struct ListNode) != 0 ||
            off / sizeof(struct ListNode) >= (uintptr_t)n) {
            printf("错误：返回的链表中出现了不属于原链表的结点（本题只能调整原有结点）\n");
            return 0;
        }
        int idx = (int)(off / sizeof(struct ListNode));
        if (seen[idx]) {
            printf("错误：返回的链表中有重复结点（可能形成了环）\n");
            return 0;
        }
        seen[idx] = 1;
        cnt++;
    }
    if (cnt != n) {
        printf("错误：返回的链表丢失了结点\n");
        return 0;
    }
    oj_print_list(ans);
    return 0;
}
