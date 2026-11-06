int main(void) {
    struct TreeNode* root = oj_read_tree();
    int k = oj_read_int();
    oj_print_int(kthSmallest(root, k));
    return 0;
}
