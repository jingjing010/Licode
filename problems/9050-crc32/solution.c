static uint32_t crc32_table[256];
static bool crc32_table_ready = false;

static void crc32_init_table(void) {
    for (uint32_t i = 0; i < 256; i++) {
        uint32_t c = i;
        for (int b = 0; b < 8; b++) {
            c = (c & 1u) ? (c >> 1) ^ 0xEDB88320u : (c >> 1);
        }
        crc32_table[i] = c;
    }
    crc32_table_ready = true;
}

uint32_t crc32(const uint8_t* buf, size_t len) {
    if (!crc32_table_ready) crc32_init_table();
    uint32_t crc = 0xFFFFFFFFu;
    for (size_t i = 0; i < len; i++) {
        crc = (crc >> 8) ^ crc32_table[(crc ^ buf[i]) & 0xFFu];
    }
    return crc ^ 0xFFFFFFFFu;
}
