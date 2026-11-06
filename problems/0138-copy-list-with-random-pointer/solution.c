struct Node* copyRandomList(struct Node* head) {
    if (!head) return NULL;
    for (struct Node* p = head; p; p = p->next->next) {
        struct Node* c = (struct Node*)malloc(sizeof(struct Node));
        c->val = p->val;
        c->next = p->next;
        c->random = NULL;
        p->next = c;
    }
    for (struct Node* p = head; p; p = p->next->next) {
        if (p->random) p->next->random = p->random->next;
    }
    struct Node* newHead = head->next;
    for (struct Node* p = head; p; p = p->next) {
        struct Node* c = p->next;
        p->next = c->next;
        c->next = c->next ? c->next->next : NULL;
    }
    return newHead;
}
