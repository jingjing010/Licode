int main(void) {
    struct TreeNode* root1 = oj_read_tree();
    struct TreeNode* root2 = oj_read_tree();
    oj_print_tree(mergeTrees(root1, root2));
    return 0;
}
