/* BFS 层序遍历，奇数层按倒序下标写入：O(n) */
int** zigzagLevelOrder(struct TreeNode* root, int* returnSize, int** returnColumnSizes) {
    *returnSize = 0;
    *returnColumnSizes = NULL;
    if (root == NULL) return NULL;
    int cap = 2001;
    struct TreeNode** q = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * cap);
    int** res = (int**)malloc(sizeof(int*) * cap);
    int* cols = (int*)malloc(sizeof(int) * cap);
    int head = 0, tail = 0, level = 0;
    q[tail++] = root;
    while (head < tail) {
        int sz = tail - head;
        int* row = (int*)malloc(sizeof(int) * sz);
        for (int i = 0; i < sz; i++) {
            struct TreeNode* t = q[head++];
            row[level % 2 == 0 ? i : sz - 1 - i] = t->val;
            if (t->left) q[tail++] = t->left;
            if (t->right) q[tail++] = t->right;
        }
        res[level] = row;
        cols[level] = sz;
        level++;
    }
    free(q);
    *returnSize = level;
    *returnColumnSizes = cols;
    return res;
}
