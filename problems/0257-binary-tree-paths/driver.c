int main(void) {
    struct TreeNode* root = oj_read_tree();
    int returnSize = 0;
    char** ans = binaryTreePaths(root, &returnSize);
    if (ans == NULL) returnSize = 0;
    oj_sort_string_array(ans, returnSize);
    oj_print_string_array(ans, returnSize);
    return 0;
}
