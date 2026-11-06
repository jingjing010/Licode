static bool drv_valid_gray(const int* a, int size, int n) {
    int total = 1 << n;
    if (a == NULL || size != total || a[0] != 0) return false;
    char* seen = (char*)calloc(total, 1);
    bool ok = true;
    for (int i = 0; i < total && ok; i++) {
        if (a[i] < 0 || a[i] >= total || seen[a[i]]) {
            ok = false;
            break;
        }
        seen[a[i]] = 1;
        unsigned int d = (unsigned int)a[i] ^ (unsigned int)a[(i + 1) % total];
        if (d == 0 || (d & (d - 1)) != 0) ok = false;
    }
    free(seen);
    return ok;
}

int main(void) {
    int n = oj_read_int();
    int returnSize = 0;
    int* ans = grayCode(n, &returnSize);
    if (ans == NULL) returnSize = 0;
    if (!drv_valid_gray(ans, returnSize, n)) {
        oj_print_int_array(ans, returnSize);
        return 0;
    }
    int total = 1 << n;
    int* std_ans = (int*)malloc(sizeof(int) * total);
    for (int i = 0; i < total; i++) std_ans[i] = i ^ (i >> 1);
    oj_print_int_array(std_ans, total);
    return 0;
}
