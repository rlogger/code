"""
Algorithm Logic

This function solves a collision counting problem where:
1. Cars moving left ("L") from the leftmost positions won't collide with anything to their left, so they're removed
2. Cars moving right ("R") from the rightmost positions won't collide with anything to their right, so they're removed
3. Any remaining "R" or "L" characters represent cars that will eventually collide, so counting them gives the total collision count
"""


def countCollisions(directions):

    directions = directions.lstrip("L")
    directions = directions.rstrip("R")

    return directions.count("R") + directions.count("L")
