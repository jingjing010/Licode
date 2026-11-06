int main(void) {
    int n1, n2;
    int* nums1 = oj_read_int_array(&n1);
    int* nums2 = oj_read_int_array(&n2);
    int returnSize = 0;
    int* ans = intersect(nums1, n1, nums2, n2, &returnSize);
    if (ans == NULL) returnSize = 0;
    if (returnSize > 0) qsort(ans, returnSize, sizeof(int), oj_cmp_int);
    oj_print_int_array(ans, returnSize);
    return 0;
}
