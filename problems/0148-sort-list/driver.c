int main(void) {
    struct ListNode* head = oj_read_list();
    struct ListNode* ans = sortList(head);
    oj_print_list(ans);
    return 0;
}
