struct ListNode* addTwoNumbers(struct ListNode* l1, struct ListNode* l2) {
    int s1[105], s2[105];
    int n1 = 0, n2 = 0;
    for (struct ListNode* p = l1; p != NULL; p = p->next) s1[n1++] = p->val;
    for (struct ListNode* p = l2; p != NULL; p = p->next) s2[n2++] = p->val;
    struct ListNode* head = NULL;
    int carry = 0;
    while (n1 > 0 || n2 > 0 || carry != 0) {
        int sum = carry;
        if (n1 > 0) sum += s1[--n1];
        if (n2 > 0) sum += s2[--n2];
        struct ListNode* node = (struct ListNode*)malloc(sizeof(struct ListNode));
        node->val = sum % 10;
        node->next = head;
        head = node;
        carry = sum / 10;
    }
    return head;
}
