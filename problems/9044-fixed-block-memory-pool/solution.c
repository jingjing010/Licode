typedef struct {
    uint8_t* mem;
    bool* used;
    int blockSize;
    int blockCount;
    int freeHead;
    int freeCount;
} MemoryPool;

static int* pool_next(MemoryPool* obj, int index) {
    return (int*)(obj->mem + (size_t)index * obj->blockSize);
}

MemoryPool* memoryPoolCreate(int blockSize, int blockCount) {
    MemoryPool* obj = (MemoryPool*)malloc(sizeof(MemoryPool));
    obj->mem = (uint8_t*)malloc((size_t)blockSize * blockCount);
    obj->used = (bool*)calloc(blockCount, sizeof(bool));
    obj->blockSize = blockSize;
    obj->blockCount = blockCount;
    for (int i = 0; i < blockCount; i++) {
        *pool_next(obj, i) = (i + 1 < blockCount) ? i + 1 : -1;
    }
    obj->freeHead = 0;
    obj->freeCount = blockCount;
    return obj;
}

int memoryPoolAlloc(MemoryPool* obj) {
    if (obj->freeHead == -1) return -1;
    int idx = obj->freeHead;
    obj->freeHead = *pool_next(obj, idx);
    obj->used[idx] = true;
    obj->freeCount--;
    return idx;
}

bool memoryPoolRelease(MemoryPool* obj, int index) {
    if (index < 0 || index >= obj->blockCount || !obj->used[index]) return false;
    *pool_next(obj, index) = obj->freeHead;
    obj->freeHead = index;
    obj->used[index] = false;
    obj->freeCount++;
    return true;
}

int memoryPoolFreeCount(MemoryPool* obj) {
    return obj->freeCount;
}

void memoryPoolFree(MemoryPool* obj) {
    free(obj->mem);
    free(obj->used);
    free(obj);
}
