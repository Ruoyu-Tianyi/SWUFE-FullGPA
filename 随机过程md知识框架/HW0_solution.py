"""
Optimization Theory and Applications - Assignment 0
Complete solution with mathematical model and Python implementation.

Problem 1 (Mandatory): Advertising Optimization LP
Problem 2 (Optional): Currency Exchange LP Formulation
"""

import numpy as np
from scipy.optimize import linprog


# ============================================================================
# PROBLEM 1: ADVERTISING OPTIMIZATION
# ============================================================================
# A department store needs to decide how many ads to purchase on TV, Newspaper,
# and Radio to minimize total cost while satisfying several advertising policies.

def solve_problem1():
    """
    Problem 1: Advertising Optimization

    Decision Variables:
        x1 : number of TV commercials
        x2 : number of newspaper ads
        x3 : number of radio commercials

    Objective Function:
        Minimize Z = 15000*x1 + 4000*x2 + 6000*x3

    Subject to:
        (a) Radio >= 2 * Newspaper:
            -2*x2 + x3 >= 0

        (b) Reach at least 100,000 customers:
            25000*x1 + 10000*x2 + 15000*x3 >= 100000

        (c) Reach at least twice as many young as senior:
            -5000*x1 - 11000*x2 + 6000*x3 >= 0
            (Derived: Young = 15000*x1 + 3000*x2 + 12000*x3,
                      Senior = 10000*x1 + 7000*x2 + 3000*x3)

        (d) At least 60% of audience is female:
            x2 <= 0
            (Derived: Female = 15000*x1 + 4000*x2 + 9000*x3,
                      Total  = 25000*x1 + 10000*x2 + 15000*x3,
                      0.6*Total = 15000*x1 + 6000*x2 + 9000*x3,
                      Female >= 0.6*Total  =>  -2000*x2 >= 0)

        (e) Newspaper ads limit:
            x2 <= 7

        (f) Non-negativity:
            x1, x2, x3 >= 0
    """
    print("=" * 70)
    print("PROBLEM 1: ADVERTISING OPTIMIZATION")
    print("=" * 70)

    # Objective: Minimize 15000*x1 + 4000*x2 + 6000*x3
    c = [15000, 4000, 6000]

    # Inequality constraints A_ub @ x <= b_ub
    A_ub = [
        # (a) 2*x2 - x3 <= 0   [from -2*x2 + x3 >= 0]
        [0, 2, -1],
        # (b) -25000*x1 - 10000*x2 - 15000*x3 <= -100000  [from >= 100000]
        [-25000, -10000, -15000],
        # (c) 5000*x1 + 11000*x2 - 6000*x3 <= 0  [from >= 0]
        [5000, 11000, -6000],
        # (d) -x2 <= 0  [from x2 >= 0, combined with (d) forces x2 = 0]
        [0, -1, 0],
        # (e) x2 <= 7
        [0, 1, 0],
    ]
    b_ub = [0, -100000, 0, 0, 7]

    # Bounds: x1, x2, x3 >= 0
    bounds = [(0, None), (0, None), (0, None)]

    # Solve using HiGHS method
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

    if not result.success:
        print("Optimization failed:", result.message)
        return None

    x1, x2, x3 = result.x
    min_cost = result.fun

    print(f"\n>>> OPTIMAL SOLUTION <<<")
    print(f"  TV commercials      (x1) = {x1:.6f}")
    print(f"  Newspaper ads       (x2) = {x2:.6f}")
    print(f"  Radio commercials   (x3) = {x3:.6f}")
    print(f"  Minimum Total Cost       = ${min_cost:,.2f}")

    # Verification
    print(f"\n--- Constraint Verification ---")

    # (a) Radio >= 2 * Newspaper
    lhs_a = x3
    rhs_a = 2 * x2
    print(f"  (a) Radio >= 2*Newspaper: {lhs_a:.4f} >= {rhs_a:.4f}  [{'PASS' if lhs_a >= rhs_a - 1e-6 else 'FAIL'}]")

    # (b) Total reach >= 100,000
    total_reach = 25000*x1 + 10000*x2 + 15000*x3
    print(f"  (b) Reach >= 100,000: {total_reach:,.2f} >= 100,000  [{'PASS' if total_reach >= 100000 - 1e-6 else 'FAIL'}]")

    # (c) Young >= 2 * Senior
    young = 15000*x1 + 3000*x2 + 12000*x3
    senior = 10000*x1 + 7000*x2 + 3000*x3
    print(f"  (c) Young >= 2*Senior: {young:,.2f} >= {2*senior:,.2f}  [{'PASS' if young >= 2*senior - 1e-6 else 'FAIL'}]")

    # (d) Female >= 60% of total
    female = 15000*x1 + 4000*x2 + 9000*x3
    print(f"  (d) Female >= 60%: {female:,.2f} / {total_reach:,.2f} = {female/total_reach:.4f} >= 0.60  [{'PASS' if female/total_reach >= 0.6 - 1e-6 else 'FAIL'}]")

    # (e) Newspaper <= 7
    print(f"  (e) Newspaper <= 7: {x2:.4f} <= 7  [{'PASS' if x2 <= 7 + 1e-6 else 'FAIL'}]")

    # Audience breakdown
    print(f"\n--- Audience Breakdown ---")
    print(f"  Senior Male   : {5000*x1 + 4000*x2 + 1500*x3:,.2f}")
    print(f"  Senior Female : {5000*x1 + 3000*x2 + 1500*x3:,.2f}")
    print(f"  Young Male    : {5000*x1 + 2000*x2 + 4500*x3:,.2f}")
    print(f"  Young Female  : {10000*x1 + 1000*x2 + 7500*x3:,.2f}")
    print(f"  Total         : {total_reach:,.2f}")

    return result


