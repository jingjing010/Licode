enum { ST_HEAD1, ST_HEAD2, ST_LEN, ST_DATA, ST_CHK };

int** parseFrames(const uint8_t* buf, size_t len, int* returnSize, int** returnColumnSizes) {
    int maxFrames = (int)(len / 4) + 1;
    int** frames = (int**)malloc(sizeof(int*) * maxFrames);
    int* sizes = (int*)malloc(sizeof(int) * maxFrames);
    int cnt = 0;

    int state = ST_HEAD1;
    uint8_t data[256];
    int need = 0, got = 0;
    uint8_t sum = 0;

    for (size_t i = 0; i < len; i++) {
        uint8_t b = buf[i];
        switch (state) {
        case ST_HEAD1:
            if (b == 0xAA) state = ST_HEAD2;
            break;
        case ST_HEAD2:
            if (b == 0x55) state = ST_LEN;
            else if (b != 0xAA) state = ST_HEAD1;
            break;
        case ST_LEN:
            need = b;
            got = 0;
            sum = b;
            state = (need > 0) ? ST_DATA : ST_CHK;
            break;
        case ST_DATA:
            data[got++] = b;
            sum = (uint8_t)(sum + b);
            if (got == need) state = ST_CHK;
            break;
        case ST_CHK:
            if (b == sum) {
                int* f = (int*)malloc(sizeof(int) * (need + 1));
                for (int k = 0; k < need; k++) f[k] = data[k];
                frames[cnt] = f;
                sizes[cnt] = need;
                cnt++;
            }
            state = ST_HEAD1;
            break;
        }
    }
    *returnSize = cnt;
    *returnColumnSizes = sizes;
    return frames;
}
