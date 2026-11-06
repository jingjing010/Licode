static int sol_gain(struct TreeNode* t, int* best) {
    if (t == NULL) return 0;
    int l = sol_gain(t->left, best);
    int r = sol_gain(t->right, best);
    if (l < 0) l = 0;
    if (r < 0) r = 0;
    if (t->val + l + r > *best) *best = t->val + l + r;
    return t->val + (l > r ? l : r);
}

int maxPathSum(struct TreeNode* root) {
    int best = INT_MIN;
    sol_gain(root, &best);
    return best;
}
