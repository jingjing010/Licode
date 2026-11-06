int main(void) {
    struct ListNode* head = oj_read_list();
    struct ListNode* ans = reverseList(head);
    oj_print_list(ans);
    return 0;
}
