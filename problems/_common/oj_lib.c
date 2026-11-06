/*
 * ===================== OJ 驱动公共库 =====================
 * 判题时自动拼接在【你的代码之后】、driver.c 之前。
 * 负责：读取 LeetCode 风格的输入（如 [1,2,3]、"abc"），以及按统一格式输出。
 * 所有名字都带 oj_ 前缀，避免与你的代码冲突。
 * ==========================================================
 */

#define OJ_LINE_MAX (1 << 21)
char oj_line_buf[OJ_LINE_MAX];

void oj_fail(const char* msg) {
    fprintf(stderr, "[OJ] 输入格式错误: %s\n", msg);
    exit(3);
}

/* 读取下一行非空输入（去掉行尾的 \r \n 和空格）。读完返回 NULL */
char* oj_next_line(void) {
    while (fgets(oj_line_buf, OJ_LINE_MAX, stdin)) {
        size_t len = strlen(oj_line_buf);
        while (len > 0 && (oj_line_buf[len - 1] == '\n' || oj_line_buf[len - 1] == '\r' ||
                           oj_line_buf[len - 1] == ' ' || oj_line_buf[len - 1] == '\t'))
            oj_line_buf[--len] = '\0';
        char* p = oj_line_buf;
        while (*p == ' ' || *p == '\t') p++;
        if (*p) return p;
    }
    return NULL;
}

char* oj_must_line(void) {
    char* s = oj_next_line();
    if (!s) oj_fail("输入行数不够");
    return s;
}

/* ---------- 读取 ---------- */

int oj_read_int(void) {
    char* s = oj_must_line();
    char* end;
    long v = strtol(s, &end, 10);
    if (end == s) oj_fail("期望一个整数");
    return (int)v;
}

long long oj_read_ll(void) {
    char* s = oj_must_line();
    char* end;
    long long v = strtoll(s, &end, 10);
    if (end == s) oj_fail("期望一个整数");
    return v;
}

double oj_read_double(void) {
    char* s = oj_must_line();
    return strtod(s, NULL);
}

bool oj_read_bool(void) {
    char* s = oj_must_line();
    return strncmp(s, "true", 4) == 0 || strcmp(s, "1") == 0;
}

/* 从 p 开始解析整数数组 "[1,2,3]"，返回 malloc 的数组，*size 为长度，*endp 指向 ']' 之后 */
int* oj_parse_int_array_at(const char* p, int* size, const char** endp) {
    int cap = 16, n = 0;
    int* a = (int*)malloc(sizeof(int) * cap);
    while (*p && *p != '[') p++;
    if (*p != '[') oj_fail("期望形如 [1,2,3] 的数组");
    p++;
    while (*p) {
        while (*p == ' ' || *p == ',') p++;
        if (*p == ']') { p++; break; }
        if (!*p) break;
        char* end;
        long v = strtol(p, &end, 10);
        if (end == p) oj_fail("数组中有非法数字");
        if (n == cap) { cap *= 2; a = (int*)realloc(a, sizeof(int) * cap); }
        a[n++] = (int)v;
        p = end;
    }
    *size = n;
    if (endp) *endp = p;
    return a;
}

int* oj_read_int_array(int* size) {
    return oj_parse_int_array_at(oj_must_line(), size, NULL);
}

/* 二维数组 "[[1,2],[3]]"，*colSizes 为每行长度 */
int** oj_read_int_matrix(int* rows, int** colSizes) {
    const char* p = oj_must_line();
    while (*p && *p != '[') p++;
    if (*p != '[') oj_fail("期望形如 [[1,2],[3,4]] 的二维数组");
    p++;
    int cap = 16, n = 0;
    int** m = (int**)malloc(sizeof(int*) * cap);
    int* cs = (int*)malloc(sizeof(int) * cap);
    while (*p) {
        while (*p == ' ' || *p == ',') p++;
        if (*p == ']' || !*p) break;
        if (n == cap) {
            cap *= 2;
            m = (int**)realloc(m, sizeof(int*) * cap);
            cs = (int*)realloc(cs, sizeof(int) * cap);
        }
        m[n] = oj_parse_int_array_at(p, &cs[n], &p);
        n++;
    }
    *rows = n;
    *colSizes = cs;
    return m;
}

