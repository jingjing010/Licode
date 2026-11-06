int main(void) {
    int arrSize;
    int *arr = oj_read_int_array(&arrSize);
    int k = (int)oj_read_ll();
    oj_print_int(findKthPositive(arr, arrSize, k));
    free(arr);
    return 0;
}
