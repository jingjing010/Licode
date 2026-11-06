int main(void) {
    int nOps, nArgs;
    int* argSizes;
    char** ops = oj_read_string_array(&nOps);
    int** args = oj_read_int_matrix(&nArgs, &argSizes);
    if (nOps == 0 || strcmp(ops[0], "LRUCache") != 0) oj_fail("第一个操作必须是 LRUCache");
    if (nArgs != nOps) oj_fail("操作数组与参数数组长度不一致");
    LRUCache* obj = NULL;
    putchar('[');
    for (int i = 0; i < nOps; i++) {
        if (i) putchar(',');
        if (strcmp(ops[i], "LRUCache") == 0) {
            if (argSizes[i] < 1) oj_fail("LRUCache 需要一个参数 capacity");
            obj = lRUCacheCreate(args[i][0]);
            printf("null");
        } else if (strcmp(ops[i], "get") == 0) {
            if (argSizes[i] < 1) oj_fail("get 需要一个参数");
            printf("%d", lRUCacheGet(obj, args[i][0]));
        } else if (strcmp(ops[i], "put") == 0) {
            if (argSizes[i] < 2) oj_fail("put 需要两个参数");
            lRUCachePut(obj, args[i][0], args[i][1]);
            printf("null");
        } else {
            oj_fail("未知操作");
        }
    }
    printf("]\n");
    if (obj) lRUCacheFree(obj);
    return 0;
}
