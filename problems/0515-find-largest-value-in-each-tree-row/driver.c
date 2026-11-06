int main(void) {
    struct TreeNode* root = oj_read_tree();
    int returnSize = 0;
    int* ans = largestValues(root, &returnSize);
    if (ans == NULL) returnSize = 0;
    oj_print_int_array(ans, returnSize);
    return 0;
}
