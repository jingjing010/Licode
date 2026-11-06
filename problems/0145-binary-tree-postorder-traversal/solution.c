int* postorderTraversal(struct TreeNode* root, int* returnSize) {
    int* res = (int*)malloc(sizeof(int) * 100);
    struct TreeNode* st[100];
    int top = 0, cnt = 0;
    struct TreeNode* cur = root;
    struct TreeNode* prev = NULL;
    while (cur != NULL || top > 0) {
        while (cur != NULL) {
            st[top++] = cur;
            cur = cur->left;
        }
        struct TreeNode* node = st[top - 1];
        if (node->right != NULL && node->right != prev) {
            cur = node->right;
        } else {
            res[cnt++] = node->val;
            prev = node;
            top--;
        }
    }
    *returnSize = cnt;
    return res;
}
