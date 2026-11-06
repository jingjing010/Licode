int findBottomLeftValue(struct TreeNode* root) {
    struct TreeNode** q = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * 10000);
    int head = 0, tail = 0;
    q[tail++] = root;
    struct TreeNode* node = root;
    while (head < tail) {
        node = q[head++];
        if (node->right) q[tail++] = node->right;
        if (node->left) q[tail++] = node->left;
    }
    int ans = node->val;
    free(q);
    return ans;
}
