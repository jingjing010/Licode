int pwmRamp(int initial, int target, int step, int ticks) {
    int64_t distance = (int64_t)step * ticks;
    if (initial < target)
        return distance >= target - initial ? target : initial + (int)distance;
    return distance >= initial - target ? target : initial - (int)distance;
}
