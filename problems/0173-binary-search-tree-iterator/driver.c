/* 从字符串 p（指向 '['）解析层序二叉树，规则与 oj_read_tree 相同；*endp 指向对应 ']' 之后 */
static struct TreeNode* drv_parse_tree(const char* p, const char** endp) {
    if (*p != '[') oj_fail("构造参数应为形如 [7,3,15] 的二叉树");
    p++;
    int cap = 16, n = 0;
    struct TreeNode** nodes = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * cap);
    while (*p) {
        while (*p == ' ' || *p == ',') p++;
        if (*p == ']' || !*p) break;
        if (n == cap) { cap *= 2; nodes = (struct TreeNode**)realloc(nodes, sizeof(struct TreeNode*) * cap); }
        if (strncmp(p, "null", 4) == 0) {
            nodes[n++] = NULL;
            p += 4;
        } else {
            char* end;
            long v = strtol(p, &end, 10);
            if (end == p) oj_fail("二叉树中有非法值");
            struct TreeNode* t = (struct TreeNode*)malloc(sizeof(struct TreeNode));
            t->val = (int)v;
            t->left = t->right = NULL;
            nodes[n++] = t;
            p = end;
        }
    }
    if (*p != ']') oj_fail("二叉树缺少 ]");
    *endp = p + 1;
    if (n == 0 || nodes[0] == NULL) return NULL;
    int child = 1;
    for (int i = 0; i < n && child < n; i++) {
        if (!nodes[i]) continue;
        if (child < n) nodes[i]->left = nodes[child++];
        if (child < n) nodes[i]->right = nodes[child++];
    }
    return nodes[0];
}

int main(void) {
    int nOps;
    char** ops = oj_read_string_array(&nOps);
    if (nOps == 0 || strcmp(ops[0], "BSTIterator") != 0) oj_fail("第一个操作必须是 BSTIterator");
    const char* p = oj_must_line();
    while (*p == ' ') p++;
    if (*p != '[') oj_fail("参数行格式错误");
    p++;
    while (*p == ' ') p++;
    if (*p != '[') oj_fail("参数行格式错误");
    p++;
    while (*p == ' ') p++;
    const char* end;
    struct TreeNode* root = drv_parse_tree(p, &end);

    BSTIterator* obj = NULL;
    putchar('[');
    for (int i = 0; i < nOps; i++) {
        if (i) putchar(',');
        if (strcmp(ops[i], "BSTIterator") == 0) {
            obj = bSTIteratorCreate(root);
            printf("null");
        } else if (strcmp(ops[i], "next") == 0) {
            printf("%d", bSTIteratorNext(obj));
        } else if (strcmp(ops[i], "hasNext") == 0) {
            printf("%s", bSTIteratorHasNext(obj) ? "true" : "false");
        } else {
            oj_fail("未知操作");
        }
    }
    printf("]\n");
    if (obj) bSTIteratorFree(obj);
    return 0;
}
