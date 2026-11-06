int main(void) {
    struct ListNode* head = oj_read_list();
    int x = oj_read_int();
    struct ListNode* ans = partition(head, x);
    oj_print_list(ans);
    return 0;
}
