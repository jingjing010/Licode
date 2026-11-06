int* preorderTraversal(struct TreeNode* root, int* returnSize) {
    int* res = (int*)malloc(sizeof(int) * 100);
    struct TreeNode* st[100];
    int top = 0, cnt = 0;
    if (root) st[top++] = root;
    while (top > 0) {
        struct TreeNode* node = st[--top];
        res[cnt++] = node->val;
        if (node->right) st[top++] = node->right;
        if (node->left) st[top++] = node->left;
    }
    *returnSize = cnt;
    return res;
}
