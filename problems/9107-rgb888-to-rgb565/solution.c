uint16_t rgb565(int red, int green, int blue) {
    return (uint16_t)(((red >> 3) << 11) | ((green >> 2) << 5) | (blue >> 3));
}
