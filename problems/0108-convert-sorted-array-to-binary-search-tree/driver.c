/* 中序遍历返回的树（带结点数上限，防止有环或结点被重复使用），检查是否与 nums 完全一致 */
static bool drv_inorder_matches(struct TreeNode* root, const int* nums, int n) {
    struct TreeNode** stk = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * (n + 2));
    int top = 0, cnt = 0;
    struct TreeNode* cur = root;
    while (cur != NULL || top > 0) {
        while (cur != NULL) {
            if (top > n) { free(stk); return false; }
            stk[top++] = cur;
            cur = cur->left;
        }
        cur = stk[--top];
        if (cnt >= n || cur->val != nums[cnt]) { free(stk); return false; }
        cnt++;
        cur = cur->right;
    }
    free(stk);
    return cnt == n;
}

/* 返回树高；若某个结点左右子树高度差超过 1，把 *ok 置为 false */
static int drv_height(struct TreeNode* t, bool* ok) {
    if (t == NULL) return 0;
    int l = drv_height(t->left, ok);
    int r = drv_height(t->right, ok);
    if (l - r > 1 || r - l > 1) *ok = false;
    return (l > r ? l : r) + 1;
}

int main(void) {
    int n;
    int* nums = oj_read_int_array(&n);
    int* copy = (int*)malloc(sizeof(int) * (n > 0 ? n : 1));
    memcpy(copy, nums, sizeof(int) * n);
    struct TreeNode* root = sortedArrayToBST(nums, n);
    bool ok = drv_inorder_matches(root, copy, n);
    if (ok) drv_height(root, &ok);
    oj_print_bool(ok);
    return 0;
}
