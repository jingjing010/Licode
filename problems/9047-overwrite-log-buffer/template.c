typedef struct {
    
} LogBuffer;


LogBuffer* logBufferCreate(int capacity) {
    
}

void logBufferWrite(LogBuffer* obj, int32_t value) {
    
}

/**
 * Note: The returned array must be malloced, assume caller calls free().
 * 注意：返回的数组必须用 malloc 申请，*returnSize 要设置为返回数组的长度。
 */
int* logBufferGetAll(LogBuffer* obj, int* returnSize) {
    
}

int logBufferCount(LogBuffer* obj) {
    
}

void logBufferFree(LogBuffer* obj) {
    
}
