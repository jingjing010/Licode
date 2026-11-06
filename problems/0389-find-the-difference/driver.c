int main(void) {
    char* s = oj_read_string();
    char* t = oj_read_string();
    char c = findTheDifference(s, t);
    char out[2] = {c, '\0'};
    oj_print_string(out);
    return 0;
}
