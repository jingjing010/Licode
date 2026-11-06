static int depth(struct TreeNode* node, int* best) {
    if (node == NULL) return 0;
    int l = depth(node->left, best);
    int r = depth(node->right, best);
    if (l + r > *best) *best = l + r;
    return (l > r ? l : r) + 1;
}

int diameterOfBinaryTree(struct TreeNode* root) {
    int best = 0;
    depth(root, &best);
    return best;
}
