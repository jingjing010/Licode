int getDecimalValue(struct ListNode* head) {
    int ans = 0;
    for (struct ListNode* p = head; p != NULL; p = p->next) {
        ans = (ans << 1) | p->val;
    }
    return ans;
}
