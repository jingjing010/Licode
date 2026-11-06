/* 沿 BST 找到结点；两个孩子时用右子树最小结点（后继）顶替：O(h) */
struct TreeNode* deleteNode(struct TreeNode* root, int key) {
    if (root == NULL) return NULL;
    if (key < root->val) {
        root->left = deleteNode(root->left, key);
        return root;
    }
    if (key > root->val) {
        root->right = deleteNode(root->right, key);
        return root;
    }
    struct TreeNode* rep;
    if (root->left == NULL) {
        rep = root->right;
    } else if (root->right == NULL) {
        rep = root->left;
    } else {
        struct TreeNode* parent = root;
        rep = root->right;
        while (rep->left != NULL) {
            parent = rep;
            rep = rep->left;
        }
        if (parent != root) {
            parent->left = rep->right;
            rep->right = root->right;
        }
        rep->left = root->left;
    }
    free(root);
    return rep;
}
