int main(void) {
    int nOps, nArgs;
    char** ops = oj_read_string_array(&nOps);
    int* argSizes;
    int** args = oj_read_int_matrix(&nArgs, &argSizes);
    if (nOps != nArgs) oj_fail("操作数与参数个数不一致");
    TimerManager* obj = NULL;
    putchar('[');
    for (int i = 0; i < nOps; i++) {
        if (i) putchar(',');
        if (strcmp(ops[i], "TimerManager") == 0) {
            obj = timerManagerCreate(args[i][0]);
            printf("null");
        } else if (strcmp(ops[i], "start") == 0) {
            timerManagerStart(obj, args[i][0], args[i][1], args[i][2] != 0);
            printf("null");
        } else if (strcmp(ops[i], "stop") == 0) {
            timerManagerStop(obj, args[i][0]);
            printf("null");
        } else if (strcmp(ops[i], "tick") == 0) {
            int sz = 0;
            int* a = timerManagerTick(obj, &sz);
            if (a == NULL) sz = 0;
            putchar('[');
            for (int j = 0; j < sz; j++) printf(j ? ",%d" : "%d", a[j]);
            putchar(']');
            free(a);
        } else {
            oj_fail("未知操作");
        }
    }
    printf("]\n");
    if (obj) timerManagerFree(obj);
    return 0;
}
