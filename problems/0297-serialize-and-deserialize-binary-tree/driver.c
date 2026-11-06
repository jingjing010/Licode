/* 清空并释放整棵树，确保 deserialize 只能依赖字符串里的信息 */
static void drv_destroy(struct TreeNode* root) {
    if (root == NULL) return;
    int cap = 1024, top = 0;
    struct TreeNode** st = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * cap);
    st[top++] = root;
    while (top > 0) {
        struct TreeNode* t = st[--top];
        if (top + 2 > cap) { cap *= 2; st = (struct TreeNode**)realloc(st, sizeof(struct TreeNode*) * cap); }
        if (t->left) st[top++] = t->left;
        if (t->right) st[top++] = t->right;
        t->val = 0x5A5A5A5A;
        t->left = t->right = NULL;
        free(t);
    }
    free(st);
}

int main(void) {
    struct TreeNode* root = oj_read_tree();
    char* data = serialize(root);
    if (data == NULL) {
        printf("serialize 返回了 NULL\n");
        return 0;
    }
    size_t len = strlen(data);
    char* copy = (char*)malloc(len + 1);
    memcpy(copy, data, len + 1);
    drv_destroy(root);
    struct TreeNode* ans = deserialize(copy);
    oj_print_tree(ans);
    return 0;
}
