static struct ListNode* sol_merge(struct ListNode* a, struct ListNode* b) {
    struct ListNode dummy;
    struct ListNode* tail = &dummy;
    while (a && b) {
        if (a->val <= b->val) { tail->next = a; a = a->next; }
        else { tail->next = b; b = b->next; }
        tail = tail->next;
    }
    tail->next = a ? a : b;
    return dummy.next;
}

struct ListNode* sortList(struct ListNode* head) {
    if (!head || !head->next) return head;
    struct ListNode *slow = head, *fast = head->next;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    struct ListNode* right = slow->next;
    slow->next = NULL;
    return sol_merge(sortList(head), sortList(right));
}
