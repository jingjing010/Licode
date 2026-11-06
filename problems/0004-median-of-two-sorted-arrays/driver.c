int main(void) {
    int m, n;
    int* nums1 = oj_read_int_array(&m);
    int* nums2 = oj_read_int_array(&n);
    oj_print_double(findMedianSortedArrays(nums1, m, nums2, n), 5);
    return 0;
}
