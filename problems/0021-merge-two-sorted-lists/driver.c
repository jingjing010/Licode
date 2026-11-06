int main(void) {
    struct ListNode* list1 = oj_read_list();
    struct ListNode* list2 = oj_read_list();
    struct ListNode* ans = mergeTwoLists(list1, list2);
    oj_print_list(ans);
    return 0;
}
