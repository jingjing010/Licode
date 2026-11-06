static int sol_pos[6001];

static struct TreeNode* sol_build(int* pre, int pl, int pr, int il) {
    if (pl > pr) return NULL;
    struct TreeNode* t = (struct TreeNode*)malloc(sizeof(struct TreeNode));
    t->val = pre[pl];
    int k = sol_pos[pre[pl] + 3000];
    int leftSize = k - il;
    t->left = sol_build(pre, pl + 1, pl + leftSize, il);
    t->right = sol_build(pre, pl + leftSize + 1, pr, k + 1);
    return t;
}

struct TreeNode* buildTree(int* preorder, int preorderSize, int* inorder, int inorderSize) {
    for (int i = 0; i < inorderSize; i++) sol_pos[inorder[i] + 3000] = i;
    return sol_build(preorder, 0, preorderSize - 1, 0);
}
