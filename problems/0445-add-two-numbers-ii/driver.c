int main(void) {
    struct ListNode* l1 = oj_read_list();
    struct ListNode* l2 = oj_read_list();
    struct ListNode* ans = addTwoNumbers(l1, l2);
    oj_print_list(ans);
    return 0;
}
