/* 受控的迭代中序遍历：栈里只保存“左链”，O(h) 内存，next 均摊 O(1) */
typedef struct {
    struct TreeNode** stack;
    int top;
    int cap;
} BSTIterator;

static void pushLeft(BSTIterator* it, struct TreeNode* node) {
    while (node != NULL) {
        if (it->top == it->cap) {
            it->cap *= 2;
            it->stack = (struct TreeNode**)realloc(it->stack, sizeof(struct TreeNode*) * it->cap);
        }
        it->stack[it->top++] = node;
        node = node->left;
    }
}

BSTIterator* bSTIteratorCreate(struct TreeNode* root) {
    BSTIterator* it = (BSTIterator*)malloc(sizeof(BSTIterator));
    it->cap = 64;
    it->top = 0;
    it->stack = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * it->cap);
    pushLeft(it, root);
    return it;
}

int bSTIteratorNext(BSTIterator* obj) {
    struct TreeNode* node = obj->stack[--obj->top];
    pushLeft(obj, node->right);
    return node->val;
}

bool bSTIteratorHasNext(BSTIterator* obj) {
    return obj->top > 0;
}

void bSTIteratorFree(BSTIterator* obj) {
    free(obj->stack);
    free(obj);
}
