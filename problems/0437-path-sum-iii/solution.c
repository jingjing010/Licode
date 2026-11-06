#define SOL_HS 4096
static long long sol_key[SOL_HS];
static int sol_cnt[SOL_HS];
static bool sol_used[SOL_HS];

static int sol_slot(long long key) {
    unsigned long long h = (unsigned long long)key * 11400714819323198485ULL;
    int i = (int)(h >> 52);
    while (sol_used[i] && sol_key[i] != key) i = (i + 1) & (SOL_HS - 1);
    return i;
}

static int sol_dfs(struct TreeNode* t, long long cur, long long target) {
    if (t == NULL) return 0;
    cur += t->val;
    int i = sol_slot(cur - target);
    int res = sol_used[i] ? sol_cnt[i] : 0;
    int j = sol_slot(cur);
    sol_used[j] = true;
    sol_key[j] = cur;
    sol_cnt[j]++;
    res += sol_dfs(t->left, cur, target);
    res += sol_dfs(t->right, cur, target);
    sol_cnt[j]--;
    return res;
}

int pathSum(struct TreeNode* root, int targetSum) {
    memset(sol_used, 0, sizeof(sol_used));
    memset(sol_cnt, 0, sizeof(sol_cnt));
    int j = sol_slot(0);
    sol_used[j] = true;
    sol_key[j] = 0;
    sol_cnt[j] = 1;
    return sol_dfs(root, 0, targetSum);
}
