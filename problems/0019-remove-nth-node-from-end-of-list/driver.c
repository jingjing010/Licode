int main(void) {
    struct ListNode* head = oj_read_list();
    int n = oj_read_int();
    struct ListNode* ans = removeNthFromEnd(head, n);
    oj_print_list(ans);
    return 0;
}
