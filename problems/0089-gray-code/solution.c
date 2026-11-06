int* grayCode(int n, int* returnSize) {
    int total = 1 << n;
    int* res = (int*)malloc(sizeof(int) * total);
    for (int i = 0; i < total; i++) res[i] = i ^ (i >> 1);
    *returnSize = total;
    return res;
}
