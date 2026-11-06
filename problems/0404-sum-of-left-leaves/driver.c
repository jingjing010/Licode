int main(void) {
    struct TreeNode* root = oj_read_tree();
    oj_print_int(sumOfLeftLeaves(root));
    return 0;
}
