int* largestValues(struct TreeNode* root, int* returnSize) {
    int* res = (int*)malloc(sizeof(int) * 10000);
    int cnt = 0;
    *returnSize = 0;
    if (root == NULL) return res;
    struct TreeNode** q = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * 10000);
    int head = 0, tail = 0;
    q[tail++] = root;
    while (head < tail) {
        int size = tail - head;
        int mx = INT_MIN;
        for (int i = 0; i < size; i++) {
            struct TreeNode* node = q[head++];
            if (node->val > mx) mx = node->val;
            if (node->left) q[tail++] = node->left;
            if (node->right) q[tail++] = node->right;
        }
        res[cnt++] = mx;
    }
    free(q);
    *returnSize = cnt;
    return res;
}
