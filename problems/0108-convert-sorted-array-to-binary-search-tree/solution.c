static struct TreeNode* build(int* nums, int lo, int hi) {
    if (lo > hi) return NULL;
    int mid = lo + (hi - lo) / 2;
    struct TreeNode* t = (struct TreeNode*)malloc(sizeof(struct TreeNode));
    t->val = nums[mid];
    t->left = build(nums, lo, mid - 1);
    t->right = build(nums, mid + 1, hi);
    return t;
}

struct TreeNode* sortedArrayToBST(int* nums, int numsSize) {
    return build(nums, 0, numsSize - 1);
}
