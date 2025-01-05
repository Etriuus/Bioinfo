# PARA EJECUTAR INSTALAR STREAMLIT: pip install streamlit Y EJECUTAR: streamlit run lab6.py

import time
from itertools import permutations, combinations
import streamlit as st

# Función 1: Generación de permutaciones únicas (evitar duplicados)
def generate_unique_permutations(elements):
    """Genera todas las permutaciones únicas de una lista de elementos, 
    evitando duplicados mediante un conjunto.
    Argumentos:
        elements: lista de elementos (pueden ser números o caracteres).
    Retorna:
        Lista de permutaciones únicas.
    """
    def backtrack(path, options):
        """Algoritmo de backtracking para construir las permutaciones únicas.
        Evita generar duplicados al usar un conjunto `seen` para controlar
        qué elementos ya se han utilizado en el nivel actual de la recursión.
        """
        if not options:
            results.add(tuple(path))  # Usar tuplas para que sean hashables (y únicas en sets)
            return
        seen = set()  # Controla los elementos utilizados en este nivel
        for i in range(len(options)):
            if options[i] not in seen:  # Evitar duplicados en el mismo nivel
                seen.add(options[i])
                backtrack(path + [options[i]], options[:i] + options[i+1:])

    results = set()  # Almacena las permutaciones únicas
    backtrack([], elements)
    return list(results)


# Función 2: Comparar tiempo y resultados de las permutaciones únicas
def compare_permutation_methods(elements):
    """Compara el rendimiento entre la implementación de permutaciones únicas 
    personalizada y la de itertools.
    Argumentos:
        elements: lista de elementos (pueden ser números o caracteres).
    Retorna:
        - Número de permutaciones únicas.
        - Tiempo de ejecución para la implementación personalizada.
        - Tiempo de ejecución para itertools.
    """
    # Implementación personalizada
    start_unique = time.time()
    unique_results = generate_unique_permutations(elements)
    time_unique = time.time() - start_unique

    # Usando itertools con eliminación de duplicados
    start_itertools = time.time()
    itertools_results = list(set(permutations(elements)))  # Eliminar duplicados con set
    time_itertools = time.time() - start_itertools

    return len(unique_results), time_unique, time_itertools, itertools_results


# Función 3: Generar combinaciones únicas para una lista de tamaño arbitrario
def generate_unique_combinations(elements, r):
    """Genera combinaciones únicas de tamaño `r` a partir de una lista de elementos.
    Argumentos:
        elements: lista de elementos.
        r: tamaño de las combinaciones.
    Retorna:
        Lista de combinaciones únicas.
    """
    # Usar un conjunto para asegurar combinaciones únicas
    return list(set(combinations(sorted(elements), r)))


# Función 4: Comparar tiempo de ejecución de combinaciones únicas
def compare_unique_combinations(elements, r):
    """Calcula el número de combinaciones únicas y su tiempo de ejecución.
    Argumentos:
        elements: lista de elementos.
        r: tamaño de las combinaciones.
    Retorna:
        - Número de combinaciones únicas.
        - Tiempo de ejecución.
        - Lista de combinaciones únicas.
    """
    start_combinations = time.time()
    unique_combinations = generate_unique_combinations(elements, r)
    time_combinations = time.time() - start_combinations
    return len(unique_combinations), time_combinations, unique_combinations

# Función 5: Transformación de Secuencia
def transform_sequence(start, target):
    """Realiza una transformación paso a paso desde una secuencia inicial hasta 
    una secuencia objetivo.
    Argumentos:
        start: Secuencia inicial como lista.
        target: Secuencia objetivo como lista.
    Retorna:
        Lista de pasos necesarios para transformar la secuencia inicial 
        en la final, con detalles de los intercambios realizados.
    """
    steps = []  # Almacena los pasos realizados
    current = list(start)  # Copia la secuencia inicial
    for i in range(len(current)):
        if current[i] != target[i]:  # Verificar si hay una discrepancia
            steps.append((current.copy(), f"Intercambiar {current[i]} con {target[i]}"))
            current[i] = target[i]  # Realizar el cambio
    return steps


