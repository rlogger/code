import sys
# pypi
def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    ni = lambda: int(next(it))

    N = ni(); S = ni(); L = ni()
    M = ni(); K = ni(); P = ni()

    SPP = S // P
    OPP = M // P
    R = N * SPP * K  # ports per OXC
    STRIDE_G = SPP * K

    # Persistent OXC config across queries
    oxc_config = [[-1] * R for _ in range(M)]

    # OXCs per plane
    oxcs_in_plane = [list(range(p * OPP, (p + 1) * OPP)) for p in range(P)]

    # Precompute base port offsets: base[g][local_spine] = g*STRIDE_G + local*K
    base_port = [[g * STRIDE_G + local * K for local in range(SPP)] for g in range(N)]

    # helper: find two min-load spines in plane p for group g (global spine idx)
    def min2_spines(load_row, p_offset):
        best1 = p_offset
        l1 = load_row[best1]
        best2 = -1
        l2 = 10**18
        # scan remaining local spines
        end = p_offset + SPP
        for s in range(p_offset + 1, end):
            v = load_row[s]
            if v < l1:
                best2, l2 = best1, l1
                best1, l1 = s, v
            elif v < l2:
                best2, l2 = s, v
        return best1, best2  # best2 may be -1 if SPP==1

    out = sys.stdout.write

    # 5 queries
    for _q in range(5):
        try:
            Q = ni()
        except StopIteration:
            break

        # read flows into flat arrays (faster than dicts)
        gA = [0]*Q; lA = [0]*Q; gB = [0]*Q; lB = [0]*Q
        for i in range(Q):
            gA[i] = ni(); lA[i] = ni(); gB[i] = ni(); lB[i] = ni()

        spine_load = [[0]*S for _ in range(N)]
        oxc_load = [0]*M

        # per-OXC locked ports, reused: 0/1 bytearray
        locked = [bytearray(R) for _ in range(M)]
        touched = [[] for _ in range(M)]  # ports we set to 1, so we can reset fast

        results = [""] * Q

        for i in range(Q):
            GA = gA[i]; GB = gB[i]

            best = None
            best_score = (10**18, 10**18, 10**18)

            loadA = spine_load[GA]
            loadB = spine_load[GB]

            # iterate planes
            for p in range(P):
                p_off = p * SPP

                sA1, sA2 = min2_spines(loadA, p_off)
                sB1, sB2 = min2_spines(loadB, p_off)

                # candidate spines (avoid building new lists)
                candA = (sA1, sA2) if sA2 != -1 else (sA1,)
                candB = (sB1, sB2) if sB2 != -1 else (sB1,)

                oxcs = oxcs_in_plane[p]

                for sA in candA:
                    localA = sA - p_off
                    baseA = base_port[GA][localA]
                    la = loadA[sA]

                    for sB in candB:
                        localB = sB - p_off
                        baseB = base_port[GB][localB]
                        lb = loadB[sB]

                        base_conf = la if la > lb else lb
                        if base_conf > best_score[0]:
                            continue

                        for m in oxcs:
                            lockm = locked[m]
                            cfgm = oxc_config[m]
                            om_load = oxc_load[m]

                            # try K lanes on each side
                            for kx in range(K):
                                portA = baseA + kx
                                if lockm[portA]:
                                    continue

                                connA = cfgm[portA]

                                for ky in range(K):
                                    portB = baseB + ky
                                    if lockm[portB]:
                                        continue

                                    connB = cfgm[portB]

                                    # IMPORTANT: don't break a connection if the partner port is locked this query
                                    # (otherwise you'd be rewiring a "used" port).
                                    if connA != -1 and connA != portB and lockm[connA]:
                                        continue
                                    if connB != -1 and connB != portA and lockm[connB]:
                                        continue

                                    if connA == portB:
                                        cost = 0
                                    else:
                                        cost = 1
                                        if connA != -1: cost += 1
                                        if connB != -1: cost += 1

                                    score = (base_conf, cost, om_load)
                                    if score < best_score:
                                        best_score = score
                                        best = (sA, kx, m, sB, ky, portA, portB)

                                        # early exit: perfect local choice
                                        if cost == 0 and base_conf == 0:
                                            break
                                else:
                                    continue
                                break
                            else:
                                continue
                            # broke from k-loops
                            if best_score[0] == 0 and best_score[1] == 0:
                                break
                        if best_score[0] == 0 and best_score[1] == 0:
                            break
                    if best_score[0] == 0 and best_score[1] == 0:
                        break
                if best_score[0] == 0 and best_score[1] == 0:
                    break

            # commit
            if best is None:
                # Emergency: search ALL spines and ALL OXCs if greedy failed
                found = False
                for p in range(P):
                    if found: break
                    for sA in range(p * SPP, (p + 1) * SPP):
                        if found: break
                        for sB in range(p * SPP, (p + 1) * SPP):
                            if found: break
                            for m in oxcs_in_plane[p]:
                                if found: break
                                for kx in range(K):
                                    if found: break
                                    portA = base_port[GA][sA - p * SPP] + kx
                                    if locked[m][portA]: continue
                                    for ky in range(K):
                                        portB = base_port[GB][sB - p * SPP] + ky
                                        if locked[m][portB]: continue
                                        connA = oxc_config[m][portA]
                                        connB = oxc_config[m][portB]
                                        if connA != -1 and connA != portB and locked[m][connA]: continue
                                        if connB != -1 and connB != portA and locked[m][connB]: continue
                                        best = (sA, kx, m, sB, ky, portA, portB)
                                        found = True
                                        break
                if best is None:
                    results[i] = "0 0 0 0 0"
                    continue

            sA, kx, m, sB, ky, portA, portB = best

            # lock
            lockm = locked[m]
            if not lockm[portA]:
                lockm[portA] = 1
                touched[m].append(portA)
            if not lockm[portB]:
                lockm[portB] = 1
                touched[m].append(portB)

            cfgm = oxc_config[m]
            if cfgm[portA] != portB:
                oldA = cfgm[portA]
                oldB = cfgm[portB]

                # disconnect old partners
                if oldA != -1:
                    cfgm[oldA] = -1
                if oldB != -1:
                    cfgm[oldB] = -1

                cfgm[portA] = portB
                cfgm[portB] = portA

            spine_load[GA][sA] += 1
            spine_load[GB][sB] += 1
            oxc_load[m] += 1

            results[i] = f"{sA} {kx} {m} {sB} {ky}"

        # output config + routes (fast)
        buf = []
        for m in range(M):
            buf.append(" ".join(map(str, oxc_config[m])))
        buf.extend(results)
        out("\n".join(buf) + "\n")

        # reset locks cheaply (no O(M*R) clear)
        for m in range(M):
            lockm = locked[m]
            for pidx in touched[m]:
                lockm[pidx] = 0

if __name__ == "__main__":
    solve()
