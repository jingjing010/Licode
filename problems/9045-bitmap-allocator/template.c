typedef struct {
    
} BitmapAllocator;


BitmapAllocator* bitmapAllocatorCreate(int blockCount) {
    
}

int bitmapAllocatorAlloc(BitmapAllocator* obj, int count) {
    
}

bool bitmapAllocatorRelease(BitmapAllocator* obj, int start, int count) {
    
}

int bitmapAllocatorUsedCount(BitmapAllocator* obj) {
    
}

void bitmapAllocatorFree(BitmapAllocator* obj) {
    
}

/**
 * Your BitmapAllocator struct will be instantiated and called as such:
 * BitmapAllocator* obj = bitmapAllocatorCreate(blockCount);
 * int param_1 = bitmapAllocatorAlloc(obj, count);
 * bool param_2 = bitmapAllocatorRelease(obj, start, count);
 * int param_3 = bitmapAllocatorUsedCount(obj);
 * bitmapAllocatorFree(obj);
 */