/* 从 p（指向开头的引号）解析一个带引号的字符串，返回 malloc 的副本 */
char* oj_parse_quoted_at(const char* p, const char** endp) {
    while (*p && *p != '"') p++;
    if (*p != '"') oj_fail("期望带双引号的字符串");
    p++;
    size_t cap = 64, n = 0;
    char* s = (char*)malloc(cap);
    while (*p && *p != '"') {
        char c = *p++;
        if (c == '\\' && *p) {
            char e = *p++;
            if (e == 'n') c = '\n';
            else if (e == 't') c = '\t';
            else c = e;
        }
        if (n + 1 >= cap) { cap *= 2; s = (char*)realloc(s, cap); }
        s[n++] = c;
    }
    if (*p == '"') p++;
    s[n] = '\0';
    if (endp) *endp = p;
    return s;
}

/* 读取字符串：如果有双引号就解析引号内的内容，否则整行作为字符串 */
char* oj_read_string(void) {
    char* line = oj_must_line();
    if (line[0] == '"') return oj_parse_quoted_at(line, NULL);
    char* s = (char*)malloc(strlen(line) + 1);
    strcpy(s, line);
    return s;
}

/* 字符串数组 ["ab","cd"] */
char** oj_read_string_array(int* size) {
    const char* p = oj_must_line();
    while (*p && *p != '[') p++;
    if (*p != '[') oj_fail("期望形如 [\"a\",\"b\"] 的字符串数组");
    p++;
    int cap = 16, n = 0;
    char** a = (char**)malloc(sizeof(char*) * cap);
    while (*p) {
        while (*p == ' ' || *p == ',') p++;
        if (*p == ']' || !*p) break;
        if (n == cap) { cap *= 2; a = (char**)realloc(a, sizeof(char*) * cap); }
        a[n++] = oj_parse_quoted_at(p, &p);
    }
    *size = n;
    return a;
}

/* 字符数组 ["h","e","l"]，返回以 '\0' 结尾的 char*，*size 为字符个数 */
char* oj_read_char_array(int* size) {
    int n;
    char** strs = oj_read_string_array(&n);
    char* s = (char*)malloc(n + 1);
    for (int i = 0; i < n; i++) s[i] = strs[i][0];
    s[n] = '\0';
    *size = n;
    return s;
}

/* ---------- 输出 ---------- */

void oj_print_int(long long x) { printf("%lld\n", x); }

void oj_print_bool(bool b) { printf("%s\n", b ? "true" : "false"); }

void oj_print_double(double x, int digits) { printf("%.*f\n", digits, x); }

void oj_print_int_array(const int* a, int n) {
    putchar('[');
    for (int i = 0; i < n; i++) {
        if (i) putchar(',');
        printf("%d", a[i]);
    }
    printf("]\n");
}

void oj_print_int_matrix(int** m, int rows, const int* colSizes) {
    putchar('[');
    for (int i = 0; i < rows; i++) {
        if (i) putchar(',');
        putchar('[');
        for (int j = 0; j < colSizes[i]; j++) {
            if (j) putchar(',');
            printf("%d", m[i][j]);
        }
        putchar(']');
    }
    printf("]\n");
}

void oj_print_quoted(const char* s) {
    putchar('"');
    if (s) {
        for (; *s; s++) {
            if (*s == '"' || *s == '\\') putchar('\\');
            if (*s == '\n') { printf("\\n"); continue; }
            putchar(*s);
        }
    }
    putchar('"');
}

void oj_print_string(const char* s) {
    oj_print_quoted(s);
    putchar('\n');
}

void oj_print_string_array(char** a, int n) {
    putchar('[');
    for (int i = 0; i < n; i++) {
        if (i) putchar(',');
        oj_print_quoted(a[i]);
    }
    printf("]\n");
}

void oj_print_char_array(const char* s, int n) {
    putchar('[');
    for (int i = 0; i < n; i++) {
        if (i) putchar(',');
        printf("\"%c\"", s[i]);
    }
    printf("]\n");
}

int oj_cmp_int(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b;
    return (x > y) - (x < y);
}

/* ---------- 字符矩阵 / 字符串矩阵 ---------- */

/* 字符矩阵 [["1","0"],["0","1"]]：返回 rows 行，每行是以 '\0' 结尾的 char*，*cols 为列数（取第一行） */
char** oj_read_char_matrix(int* rows, int* cols) {
    const char* p = oj_must_line();
    while (*p && *p != '[') p++;
    if (*p != '[') oj_fail("期望形如 [[\"a\",\"b\"],[\"c\",\"d\"]] 的字符矩阵");
    p++;
    int cap = 16, n = 0;
    char** g = (char**)malloc(sizeof(char*) * cap);
    *cols = 0;
    while (*p) {
        while (*p == ' ' || *p == ',') p++;
        if (*p == ']' || !*p) break;
        if (*p != '[') oj_fail("字符矩阵格式错误");
        p++;
        int rc = 16, m = 0;
        char* row = (char*)malloc(rc);
        while (*p) {
            while (*p == ' ' || *p == ',') p++;
            if (*p == ']') { p++; break; }
            if (!*p) break;
            char* s = oj_parse_quoted_at(p, &p);
            if (m + 1 >= rc) { rc *= 2; row = (char*)realloc(row, rc); }
            row[m++] = s[0];
            free(s);
        }
        row[m] = '\0';
        if (n == 0) *cols = m;
        if (n == cap) { cap *= 2; g = (char**)realloc(g, sizeof(char*) * cap); }
        g[n++] = row;
    }
    *rows = n;
    return g;
}

