# import time
import random
import numpy as np

from collections import deque
from game_parameters import OBSERVATION, INITIAL_EPSILON, FINAL_EPSILON, \
    EXPLORE, REPLAY_MEMORY, BATCH, GAMMA, ACTIONS


def train_network(model, game_state):
    """Método para treinar a rede,

    Args:
        model: Modelo keras.
        game_state: Módulo Game State.
    """
    D = deque()
    do_nothing = np.zeros(ACTIONS)
    do_nothing[0] = 1

    x_t, r_0, terminal = game_state.get_state(do_nothing)
    s_t = np.stack((x_t, x_t, x_t, x_t), axis=2).reshape(1, 20, 40, 4)

    OBSERVE = OBSERVATION
    epsilon = INITIAL_EPSILON
    t = 0

    while True:

        loss = 0
        Q_sa = 0
        action_index = 0
        r_t = 0
        a_t = np.zeros([ACTIONS])

        # escolha uma ação aleatória
        if random.random() <= epsilon:
            print('Ação aleatória')
            action_index = random.randrange(ACTIONS)
            a_t[action_index] = 1
        else:
            q = model.predict(s_t)
            max_Q = np.argmax(q)
            action_index = max_Q
            a_t[action_index] = 1

        if epsilon > FINAL_EPSILON and t > OBSERVE:
            epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE

        x_t1, r_t, terminal = game_state.get_state(a_t)
        # last_time = time.time()
        x_t1 = x_t1.reshape(1, x_t1.shape[0], x_t1.shape[1], 1)
        s_t1 = np.append(x_t1, s_t[:, :, :, :3], axis=3)

        D.append((s_t, action_index, r_t, s_t1, terminal))
        if len(D) > REPLAY_MEMORY:
            D.popleft()

        if t > OBSERVE:
            train_batch(random.sample(D, BATCH), s_t, model)
        s_t = s_t1
        t += 1
        print(f'TIMESTEP: {t}, EPSILON: {epsilon}, ACTION: {action_index}, \
            REWARD: {r_t}, Q_MAX: {np.max(Q_sa)}, Loss: {loss}')


def train_batch(mini_batch, s_t, model):
    """Realiza o treino por lote.

    Args:
        mini_batch: Mini lote.

    Returns: None
    """
    inputs = np.zeros((BATCH, s_t.shape[1], s_t.shape[2], s_t.shape[3]))
    targets = np.zeros((inputs.shape[0], ACTIONS))
    loss = 0

    for i in range(0, len(mini_batch)):
        state_t = mini_batch[i][0]
        action_t = mini_batch[i][1]
        reward_t = mini_batch[i][2]
        state_t1 = mini_batch[i][3]
        terminal = mini_batch[i][4]
        inputs[i:i + 1] = state_t
        targets[i] = model.predict(state_t)
        Q_sa = model.predict(state_t1)
        if terminal:
            targets[i, action_t] = reward_t
        else:
            targets[i, action_t] = reward_t + GAMMA * np.max(Q_sa)
    loss += model.train_on_batch(inputs, targets)
