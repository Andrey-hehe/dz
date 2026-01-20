import sys


def solve(n: int, m: int, c: list, edges: list) -> int:  # 1
    graph = []  # 2
    for _ in range(n):  # 2
        graph.append([])  # 3
    for x, y in edges:  # 4
        x -= 1  # 5
        y -= 1  # 5
        graph[x].append(y)  # 5
        graph[y].append(x)  # 5
    o = 0  # 6
    stack = [(0, -1, c[0])]  # 6
    while stack:  # 7
        v, pr, k = stack.pop()  # 8
        if k > m:  # 8
            continue  # 9
        is_leaf = True  # 10
        for neighbor in graph[v]:  # 10
            if neighbor != pr:  # 11
                is_leaf = False  # 12
                next_k = k * c[neighbor] + c[neighbor]  # 12
                stack.append((neighbor, v, next_k))  # 12
        if is_leaf and v != 0:  # 13
            o += 1  # 14
    return o  # 15


if __name__ == "__main__":
    # Для быстрого ввода больших данных
    data = sys.stdin.read().split()

    n = int(data[0])
    m = int(data[1])

    # Чтение массива котов
    c = list(map(int, data[2 : 2 + n]))

    # Чтение ребер
    edges = []
    idx = 2 + n
    for i in range(n - 1):
        x = int(data[idx])
        y = int(data[idx + 1])
        edges.append((x, y))
        idx += 2

    result = solve(n, m, c, edges)
    print(result)
