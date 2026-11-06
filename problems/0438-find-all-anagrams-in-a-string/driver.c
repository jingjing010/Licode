int main(void) {
    char* s = oj_read_string();
    char* p = oj_read_string();
    int returnSize = 0;
    int* ans = findAnagrams(s, p, &returnSize);
    if (ans == NULL) returnSize = 0;
    if (returnSize > 1) qsort(ans, returnSize, sizeof(int), oj_cmp_int);
    oj_print_int_array(ans, returnSize);
    return 0;
}
