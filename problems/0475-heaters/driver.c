int main(void) {
    int n, m;
    int* houses = oj_read_int_array(&n);
    int* heaters = oj_read_int_array(&m);
    oj_print_int(findRadius(houses, n, heaters, m));
    return 0;
}
