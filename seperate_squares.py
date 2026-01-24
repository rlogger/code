# problem 1: to review
# find hte minimum y-coordinate value of a horizontal line such that the total area of the square above the line equals the total area of squares below the line


squares = [[0, 0, 1], [2, 2, 1]]
# out = 1

squares = [[0, 0, 2], [1, 1, 1]]
# out = 1.166667


def seperate_squares(squares):
    def area_below(h):
        total = 0
        for x, y, L in squares:
            if h <= y:
                continue
            elif h >= y + L:
                total += L * L
            else:
                total += L * (h - y)
        return total

    def area_above(h):
        total = 0
        for x, y, L in squares:
            if h >= y + L:
                continue
            elif h <= y:
                total += L * L
            else:
                total += L * (y + L - h)
        return total
    
    min_y = min(y for x, y, L in squares)
    max_y = max(y + L for x, y, L in squares)

    left, right = min_y, max_y

    for _ in range(100):
        mid = (left + right) / 2
        below  = area_below(mid)
        above = area_above(mid)

        if below > above:
            left = mid
        else:
            right = mid
    
    return (left + right) / 2
