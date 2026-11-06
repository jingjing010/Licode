int applyDeadband(int value, int threshold) {
    if (value > threshold)
        return value - threshold;
    if (value < -threshold)
        return value + threshold;
    return 0;
}
