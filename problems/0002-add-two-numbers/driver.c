int main(void) {
    struct ListNode* l1 = oj_read_list();
    struct ListNode* l2 = oj_read_list();
    oj_print_list(addTwoNumbers(l1, l2));
    return 0;
}
