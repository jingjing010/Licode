/* 左右高度相等则为满二叉树直接用公式，否则递归：O(log^2 n) */
int countNodes(struct TreeNode* root) {
    if (root == NULL) return 0;
    int lh = 0, rh = 0;
    for (struct TreeNode* p = root; p != NULL; p = p->left) lh++;
    for (struct TreeNode* p = root; p != NULL; p = p->right) rh++;
    if (lh == rh) return (1 << lh) - 1;
    return 1 + countNodes(root->left) + countNodes(root->right);
}
