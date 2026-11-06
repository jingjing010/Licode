int main(void) {
    char* s = oj_read_string();
    char* d = oj_read_string();
    int maxTokens = oj_read_int();
    if (d[0] == '\0') oj_fail("分隔符不能为空");
    if (maxTokens < 1) oj_fail("maxTokens 至少为 1");
    int len = (int)strlen(s);

    /* str 后面 16 字节哨兵；tokens 后面再放 4 个哨兵指针，用于检测越界写 */
    char* str = (char*)malloc(len + 1 + 16);
    memcpy(str, s, len + 1);
    memset(str + len + 1, 0x7F, 16);
    char* sentinel = (char*)&maxTokens;
    char** tokens = (char**)malloc(sizeof(char*) * (maxTokens + 4));
    for (int i = 0; i < maxTokens + 4; i++) tokens[i] = sentinel;

    int cnt = split_string(str, d[0], tokens, maxTokens);

    for (int i = 0; i < 16; i++)
        if (str[len + 1 + i] != 0x7F) { puts("错误：写到了 str 之外的内存"); return 0; }
    for (int i = maxTokens; i < maxTokens + 4; i++)
        if (tokens[i] != sentinel) { puts("错误：写到了 tokens 数组之外"); return 0; }
    if (cnt < 0 || cnt > maxTokens) { puts("错误：返回值必须在 0 ~ maxTokens 之间"); return 0; }
    for (int i = 0; i < cnt; i++)
        if (tokens[i] < str || tokens[i] > str + len) { puts("错误：tokens 必须指向 str 内部（原地分割）"); return 0; }
    oj_print_string_array(tokens, cnt);
    return 0;
}
