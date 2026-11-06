typedef struct {
    int value, index;
} Entry;
static int cmpEntry(const void *a, const void *b) {
    const Entry *x = a, *y = b;
    if (x->value != y->value)
        return (x->value > y->value) - (x->value < y->value);
    return (x->index > y->index) - (x->index < y->index);
}
bool containsNearbyDuplicate(int *nums, int numsSize, int k) {
    Entry *a = malloc(numsSize * sizeof(Entry));
    for (int i = 0; i < numsSize; ++i) {
        a[i].value = nums[i];
        a[i].index = i;
    }
    qsort(a, numsSize, sizeof(Entry), cmpEntry);
    bool found = false;
    /* 相同值的原下标排序后，只需检查相邻下标差。 */
    for (int i = 1; i < numsSize; ++i)
        if (a[i].value == a[i - 1].value && a[i].index - a[i - 1].index <= k) {
            found = true;
            break;
        }
    free(a);
    return found;
}
