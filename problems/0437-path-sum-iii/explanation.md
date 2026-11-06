# 437. 路径总和 III —— 小白详细题解

> 这道题把"数组里和为 k 的子数组"（第 560 题）搬到了树上。先用双重递归把题做对，再学**前缀和 + 哈希表 + 回溯**这个强力组合。

---

## 📖 第一步：先读懂题目

数一数树里有多少条**向下**的路径，结点值加起来正好等于 `targetSum`。路径可以从**任意结点**开始、在**任意结点**结束，但只能从父亲走到孩子。

示例 1，`targetSum = 8`：

```
          10
         /  \
        5    -3
       / \     \
      3   2    11
     / \   \
    3  -2   1
```

| 路径 | 和 |
|---|---|
| 5 → 3 | 8 ✓ |
| 5 → 2 → 1 | 8 ✓ |
| -3 → 11 | 8 ✓ |
| 10 → 5 → 3 | 18 ✗ |
| 10 → -3 | 7 ✗ |

答案 `3`。

**几个需要注意的细节：**

1. 路径不一定从根开始，也不一定到叶子结束；**单个结点**也算一条路径。
2. 结点值可达 ±10⁹，一条路径上可能有 1000 个结点，和可达 10¹²，**必须用 `long long`**。
3. 树可能为空，答案为 0。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. `long long` 防溢出

`int` 最大约 2.1×10⁹，两个 10⁹ 相加就溢出了。累加路径和的变量要声明为 `long long`；函数参数里的"剩余目标"也一样。

### 2. 静态数组实现简单哈希表

C 没有自带哈希表。思路二会用"开放寻址"实现一个：数组 `keys[]` 存键、`cnt[]` 存次数、`used[]` 标记是否占用；冲突时往后找下一个格子（与第 1 题的哈希表相同）。

### 3. 回溯

递归进入孩子前"做一件事"，从孩子返回后"撤销这件事"，保证兄弟子树看到的状态是干净的。

---

## 💡 第三步：思路一 —— 双重递归（以每个结点为起点）

### 思路

1. 写函数 `countFrom(node, remain)`：**从 `node` 出发向下**，有几条路径的和等于 `remain`。
   - `node` 为空返回 0；
   - 如果 `node->val == remain`，计 1 条（路径在这里结束）；
   - 再加上 `countFrom(左孩子, remain - val)` 和 `countFrom(右孩子, remain - val)`（路径继续往下）。
2. 主函数：答案 = `countFrom(root, target)` + 对左子树、右子树**递归地**做同样的事（换一个起点）。

### 代码

```c
// 从 node 出发向下、和恰好为 remain 的路径数
int countFrom(struct TreeNode* node, long long remain) {
    if (node == NULL) return 0;
    int res = 0;
    if (node->val == remain) res++;                        // 路径在 node 结束
    res += countFrom(node->left, remain - node->val);     // 路径继续往左下走
    res += countFrom(node->right, remain - node->val);    // 路径继续往右下走
    return res;
}

int pathSum(struct TreeNode* root, int targetSum) {
    if (root == NULL) return 0;
    return countFrom(root, targetSum)                      // 以 root 为起点
         + pathSum(root->left, targetSum)                  // 起点在左子树里
         + pathSum(root->right, targetSum);                // 起点在右子树里
}
```

> 💬 `remain` 用 `long long`：`remain - node->val` 可能是 `1000 - (-10^9)`，继续往下减会超出 `int`。

### 复杂度分析

- **时间复杂度 O(n²)**（最坏，链状树）：每个结点作为起点都要往下走一遍。n = 1000 时约 50 万次，能过。
- **空间复杂度 O(h)**：递归栈。

---

## 🚀 第四步：思路二 —— 前缀和 + 哈希表 + 回溯（O(n)）

### 思路

记 `cur` = 从根到当前结点的路径和（前缀和）。对于当前结点上方的某个祖先 `A`，从根到 `A` 的前缀和为 `pre`，那么"从 `A` 的下一个结点到当前结点"这段路径的和就是 `cur - pre`。

> 要让这段和等于 `target`，就需要 `pre == cur - target`。

所以：用哈希表记录**当前这条根到结点的路径上**，每个前缀和出现了几次。到达一个结点时，查一下 `cur - target` 出现了几次，就是以当前结点结尾的合法路径数。

两个要点：

