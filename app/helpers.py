import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def load_products(file_path='data/products.csv'):
    """
    Carga los productos desde un archivo CSV.
    """
    products = pd.read_csv(file_path)
    return products

def encode_product_features(products):
    """
    Codifica las características categóricas de los productos.
    """
    # Crear copia para no modificar el original
    products_to_encode = products.copy()

    # Convertir características categóricas en variables dummy
    products_encoded = pd.get_dummies(
        products_to_encode,
        columns=['Category', 'Material', 'Color', 'Calidez_Color', 'Textura']
    )

    # Asegurarse de que 'Product' sea la columna de identificación
    if 'Product' not in products_encoded.columns:
        raise ValueError("La columna 'Product' no está presente en los datos codificados.")

    # Eliminar columnas no numéricas
    products_numeric = products_encoded.drop(['Product'], axis=1, errors='ignore')
    return products_numeric

def calculate_similarity(reference_products, candidate_products, products_encoded):
    """
    Calcula la similitud del coseno entre productos de referencia y candidatos.
    """
    similarities = []
    for idx_rec in candidate_products.index:
        sim_scores = []
        for idx_ref in reference_products.index:
            sim = cosine_similarity(
                products_encoded.loc[[idx_ref]],
                products_encoded.loc[[idx_rec]]
            )[0][0]
            sim_scores.append(sim)
        similarities.append(np.mean(sim_scores))
    return similarities

def recommend_product(criteria, products_df, criterion_values):
    """
    Genera recomendaciones de productos basadas en criterios y similitud.
    """
    # Codificar características para cálculo de similitud
    products_encoded = encode_product_features(products_df)

    # Caso de un solo criterio
    if len(criteria) == 1:
        criterion = criteria[0]
        value = criterion_values[criterion]

        # Obtener productos de referencia y alternativas
        reference_products = products_df[products_df[criterion] == value]
        recommended = products_df[products_df[criterion] != value].copy()

        if not recommended.empty:
            # Calcular similitudes
            similarities = calculate_similarity(reference_products, recommended, products_encoded)
            recommended['Similitud'] = similarities
            return recommended.sort_values(['Similitud', 'Price'], ascending=[False, True]).drop_duplicates()

    # Caso de múltiples criterios
    recommended = products_df.copy()

    # Máscara para coincidencias exactas
    exact_match_mask = pd.Series(True, index=recommended.index)
    for criterion, value in criterion_values.items():
        exact_match_mask &= (recommended[criterion] == value)

    # Máscara para coincidencias parciales
    filter_mask = pd.Series(False, index=recommended.index)
    for criterion, value in criterion_values.items():
        filter_mask |= (recommended[criterion] == value)

    # Filtrar recomendaciones
    recommended = recommended[filter_mask & ~exact_match_mask]

    if not recommended.empty:
        # Calcular similitudes para múltiples criterios
        reference_products = products_df[exact_match_mask]
        similarities = calculate_similarity(reference_products, recommended, products_encoded)
        recommended['Similitud'] = similarities
        return recommended.sort_values(['Similitud', 'Price'], ascending=[False, True]).drop_duplicates()

    # Si no hay recomendaciones, usar primer criterio
    if len(criteria) > 1:
        primary_criterion = criteria[0]
        primary_value = criterion_values[primary_criterion]
        recommended = products_df[products_df[primary_criterion] == primary_value].copy()

        if not recommended.empty:
            reference_products = products_df[exact_match_mask]
            similarities = calculate_similarity(reference_products, recommended, products_encoded)
            recommended['Similitud'] = similarities
            return recommended.sort_values(['Similitud', 'Price'], ascending=[False, True]).drop_duplicates()

    return recommended.sort_values('Price').drop_duplicates()