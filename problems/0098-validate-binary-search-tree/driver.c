int main(void) {
    struct TreeNode* root = oj_read_tree();
    oj_print_bool(isValidBST(root));
    return 0;
}
