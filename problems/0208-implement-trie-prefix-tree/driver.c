int main(void) {
    int nOps, nArgs;
    char** ops = oj_read_string_array(&nOps);
    int* argc;
    char*** args = oj_read_string_matrix(&nArgs, &argc);
    if (nArgs < nOps) oj_fail("参数个数与操作个数不一致");
    Trie* obj = NULL;
    putchar('[');
    for (int i = 0; i < nOps; i++) {
        if (i) putchar(',');
        if (strcmp(ops[i], "Trie") == 0) {
            if (obj) trieFree(obj);
            obj = trieCreate();
            printf("null");
        } else if (strcmp(ops[i], "insert") == 0) {
            trieInsert(obj, args[i][0]);
            printf("null");
        } else if (strcmp(ops[i], "search") == 0) {
            printf("%s", trieSearch(obj, args[i][0]) ? "true" : "false");
        } else if (strcmp(ops[i], "startsWith") == 0) {
            printf("%s", trieStartsWith(obj, args[i][0]) ? "true" : "false");
        } else {
            oj_fail("未知的操作名");
        }
    }
    printf("]\n");
    if (obj) trieFree(obj);
    return 0;
}
