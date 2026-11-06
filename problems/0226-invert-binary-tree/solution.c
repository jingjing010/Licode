struct TreeNode* invertTree(struct TreeNode* root) {
    if (root == NULL) return NULL;
    struct TreeNode* t = root->left;
    root->left = root->right;
    root->right = t;
    invertTree(root->left);
    invertTree(root->right);
    return root;
}
