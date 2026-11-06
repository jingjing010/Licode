int main(void) {
    struct ListNode* head = oj_read_list();
    oj_print_int(getDecimalValue(head));
    return 0;
}
