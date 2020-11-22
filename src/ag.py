# Funções para a execução de um AG
import random
from typing import List, Tuple


def select_father(pop: List[List[float]]) -> List[float]:
    """Função para selecionar um pai em um determinada população.

    Args:
        pop: População.

    Returns: Indiíduo selecionado.
    """
    # utilizando a roleta
    sorted_value: int = random.randint(0, 100)
    relative_sum: int = 0
    for index, element in enumerate(pop):
        # trocar index pela posição do valor da fitness
        relative_sum += element[index]
        if sorted_value <= relative_sum:
            return element
    # caso não consiga encontrar um indivíduo retornamos o melhor
    return pop[-1]


def crossover(father_1: List[float], father_2: List[float], crossing_rate: float
              ) -> Tuple[List[float], List[float]]:
    """Realiza o cruzamento de acordo com a taza informada.

    Args:
        father_1: Primeiro pai.
        father_2: Segundo pai.
        crossing_rate: Taxa de mutação.

    Returns: Filho 1 e filho 2.
    """
    # ponto de mutação
    mutation_dot: int = 3
    child_1: List[float] = []
    child_2: List[float] = []
    # se houver mutação
    if random.uniform(0.0, 1.0) <= crossing_rate:
        for index, _ in enumerate(father_1):
            if index < mutation_dot:
                child_1.append(father_1[index])
                child_2.append(father_2[index])
            else:
                child_1.append(father_2[index])
                child_2.append(father_1[index])
    # se não houver cruzamento
    else:
        child_1 = father_1
        child_2 = father_2
    return child_1, child_2


def mutation(child: List[float], mutation_rate: float) -> List[float]:
    """Realiza a mutação em um determinado indivíduo.

    Args:
        child: Elemento a ser mutado.
        mutation_rate: Taxa de mutação.

    Returns: Elemento mutado.
    """
    # limiar de mutação
    mutation_threshold = random.uniform(0, 1)
    # fator de mutação, mude se necessário
    mutation_factor = random.uniform(-0.2, 0.2)
    gene = random.randint(0, len(child) - 1)
    # se houver mutação
    if mutation_threshold <= mutation_rate:
        child[gene] = child[gene] + mutation_factor
    return child


def create_population(pop: List[List[float]], crossing_rate: float,
                      mutation_rate: float) -> List[List[float]]:
    """Cria uma população de acordo com os dados da população passada como parâ-
    metro e as demais opções. Realiza a mutação e o crossover.

    Args:
        pop: População.
        crossing_rate: Taxa de cruzamento. Deve estar entre 0 e 1.
        mutation_rate: Taxa de mutação.

    Returns: Nova população com o mesmo tamanho da passada como parâmetro.
    """
    # nova população
    new_pop: List[List[float]] = []
    pop_length: int = len(pop)
    # para cada casal da população passada como parâmetro
    for _ in range(pop_length // 2):
        # seleciona os pais da população
        father_1 = select_father(pop)
        father_2 = select_father(pop)
        # realiza o cruzamento
        child_1, child_2 = crossover(father_1, father_2, crossing_rate)
        # realiza a mutação
        child_1 = mutation(child_1, mutation_rate)
        child_2 = mutation(child_2, mutation_rate)
        new_pop.append(child_1)
        new_pop.append(child_2)
    return new_pop
