int* rightSideView(struct TreeNode* root, int* returnSize) {
    int* res = (int*)malloc(sizeof(int) * 128);
    struct TreeNode* q[128];
    int head = 0, tail = 0, n = 0;
    if (root) q[tail++] = root;
    while (head < tail) {
        int size = tail - head;
        for (int i = 0; i < size; i++) {
            struct TreeNode* t = q[head++];
            if (i == size - 1) res[n++] = t->val;
            if (t->left) q[tail++] = t->left;
            if (t->right) q[tail++] = t->right;
        }
    }
    *returnSize = n;
    return res;
}