# ============================================================================
# PROBLEM 2: CURRENCY EXCHANGE LP (Optional)
# ============================================================================
# Given N currencies with exchange rates r_ij and daily limits u_i,
# maximize the final amount of currency N starting from B_1 units of currency 1.

def formulate_problem2():
    """
    Problem 2: Currency Exchange Linear Programming Formulation

    Decision Variables:
        x_{ij} >= 0 : amount of currency i exchanged into currency j
                      for all i, j in {1, 2, ..., N}

    Objective Function:
        Maximize W_N = B_N + sum_{i=1}^{N} r_{iN} * x_{iN} - sum_{j=1}^{N} x_{Nj}

        Since we start with B_1 > 0 and B_i = 0 for i >= 2, and we would never
        exchange currency N away (as it would decrease the final amount),
        the objective simplifies to:

        Maximize Z = sum_{i=1}^{N-1} r_{iN} * x_{iN}

    Subject to:
        (1) Flow conservation (cannot exchange more than available):
            For each currency i = 1, ..., N:
            sum_{j=1}^{N} x_{ij} <= B_i + sum_{k=1}^{N} r_{ki} * x_{ki}

        (2) Daily exchange limit:
            For each currency i = 1, ..., N:
            sum_{j=1}^{N} x_{ij} <= u_i

        (3) Non-negativity:
            x_{ij} >= 0 for all i, j = 1, ..., N

    Note: The no-arbitrage condition r_{i1,i2} * r_{i2,i3} * ... * r_{ik,i1} <= 1
    ensures that no unlimited profit can be made through currency cycles,
    which guarantees the LP has a finite optimal solution.
    """
    print("\n" + "=" * 70)
    print("PROBLEM 2: CURRENCY EXCHANGE LP (Optional - Formulation)")
    print("=" * 70)

    print("""
    DECISION VARIABLES:
        x_{ij} >= 0  for all i, j in {{1, 2, ..., N}}
        (amount of currency i exchanged into currency j)

    OBJECTIVE FUNCTION:
        Maximize Z = sum_{{i=1}}^{{N-1}} r_{{iN}} * x_{{iN}}

    SUBJECT TO:
        (1) Balance constraint for each currency i:
            sum_{{j=1}}^{{N}} x_{{ij}} <= B_i + sum_{{k=1}}^{{N}} r_{{ki}} * x_{{ki}}

        (2) Daily limit constraint for each currency i:
            sum_{{j=1}}^{{N}} x_{{ij}} <= u_i

        (3) Non-negativity:
            x_{{ij}} >= 0,  for all i, j in {{1, ..., N}}
    """)


