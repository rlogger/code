import sys

# Increase recursion depth just in case
sys.setrecursionlimit(2000)

def solve():
    # -------------------------------------------------------------------------
    # 1. Fast Input
    # -------------------------------------------------------------------------
    input_data = sys.stdin.buffer.read().split()
    if not input_data:
        return
    iterator = iter(input_data)
    
    def ni():
        return int(next(iterator))

    # -------------------------------------------------------------------------
    # 2. Setup Constants
    # -------------------------------------------------------------------------
    N = ni(); S = ni(); L = ni()
    M = ni(); K = ni(); P = ni()

    SPP = S // P
    OPP = M // P
    
    # R: Ports per OXC
    # Formula: N * (S/P) * K
    R = N * SPP * K
    STRIDE_G = SPP * K

    # Persistent OXC config: [m][port] -> connected_port (or -1)
    oxc_config = [[-1] * R for _ in range(M)]

    # Precompute OXCs belonging to each plane
    oxcs_in_plane = [list(range(p * OPP, (p + 1) * OPP)) for p in range(P)]
    
    # Precompute Spines belonging to each plane (Global Indices)
    spines_in_plane = [list(range(p * SPP, (p + 1) * SPP)) for p in range(P)]

    # Precompute base port offsets
    # Port = Group_Offset + LocalSpine_Offset + Link
    # base_port[group][local_spine_index]
    base_port = [[g * STRIDE_G + local * K for local in range(SPP)] for g in range(N)]

    out = sys.stdout.write

    # -------------------------------------------------------------------------
    # 3. Query Loop
    # -------------------------------------------------------------------------
    for _q in range(5):
        try:
            Q_val = ni()
        except StopIteration:
            break

        # Read flows
        gA_list = [0] * Q_val
        lA_list = [0] * Q_val
        gB_list = [0] * Q_val
        lB_list = [0] * Q_val
        
        for i in range(Q_val):
            gA_list[i] = ni()
            lA_list[i] = ni()
            gB_list[i] = ni()
            lB_list[i] = ni()

        # Load Tracking
        spine_load = [[0] * S for _ in range(N)]
        oxc_load = [0] * M

        # Port Locking (Per Query)
        # locked[m][port] = 1 if used this query
        locked = [bytearray(R) for _ in range(M)]
        # Track touched ports to reset fast
        touched = [[] for _ in range(M)]

        results = [""] * Q_val

        # ---------------------------------------------------------------------
        # 4. Route Flows
        # ---------------------------------------------------------------------
        for i in range(Q_val):
            GA = gA_list[i]
            GB = gB_list[i]

            best_path = None
            # Score: (Max_Conflict, Adjustment_Cost, OXC_Load)
            best_score = (10**9, 10**9, 10**9)

            loadA = spine_load[GA]
            loadB = spine_load[GB]

            # Iterate through Planes
            for p in range(P):
                p_off = p * SPP
                p_oxcs = oxcs_in_plane[p]
                p_spines = spines_in_plane[p]

                # -------------------------------------------------------------
                # Adaptive Search Strategy
                # 1. Sort spines by load (Greedy)
                # 2. Try top 2 spines first (Fast Path)
                # 3. If no path found yet, try ALL spines (Fallback)
                # -------------------------------------------------------------
                
                # Get sorted candidates
                candA = sorted(p_spines, key=lambda s: loadA[s])
                candB = sorted(p_spines, key=lambda s: loadB[s])
                
                # Heuristic Limit: Check top 2 spines for speed
                # If we fail to find ANY path, we will ignore this limit
                check_limit = 2 

                found_in_plane = False

                for ia, sA in enumerate(candA):
                    # Pruning: If we have a good path, and this spine is already highly loaded, skip
                    # But if we have NO path, we must keep going.
                    if best_path is not None and ia >= check_limit:
                        # Only break if the load is actually worse than what we found
                        if loadA[sA] > best_score[0]:
                            break
                    
                    la = loadA[sA]
                    localA = sA - p_off
                    baseA = base_port[GA][localA]

                    for ib, sB in enumerate(candB):
                        if best_path is not None and ib >= check_limit:
                             if loadB[sB] > best_score[0]:
                                break
                        
                        lb = loadB[sB]
                        localB = sB - p_off
                        baseB = base_port[GB][localB]

                        # Base Max Load for this path
                        current_base = la if la > lb else lb
                        
                        # Optimization: If base load exceeds best found, stop checking this pair
                        if current_base > best_score[0]:
                            continue

                        # Iterate OXCs
                        for m in p_oxcs:
                            lockm = locked[m]
                            cfgm = oxc_config[m]
                            ol = oxc_load[m]

                            # Iterate Links
                            for kx in range(K):
                                portA = baseA + kx
                                if lockm[portA]: continue
                                
                                connA = cfgm[portA]

                                for ky in range(K):
                                    portB = baseB + ky
                                    if lockm[portB]: continue

                                    connB = cfgm[portB]

                                    # Locking Logic Check:
                                    # We cannot break a connection if the partner is locked by another flow
                                    if connA != -1 and connA != portB and lockm[connA]:
                                        continue
                                    if connB != -1 and connB != portA and lockm[connB]:
                                        continue
                                    
                                    # Cost Calc
                                    cost = 0
                                    if connA == portB:
                                        cost = 0
                                    else:
                                        cost = 1
                                        if connA != -1: cost += 1
                                        if connB != -1: cost += 1
                                    
                                    # Score comparison
                                    # (Load, Cost, OXC_Load)
                                    if current_base < best_score[0] or \
                                       (current_base == best_score[0] and cost < best_score[1]) or \
                                       (current_base == best_score[0] and cost == best_score[1] and ol < best_score[2]):
                                        
                                        best_score = (current_base, cost, ol)
                                        best_path = (sA, kx, m, sB, ky, portA, portB)
                                        
                                        # Super Greedy Exit: Perfect path
                                        if cost == 0 and current_base == 0:
                                            # We can't return from function, but we can break loops
                                            # Use a flag or strict break
                                            pass
            
            # -----------------------------------------------------------------
            # Commit Best Path
            # -----------------------------------------------------------------
            if best_path is None:
                # This is a critical failure case, but we output valid format to prevent crashes.
                # In competition, this likely implies insufficient capacity or logic bug.
                results[i] = "0 0 0 0 0"
            else:
                sA, kx, m, sB, ky, portA, portB = best_path
                
                # Lock ports
                if not locked[m][portA]:
                    locked[m][portA] = 1
                    touched[m].append(portA)
                if not locked[m][portB]:
                    locked[m][portB] = 1
                    touched[m].append(portB)
                
                # Update Config
                if oxc_config[m][portA] != portB:
                    oldA = oxc_config[m][portA]
                    oldB = oxc_config[m][portB]
                    
                    if oldA != -1: oxc_config[m][oldA] = -1
                    if oldB != -1: oxc_config[m][oldB] = -1
                    
                    oxc_config[m][portA] = portB
                    oxc_config[m][portB] = portA
                
                # Update Loads
                spine_load[GA][sA] += 1
                spine_load[GB][sB] += 1
                oxc_load[m] += 1
                
                results[i] = f"{sA} {kx} {m} {sB} {ky}"

        # ---------------------------------------------------------------------
        # Output Results
        # ---------------------------------------------------------------------
        buf = []
        for m in range(M):
            # Convert int list to string
            buf.append(" ".join(map(str, oxc_config[m])))
        buf.extend(results)
        out("\n".join(buf) + "\n")
        
        # Reset Locks
        for m in range(M):
            lockm = locked[m]
            for pidx in touched[m]:
                lockm[pidx] = 0

if __name__ == "__main__":
    solve()
