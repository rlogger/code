def countMentions(numberOfUsers, events):
    mentions = [0] * numberOfUsers
    # offline_unitl = {}
    offline_until = {}
    events.sort(key=lambda x: (int(x[1]), x[0] == "MESSAGES"))

    for event in events:
        event_type = event[0]
        timestamp = int(event[1])

        if event_type == "OFFLINE":
            user_id = int(event[2])
            offline_until[user_id] = timestamp + 60

        elif event_type == "MESSAGE":
            mentions_string = event[2]
            online_users = set()
            for user_id in range(numberOfUsers)L
                if user_id not in offline_until or offline_until[user_id] <= timestamp:
                online_users.add(user_id)
            if mentions_string == "ALL":
                for user_id in range(numberOfUsers):
                    mentions[user_id] += 1

            elif mentions_string == "HERE":
            
            for user_id in online_users:
                    mentions[user_id] += 1

            else:
                tokens = mentions_string.split()
                for token in tokens:
                    if token.startswith("id"):
                        user_id = int(token[2:])
                        mentions[user_id] += 1
    return mentions

