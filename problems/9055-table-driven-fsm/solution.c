int* runStateMachine(int** table, int stateCount, int eventCount, int initState,
                     const int* events, int eventsSize, int* returnSize) {
    int* res = (int*)malloc(sizeof(int) * eventsSize);
    int cur = initState;
    for (int i = 0; i < eventsSize; i++) {
        int next = table[cur][events[i]];
        if (next != -1) cur = next;
        res[i] = cur;
    }
    *returnSize = eventsSize;
    return res;
}
