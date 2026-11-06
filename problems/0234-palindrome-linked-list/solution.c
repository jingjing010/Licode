static struct ListNode* sol_reverse(struct ListNode* head) {
    struct ListNode* prev = NULL;
    while (head) {
        struct ListNode* next = head->next;
        head->next = prev;
        prev = head;
        head = next;
    }
    return prev;
}

bool isPalindrome(struct ListNode* head) {
    if (!head || !head->next) return true;
    struct ListNode *slow = head, *fast = head;
    while (fast->next && fast->next->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    struct ListNode* second = sol_reverse(slow->next);
    bool ok = true;
    for (struct ListNode *p = head, *q = second; q; p = p->next, q = q->next) {
        if (p->val != q->val) { ok = false; break; }
    }
    slow->next = sol_reverse(second);
    return ok;
}
