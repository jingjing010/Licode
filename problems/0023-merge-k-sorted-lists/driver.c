int main(void) {
    int k;
    int* sizes;
    int** m = oj_read_int_matrix(&k, &sizes);
    struct ListNode** lists = (struct ListNode**)malloc(sizeof(struct ListNode*) * (k > 0 ? k : 1));
    for (int i = 0; i < k; i++) lists[i] = oj_build_list(m[i], sizes[i]);
    oj_print_list(mergeKLists(lists, k));
    return 0;
}
