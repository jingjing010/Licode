struct TreeNode* lowestCommonAncestor(struct TreeNode* root, struct TreeNode* p, struct TreeNode* q) {
    if (root == NULL || root == p || root == q) return root;
    struct TreeNode* l = lowestCommonAncestor(root->left, p, q);
    struct TreeNode* r = lowestCommonAncestor(root->right, p, q);
    if (l != NULL && r != NULL) return root;
    return l != NULL ? l : r;
}
