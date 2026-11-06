int main(void) {
    struct TreeNode* root = oj_read_tree();
    flatten(root);
    oj_print_tree(root);
    return 0;
}
