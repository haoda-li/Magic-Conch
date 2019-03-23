import numpy as np
from scipy.special import comb
from itertools import combinations


def permutation_test(A, B, N=0, stats="mean", side=1):
    """ return None if error, 
        else return p-value, distribution, and observed difference
        A, B: two list-like data for the two groups
        N: number of sampling, 0 for all permutations
        stats: summary stats to test, choices of "mean", "median"
        side: 1 or 2 for one-sided or two-sided
    """
    A, B = np.array(A), np.array(B)
    num = comb(len(A) + len(B), len(A), exact=True) if N == 0 else N
    if stats == "mean":
        sample_stats = A.mean() - B.mean()
    elif stats == "median":
        sample_stats = A.median() - B.median()
    else:
        return -1
    
    rand_dist = np.zeros(num)
    
    pooled = np.array(np.concatenate((A, B)))
    if N == 0:
        ranging = range(len(A) + len(B))
        index = list(combinations(ranging, len(A)))
        for i in range(num):
            x1 = [pooled[j] for j in index[i]]
            x2 = [pooled[j] for j in a if j not in index[i]]
            rand_dist[i] = np.mean(x1)-np.mean(x2) if stats == "mean" else np.median(x1)-np.median(x2)
    
    if N != 0:
        for i in range(N):
            np.random.shuffle(pooled)
            pooled = list(pooled)
            x1 = pooled[:len(A)]
            x2 = pooled[len(A):]
            rand_dist[i] = np.mean(x1)-np.mean(x2) if stats == "mean" else np.median(x1)-np.median(x2)
    
    return {"p": sum(rand_dist > sample_stats) / len(rand_dist) if side == 1 else sum(abs(rand_dist) > abs(sample_stats)) / len(rand_dist),
            "distribution": rand_dist, 
            "ob": sample_stats}