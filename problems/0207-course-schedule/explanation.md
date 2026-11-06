# 207. 课程表 —— 小白详细题解

> 这是「图」的入门题。核心问题只有一个：**有向图里有没有环？** 会用到两种经典算法：DFS 判环和拓扑排序（BFS）。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 有 `numCourses` 门课，有些课有先修要求：`[a, b]` 表示「想学 a，必须先学完 b」。问：能不能把所有课都学完？

把每门课画成一个点，`[a, b]` 画成一条箭头 **b → a**（先 b 后 a）：

| 示例 | 先修关系 | 画出来 | 能学完吗 |
|---|---|---|---|
| 示例 1 | `[[1,0]]` | 0 → 1 | ✅ 先学 0 再学 1 |
| 示例 2 | `[[1,0],[0,1]]` | 0 → 1 → 0（绕了一圈） | ❌ 互相等待 |

**关键结论：** 只要箭头绕成一个**圈（环）**，圈上的课谁都没法先学，就学不完；没有环就一定能学完。

**几个需要注意的细节：**

1. 先修关系可能为空（`[]`），这时所有课都能直接学，返回 `true`。
2. 图可能不连通，分成好几块，每一块都要检查。
3. `[a, b]` 的方向别搞反：是 **b 指向 a**。（其实本题只判断有没有环，方向整体反过来答案也一样，但下一题 210 要输出顺序时就不一样了。）

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 用「邻接表」存图

对每门课 `u`，记录「学完 u 之后可以解锁哪些课」。C 语言没有动态数组，我们分两步：

```c
int* outCnt = (int*)calloc(n, sizeof(int));     // 第 1 遍：数一数每个点有几条出边
for (int i = 0; i < m; i++) outCnt[prerequisites[i][1]]++;

int** adj = (int**)malloc(sizeof(int*) * n);    // 第 2 遍：按数量给每个点申请空间，再填进去
for (int u = 0; u < n; u++) adj[u] = (int*)malloc(sizeof(int) * (outCnt[u] + 1));
```

### 2. `calloc` 和 `malloc` 的区别

`calloc(个数, 每个大小)` 会把内存**全部清零**，`malloc` 不会（里面是随机垃圾值）。计数数组一定要从 0 开始，所以用 `calloc` 最省心。

### 3. 用完要 `free`

本题申请了好几块内存，函数结束前记得释放。`adj` 是「数组的数组」，要先释放每一行，再释放 `adj` 本身。

---

## 💡 第三步：思路一 —— DFS 三色标记判环

### 思路

给每个点一个颜色：

| 颜色 | 含义 |
|---|---|
| 0（白） | 还没访问过 |
| 1（灰） | **正在访问**：它在当前这条 DFS 路径上 |
| 2（黑） | 已经访问完，从它出发不会有环 |

从一个点出发 DFS，沿着箭头走：

- 走到**灰色**的点 → 说明绕回了当前路径上的点，**有环**！
- 走到**黑色**的点 → 之前检查过了，安全，跳过。
- 一个点的所有出边都走完了 → 把它染成黑色。

### 手动模拟（示例 2：0 → 1，1 → 0）

| 步骤 | 操作 | color[0] | color[1] |
|---|---|---|---|
| 1 | 从 0 出发，0 染灰 | 1 | 0 |
| 2 | 沿 0 → 1，1 染灰 | 1 | 1 |
| 3 | 沿 1 → 0，0 是**灰色** | 1 | 1 |
| 4 | 发现环，返回 `false` | | |

### 代码

```c
// 从 u 出发 DFS，发现环返回 true
bool hasCycle(int u, int** adj, int* outCnt, int* color) {
    color[u] = 1;                                // 染灰：u 在当前路径上
    for (int k = 0; k < outCnt[u]; k++) {
        int v = adj[u][k];
        if (color[v] == 1) return true;          // 遇到灰色：绕回来了，有环
        if (color[v] == 0 && hasCycle(v, adj, outCnt, color)) return true;
        // color[v] == 2：已经确认安全，跳过
    }
    color[u] = 2;                                // 染黑：从 u 出发没有环
    return false;
}

bool canFinish(int numCourses, int** prerequisites, int prerequisitesSize, int* prerequisitesColSize) {
    int n = numCourses, m = prerequisitesSize;

    // 1. 建邻接表：b -> a
    int* outCnt = (int*)calloc(n, sizeof(int));
    for (int i = 0; i < m; i++) outCnt[prerequisites[i][1]]++;
    int** adj = (int**)malloc(sizeof(int*) * n);
    for (int u = 0; u < n; u++) adj[u] = (int*)malloc(sizeof(int) * (outCnt[u] + 1));
    int* fill = (int*)calloc(n, sizeof(int));    // 每个点已经填了几条边
    for (int i = 0; i < m; i++) {
        int a = prerequisites[i][0], b = prerequisites[i][1];
        adj[b][fill[b]++] = a;
    }

    // 2. 每个还没访问的点都出发一次（图可能不连通）
    int* color = (int*)calloc(n, sizeof(int));
    bool ok = true;
    for (int u = 0; u < n && ok; u++) {
        if (color[u] == 0 && hasCycle(u, adj, outCnt, color)) ok = false;
    }

    // 3. 释放内存
    for (int u = 0; u < n; u++) free(adj[u]);
    free(adj); free(outCnt); free(fill); free(color);
    return ok;
}
```

### 复杂度分析

