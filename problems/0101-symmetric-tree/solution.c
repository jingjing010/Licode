static bool mirror(struct TreeNode* a, struct TreeNode* b) {
    if (a == NULL && b == NULL) return true;
    if (a == NULL || b == NULL) return false;
    return a->val == b->val && mirror(a->left, b->right) && mirror(a->right, b->left);
}

bool isSymmetric(struct TreeNode* root) {
    if (root == NULL) return true;
    return mirror(root->left, root->right);
}