1. 一开始放入前缀和 `0`，出现 1 次（表示"从根开始的路径"）。
2. **回溯**：离开一个结点时，要把它的前缀和次数减 1，因为兄弟子树里的结点不能把它当祖先。

### 手动模拟（示例 1 的一条路径 10 → 5 → 3 → 3，target = 8）

| 结点 | cur | 查 cur - 8 | 次数 | 表中内容（访问后） |
|---|---|---|---|---|
| 10 | 10 | 2 | 0 | {0:1, 10:1} |
| 5 | 15 | 7 | 0 | {0:1, 10:1, 15:1} |
| 3 | 18 | **10** | **1**（路径 5→3） | {…, 18:1} |
| 3 | 21 | 13 | 0 | {…, 21:1} |

### 代码

```c
#define HS 4096                       // 哈希表格子数（2 的幂，远大于结点数 1000）
static long long keys[HS];            // 前缀和
static int cnt[HS];                   // 这个前缀和在当前路径上出现的次数
static bool used[HS];                 // 格子是否被占用

// 找到 key 所在的格子；如果不存在，返回它应该放进去的空格子
int slot(long long key) {
    unsigned long long h = (unsigned long long)key * 11400714819323198485ULL;
    int i = (int)(h >> 52);                              // 取高 12 位作为格子号（0 ~ 4095）
    while (used[i] && keys[i] != key) i = (i + 1) & (HS - 1);   // 被占了就看下一格
    return i;
}

int dfs(struct TreeNode* node, long long cur, long long target) {
    if (node == NULL) return 0;
    cur += node->val;                                    // 根到当前结点的前缀和

    int i = slot(cur - target);                          // 有几个祖先的前缀和是 cur - target
    int res = used[i] ? cnt[i] : 0;

    int j = slot(cur);                                   // 把当前前缀和加入表
    used[j] = true;
    keys[j] = cur;
    cnt[j]++;

    res += dfs(node->left, cur, target);
    res += dfs(node->right, cur, target);

    cnt[j]--;                                            // 回溯：离开当前结点，撤销
    return res;
}

int pathSum(struct TreeNode* root, int targetSum) {
    memset(used, 0, sizeof(used));                       // 每次调用都要清空
    memset(cnt, 0, sizeof(cnt));
    int j = slot(0);                                     // 前缀和 0 出现 1 次
    used[j] = true;
    keys[j] = 0;
    cnt[j] = 1;
    return dfs(root, 0, targetSum);
}
```

> 💬 回溯时只把次数减 1，不把格子标记为"空"：如果真的清空格子，线性探测链会断开，后面的键就找不到了。次数为 0 的格子留着不影响结果。

### 复杂度分析

- **时间复杂度 O(n)**：每个结点做常数次哈希操作。
- **空间复杂度 O(n)**：哈希表 + 递归栈。

---

## ⚠️ 第五步：小白常见错误

1. **用 `int` 累加路径和**：`[1000000000,1000000000,null,294967296,null,1000000000,null,1000000000,null,1000000000]`、`target = 0` 时，`int` 溢出后会"凑出" 0，得到错误答案。
2. **找到一条就停**：`if (node->val == remain) return 1;` 后面还可能有更长的路径（例如中间有 0 或正负抵消），不能提前返回。
3. **只从根出发**：只调用 `countFrom(root, target)`，漏掉了不从根开始的路径。
4. **忘记回溯**：思路二不写 `cnt[j]--`，右子树会把左子树里的结点当成祖先，多数了路径。
5. **忘了放入前缀和 0**：从根开始的路径（例如示例 2 的 `5→4→11→2`）就数不到了。
6. **哈希表不清空**：`static` 数组在多次调用之间会保留上一次的数据。

---

## 📊 第六步：方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| 双重递归 | O(n²) | O(h) | ⭐⭐ | 先写这个，思路直接 |
| 前缀和 + 哈希 + 回溯 | O(n) | O(n) | ⭐⭐⭐ | 最优解，面试加分 |

---

## 🔗 举一反三

- **112. 路径总和**：是否存在从根到叶子、和为 target 的路径。
- **113. 路径总和 II**：输出所有根到叶子的路径。
- **560. 和为 K 的子数组**：本题思路二在数组上的版本。
- **思考题**：如果路径可以"拐弯"（先上后下，像第 124 题那样），还能用前缀和吗？
