bool canPlaceFlowers(int* flowerbed, int flowerbedSize, int n) {
    int planted = 0;
    for (int i = 0; i < flowerbedSize; ++i) {
        /* 最左可种位置立即种花，给后续保留尽可能多的空间。 */
        if (flowerbed[i] == 0 && (i == 0 || flowerbed[i - 1] == 0)
            && (i + 1 == flowerbedSize || flowerbed[i + 1] == 0)) {
            flowerbed[i] = 1;
            ++planted;
        }
    }
    return planted >= n;
}
