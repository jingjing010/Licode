static uint32_t crc32_table[256];
static bool crc32_ready = false;

static void crc32_init(void) {
    for (uint32_t v = 0; v < 256; v++) {
        uint32_t c = v;
        for (int k = 0; k < 8; k++) {
            c = (c & 1u) ? (c >> 1) ^ 0xEDB88320u : (c >> 1);
        }
        crc32_table[v] = c;
    }
    crc32_ready = true;
}

uint32_t crc32(const uint8_t* buf, size_t len) {
    if (!crc32_ready) crc32_init();
    uint32_t crc = 0xFFFFFFFFu;
    for (size_t i = 0; i < len; i++) {
        crc = (crc >> 8) ^ crc32_table[(crc ^ buf[i]) & 0xFFu];
    }
    return crc ^ 0xFFFFFFFFu;
}
