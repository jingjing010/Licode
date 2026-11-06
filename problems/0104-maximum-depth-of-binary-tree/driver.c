int main(void) {
    struct TreeNode* root = oj_read_tree();
    oj_print_int(maxDepth(root));
    return 0;
}
