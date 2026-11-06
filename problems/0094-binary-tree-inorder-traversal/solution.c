int* inorderTraversal(struct TreeNode* root, int* returnSize) {
    int* res = (int*)malloc(sizeof(int) * 128);
    struct TreeNode* stk[128];
    int top = 0, n = 0;
    struct TreeNode* cur = root;
    while (cur != NULL || top > 0) {
        while (cur != NULL) {
            stk[top++] = cur;
            cur = cur->left;
        }
        cur = stk[--top];
        res[n++] = cur->val;
        cur = cur->right;
    }
    *returnSize = n;
    return res;
}
