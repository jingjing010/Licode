int main(void) {
    int nOps, nArgs;
    char** ops = oj_read_string_array(&nOps);
    int* argSizes;
    int** args = oj_read_int_matrix(&nArgs, &argSizes);
    if (nOps != nArgs) oj_fail("操作数与参数个数不一致");
    RingBuffer* obj = NULL;
    putchar('[');
    for (int i = 0; i < nOps; i++) {
        if (i) putchar(',');
        if (strcmp(ops[i], "RingBuffer") == 0) {
            obj = ringBufferCreate(args[i][0]);
            printf("null");
        } else if (strcmp(ops[i], "push") == 0) {
            printf("%s", ringBufferPush(obj, (uint8_t)args[i][0]) ? "true" : "false");
        } else if (strcmp(ops[i], "pop") == 0) {
            printf("%d", ringBufferPop(obj));
        } else if (strcmp(ops[i], "count") == 0) {
            printf("%d", ringBufferCount(obj));
        } else if (strcmp(ops[i], "isFull") == 0) {
            printf("%s", ringBufferIsFull(obj) ? "true" : "false");
        } else {
            oj_fail("未知操作");
        }
    }
    printf("]\n");
    if (obj) ringBufferFree(obj);
    return 0;
}
