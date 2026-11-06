int *expandRgb565(int pixel, int *returnSize) {
    int r = (pixel >> 11) & 31, g = (pixel >> 5) & 63, b = pixel & 31,
        *out = malloc(3 * sizeof(int));
    /* 高位复制到低位，使全亮值恢复为255。 */
    out[0] = (r << 3) | (r >> 2);
    out[1] = (g << 2) | (g >> 4);
    out[2] = (b << 3) | (b >> 2);
    *returnSize = 3;
    return out;
}
