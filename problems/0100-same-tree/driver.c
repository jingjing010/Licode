int main(void) {
    struct TreeNode* p = oj_read_tree();
    struct TreeNode* q = oj_read_tree();
    oj_print_bool(isSameTree(p, q));
    return 0;
}
