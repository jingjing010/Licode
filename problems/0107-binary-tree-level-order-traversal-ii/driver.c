int main(void) {
    struct TreeNode* root = oj_read_tree();
    int returnSize = 0;
    int* colSizes = NULL;
    int** ans = levelOrderBottom(root, &returnSize, &colSizes);
    if (ans == NULL || colSizes == NULL) returnSize = 0;
    oj_print_int_matrix(ans, returnSize, colSizes);
    return 0;
}
