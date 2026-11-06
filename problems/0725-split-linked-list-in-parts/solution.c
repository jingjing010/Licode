struct ListNode** splitListToParts(struct ListNode* head, int k, int* returnSize) {
    int n = 0;
    for (struct ListNode* p = head; p != NULL; p = p->next) n++;
    int base = n / k, extra = n % k;
    struct ListNode** parts = (struct ListNode**)malloc(sizeof(struct ListNode*) * k);
    struct ListNode* cur = head;
    for (int i = 0; i < k; i++) {
        parts[i] = cur;
        int size = base + (i < extra ? 1 : 0);
        for (int j = 0; j < size - 1; j++) cur = cur->next;
        if (size > 0) {
            struct ListNode* next = cur->next;
            cur->next = NULL;
            cur = next;
        }
    }
    *returnSize = k;
    return parts;
}
