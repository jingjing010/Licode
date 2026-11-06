int main(void) {
    struct ListNode* head = oj_read_list();
    int k = oj_read_int();
    struct ListNode* ans = rotateRight(head, k);
    oj_print_list(ans);
    return 0;
}
