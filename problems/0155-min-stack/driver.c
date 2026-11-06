int main(void) {
    int nOps, nArgs;
    int* argSizes;
    char** ops = oj_read_string_array(&nOps);
    int** args = oj_read_int_matrix(&nArgs, &argSizes);
    if (nOps == 0 || strcmp(ops[0], "MinStack") != 0) oj_fail("第一个操作必须是 MinStack");
    if (nArgs != nOps) oj_fail("操作数组与参数数组长度不一致");
    MinStack* obj = NULL;
    putchar('[');
    for (int i = 0; i < nOps; i++) {
        if (i) putchar(',');
        if (strcmp(ops[i], "MinStack") == 0) {
            obj = minStackCreate();
            printf("null");
        } else if (strcmp(ops[i], "push") == 0) {
            if (argSizes[i] < 1) oj_fail("push 需要一个参数");
            minStackPush(obj, args[i][0]);
            printf("null");
        } else if (strcmp(ops[i], "pop") == 0) {
            minStackPop(obj);
            printf("null");
        } else if (strcmp(ops[i], "top") == 0) {
            printf("%d", minStackTop(obj));
        } else if (strcmp(ops[i], "getMin") == 0) {
            printf("%d", minStackGetMin(obj));
        } else {
            oj_fail("未知操作");
        }
    }
    printf("]\n");
    if (obj) minStackFree(obj);
    return 0;
}
