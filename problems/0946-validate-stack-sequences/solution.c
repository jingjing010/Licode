bool validateStackSequences(int* pushed, int pushedSize, int* popped, int poppedSize) {
    int* st = (int*)malloc(sizeof(int) * (pushedSize + 1));
    int top = 0, j = 0;
    for (int i = 0; i < pushedSize; i++) {
        st[top++] = pushed[i];
        while (top > 0 && j < poppedSize && st[top - 1] == popped[j]) {
            top--;
            j++;
        }
    }
    free(st);
    return j == poppedSize;
}
