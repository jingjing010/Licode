/* 后序最后一个是根；用 值 -> 中序下标 的直接映射表定位根，分治构造：O(n) */
#define OFFSET 3000

static int g_pos[2 * OFFSET + 1];
static int* g_post;
static int g_postIdx;

static struct TreeNode* build(int inL, int inR) {
    if (inL > inR) return NULL;
    int v = g_post[g_postIdx--];
    struct TreeNode* node = (struct TreeNode*)malloc(sizeof(struct TreeNode));
    node->val = v;
    int k = g_pos[v + OFFSET];
    node->right = build(k + 1, inR);
    node->left = build(inL, k - 1);
    return node;
}

struct TreeNode* buildTree(int* inorder, int inorderSize, int* postorder, int postorderSize) {
    for (int i = 0; i < inorderSize; i++) g_pos[inorder[i] + OFFSET] = i;
    g_post = postorder;
    g_postIdx = postorderSize - 1;
    return build(0, inorderSize - 1);
}
