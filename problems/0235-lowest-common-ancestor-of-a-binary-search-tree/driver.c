/* 在二叉搜索树中按值查找结点 */
static struct TreeNode* drv_find(struct TreeNode* root, int v) {
    while (root != NULL && root->val != v) root = v < root->val ? root->left : root->right;
    return root;
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
