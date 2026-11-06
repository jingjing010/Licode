int main(void) {
    struct ListNode* head = oj_read_list();
    oj_print_bool(isPalindrome(head));
    return 0;
}
