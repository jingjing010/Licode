struct ListNode* rotateRight(struct ListNode* head, int k) {
    if (head == NULL || head->next == NULL || k == 0) return head;
    int n = 1;
    struct ListNode* tail = head;
    while (tail->next != NULL) {
        tail = tail->next;
        n++;
    }
    k %= n;
    if (k == 0) return head;
    tail->next = head;
    struct ListNode* newTail = head;
    for (int i = 0; i < n - k - 1; i++) newTail = newTail->next;
    struct ListNode* newHead = newTail->next;
    newTail->next = NULL;
    return newHead;
}
