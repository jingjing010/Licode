/* 判题系统提供的 guess 接口：隐藏答案由 driver 设置，并统计调用次数 */
static int drv_n_range;
static int drv_pick;
static long long drv_calls;
static long long drv_call_limit;

int guess(int num) {
    if (num < 1 || num > drv_n_range) {
        printf("guess(%d) 参数越界：数字必须在 [1, %d] 内\n", num, drv_n_range);
        exit(0);
    }
    if (++drv_calls > drv_call_limit) {
        printf("guess 调用次数超过上限 %lld\n", drv_call_limit);
        exit(0);
    }
    if (num > drv_pick) return -1;
    if (num < drv_pick) return 1;
    return 0;
}
