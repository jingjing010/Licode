int main(void) {
    int nOps, nArgs;
    int* argSizes;
    char** ops = oj_read_string_array(&nOps);
    int** args = oj_read_int_matrix(&nArgs, &argSizes);
    if (nOps == 0 || strcmp(ops[0], "StockSpanner") != 0) oj_fail("第一个操作必须是 StockSpanner");
    if (nArgs != nOps) oj_fail("操作数组与参数数组长度不一致");
    StockSpanner* obj = NULL;
    putchar('[');
    for (int i = 0; i < nOps; i++) {
        if (i) putchar(',');
        if (strcmp(ops[i], "StockSpanner") == 0) {
            obj = stockSpannerCreate();
            printf("null");
        } else if (strcmp(ops[i], "next") == 0) {
            if (argSizes[i] < 1) oj_fail("next 需要一个参数");
            printf("%d", stockSpannerNext(obj, args[i][0]));
        } else {
            oj_fail("未知操作");
        }
    }
    printf("]\n");
    if (obj) stockSpannerFree(obj);
    return 0;
}
