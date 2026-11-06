int main(void) {
    int n1, n2;
    int* inorder = oj_read_int_array(&n1);
    int* postorder = oj_read_int_array(&n2);
    if (n1 != n2) oj_fail("inorder 与 postorder 长度不一致");
    struct TreeNode* root = buildTree(inorder, n1, postorder, n2);
    oj_print_tree(root);
    return 0;
}
