int minDepth(struct TreeNode* root) {
    if (root == NULL) return 0;
    struct TreeNode** q = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * 100001);
    int head = 0, tail = 0, depth = 0;
    q[tail++] = root;
    while (head < tail) {
        int size = tail - head;
        depth++;
        for (int i = 0; i < size; i++) {
            struct TreeNode* node = q[head++];
            if (node->left == NULL && node->right == NULL) {
                free(q);
                return depth;
            }
            if (node->left) q[tail++] = node->left;
            if (node->right) q[tail++] = node->right;
        }
    }
    free(q);
    return depth;
}
