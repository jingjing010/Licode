static struct ListNode* sol_merge2(struct ListNode* a, struct ListNode* b) {
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

static struct ListNode* sol_range(struct ListNode** lists, int l, int r) {
    if (l > r) return NULL;
    if (l == r) return lists[l];
    int mid = l + (r - l) / 2;
    return sol_merge2(sol_range(lists, l, mid), sol_range(lists, mid + 1, r));
}

struct ListNode* mergeKLists(struct ListNode** lists, int listsSize) {
    return sol_range(lists, 0, listsSize - 1);
}
