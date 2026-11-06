typedef struct {
    int32_t* buf;
    int capacity;
    int head;   /* 最旧一条的位置 */
    int count;
} LogBuffer;

LogBuffer* logBufferCreate(int capacity) {
    LogBuffer* obj = (LogBuffer*)malloc(sizeof(LogBuffer));
    obj->buf = (int32_t*)malloc(sizeof(int32_t) * capacity);
    obj->capacity = capacity;
    obj->head = 0;
    obj->count = 0;
    return obj;
}

void logBufferWrite(LogBuffer* obj, int32_t value) {
    int tail = (obj->head + obj->count) % obj->capacity;
    obj->buf[tail] = value;
    if (obj->count < obj->capacity) {
        obj->count++;
    } else {
        obj->head = (obj->head + 1) % obj->capacity;
    }
}

int* logBufferGetAll(LogBuffer* obj, int* returnSize) {
    int* res = (int*)malloc(sizeof(int) * (obj->count + 1));
    for (int i = 0; i < obj->count; i++) {
        res[i] = obj->buf[(obj->head + i) % obj->capacity];
    }
    *returnSize = obj->count;
    return res;
}

int logBufferCount(LogBuffer* obj) {
    return obj->count;
}

void logBufferFree(LogBuffer* obj) {
    free(obj->buf);
    free(obj);
}
