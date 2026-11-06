int main(void) {
    int rows;
    int* cols;
    int** table = oj_read_int_matrix(&rows, &cols);
    int initState = oj_read_int();
    int n;
    int* events = oj_read_int_array(&n);
    int returnSize = 0;
    int* res = runStateMachine(table, rows, rows > 0 ? cols[0] : 0, initState, events, n, &returnSize);
    if (res == NULL) returnSize = 0;
    oj_print_int_array(res, returnSize);
    return 0;
}
