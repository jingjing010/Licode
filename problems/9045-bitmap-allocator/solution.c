typedef struct {
    uint32_t* bits;
    int blockCount;
    int used;
} BitmapAllocator;

static bool bm_test(const BitmapAllocator* obj, int i) {
    return (obj->bits[i >> 5] >> (i & 31)) & 1u;
}

static void bm_set(BitmapAllocator* obj, int i) {
    obj->bits[i >> 5] |= 1u << (i & 31);
}

static void bm_clear(BitmapAllocator* obj, int i) {
    obj->bits[i >> 5] &= ~(1u << (i & 31));
}

BitmapAllocator* bitmapAllocatorCreate(int blockCount) {
    BitmapAllocator* obj = (BitmapAllocator*)malloc(sizeof(BitmapAllocator));
    obj->bits = (uint32_t*)calloc((blockCount + 31) / 32, sizeof(uint32_t));
    obj->blockCount = blockCount;
    obj->used = 0;
    return obj;
}

int bitmapAllocatorAlloc(BitmapAllocator* obj, int count) {
    if (count < 1 || count > obj->blockCount) return -1;
    int run = 0;
    for (int i = 0; i < obj->blockCount; i++) {
        if (bm_test(obj, i)) {
            run = 0;
        } else if (++run == count) {
            int start = i - count + 1;
            for (int j = start; j <= i; j++) bm_set(obj, j);
            obj->used += count;
            return start;
        }
    }
    return -1;
}

bool bitmapAllocatorRelease(BitmapAllocator* obj, int start, int count) {
    if (start < 0 || count < 1 || start + count > obj->blockCount) return false;
    for (int i = start; i < start + count; i++)
        if (!bm_test(obj, i)) return false;
    for (int i = start; i < start + count; i++) bm_clear(obj, i);
    obj->used -= count;
    return true;
}

int bitmapAllocatorUsedCount(BitmapAllocator* obj) {
    return obj->used;
}

void bitmapAllocatorFree(BitmapAllocator* obj) {
    free(obj->bits);
    free(obj);
}
