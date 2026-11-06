int main(void) {
    struct TreeNode* root = oj_read_tree();
    int targetSum = oj_read_int();
    oj_print_bool(hasPathSum(root, targetSum));
    return 0;
}
