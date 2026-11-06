/* 原地双指针：交换的同时取反，O(n^2) */
int** flipAndInvertImage(int** image, int imageSize, int* imageColSize, int* returnSize, int** returnColumnSizes) {
    for (int i = 0; i < imageSize; i++) {
        int* row = image[i];
        int l = 0, r = imageColSize[i] - 1;
        while (l < r) {
            int t = row[l];
            row[l] = row[r] ^ 1;
            row[r] = t ^ 1;
            l++;
            r--;
        }
        if (l == r) row[l] ^= 1;
    }
    *returnSize = imageSize;
    *returnColumnSizes = (int*)malloc(sizeof(int) * imageSize);
    for (int i = 0; i < imageSize; i++) (*returnColumnSizes)[i] = imageColSize[i];
    return image;
}
