int main(void) {
    int size1, size2;
    int* nums1 = oj_read_int_array(&size1);
    int m = oj_read_int();
    int* nums2 = oj_read_int_array(&size2);
    int n = oj_read_int();
    merge(nums1, size1, m, nums2, size2, n);
    oj_print_int_array(nums1, size1);
    return 0;
}
