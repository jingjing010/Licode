typedef struct {
    
} MemoryPool;


MemoryPool* memoryPoolCreate(int blockSize, int blockCount) {
    
}

int memoryPoolAlloc(MemoryPool* obj) {
    
}

bool memoryPoolRelease(MemoryPool* obj, int index) {
    
}

int memoryPoolFreeCount(MemoryPool* obj) {
    
}

void memoryPoolFree(MemoryPool* obj) {
    
}

/**
 * Your MemoryPool struct will be instantiated and called as such:
 * MemoryPool* obj = memoryPoolCreate(blockSize, blockCount);
 * int param_1 = memoryPoolAlloc(obj);
 * bool param_2 = memoryPoolRelease(obj, index);
 * int param_3 = memoryPoolFreeCount(obj);
 * memoryPoolFree(obj);
 */