void oj_print_char_matrix(char** g, int rows, int cols) {
    putchar('[');
    for (int i = 0; i < rows; i++) {
        if (i) putchar(',');
        putchar('[');
        for (int j = 0; j < cols; j++) {
            if (j) putchar(',');
            printf("\"%c\"", g[i][j]);
        }
        putchar(']');
    }
    printf("]\n");
}

/* 字符串矩阵 [["a","b"],["c"]]，*colSizes 为每行长度 */
char*** oj_read_string_matrix(int* rows, int** colSizes) {
    const char* p = oj_must_line();
    while (*p && *p != '[') p++;
    if (*p != '[') oj_fail("期望形如 [[\"a\"],[\"b\",\"c\"]] 的字符串矩阵");
    p++;
    int cap = 16, n = 0;
    char*** m = (char***)malloc(sizeof(char**) * cap);
    int* cs = (int*)malloc(sizeof(int) * cap);
    while (*p) {
        while (*p == ' ' || *p == ',') p++;
        if (*p == ']' || !*p) break;
        if (*p != '[') oj_fail("字符串矩阵格式错误");
        p++;
        int rc = 4, k = 0;
        char** row = (char**)malloc(sizeof(char*) * rc);
        while (*p) {
            while (*p == ' ' || *p == ',') p++;
            if (*p == ']') { p++; break; }
            if (!*p) break;
            if (k == rc) { rc *= 2; row = (char**)realloc(row, sizeof(char*) * rc); }
            row[k++] = oj_parse_quoted_at(p, &p);
        }
        if (n == cap) {
            cap *= 2;
            m = (char***)realloc(m, sizeof(char**) * cap);
            cs = (int*)realloc(cs, sizeof(int) * cap);
        }
        m[n] = row;
        cs[n++] = k;
    }
    *rows = n;
    *colSizes = cs;
    return m;
}

void oj_print_string_matrix(char*** m, int rows, const int* colSizes) {
    putchar('[');
    for (int i = 0; i < rows; i++) {
        if (i) putchar(',');
        putchar('[');
        for (int j = 0; j < colSizes[i]; j++) {
            if (j) putchar(',');
            oj_print_quoted(m[i][j]);
        }
        putchar(']');
    }
    printf("]\n");
}

/* ---------- 规范化（答案顺序任意的题，driver 先排序再输出） ---------- */

int oj_cmp_str(const void* a, const void* b) {
    return strcmp(*(char* const*)a, *(char* const*)b);
}

void oj_sort_string_array(char** a, int n) {
    if (a && n > 1) qsort(a, n, sizeof(char*), oj_cmp_str);
}

typedef struct { int* row; int size; } oj_int_row;

static int oj_cmp_int_row(const void* a, const void* b) {
    const oj_int_row* x = (const oj_int_row*)a;
    const oj_int_row* y = (const oj_int_row*)b;
    for (int i = 0; i < x->size && i < y->size; i++)
        if (x->row[i] != y->row[i]) return x->row[i] < y->row[i] ? -1 : 1;
    return (x->size > y->size) - (x->size < y->size);
}

/* sortEachRow 为真时先把每行内部升序排列；然后按字典序排列各行（colSizes 同步调整） */
void oj_sort_int_matrix(int** m, int rows, int* colSizes, bool sortEachRow) {
    if (!m || rows <= 0) return;
    oj_int_row* t = (oj_int_row*)malloc(sizeof(oj_int_row) * rows);
    for (int i = 0; i < rows; i++) {
        t[i].row = m[i];
        t[i].size = colSizes[i];
        if (sortEachRow && colSizes[i] > 1) qsort(m[i], colSizes[i], sizeof(int), oj_cmp_int);
    }
    qsort(t, rows, sizeof(oj_int_row), oj_cmp_int_row);
    for (int i = 0; i < rows; i++) { m[i] = t[i].row; colSizes[i] = t[i].size; }
    free(t);
}

typedef struct { char** row; int size; } oj_str_row;

