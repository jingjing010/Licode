/* 判题系统提供的 isBadVersion 接口：隐藏答案由 driver 设置，并统计调用次数 */
static int drv_n_versions;
static int drv_first_bad;
static long long drv_calls;
static long long drv_call_limit;

bool isBadVersion(int version) {
    if (version < 1 || version > drv_n_versions) {
        printf("isBadVersion(%d) 参数越界：版本号必须在 [1, %d] 内\n", version, drv_n_versions);
        exit(0);
    }
    if (++drv_calls > drv_call_limit) {
        printf("isBadVersion 调用次数超过上限 %lld\n", drv_call_limit);
        exit(0);
    }
    return version >= drv_first_bad;
}
