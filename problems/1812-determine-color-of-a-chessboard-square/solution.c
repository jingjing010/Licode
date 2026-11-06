bool squareIsWhite(char *coordinates) {
    /* a1为黑色，横纵坐标奇偶性不同时为白色。 */
    return ((coordinates[0] - 'a') + (coordinates[1] - '1')) % 2 != 0;
}