def solve_problem2_example():
    """
    Solve a small example of Problem 2 with N=3 currencies to demonstrate
    the formulation works correctly.

    Example:
        N = 3 currencies
        r = [[1.0, 0.8, 0.5],   # 1 unit of cur 1 -> 0.8 cur 2, 0.5 cur 3
             [1.2, 1.0, 0.6],   # 1 unit of cur 2 -> 1.2 cur 1, 0.6 cur 3
             [1.8, 1.5, 1.0]]   # 1 unit of cur 3 -> 1.8 cur 1, 1.5 cur 2
        u = [100, 100, 100]       # daily limits
        B = [100, 0, 0]           # start with 100 units of currency 1
    """
    print("\n--- Problem 2: Small Example (N=3) ---")

    N = 3
    # Exchange rates: r[i][j] = units of j obtained from 1 unit of i
    r = np.array([
        [1.0, 0.8, 0.5],   # from currency 1
        [1.2, 1.0, 0.6],   # from currency 2
        [1.8, 1.5, 1.0],   # from currency 3
    ])
    u = np.array([100, 100, 100])  # daily limits
    B = np.array([100, 0, 0])       # initial holdings

    # Variables: x_ij for all i,j
    # We need N*N variables. Let variable index be: idx = i*N + j
    # Objective: maximize sum_i r[i][N-1] * x[i][N-1] - sum_j x[N-1][j]
    # Since we want to maximize, we negate for linprog (which minimizes)

    # Objective coefficients
    c = np.zeros(N * N)
    for i in range(N):
        for j in range(N):
            idx = i * N + j
            if j == N - 1:  # incoming to N
                c[idx] = -r[i][j]  # negate for maximization
            if i == N - 1:  # outgoing from N
                c[idx] += 1.0  # subtract outgoing

    # Constraints:
    # (1) Balance: for each currency i
    #     sum_j x_ij - sum_k r_ki * x_ki <= B_i
    A_balance = []
    b_balance = []
    for i in range(N):
        row = np.zeros(N * N)
        # Outgoing from i
        for j in range(N):
            row[i * N + j] += 1
        # Incoming to i (subtracted)
        for k in range(N):
            row[k * N + i] -= r[k][i]
        A_balance.append(row)
        b_balance.append(B[i])

    # (2) Daily limit: for each currency i
    #     sum_j x_ij <= u_i
    A_limit = []
    b_limit = []
    for i in range(N):
        row = np.zeros(N * N)
        for j in range(N):
            row[i * N + j] = 1
        A_limit.append(row)
        b_limit.append(u[i])

    A_ub = np.vstack([A_balance, A_limit])
    b_ub = np.hstack([b_balance, b_limit])

    # Bounds: x_ij >= 0
    bounds = [(0, None)] * (N * N)

    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

    if result.success:
        x = result.x.reshape(N, N)
        final_amount = -result.fun
        print(f"Optimal final amount of currency {N}: {final_amount:.4f}")
        print(f"Exchange matrix x[i][j] (amount of i -> j):")
        print(np.round(x, 4))
        print(f"\nVerification:")
        for i in range(N):
            outflow = sum(x[i][j] for j in range(N))
            inflow = sum(r[k][i] * x[k][i] for k in range(N))
            available = B[i] + inflow
            print(f"  Currency {i+1}: out={outflow:.4f}, available={available:.4f}, limit={u[i]}, "
                  f"out<=avail: {outflow <= available + 1e-6}, out<=limit: {outflow <= u[i] + 1e-6}")
    else:
        print("Optimization failed:", result.message)


if __name__ == "__main__":
    # Run Problem 1
    solve_problem1()

    # Run Problem 2 formulation
    formulate_problem2()

    # Run Problem 2 small example
    solve_problem2_example()
