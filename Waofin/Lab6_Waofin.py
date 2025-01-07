import time
from itertools import permutations, combinations

def generate_unique_permutations(elements):
    """Genera todas las permutaciones únicas de una lista de elementos"""
    def backtrack(path, options):
        if not options:
            results.add(tuple(path))
            return
        seen = set()
        for i in range(len(options)):
            if options[i] not in seen:
                seen.add(options[i])
                backtrack(path + [options[i]], options[:i] + options[i+1:])

    results = set()
    backtrack([], elements)
    return list(results)

def compare_permutation_methods(elements):
    """Compara el rendimiento entre implementaciones de permutaciones únicas"""
    start_unique = time.time()
    unique_results = generate_unique_permutations(elements)
    time_unique = time.time() - start_unique

    start_itertools = time.time()
    itertools_results = list(set(permutations(elements)))
    time_itertools = time.time() - start_itertools

    return len(unique_results), time_unique, time_itertools, itertools_results

def generate_unique_combinations(elements, r):
    """Genera combinaciones únicas de tamaño r"""
    return list(set(combinations(sorted(elements), r)))

def compare_unique_combinations(elements, r):
    """Calcula el número de combinaciones únicas y su tiempo de ejecución"""
    start_combinations = time.time()
    unique_combinations = generate_unique_combinations(elements, r)
    time_combinations = time.time() - start_combinations
    return len(unique_combinations), time_combinations, unique_combinations

def transform_sequence(start, target):
    """Realiza una transformación paso a paso desde una secuencia inicial hasta una objetivo"""
    steps = []
    current = list(start)
    for i in range(len(current)):
        if current[i] != target[i]:
            steps.append((current.copy(), f"Intercambiar {current[i]} con {target[i]}"))
            current[i] = target[i]
    return steps
