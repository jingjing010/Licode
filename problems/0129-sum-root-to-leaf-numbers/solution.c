/* DFS：携带从根到当前结点拼出的数，到叶子时累加：O(n) */
static int dfs(struct TreeNode* node, int prefix) {
    if (node == NULL) return 0;
    int cur = prefix * 10 + node->val;
    if (node->left == NULL && node->right == NULL) return cur;
    return dfs(node->left, cur) + dfs(node->right, cur);
}

int sumNumbers(struct TreeNode* root) {
    return dfs(root, 0);
}
