int heightChecker(int *heights, int heightsSize) {
    int counts[101] = {0};
    for (int i = 0; i < heightsSize; ++i)
        ++counts[heights[i]];
    int index = 0, wrong = 0;
    /* 计数得到排序序列，与原位置逐个比较。 */
    for (int h = 1; h <= 100; ++h)
        while (counts[h]-- > 0) {
            if (heights[index] != h)
                ++wrong;
            ++index;
        }
    return wrong;
}
