int main(void) {
    struct TreeNode* root = oj_read_tree();
    struct TreeNode* subRoot = oj_read_tree();
    oj_print_bool(isSubtree(root, subRoot));
    return 0;
}