static int oj_cmp_str_row(const void* a, const void* b) {
    const oj_str_row* x = (const oj_str_row*)a;
    const oj_str_row* y = (const oj_str_row*)b;
    for (int i = 0; i < x->size && i < y->size; i++) {
        int c = strcmp(x->row[i], y->row[i]);
        if (c) return c;
    }
    return (x->size > y->size) - (x->size < y->size);
}

void oj_sort_string_matrix(char*** m, int rows, int* colSizes, bool sortEachRow) {
    if (!m || rows <= 0) return;
    oj_str_row* t = (oj_str_row*)malloc(sizeof(oj_str_row) * rows);
    for (int i = 0; i < rows; i++) {
        t[i].row = m[i];
        t[i].size = colSizes[i];
        if (sortEachRow) oj_sort_string_array(m[i], colSizes[i]);
    }
    qsort(t, rows, sizeof(oj_str_row), oj_cmp_str_row);
    for (int i = 0; i < rows; i++) { m[i] = t[i].row; colSizes[i] = t[i].size; }
    free(t);
}

/* ---------- 链表（题目的 prelude.c 中 #define OJ_HAS_LISTNODE 时启用） ---------- */
#ifdef OJ_HAS_LISTNODE
struct ListNode* oj_build_list(const int* a, int n) {
    struct ListNode dummy;
    struct ListNode* tail = &dummy;
    dummy.next = NULL;
    for (int i = 0; i < n; i++) {
        struct ListNode* node = (struct ListNode*)malloc(sizeof(struct ListNode));
        node->val = a[i];
        node->next = NULL;
        tail->next = node;
        tail = node;
    }
    return dummy.next;
}

struct ListNode* oj_read_list(void) {
    int n;
    int* a = oj_read_int_array(&n);
    return oj_build_list(a, n);
}

void oj_print_list(struct ListNode* head) {
    putchar('[');
    int first = 1, guard = 0;
    while (head) {
        if (!first) putchar(',');
        printf("%d", head->val);
        first = 0;
        head = head->next;
        if (++guard > 1000000) { printf(",...(链表可能有环)"); break; }
    }
    printf("]\n");
}
#endif

/* ---------- 二叉树（prelude.c 中 #define OJ_HAS_TREENODE 时启用） ---------- */
#ifdef OJ_HAS_TREENODE
/* 层序表示： [3,9,20,null,null,15,7] */
struct TreeNode* oj_read_tree(void) {
    const char* p = oj_must_line();
    while (*p && *p != '[') p++;
    if (*p != '[') oj_fail("期望形如 [1,null,2] 的二叉树");
    p++;
    int cap = 16, n = 0;
    struct TreeNode** nodes = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * cap);
    while (*p) {
        while (*p == ' ' || *p == ',') p++;
        if (*p == ']' || !*p) break;
        if (n == cap) { cap *= 2; nodes = (struct TreeNode**)realloc(nodes, sizeof(struct TreeNode*) * cap); }
        if (strncmp(p, "null", 4) == 0) {
            nodes[n++] = NULL;
            p += 4;
        } else {
            char* end;
            long v = strtol(p, &end, 10);
            if (end == p) oj_fail("二叉树中有非法值");
            struct TreeNode* t = (struct TreeNode*)malloc(sizeof(struct TreeNode));
            t->val = (int)v;
            t->left = t->right = NULL;
            nodes[n++] = t;
            p = end;
        }
    }
    if (n == 0 || nodes[0] == NULL) return NULL;
    int child = 1;
    for (int i = 0; i < n && child < n; i++) {
        if (!nodes[i]) continue;
        if (child < n) nodes[i]->left = nodes[child++];
        if (child < n) nodes[i]->right = nodes[child++];
    }
    return nodes[0];
}

void oj_print_tree(struct TreeNode* root) {
    if (!root) { printf("[]\n"); return; }
    int cap = 1024, head = 0, tail = 0;
    struct TreeNode** q = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * cap);
    q[tail++] = root;
    while (head < tail) {
        struct TreeNode* t = q[head++];
        if (!t) continue;
        if (tail + 2 >= cap) { cap *= 2; q = (struct TreeNode**)realloc(q, sizeof(struct TreeNode*) * cap); }
        q[tail++] = t->left;
        q[tail++] = t->right;
    }
    while (tail > 0 && q[tail - 1] == NULL) tail--;
    putchar('[');
    for (int i = 0; i < tail; i++) {
        if (i) putchar(',');
        if (q[i]) printf("%d", q[i]->val);
        else printf("null");
    }
    printf("]\n");
}
#endif
