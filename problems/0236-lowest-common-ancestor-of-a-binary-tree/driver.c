/* 迭代遍历整棵树，找到值为 v 的结点（值互不相同） */
static struct TreeNode* drv_find(struct TreeNode* root, int v) {
    if (root == NULL) return NULL;
    int cap = 1024, top = 0;
    struct TreeNode** st = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * cap);
    struct TreeNode* found = NULL;
    st[top++] = root;
    while (top > 0) {
        struct TreeNode* t = st[--top];
        if (t->val == v) { found = t; break; }
        if (top + 2 > cap) { cap *= 2; st = (struct TreeNode**)realloc(st, sizeof(struct TreeNode*) * cap); }
        if (t->left) st[top++] = t->left;
        if (t->right) st[top++] = t->right;
    }
    free(st);
    return found;
}

int main(void) {
    struct TreeNode* root = oj_read_tree();
    int pv = oj_read_int();
    int qv = oj_read_int();
    struct TreeNode* p = drv_find(root, pv);
    struct TreeNode* q = drv_find(root, qv);
    if (p == NULL || q == NULL) oj_fail("p 或 q 不在树中");
    struct TreeNode* ans = lowestCommonAncestor(root, p, q);
    if (ans == NULL) printf("null\n");
    else oj_print_int(ans->val);
    return 0;
}
