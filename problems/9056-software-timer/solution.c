typedef struct {
    bool running;
    bool repeat;
    uint32_t period;
    uint32_t remaining;
} SoftTimer;

typedef struct {
    SoftTimer* timers;
    int n;
} TimerManager;

TimerManager* timerManagerCreate(int maxTimers) {
    TimerManager* obj = (TimerManager*)malloc(sizeof(TimerManager));
    obj->timers = (SoftTimer*)calloc(maxTimers, sizeof(SoftTimer));
    obj->n = maxTimers;
    return obj;
}

void timerManagerStart(TimerManager* obj, int id, int period, bool repeat) {
    SoftTimer* t = &obj->timers[id];
    t->running = true;
    t->repeat = repeat;
    t->period = (uint32_t)period;
    t->remaining = (uint32_t)period;
}

void timerManagerStop(TimerManager* obj, int id) {
    obj->timers[id].running = false;
}

int* timerManagerTick(TimerManager* obj, int* returnSize) {
    int* fired = (int*)malloc(sizeof(int) * obj->n);
    int m = 0;
    for (int id = 0; id < obj->n; id++) {
        SoftTimer* t = &obj->timers[id];
        if (!t->running) continue;
        if (--t->remaining == 0) {
            fired[m++] = id;
            if (t->repeat) t->remaining = t->period;
            else t->running = false;
        }
    }
    *returnSize = m;
    return fired;
}

void timerManagerFree(TimerManager* obj) {
    free(obj->timers);
    free(obj);
}
