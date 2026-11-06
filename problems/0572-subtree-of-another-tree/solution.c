#define NIL INT_MIN

static void serialize(struct TreeNode* node, int* out, int* len) {
    if (node == NULL) {
        out[(*len)++] = NIL;
        return;
    }
    out[(*len)++] = node->val;
    serialize(node->left, out, len);
    serialize(node->right, out, len);
}

bool isSubtree(struct TreeNode* root, struct TreeNode* subRoot) {
    int* a = (int*)malloc(sizeof(int) * 4001);
    int* b = (int*)malloc(sizeof(int) * 2001);
    int n = 0, m = 0;
    serialize(root, a, &n);
    serialize(subRoot, b, &m);

    int* next = (int*)malloc(sizeof(int) * m);
    next[0] = 0;
    for (int i = 1, k = 0; i < m; i++) {
        while (k > 0 && b[i] != b[k]) k = next[k - 1];
        if (b[i] == b[k]) k++;
        next[i] = k;
    }
    bool found = false;
    for (int i = 0, k = 0; i < n; i++) {
        while (k > 0 && a[i] != b[k]) k = next[k - 1];
        if (a[i] == b[k]) k++;
        if (k == m) {
            found = true;
            break;
        }
    }
    free(a);
    free(b);
    free(next);
    return found;
}
