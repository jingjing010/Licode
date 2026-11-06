typedef struct {
    uint16_t* buf;
    int size;
    int pos;
    int count;
    uint32_t sum;
} MovingAvg;

MovingAvg* movingAvgCreate(int windowSize) {
    MovingAvg* obj = (MovingAvg*)malloc(sizeof(MovingAvg));
    obj->buf = (uint16_t*)malloc(sizeof(uint16_t) * windowSize);
    obj->size = windowSize;
    obj->pos = 0;
    obj->count = 0;
    obj->sum = 0;
    return obj;
}

uint16_t movingAvgUpdate(MovingAvg* obj, uint16_t sample) {
    if (obj->count == obj->size) {
        obj->sum -= obj->buf[obj->pos];
    } else {
        obj->count++;
    }
    obj->buf[obj->pos] = sample;
    obj->sum += sample;
    obj->pos = (obj->pos + 1) % obj->size;
    return (uint16_t)((obj->sum + (uint32_t)obj->count / 2) / (uint32_t)obj->count);
}

void movingAvgReset(MovingAvg* obj) {
    obj->pos = 0;
    obj->count = 0;
    obj->sum = 0;
}

void movingAvgFree(MovingAvg* obj) {
    free(obj->buf);
    free(obj);
}
