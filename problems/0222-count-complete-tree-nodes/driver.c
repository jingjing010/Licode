int main(void) {
    struct TreeNode* root = oj_read_tree();
    oj_print_int(countNodes(root));
    return 0;
}
