import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def load_products(file_path='data/products.csv'):
    """
    Carga los productos desde un archivo CSV.
    """
    products = pd.read_csv(file_path)
    return products

def encode_product_features(products):
    """
    Codifica las características categóricas de los productos (como 'Material', 'Color', etc.)
    y devuelve los productos con las columnas numéricas necesarias para la recomendación.
    """
    # Convertir las características categóricas en variables dummy (one-hot encoding)
    products_encoded = pd.get_dummies(products, columns=['Category', 'Material', 'Color', 'Calidez_Color', 'Textura'])

    # Asegurarse de que 'Product' sea la columna de identificación
    if 'Product' not in products_encoded.columns:
        raise ValueError("La columna 'Product' no está presente en los datos codificados.")

    # Eliminar la columna 'Product' para la similitud
    products_numeric = products_encoded.drop('Product', axis=1, errors='ignore')  # Eliminar solo si existe
    return products_numeric

def get_product_index(products, product_name):
    """
    Devuelve el índice del producto seleccionado.
    """
    return products[products['Product'] == product_name].index[0]

def calculate_similarity(products_numeric):
    """
    Calcula la matriz de similitud entre productos.
    """
    similarity_matrix = cosine_similarity(products_numeric)
    return similarity_matrix

def recommend_product(criterion, products, criterion_value, n_recommendations=3):
    """
    Genera recomendaciones basadas en un criterio específico usando similitud del coseno.

    Args:
        criterion (str): Columna a utilizar para la recomendación
        products (pd.DataFrame): DataFrame con todos los productos
        criterion_value: Valor específico del criterio seleccionado
        n_recommendations (int): Número de recomendaciones a devolver
    """
    # Filtrar productos que coincidan con el criterio
    base_products = products[products[criterion] == criterion_value]

    # Codificar las características de los productos
    products_encoded = encode_product_features(products)

    # Extraer las columnas numéricas
    products_numeric = products_encoded.drop('Product', axis=1, errors='ignore')

    # Calcular la matriz de similitudes
    similarity_matrix = calculate_similarity(products_numeric)

    # Obtener los índices de los productos base
    base_indices = base_products.index

    # Calcular la similitud promedio con todos los productos base
    avg_similarities = similarity_matrix[base_indices].mean(axis=0)

    # Ordenar por similitud (excluyendo los productos base)
    recommended_indices = avg_similarities.argsort()[::-1]

    # Filtrar los productos que ya están en la base
    recommended_indices = [idx for idx in recommended_indices if idx not in base_indices]

    # Seleccionar los top n productos recomendados
    recommended_indices = recommended_indices[:n_recommendations]

    # Obtener los productos recomendados
    recommended_products = products.iloc[recommended_indices]

    return recommended_products
