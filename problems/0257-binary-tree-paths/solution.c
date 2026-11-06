static char buf[1024];
static char** res;
static int cnt;

static void dfs(struct TreeNode* node, int len) {
    if (node == NULL) return;
    int newLen = len + sprintf(buf + len, len == 0 ? "%d" : "->%d", node->val);
    if (node->left == NULL && node->right == NULL) {
        char* s = (char*)malloc(newLen + 1);
        memcpy(s, buf, newLen + 1);
        res[cnt++] = s;
        return;
    }
    dfs(node->left, newLen);
    dfs(node->right, newLen);
}

char** binaryTreePaths(struct TreeNode* root, int* returnSize) {
    res = (char**)malloc(sizeof(char*) * 100);
    cnt = 0;
    dfs(root, 0);
    *returnSize = cnt;
    return res;
}
