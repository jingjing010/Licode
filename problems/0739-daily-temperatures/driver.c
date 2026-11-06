int main(void) {
    int n;
    int* t = oj_read_int_array(&n);
    int returnSize = 0;
    int* ans = dailyTemperatures(t, n, &returnSize);
    if (ans == NULL) returnSize = 0;
    oj_print_int_array(ans, returnSize);
    return 0;
}
