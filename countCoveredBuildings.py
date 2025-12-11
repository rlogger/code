def countCoveredBUildings(n, buildings):
    rows = {}
    cols = {}

    for x, y in buildings:
        if x not in rows:
            rows[x] = []
        rows[x].append(y)

        if y not in cols:
            cols[y] = []
        cols[y].append(x)

        count = 0

        for x, y in buildings:
            has_left = any(y_val < y for y_val in rows.get(x, []))
            has_right = any(y_val > y for y_val in rows.get(x, []))
            has_above = any(x_val < x for x_val in cols.get(y, []))
            has_below = any(x_val > x for x_val in cols.get(y, []))

        if has_left and has_right and has_above and has_below:
            count += 1

    return count
