static int height(struct TreeNode* node) {
    if (node == NULL) return 0;
    int l = height(node->left);
    if (l < 0) return -1;
    int r = height(node->right);
    if (r < 0) return -1;
    if (l - r > 1 || r - l > 1) return -1;
    return (l > r ? l : r) + 1;
}

bool isBalanced(struct TreeNode* root) {
    return height(root) >= 0;
}
