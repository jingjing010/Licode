int main(void) {
    int nOps, nArgs;
    int* argSizes;
    char** ops = oj_read_string_array(&nOps);
    int** args = oj_read_int_matrix(&nArgs, &argSizes);
    if (nOps == 0 || strcmp(ops[0], "MedianFinder") != 0) oj_fail("第一个操作必须是 MedianFinder");
    if (nArgs != nOps) oj_fail("操作数组与参数数组长度不一致");
    MedianFinder* obj = NULL;
    putchar('[');
    for (int i = 0; i < nOps; i++) {
        if (i) putchar(',');
        if (strcmp(ops[i], "MedianFinder") == 0) {
            obj = medianFinderCreate();
            printf("null");
        } else if (strcmp(ops[i], "addNum") == 0) {
            if (argSizes[i] < 1) oj_fail("addNum 需要一个参数");
            medianFinderAddNum(obj, args[i][0]);
            printf("null");
        } else if (strcmp(ops[i], "findMedian") == 0) {
            printf("%.5f", medianFinderFindMedian(obj));
        } else {
            oj_fail("未知操作");
        }
    }
    printf("]\n");
    if (obj) medianFinderFree(obj);
    return 0;
}
