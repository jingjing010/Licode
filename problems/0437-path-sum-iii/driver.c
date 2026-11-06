int main(void) {
    struct TreeNode* root = oj_read_tree();
    int targetSum = oj_read_int();
    oj_print_int(pathSum(root, targetSum));
    return 0;
}
