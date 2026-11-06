struct ListNode* deleteDuplicates(struct ListNode* head) {
    struct ListNode dummy;
    dummy.next = head;
    struct ListNode* prev = &dummy;
    while (prev->next != NULL && prev->next->next != NULL) {
        if (prev->next->val == prev->next->next->val) {
            int x = prev->next->val;
            while (prev->next != NULL && prev->next->val == x) {
                struct ListNode* del = prev->next;
                prev->next = del->next;
                free(del);
            }
        } else {
            prev = prev->next;
        }
    }
    return dummy.next;
}
