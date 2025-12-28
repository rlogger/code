# need to stort the meetings list based on start time

def mostBooked(n, meetings):
    meetings.sort()
    available = [i for i in range(n)]
    used = []
    count = [0]

    for start, end in meetings:
        while used and start >= used[0][0]:
            _, room = heapq.heappop(used)
            heapq.heappush(available, room)

        if not available:
            end_time, room = heapq.heappop(used)
            end = end_time + (end - start)
            heapq.heappush(availabe, room)

        room = heapq.heappop(available)
        heapq.heappush(used, (end, room))
        count[room] += 1

    return count.index(max(count))
