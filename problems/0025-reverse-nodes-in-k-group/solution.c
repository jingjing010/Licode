struct ListNode* reverseKGroup(struct ListNode* head, int k) {
    struct ListNode dummy;
    dummy.next = head;
    struct ListNode* prev = &dummy;
    while (1) {
        struct ListNode* end = prev;
        for (int i = 0; i < k && end; i++) end = end->next;
        if (!end) break;
        struct ListNode* start = prev->next;
        struct ListNode* next = end->next;
        struct ListNode* p = start;
        struct ListNode* q = next;
        while (p != next) {
            struct ListNode* t = p->next;
            p->next = q;
            q = p;
            p = t;
        }
        prev->next = end;
        prev = start;
    }
    return dummy.next;
}
