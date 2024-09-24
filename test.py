def newton_cbrt(n, tolerance=1e-7, max_iterations=1000):
    x = n
    for _ in range(max_iterations):
        next_x = x - (x**3 - n) / (3 * x**2)
        if abs(next_x - x) < tolerance:
            return next_x
        x = next_x
    return x

n = float(input("请输入一个数: "))
cbrt_n = newton_cbrt(n)
print(f"{n} 的三次方根是 {cbrt_n}")