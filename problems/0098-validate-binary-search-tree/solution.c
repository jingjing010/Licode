static bool check(struct TreeNode* t, long long lo, long long hi) {
    if (t == NULL) return true;
    if (t->val <= lo || t->val >= hi) return false;
    return check(t->left, lo, t->val) && check(t->right, t->val, hi);
}

bool isValidBST(struct TreeNode* root) {
    return check(root, LLONG_MIN, LLONG_MAX);
}
