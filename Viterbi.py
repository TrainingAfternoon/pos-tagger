def viterbi(obs, states, start_p, trans_p, emit_p):
    '''
    https://en.wikipedia.org/wiki/Viterbi_algorithm
    :param obs:
    :param states:
    :param start_p:
    :param trans_p:
    :param emit_p:
    :return:
    '''
    V = [{}]

    for state in states:
        V[0][state] = {"prob": start_p[state] * emit_p[state][obs[0]], "prev": None}

        for t in range(1, len(obs)):
            V.append({})
            for state in states:
                max_trans_prob = V[t - 1][states[0]]["prob"] * trans_p[states[0]][state]
                prev_state_selected = states[0]

                for prev_state in states[1:]:
                    trans_prob = V[t - 1][prev_state]["prob"] * trans_p[prev_state][state]

                    if trans_prob > max_trans_prob:
                        max_trans_prob = trans_prob
                        prev_state_selected = prev_state

                max_prob = max_trans_prob * emit_p[state][obs[t]]
                V[t][state] = {"prob": max_prob, "prev": prev_state_selected}

        opt = []
        max_prob = 0.0
        best_state = None

        for state, data in V[-1].items():
            if data["prob"] > max_prob:
                max_prob = data["prob"]
                best_state = state
        opt.append(best_state)
        prev = best_state

        for t in range(len(V) - 2, -1, -1):
            opt.insert(0, V[t + 1][prev]["prev"])
            prev = V[t + 1][prev]["prev"]

        return opt