bool hasPathSum(struct TreeNode* root, int targetSum) {
    if (root == NULL) return false;
    if (root->left == NULL && root->right == NULL) return root->val == targetSum;
    int rest = targetSum - root->val;
    return hasPathSum(root->left, rest) || hasPathSum(root->right, rest);
}