- **时间复杂度 O(n + m)**：每个点、每条边各处理一次（n 是课程数，m 是先修关系数）。
- **空间复杂度 O(n + m)**：邻接表 + 递归栈。

> 💬 `outCnt[u] + 1`：多申请 1 个位置，避免出边数为 0 时 `malloc(0)` 的不确定行为。

---

## 🚀 第四步：思路二 —— 拓扑排序（Kahn 算法 / BFS）

### 思路

更贴近「排课」的直觉：

1. **入度** = 一门课还有几门先修课没学。入度为 0 的课可以马上学。
2. 把所有入度为 0 的课放进队列。
3. 每次从队列里取一门课「学掉」，计数 `+1`；它解锁的每门课入度 `-1`，减到 0 就入队。
4. 最后学掉的课数 == `numCourses` 就是 `true`。环上的课入度永远减不到 0，永远进不了队列。

### 手动模拟（`numCourses = 4`，`[[1,0],[2,0],[3,1],[3,2]]`，即 0→1、0→2、1→3、2→3）

| 步骤 | 出队（学掉） | 入度变化 | 队列 | 已学 |
|---|---|---|---|---|
| 初始 | — | 入度 = [0,1,1,2] | [0] | 0 |
| 1 | 0 | 1:1→0，2:1→0 | [1,2] | 1 |
| 2 | 1 | 3:2→1 | [2] | 2 |
| 3 | 2 | 3:1→0 | [3] | 3 |
| 4 | 3 | — | [] | 4 ✅ |

### 代码

```c
bool canFinish(int numCourses, int** prerequisites, int prerequisitesSize, int* prerequisitesColSize) {
    int n = numCourses, m = prerequisitesSize;

    // 1. 建邻接表 b -> a，同时统计入度
    int* outCnt = (int*)calloc(n, sizeof(int));
    int* indeg = (int*)calloc(n, sizeof(int));
    for (int i = 0; i < m; i++) {
        outCnt[prerequisites[i][1]]++;
        indeg[prerequisites[i][0]]++;            // a 多了一门先修课
    }
    int** adj = (int**)malloc(sizeof(int*) * n);
    for (int u = 0; u < n; u++) adj[u] = (int*)malloc(sizeof(int) * (outCnt[u] + 1));
    int* fill = (int*)calloc(n, sizeof(int));
    for (int i = 0; i < m; i++) {
        int a = prerequisites[i][0], b = prerequisites[i][1];
        adj[b][fill[b]++] = a;
    }

    // 2. 入度为 0 的课先入队
    int* queue = (int*)malloc(sizeof(int) * n);  // 每门课最多入队一次
    int head = 0, tail = 0;
    for (int u = 0; u < n; u++)
        if (indeg[u] == 0) queue[tail++] = u;

    // 3. BFS：学掉一门课，解锁它的后续课程
    int learned = 0;
    while (head < tail) {
        int u = queue[head++];
        learned++;
        for (int k = 0; k < outCnt[u]; k++) {
            int v = adj[u][k];
            indeg[v]--;
            if (indeg[v] == 0) queue[tail++] = v;  // 先修课全学完了，可以学 v 了
        }
    }

    // 4. 释放内存
    for (int u = 0; u < n; u++) free(adj[u]);
    free(adj); free(outCnt); free(indeg); free(fill); free(queue);
    return learned == n;
}
```

### 复杂度分析

- **时间复杂度 O(n + m)**。
- **空间复杂度 O(n + m)**，而且没有递归，不用担心栈溢出。

---

## ⚠️ 第五步：小白常见错误

1. **只用「访问过 / 没访问过」两种状态做 DFS**：遇到「访问过」就判有环是错的。例如 0→1、0→2、1→2，从 0 出发先走完 1→2，再走 0→2 时 2 已访问过，但这并不是环。必须区分「正在访问（灰）」和「访问完毕（黑）」。
2. **只从 0 号点出发**：图可能不连通，例如 `numCourses = 4`，环在 2、3 之间，只从 0 出发就发现不了。
3. **计数数组用 `malloc` 没清零**：`indeg`、`outCnt` 里是垃圾值，结果随机出错。用 `calloc` 或 `memset`。
4. **用 `n*n` 的邻接矩阵还每次扫描整行**：n = 2000 时矩阵有 400 万格，BFS 每出队一个点扫 2000 格，虽然本题能过，但思路上不是 O(n + m)，边稀疏的大图会超时。
5. **`prerequisitesSize == 0` 时出错**：比如写 `prerequisitesColSize[0]` 就会越界。本题根本不需要用 `prerequisitesColSize`（每行固定是 2）。

---

## 📊 第六步：两种方法对比

| 方法 | 时间复杂度 | 空间复杂度 | 难度 | 建议 |
|---|---|---|---|---|
| DFS 三色判环 | O(n + m) | O(n + m)（含递归栈） | ⭐⭐⭐ | 理解「环」的本质 |
| 拓扑排序 BFS | O(n + m) | O(n + m) | ⭐⭐ | 最常用，还能直接输出学习顺序 |

> 🎯 **学习建议**：两种都要会。拓扑排序更直观，也是 210 题的直接答案。

---

## 🔗 举一反三

- **210. 课程表 II**：把拓扑排序时的出队顺序记下来，就是一种可行的学习顺序。
- **802. 找到最终的安全状态**：三色标记法的直接应用。
- **思考题**：如果要求「每学期最多学 k 门课」，最少需要几个学期？
