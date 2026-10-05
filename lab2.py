import random, statistics, time
def generate_data(n, lo=0.0, hi=1.0, seed=42):
    rng = random.Random(seed + n)
    return [rng.uniform(lo, hi) for _ in range(n)]

def measure(sort_func, data, repeats=3):
    times, comps = [], []
    for _ in range(repeats):
        start = time.perf_counter()
        result, cmp_cnt = sort_func(data)
        times.append(time.perf_counter() - start)
        comps.append(cmp_cnt)
        assert result == sorted(data), f"{sort_func.__name__}: ошибка!"
    return statistics.median(times), int(statistics.median(comps))
"""ЛР2, вариант 7: R, вещественные [0;1), М6 (вставки с бинарным поиском)."""
from sorts_common import generate_data, measure
def bubble_sort(arr):
    a, n, cmp_cnt = arr.copy(), len(arr), 0
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            cmp_cnt += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a, cmp_cnt
def insertion_sort(arr):
    a, cmp_cnt = arr.copy(), 0
    for i in range(1, len(a)):
        key, j = a[i], i - 1
        while j >= 0:
            cmp_cnt += 1
            if a[j] > key:
                a[j + 1], j = a[j], j - 1
            else:
                break
        a[j + 1] = key
    return a, cmp_cnt
def _upper_bound(a, key, lo, hi):
    c = 0
    while lo < hi:
        mid = (lo + hi) // 2
        c += 1
        if a[mid] <= key:
            lo = mid + 1
        else:
            hi = mid
    return lo, c
def binary_insertion_sort(arr):
    a = arr.copy()
    total = 0
    for i in range(1, len(a)):
        key = a[i]
        pos, c = _upper_bound(a, key, 0, i)
        total += c
        for j in range(i, pos, -1):
            a[j] = a[j - 1]
        a[pos] = key
    return a, total
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    SIZES, REPEATS = [1000, 1500, 2000, 2500, 3000], 3
    algos = {
        "bubble": bubble_sort,
        "insert": insertion_sort,
        "binary": binary_insertion_sort,
    }
    names = list(algos)
    print(f"{'n':>6}" + "".join(f"{n:>12}T  {n:>12}C" for n in names))
    print("-" * (6 + 25 * len(names)))
    times = {n: [] for n in names}
    comps = {n: [] for n in names}
    for size in SIZES:
        data = generate_data(size)
        row = f"{size:>6}"
        for name, func in algos.items():
            t, c = measure(func, data, REPEATS)
            times[name].append(t)
            comps[name].append(c)
            row += f"{t:>12.6f}  {c:>12d}"
        print(row)
    print("\nC(n)/n^2 (const для квадратичных, →0 для n log n):")
    for name in names:
        print(f"  {name:>7}: " + "  ".join(
            f"{c / s**2:.3f}" for c, s in zip(comps[name], SIZES)))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    for name in names:
        ax1.plot(SIZES, times[name], marker="o", label=name)
        ax2.plot(SIZES, [c / s**2 for c, s in zip(comps[name], SIZES)],
                 marker="s", label=name)
    ax1.set(xlabel="n", ylabel="Время, с", title="T(n)")
    ax2.set(xlabel="n", ylabel="C(n)/n²", title="Сравнения")
    for ax in (ax1, ax2):
        ax.grid(True); ax.legend()
    plt.tight_layout()
    plt.savefig("lr2_variant7.png", dpi=150)
    plt.show()