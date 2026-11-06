int main(void) {
    int numCourses = oj_read_int();
    int rows;
    int* colSizes;
    int** pre = oj_read_int_matrix(&rows, &colSizes);
    oj_print_bool(canFinish(numCourses, pre, rows, colSizes));
    return 0;
}
