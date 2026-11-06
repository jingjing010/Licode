int main(void) {
    struct TreeNode* root = oj_read_tree();
    oj_print_bool(isBalanced(root));
    return 0;
}
