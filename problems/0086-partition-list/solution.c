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
