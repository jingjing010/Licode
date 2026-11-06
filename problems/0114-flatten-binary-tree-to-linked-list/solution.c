void flatten(struct TreeNode* root) {
    struct TreeNode* cur = root;
    while (cur != NULL) {
        if (cur->left != NULL) {
            struct TreeNode* pre = cur->left;
            while (pre->right != NULL) pre = pre->right;
            pre->right = cur->right;
            cur->right = cur->left;
            cur->left = NULL;
        }
        cur = cur->right;
    }
}
