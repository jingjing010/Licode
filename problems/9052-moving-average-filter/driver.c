int main(void) {
    int nOps, nArgs;
    char** ops = oj_read_string_array(&nOps);
    int* argSizes;
    int** args = oj_read_int_matrix(&nArgs, &argSizes);
    if (nOps != nArgs) oj_fail("操作数与参数个数不一致");
    MovingAvg* obj = NULL;
    putchar('[');
    for (int i = 0; i < nOps; i++) {
        if (i) putchar(',');
        if (strcmp(ops[i], "MovingAvg") == 0) {
            obj = movingAvgCreate(args[i][0]);
            printf("null");
        } else if (strcmp(ops[i], "update") == 0) {
            unsigned int v = movingAvgUpdate(obj, (uint16_t)args[i][0]);
            printf("%u", v);
        } else if (strcmp(ops[i], "reset") == 0) {
            movingAvgReset(obj);
            printf("null");
        } else {
            oj_fail("未知操作");
        }
    }
    printf("]\n");
    if (obj) movingAvgFree(obj);
    return 0;
}
