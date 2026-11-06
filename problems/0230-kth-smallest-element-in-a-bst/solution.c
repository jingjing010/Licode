int kthSmallest(struct TreeNode* root, int k) {
    struct TreeNode** stk = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * 10001);
    int top = 0, ans = -1;
    struct TreeNode* cur = root;
    while (cur != NULL || top > 0) {
        while (cur != NULL) {
            stk[top++] = cur;
            cur = cur->left;
        }
        cur = stk[--top];
        if (--k == 0) {
            ans = cur->val;
            break;
        }
        cur = cur->right;
    }
    free(stk);
    return ans;
}
