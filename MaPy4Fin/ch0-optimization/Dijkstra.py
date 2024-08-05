from heapq import heappop, heappush

def dijkstra(graph_dict, from_node, to_node):
    cost = -1
    ret_path = []
    T, P = [(0, from_node, ())], set()

    while T:
        # 从T中取出距离最近的节点
        (cost, v1, path) = heappop(T)
        # 如果最近节点不再P中, 加入P中
        if v1 not in P:
            P.add(v1)
            path = (v1, path)
            if v1 == to_node: # 到达终点
                break
            for v2, c in graph_dict.get(v1, ()).items():
                if v2 not in P:
                    heappush(T, (cost + c, v2, path))

    # 找到路径后进行格式化
    if len(path) > 0:
        left = path[0]
        ret_path.append(left)
        right = path[1]
        while len(right) > 0:
            left = right[0]
            ret_path.append(left)
            right = right[1]
        ret_path.reverse()

    return cost, ret_path

def main():
    # 使用字典存储图
    graph_dict = {
        'A': {'B': 12, 'G': 14, 'F': 16},
        'B': {'A': 12, 'C': 10, 'F': 7},
        'C': {'B': 10, 'D': 3, 'F': 6},
        'D': {'C': 3, 'E': 4},
        'E': {'D': 4, 'F': 2, 'G': 8},
        'F': {'B': 7, 'C': 6, 'E': 2, 'G': 9},
        'G': {'A': 16, 'F': 9, 'E': 8}
    }
    from_node = 'D'
    to_node = 'A'
    cost, ret_path = dijkstra(graph_dict, from_node, to_node)
    print(cost)
    print(ret_path) # D - C - B - A

if __name__ == '__main__':
    main()
