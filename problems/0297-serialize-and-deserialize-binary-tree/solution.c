/* 前序遍历 + 空结点标记 '#'，逗号分隔：序列化/反序列化均为 O(n) */
typedef struct {
    char* buf;
    int len;
    int cap;
} SerBuf;

static void serAppend(SerBuf* sb, const char* s) {
    int n = (int)strlen(s);
    while (sb->len + n + 1 > sb->cap) {
        sb->cap *= 2;
        sb->buf = (char*)realloc(sb->buf, sb->cap);
    }
    memcpy(sb->buf + sb->len, s, n + 1);
    sb->len += n;
}

static void serDfs(struct TreeNode* node, SerBuf* sb) {
    if (node == NULL) {
        serAppend(sb, "#,");
        return;
    }
    char tmp[16];
    sprintf(tmp, "%d,", node->val);
    serAppend(sb, tmp);
    serDfs(node->left, sb);
    serDfs(node->right, sb);
}

char* serialize(struct TreeNode* root) {
    SerBuf sb;
    sb.cap = 64;
    sb.len = 0;
    sb.buf = (char*)malloc(sb.cap);
    sb.buf[0] = '\0';
    serDfs(root, &sb);
    return sb.buf;
}

static struct TreeNode* desDfs(char** p) {
    if (**p == '#') {
        *p += 2;
        return NULL;
    }
    struct TreeNode* node = (struct TreeNode*)malloc(sizeof(struct TreeNode));
    node->val = (int)strtol(*p, p, 10);
    (*p)++;
    node->left = desDfs(p);
    node->right = desDfs(p);
    return node;
}

struct TreeNode* deserialize(char* data) {
    char* p = data;
    return desDfs(&p);
}
