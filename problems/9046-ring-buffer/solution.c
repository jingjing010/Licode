typedef struct {
    uint8_t* buf;
    int capacity;
    int head;   /* 下一个要读的位置 */
    int tail;   /* 下一个要写的位置 */
    int count;  /* 当前元素个数 */
} RingBuffer;

RingBuffer* ringBufferCreate(int capacity) {
    RingBuffer* obj = (RingBuffer*)malloc(sizeof(RingBuffer));
    obj->buf = (uint8_t*)malloc(capacity);
    obj->capacity = capacity;
    obj->head = obj->tail = obj->count = 0;
    return obj;
}

bool ringBufferPush(RingBuffer* obj, uint8_t data) {
    if (obj->count == obj->capacity) return false;
    obj->buf[obj->tail] = data;
    obj->tail = (obj->tail + 1) % obj->capacity;
    obj->count++;
    return true;
}

int ringBufferPop(RingBuffer* obj) {
    if (obj->count == 0) return -1;
    int v = obj->buf[obj->head];
    obj->head = (obj->head + 1) % obj->capacity;
    obj->count--;
    return v;
}

int ringBufferCount(RingBuffer* obj) {
    return obj->count;
}

bool ringBufferIsFull(RingBuffer* obj) {
    return obj->count == obj->capacity;
}

void ringBufferFree(RingBuffer* obj) {
    free(obj->buf);
    free(obj);
}
