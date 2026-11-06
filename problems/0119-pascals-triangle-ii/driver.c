int main(void) {
    int rowIndex = oj_read_int();
    int returnSize = 0;
    int* res = getRow(rowIndex, &returnSize);
    oj_print_int_array(res, returnSize);
    return 0;
}
