typedef struct {
    
} TimerManager;


TimerManager* timerManagerCreate(int maxTimers) {
    
}

void timerManagerStart(TimerManager* obj, int id, int period, bool repeat) {
    
}

void timerManagerStop(TimerManager* obj, int id) {
    
}

/**
 * Note: The returned array must be malloced, assume caller calls free().
 * 注意：返回的数组必须用 malloc 申请，*returnSize 要设置为返回数组的长度。
 */
int* timerManagerTick(TimerManager* obj, int* returnSize) {
    
}

void timerManagerFree(TimerManager* obj) {
    
}
