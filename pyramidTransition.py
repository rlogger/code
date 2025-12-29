def pyramidTransition(bottom, allowed):
    # Build a mapping: (left, right) -> list of possible top blocks
    patterns = {}
    
    # add pattern to the list
    for pattern in allowed:
        left, right, top = pattern[0], pattern[1], pattern[2]
        key = (left, right)
        if key not in patterns:
            patterns[key] = []
        patterns[key].append(top)
    
    # Memoization: store whether we can build from a given level
    memo = {}
    
    def buildLevel(current):
        """Try to build the next level from current level"""
        if len(current) == 1:
            return True  # Reached the top!
        
        if current in memo:
            return memo[current]
        
        # Try to build the next level
        def buildNextLevel(index, nextLevel):
            if index == len(current) - 1:
                # We've built the complete next level
                return buildLevel(nextLevel)
            
            # Get possible blocks for position (index, index+1)
            left = current[index]
            right = current[index + 1]
            key = (left, right)
            
            if key not in patterns:
                return False
            
            # Try each possible top block
            for topBlock in patterns[key]:
                if buildNextLevel(index + 1, nextLevel + topBlock):
                    return True
            
            return False
        
        result = buildNextLevel(0, "")
        memo[current] = result
        return result
    
    return buildLevel(bottom)


# Test cases
print(pyramidTransition("BCD", ["BCC","CDE","CEA","FFF"]))  # True
