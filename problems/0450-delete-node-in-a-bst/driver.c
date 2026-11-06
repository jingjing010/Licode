/* 收集树中所有结点值（任意顺序），返回个数 */
static int drv_collect(struct TreeNode* root, int** out) {
    int cap = 1024, n = 0, top = 0, scap = 1024;
    int* vals = (int*)malloc(sizeof(int) * cap);
    struct TreeNode** st = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * scap);
    if (root) st[top++] = root;
    while (top > 0) {
        struct TreeNode* t = st[--top];
        if (n == cap) { cap *= 2; vals = (int*)realloc(vals, sizeof(int) * cap); }
        vals[n++] = t->val;
        if (top + 2 > scap) { scap *= 2; st = (struct TreeNode**)realloc(st, sizeof(struct TreeNode*) * scap); }
        if (t->left) st[top++] = t->left;
        if (t->right) st[top++] = t->right;
    }
    free(st);
    *out = vals;
    return n;
}

/* 中序遍历，最多取 limit 个结点；超过 limit 说明有环或结点被重复使用，返回 -1 */
static int drv_inorder(struct TreeNode* root, int* out, int limit) {
    int n = 0, top = 0, scap = 1024;
    struct TreeNode** st = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * scap);
    struct TreeNode* cur = root;
    while (cur != NULL || top > 0) {
        while (cur != NULL) {
            if (top >= limit + 1) { free(st); return -1; }
            if (top == scap) { scap *= 2; st = (struct TreeNode**)realloc(st, sizeof(struct TreeNode*) * scap); }
            st[top++] = cur;
            cur = cur->left;
        }
        cur = st[--top];
        if (n == limit) { free(st); return -1; }
        out[n++] = cur->val;
        cur = cur->right;
    }
    free(st);
    return n;
}

int main(void) {
    struct TreeNode* root = oj_read_tree();
    int key = oj_read_int();
    int* vals;
    int n = drv_collect(root, &vals);
    qsort(vals, n, sizeof(int), oj_cmp_int);
    int m = 0;
    for (int i = 0; i < n; i++)
        if (vals[i] != key) vals[m++] = vals[i];

    struct TreeNode* ans = deleteNode(root, key);
    int* got = (int*)malloc(sizeof(int) * (m + 1));
    int k = drv_inorder(ans, got, m);
    if (k < 0) {
        printf("错误：返回的树结点数多于应有的 %d 个（可能有环、结点重复或没有删除 key）\n", m);
        return 0;
    }
    for (int i = 1; i < k; i++) {
        if (got[i - 1] >= got[i]) {
            printf("错误：返回的树不是二叉搜索树（中序遍历在 %d 与 %d 处不递增）\n", got[i - 1], got[i]);
            return 0;
        }
    }
    if (k != m) {
        printf("错误：返回的树有 %d 个结点，应为 %d 个\n", k, m);
        return 0;
    }
    for (int i = 0; i < m; i++) {
        if (got[i] != vals[i]) {
            printf("错误：返回的树的结点值集合不正确\n");
            return 0;
        }
    }
    oj_print_int_array(got, k);
    return 0;
}
