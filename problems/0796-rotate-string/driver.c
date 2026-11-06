int main(void) {
    char *s = oj_read_string();
    char *goal = oj_read_string();
    oj_print_bool(rotateString(s, goal));
    free(s);
    free(goal);
    return 0;
}