# Interfaz en Streamlit
def main():
    st.title("Laboratorio de Permutaciones y Transformación de Secuencias")
    st.write("""
    Este laboratorio explora cómo generar permutaciones únicas, combinaciones únicas 
    e implementar transformaciones en secuencias biológicas
    """)

   # Función 1: Generación de Permutaciones
    st.header("Función 1: Generación de Permutaciones Únicas")
    input_list = st.text_input("Introduce una lista (separada por comas)", "1,2,3,4")
    if st.button("Calcular Permutaciones"):
        try:
            # Permitir números o caracteres
            elements = [x.strip() for x in input_list.split(',')]
            n_perms, t_unique, t_itertools, itertools_results = compare_permutation_methods(elements)
            st.write("""Genera todas las permutaciones únicas de una lista de elementos, 
            evitando duplicados mediante un conjunto.""")
            st.write(f"**Permutaciones únicas encontradas:** {n_perms}")
            st.write(f"**Tiempo (Implementación Única):** {t_unique:.6f} segundos")
            st.write(f"**Tiempo (itertools con duplicados eliminados):** {t_itertools:.6f} segundos")

            # Mostrar las permutaciones generadas por itertools (sin duplicados)
            st.write(f"**Permutaciones generadas por itertools (sin duplicados):**")
            st.write(itertools_results)  # Mostrar las permutaciones

        except Exception as e:
            st.error(f"Error procesando la lista: {e}")
        
    # Función 2: Generar y medir combinaciones únicas
    st.header("Función 2: Combinaciones Únicas")
    input_list_combinations = st.text_input("Introduce una lista de elementos (separada por comas)", "1,2,3,3")
    r_value = st.number_input("Tamaño de las combinaciones", min_value=1, max_value=10, value=2, step=1)
    if st.button("Calcular Combinaciones Únicas"):
        try:
            elements = [x.strip() for x in input_list_combinations.split(',')]
            n_combinations, t_combinations, combinations_list = compare_unique_combinations(elements, r_value)
            st.write(f"**Número de combinaciones únicas:** {n_combinations}")
            st.write(f"**Tiempo de ejecución:** {t_combinations:.6f} segundos")
            st.write(f"**Combinaciones:** {combinations_list[:10]}")  # Mostrar las primeras 10 combinaciones
        except Exception as e:
            st.error(f"Error procesando la lista: {e}")

    # Función 3: Transformación de Secuencia
    st.header("Función 3: Transformación de Secuencia")
    start_seq = st.text_input("Secuencia inicial (separada por comas)", "1,2,3,4")
    target_seq = st.text_input("Secuencia final (separada por comas)", "4,3,2,1")
    if st.button("Transformar Secuencia"):
        try:
            start = [x.strip() for x in start_seq.split(',')]
            target = [x.strip() for x in target_seq.split(',')]
            if len(start) != len(target):
                st.error("La secuencia inicial y final deben tener la misma longitud.")
            else:
                steps = transform_sequence(start, target)
                for step, description in steps:
                    st.write(f"{description}: {step}")
                st.write(f"**Total pasos:** {len(steps)}")
        except Exception as e:
            st.error(f"Error procesando las secuencias: {e}")

    st.header("Acerca de este laboratorio")
    st.write("""
Se generan permutaciones y combinaciones únicas a partir de listas de elementos
y transforma secuencias paso a paso. Las funciones incluyen:

1. `generate_unique_permutations`: Genera todas las permutaciones únicas de una lista de elementos,
   evitando duplicados mediante un algoritmo de backtracking.
2. `compare_permutation_methods`: Compara el rendimiento de la implementación personalizada de
   permutaciones frente a la implementación de `itertools`.
3. `generate_unique_combinations`: Genera combinaciones únicas de tamaño `r` a partir de una lista.
4. `compare_unique_combinations`: Compara el rendimiento y los resultados de las combinaciones únicas.
5. `transform_sequence`: Realiza una transformación paso a paso de una secuencia inicial a una secuencia objetivo.

La interfaz gráfica de usuario está implementada usando Streamlit, lo que permite al usuario ingresar
listas y obtener resultados interactivos. Se incluye también la medición del tiempo de ejecución para
las diferentes funciones y se muestra información detallada sobre las permutaciones, combinaciones y
transformaciones realizadas.\n
**César Cerda Rifo**
""")
if __name__ == "__main__":
    main()
