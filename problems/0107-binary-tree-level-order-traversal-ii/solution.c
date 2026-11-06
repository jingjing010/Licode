int** levelOrderBottom(struct TreeNode* root, int* returnSize, int** returnColumnSizes) {
    int** res = (int**)malloc(sizeof(int*) * 2001);
    int* cols = (int*)malloc(sizeof(int) * 2001);
    int levels = 0;
    *returnSize = 0;
    *returnColumnSizes = cols;
    if (root == NULL) return res;

    struct TreeNode** q = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * 2001);
    int head = 0, tail = 0;
    q[tail++] = root;
    while (head < tail) {
        int size = tail - head;
        int* row = (int*)malloc(sizeof(int) * size);
        for (int i = 0; i < size; i++) {
            struct TreeNode* node = q[head++];
            row[i] = node->val;
            if (node->left) q[tail++] = node->left;
            if (node->right) q[tail++] = node->right;
        }
        res[levels] = row;
        cols[levels] = size;
        levels++;
    }
    free(q);

    for (int i = 0, j = levels - 1; i < j; i++, j--) {
        int* tr = res[i]; res[i] = res[j]; res[j] = tr;
        int tc = cols[i]; cols[i] = cols[j]; cols[j] = tc;
    }
    *returnSize = levels;
    return res;
}
