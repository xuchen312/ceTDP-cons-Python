import argparse
from functools import lru_cache
from math import floor, log

# =========================================================
# 1. base math functions
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
# 2. f(d,k) (memoized)
# =========================================================
@lru_cache(None)
def f(d, k):
    if d <= 0 or k <= 0:
        return 0
    return bplus(d, k) + f(d - 1, k - b(d, k))


# =========================================================
# 3. rk(k,3)
# =========================================================
@lru_cache(None)
def rk_value(k, d=3):
    best = float("inf")

    for j in range(1, k + 1):
        fj = f(d, j)
        val = (fj - j) / fj
        if val < best:
            best = val

    return best


# =========================================================
# 4. CL operations
# =========================================================

NEIGHBORS = (
    (0,0,0),
    (1,0,0), (0,1,0), (0,0,1),
    (1,1,0), (1,0,1), (0,1,1),
    (1,1,1)
)


def CLplus(CL):
    out = set()
    add = out.add

    for x, y, z in CL:
        x1, y1, z1 = x + 1, y + 1, z + 1

        add((x, y, z))
        add((x1, y, z))
        add((x, y1, z))
        add((x, y, z1))
        add((x1, y1, z))
        add((x1, y, z1))
        add((x, y1, z1))
        add((x1, y1, z1))

    return out


def CLmin(CL):
    CL = set(CL)
    CLp = CLplus(CL)
    CLrest = CLp - CL

    out = set()
    add = out.add

    for x, y, z in CL:
        keep = True
        for dx, dy, dz in NEIGHBORS:
            if (x + dx, y + dy, z + dz) in CLrest:
                keep = False
                break
        if keep:
            add((x, y, z))

    return out


def CLprune(CL, i):
    CL = set(CL)

    for _ in range(i):
        CL = CLmin(CL)

    for _ in range(i):
        CL = CLplus(CL)

    return CL


# =========================================================
# 5. lower bound
# =========================================================
def lower_bound3(CL, k):
    n = len(CL)

    # trivial case
    if k >= n:
        return 0

    rk = rk_value(k, 3)

    max_i = int(n ** (1 / 3))
    best = 0.0

    for i in range(max_i + 1):

        pruned = CLprune(CL, i)
        pruned_plus = CLplus(pruned)

        rest = pruned_plus - pruned

        # scale-stabilized score
        score = rk * len(pruned_plus) - len(rest)

        if score > best:
            best = score

    return int(best) + 1

# =========================================================
# 6. input loader (csv or tsv)
# =========================================================
def load_CL(path):
    CL = []

    with open(path, "r") as f:
        next(f)

        for line in f:
            line = line.strip()
            if not line:
                continue

            # supports TSV or CSV
            parts = line.replace(",", " ").split()

            if len(parts) < 3:
                continue

            CL.append((int(parts[0]), int(parts[1]), int(parts[2])))

    return CL

# =========================================================
# 7. CLI
# =========================================================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", type=int, required=True)
    parser.add_argument("file")

    args = parser.parse_args()

    CL = load_CL(args.file)

    print(lower_bound3(CL, args.k))

if __name__ == "__main__":
    main()
