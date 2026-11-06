int main(void) {
    int nOps, nArgs;
    char** ops = oj_read_string_array(&nOps);
    int* argSizes;
    int** args = oj_read_int_matrix(&nArgs, &argSizes);
    if (nOps != nArgs) oj_fail("操作数组和参数数组长度不一致");

    BitmapAllocator* obj = NULL;
    putchar('[');
    for (int i = 0; i < nOps; i++) {
        if (i) putchar(',');
        if (strcmp(ops[i], "BitmapAllocator") == 0) {
            if (argSizes[i] != 1) oj_fail("BitmapAllocator 需要 1 个参数");
            obj = bitmapAllocatorCreate(args[i][0]);
            printf("null");
        } else if (obj == NULL) {
            oj_fail("第一个操作必须是 BitmapAllocator");
        } else if (strcmp(ops[i], "alloc") == 0) {
            if (argSizes[i] != 1) oj_fail("alloc 需要 1 个参数");
            printf("%d", bitmapAllocatorAlloc(obj, args[i][0]));
        } else if (strcmp(ops[i], "release") == 0) {
            if (argSizes[i] != 2) oj_fail("release 需要 2 个参数");
            printf("%s", bitmapAllocatorRelease(obj, args[i][0], args[i][1]) ? "true" : "false");
        } else if (strcmp(ops[i], "usedCount") == 0) {
            printf("%d", bitmapAllocatorUsedCount(obj));
        } else {
            oj_fail("未知操作");
        }
    }
    printf("]\n");
    if (obj) bitmapAllocatorFree(obj);
    return 0;
}
