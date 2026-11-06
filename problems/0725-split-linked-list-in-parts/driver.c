/* 输出形如 [[1,2],[3],[]]，空段写作 [] */
static void drv_print_parts(struct ListNode** parts, int size) {
    putchar('[');
    for (int i = 0; i < size; i++) {
        if (i) putchar(',');
        putchar('[');
        int guard = 0;
        for (struct ListNode* p = parts[i]; p != NULL; p = p->next) {
            if (p != parts[i]) putchar(',');
            printf("%d", p->val);
            if (++guard > 100000) { printf(",...(链表可能有环)"); break; }
        }
        putchar(']');
    }
    printf("]\n");
}

int main(void) {
    struct ListNode* head = oj_read_list();
    int k = oj_read_int();
    int returnSize = 0;
    struct ListNode** parts = splitListToParts(head, k, &returnSize);
    drv_print_parts(parts, returnSize);
    return 0;
}
