int main(void) {
    char* s = oj_read_string();
    int returnSize = 0;
    int* ans = partitionLabels(s, &returnSize);
    if (ans == NULL) returnSize = 0;
    oj_print_int_array(ans, returnSize);
    return 0;
}
