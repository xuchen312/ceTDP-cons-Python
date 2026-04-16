import argparse
import os
import csv
import math
from functools import lru_cache
from math import floor, log

# =========================================================
# 1. base math
# =========================================================

def k1dfloorpowfix(d, k):
    p = int(floor(k ** (1 / d)))
    if (p + 1) ** d == k:
        return p + 1
    return p


def l_val(d, k):
    k1d = k1dfloorpowfix(d, k)

    if k == k1d ** d:
        return 0

    return int(floor(
        (log(k) - d * log(k1d)) /
        (log(k1d + 1) - log(k1d))
    ))


def b(d, k):
    k1d = k1dfloorpowfix(d, k)
    ldk = l_val(d, k)
    return (k1d ** (d - ldk)) * ((k1d + 1) ** ldk)


def bplus(d, k):
    k1d = k1dfloorpowfix(d, k)
    ldk = l_val(d, k)
    return ((k1d + 1) ** (d - ldk)) * ((k1d + 2) ** ldk)


# =========================================================
# 2. f(d,k)
# =========================================================

@lru_cache(None)
def f(d, k):
    if d <= 0 or k <= 0:
        return 0
    return bplus(d, k) + f(d - 1, k - b(d, k))


# =========================================================
# 3. RK
# =========================================================

def rk_value(k, d=3):
    fdks = [0] * (k + 1)

    for j in range(1, k + 1):
        fdks[j] = f(d, j)

    best = float("inf")

    for j in range(1, k + 1):
        fj = fdks[j]
        val = (fj - j) / fj
        if val < best:
            best = val

    return best


# =========================================================
# 4. CL
# =========================================================

def load_CL(path):
    xs, ys, zs = [], [], []

    with open(path, "r") as f:
        next(f, None)  # skip header

        for line in f:
            line = line.strip()
            if not line:
                continue

            # split flexible (CSV / TSV / space mixed)
            parts = line.replace(",", " ").split()

            nums = []
            for p in parts:
                try:
                    nums.append(float(p))
                except:
                    continue

            # CHECK: keep row if at least 3 numeric entries exist
            if len(nums) < 3:
                continue

            xs.append(int(nums[0]))
            ys.append(int(nums[1]))
            zs.append(int(nums[2]))

    return [xs, ys, zs]


# =========================================================
# 5. CL encoding
# =========================================================

def encode(x, y, z, rx, ry):
    return x + rx * y + rx * ry * z


def decode_neighbors(rx, ry):
    nx = (0,1,0,0,1,1,0,1)
    ny = (0,0,1,0,1,0,1,1)
    nz = (0,0,0,1,0,1,1,1)

    return [nx[i] + rx * ny[i] + rx * ry * nz[i] for i in range(8)]


# =========================================================
# 6. CL OPERATIONS
# =========================================================

def CLplus(CL, neighbors):
    out = set()
    add = out.add
    for v in CL:
        for n in neighbors:
            add(v + n)
    return out


def CLmin(CL, neighbors):
    CLp = CLplus(CL, neighbors)
    CLrest = CLp - CL

    remove = set()
    for v in CLrest:
        for n in neighbors:
            remove.add(v - n)

    return CL - remove


def CLprune(CL, i, neighbors):
    for _ in range(i):
        CL = CLmin(CL, neighbors)
    for _ in range(i):
        CL = CLplus(CL, neighbors)
    return CL


# =========================================================
# 7. LOWER BOUND
# =========================================================

def lower_bound3(CL_df, rk, k):

    x, y, z = CL_df

    # R exact range logic
    rx = max(x) - min(x) + 3
    ry = max(y) - min(y) + 3

    CL = [encode(xi, yi, zi, rx, ry) for xi, yi, zi in zip(x, y, z)]
    neighbors = decode_neighbors(rx, ry)

    n = len(CL)
    if n == 0:
        return 0

    if k >= n:
        return 0

    max_i = int(n ** (1 / 3))

    sV = float(len(CL) > k)

    CL_set = set(CL)

    for i in range(max_i + 1):

        pruned = CLprune(CL_set, i, neighbors)
        pruned_plus = CLplus(pruned, neighbors)

        rest = pruned_plus - pruned

        score = rk * len(pruned_plus) - len(rest)

        if score > sV:
            sV = score

    return math.ceil(sV)


# =========================================================
# 8. FILE HANDLING
# =========================================================

def collect_files(path):
    if os.path.isfile(path):
        return [path]

    return sorted(
        os.path.join(path, f)
        for f in os.listdir(path)
        if f.lower().endswith((".csv", ".tsv"))
    )


def run_one(file_path, k):
    df = load_CL(file_path)
    
    if len(df[0]) == 0:
        return file_path, 0, 0, 0

    rk = rk_value(k, 3)

    tdn = lower_bound3(df, rk, k)
    size = len(df[0])
    tdp = tdn / size if size > 0 else 0

    return file_path, size, tdn, tdp


# =========================================================
# 9. CLI
# =========================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", type=int, required=True)
    parser.add_argument("path")
    parser.add_argument("-o", "--output", default=None)
    args = parser.parse_args()

    files = collect_files(args.path)

    print(f"{'file':<30} {'size':<10} {'TDN':<10} {'TDP':<10}")

    results = []

    for f in files:
        file_path, size, tdn, tdp = run_one(f, args.k)
        #results.append([file_path, size, tdn, tdp])
        #print(f"{file_path:<30} {size:<10} {tdn:<10} {tdp:<10.6f}")
        results.append([os.path.basename(file_path), size, tdn, tdp])
        print(f"{os.path.basename(file_path):<30} {size:<10} {tdn:<10} {tdp:<10.6f}")

    if args.output:
        out = args.output
        if not out.endswith(".csv"):
            out += ".csv"

        with open(out, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["file", "size", "TDN", "TDP"])
            writer.writerows(results)

        print("Results saved to:", out)


if __name__ == "__main__":
    main()
