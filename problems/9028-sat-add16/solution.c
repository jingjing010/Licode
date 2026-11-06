void sat_add16(const int16_t* a, const int16_t* b, int16_t* out, size_t len) {
    for (size_t i = 0; i < len; i++) {
        int32_t s = (int32_t)a[i] + (int32_t)b[i];
        if (s > INT16_MAX) s = INT16_MAX;
        else if (s < INT16_MIN) s = INT16_MIN;
        out[i] = (int16_t)s;
    }
}
