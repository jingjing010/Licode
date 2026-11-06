typedef struct {
    char* buf;
    int len;
    int cap;
} DsStr;

static void dsAppend(DsStr* d, const char* src, int n) {
    if (d->len + n + 1 > d->cap) {
        while (d->len + n + 1 > d->cap) d->cap *= 2;
        d->buf = (char*)realloc(d->buf, d->cap);
    }
    memcpy(d->buf + d->len, src, n);
    d->len += n;
    d->buf[d->len] = '\0';
}

/* 从 s[*pos] 开始解码，遇到 ']' 或字符串结尾停止 */
static void dsDecode(const char* s, int* pos, DsStr* out) {
    while (s[*pos] != '\0' && s[*pos] != ']') {
        char c = s[*pos];
        if (c >= '0' && c <= '9') {
            int k = 0;
            while (s[*pos] >= '0' && s[*pos] <= '9') k = k * 10 + (s[(*pos)++] - '0');
            (*pos)++; /* 跳过 '[' */
            DsStr inner = {(char*)malloc(16), 0, 16};
            inner.buf[0] = '\0';
            dsDecode(s, pos, &inner);
            (*pos)++; /* 跳过 ']' */
            for (int i = 0; i < k; i++) dsAppend(out, inner.buf, inner.len);
            free(inner.buf);
        } else {
            dsAppend(out, &c, 1);
            (*pos)++;
        }
    }
}

char* decodeString(char* s) {
    DsStr out = {(char*)malloc(16), 0, 16};
    out.buf[0] = '\0';
    int pos = 0;
    dsDecode(s, &pos, &out);
    return out.buf;
}
