struct ListNode* deleteDuplicates(struct ListNode* head) {
    struct ListNode* cur = head;
    while (cur != NULL && cur->next != NULL) {
        if (cur->val == cur->next->val) {
            struct ListNode* del = cur->next;
            cur->next = del->next;
            free(del);
        } else {
            cur = cur->next;
        }
    }
    return head;
}
