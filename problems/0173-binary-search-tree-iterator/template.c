/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     struct TreeNode *left;
 *     struct TreeNode *right;
 * };
 * 注意：struct TreeNode 系统已经定义好了，不要重复定义，直接使用即可。
 */



typedef struct {
    
} BSTIterator;


BSTIterator* bSTIteratorCreate(struct TreeNode* root) {
    
    return NULL;
}

int bSTIteratorNext(BSTIterator* obj) {
    
    return 0;
}

bool bSTIteratorHasNext(BSTIterator* obj) {
    
    return false;
}

void bSTIteratorFree(BSTIterator* obj) {
    
}

/**
 * Your BSTIterator struct will be instantiated and called as such:
 * BSTIterator* obj = bSTIteratorCreate(root);
 * int param_1 = bSTIteratorNext(obj);
 
 * bool param_2 = bSTIteratorHasNext(obj);
 
 * bSTIteratorFree(obj);
*/
