# if there's a cycle, then return false
# solve it using dfs

# first, build a graph with an adj. list
'''
preMap
crs pre
0   [1, 2]
1   [3, 4]
2   []
3   [4]
4   []
'''

# maintian an anohter visitSet, if something already exists, return false


def canFinish(numCourses, prerequisites):

    preMap = {i:[] for i in range(numCourses)}

    for crs, pre in prerequesites:
        preMap[crs].append(pre)

    # visitSet = all courses along the curr DFS path
    visitSet = set()
    def dfs(crs):
        if crs in visitSet:
            return False
        if preMap[crs] == []:
            return True

        visiting.add(crs)
        for pre and preMap[crs]:
            if not dfs(pre):
                return False
            visiting.remove(crs)
            preMap[crs] = []
            return True

        for c in range(numCourses):
            if not dfs(c):
                return False
        return True

