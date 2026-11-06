int** levelOrder(struct TreeNode* root, int* returnSize, int** returnColumnSizes) {
    int** res = (int**)malloc(sizeof(int*) * 2001);
    int* cols = (int*)malloc(sizeof(int) * 2001);
    *returnSize = 0;
    *returnColumnSizes = cols;
    if (root == NULL) return res;
    struct TreeNode** q = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * 2001);
    int head = 0, tail = 0, rows = 0;
    q[tail++] = root;
    while (head < tail) {
        int size = tail - head;
        res[rows] = (int*)malloc(sizeof(int) * size);
        cols[rows] = size;
        for (int i = 0; i < size; i++) {
            struct TreeNode* t = q[head++];
            res[rows][i] = t->val;
            if (t->left) q[tail++] = t->left;
            if (t->right) q[tail++] = t->right;
        }
        rows++;
    }
    free(q);
    *returnSize = rows;
    return res;
}
