/* 利用 BST 大小关系从根往下走，p、q 分叉处即为答案：O(h) 时间，O(1) 空间 */
struct TreeNode* lowestCommonAncestor(struct TreeNode* root, struct TreeNode* p, struct TreeNode* q) {
    struct TreeNode* cur = root;
    while (cur != NULL) {
        if (p->val < cur->val && q->val < cur->val) cur = cur->left;
        else if (p->val > cur->val && q->val > cur->val) cur = cur->right;
        else return cur;
    }
    return NULL;
}
