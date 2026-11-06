/* 模拟，O(n) */
char** fizzBuzz(int n, int* returnSize) {
    char** ans = (char**)malloc(sizeof(char*) * n);
    for (int i = 1; i <= n; i++) {
        char* s = (char*)malloc(12);
        if (i % 15 == 0) strcpy(s, "FizzBuzz");
        else if (i % 3 == 0) strcpy(s, "Fizz");
        else if (i % 5 == 0) strcpy(s, "Buzz");
        else sprintf(s, "%d", i);
        ans[i - 1] = s;
    }
    *returnSize = n;
    return ans;
}
