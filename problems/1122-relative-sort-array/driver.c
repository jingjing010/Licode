int main(void) {
    int arr1Size;
    int *arr1 = oj_read_int_array(&arr1Size);
    int arr2Size;
    int *arr2 = oj_read_int_array(&arr2Size);
    int returnSize = 0;
    int *out = relativeSortArray(arr1, arr1Size, arr2, arr2Size, &returnSize);
    oj_print_int_array(out, returnSize);
    free(out);
    free(arr1);
    free(arr2);
    return 0;
}
