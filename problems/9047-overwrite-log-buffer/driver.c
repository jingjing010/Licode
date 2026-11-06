int main(void) {
    int nOps, nArgs;
    char** ops = oj_read_string_array(&nOps);
    int* argSizes;
    int** args = oj_read_int_matrix(&nArgs, &argSizes);
    if (nOps != nArgs) oj_fail("操作数与参数个数不一致");
    LogBuffer* obj = NULL;
    putchar('[');
    for (int i = 0; i < nOps; i++) {
        if (i) putchar(',');
        if (strcmp(ops[i], "LogBuffer") == 0) {
            obj = logBufferCreate(args[i][0]);
            printf("null");
        } else if (strcmp(ops[i], "write") == 0) {
            logBufferWrite(obj, (int32_t)args[i][0]);
            printf("null");
        } else if (strcmp(ops[i], "getAll") == 0) {
            int sz = 0;
            int* a = logBufferGetAll(obj, &sz);
            if (a == NULL) sz = 0;
            putchar('[');
            for (int j = 0; j < sz; j++) printf(j ? ",%d" : "%d", a[j]);
            putchar(']');
            free(a);
        } else if (strcmp(ops[i], "count") == 0) {
            printf("%d", logBufferCount(obj));
        } else {
            oj_fail("未知操作");
        }
    }
    printf("]\n");
    if (obj) logBufferFree(obj);
    return 0;
}
