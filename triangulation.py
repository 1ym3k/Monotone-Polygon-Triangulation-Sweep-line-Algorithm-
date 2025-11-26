from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Point:
    """
    Represents a point on a 2D plane with integer coordinates.
    """
    x: int
    y: int

def orientation(p: Point, q: Point, r: Point) -> int:
    """
    Calculates the orientation of an ordered triplet of points (p, q, r) using the cross product.

    Args:
        p, q, r: Points to check.

    Returns:
        0: Points are collinear.
        1: Left turn (Counter-Clockwise).
        -1: Right turn (Clockwise).
    """
    val = (q.x - p.x) * (r.y - p.y) - (q.y - p.y) * (r.x - p.x)
    if val == 0: return 0
    return 1 if val > 0 else -1

def read_polygon(path: str) -> List[Point]:
    """
    Reads polygon vertex coordinates from a text file.
    
    File format:
    - First line: number of vertices n.
    - Next n lines: x y coordinate pairs.

    Args:
        path: Path to the input file.

    Returns:
        List of Point objects representing the polygon vertices.
    """
    with open(path) as f:
        lines = [line.strip() for line in f.readlines()]
    n = int(lines[0])
    return [Point(*map(int, line.split())) for line in lines[1:]]

def find_chains(points: List[Point]):
    """
    Classifies polygon vertices into the upper (UPPER) or lower (LOWER) chain.

    Returns:
        List of strings ("UPPER" or "LOWER") corresponding to point indices.
    """
    n = len(points)
    left = min(range(n), key=lambda i: points[i].x)
    right = max(range(n), key=lambda i: points[i].x)

    chain = [""] * n

    # UPPER: from left to right (CCW)
    i = left
    while True:
        chain[i] = "UPPER"
        if i == right: break
        i = (i + 1) % n

    # LOWER: from right to left (CCW)
    i = right
    while True:
        if i != left and i != right:
            chain[i] = "LOWER"
        if i == left: break
        i = (i + 1) % n

    return chain

def triangulate_x_monotone(points: List[Point]) -> List[Tuple[Point, Point]]:
    """
    Triangulates a strictly x-monotone polygon using a sweep-line algorithm.

    Args:
        points: List of polygon vertices in CCW order.

    Returns:
        List of point pairs (tuples) representing the added diagonals.
    """
    n = len(points)
    chain = find_chains(points)

    # Sort indices: first by x, then by -y (upper points first)
    order = sorted(range(n), key=lambda i: (points[i].x, -points[i].y))

    stack: List[int] = []
    diagonals: List[Tuple[Point, Point]] = []

    # First two points
    stack.append(order[0])
    stack.append(order[1])

    # Loop runs to n-1 (excluding the last point)
    for i in range(2, n - 1):
        cur_idx = order[i]
        top_idx = stack[-1]

        if chain[cur_idx] != chain[top_idx]:
            # Chain change
            while len(stack) > 1:
                v = stack.pop()
                diagonals.append((points[cur_idx], points[v]))
            stack.pop()                     
            stack.append(order[i-1])        
            stack.append(cur_idx)
        else:
            # Same chain
            while len(stack) >= 2:
                a = stack[-2]
                b = stack[-1]
                ori = orientation(points[a], points[b], points[cur_idx])

                if (chain[cur_idx] == "UPPER" and ori > 0) or \
                   (chain[cur_idx] == "LOWER" and ori < 0):
                    stack.pop()
                    diagonals.append((points[cur_idx], points[a]))
                else:
                    break
            stack.append(cur_idx)

    
    # Handle the last vertex
    last_idx = order[-1]
    
    # The last point is connected by polygon edges to the first (stack[0]) 
    # and last (stack[-1]) element on the stack. 
    # Therefore, we must pop the top vertex (neighbor) and do not connect to it.
    if stack:
        stack.pop()
        
    # Then connect the last point to all remaining points on the stack,
    # EXCEPT the bottom of the stack (which is also a neighbor).
    while len(stack) > 1:
        v = stack.pop()
        diagonals.append((points[last_idx], points[v]))

    return diagonals

def print_diagonals(diagonals):
    """
    Formats and prints the list of diagonals.
    
    Diagonals are sorted first by the coordinates of the first point, then the second.
    """
    # Sort diagonals so that the point with smaller x comes first
    sorted_diags = []
    for a, b in diagonals:
        if a.x > b.x or (a.x == b.x and a.y > b.y):
            a, b = b, a
        sorted_diags.append((a, b))
    
    # Sort everything by the first point (x, then y)
    sorted_diags.sort(key=lambda p: (p[0].x, p[0].y))
    
    for a, b in sorted_diags:
        print(f"({a.x},{a.y})({b.x},{b.y})")

if __name__ == "__main__":
    pts = read_polygon("input.txt")
    result = triangulate_x_monotone(pts)
    print_diagonals(result)