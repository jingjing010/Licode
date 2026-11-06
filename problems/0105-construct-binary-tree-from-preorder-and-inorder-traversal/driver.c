int main(void) {
    int n, m;
    int* preorder = oj_read_int_array(&n);
    int* inorder = oj_read_int_array(&m);
    struct TreeNode* root = buildTree(preorder, n, inorder, m);
    oj_print_tree(root);
    return 0;
}
