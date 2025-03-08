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

def recommend_product(product_name, products):
    """
    Genera recomendaciones para un producto basado en su similitud con otros productos.
    """
    # Codificar las características de los productos
    products_encoded = encode_product_features(products)

    # Extraer las columnas numéricas
    products_numeric = products_encoded.drop('Product', axis=1, errors='ignore')  # Asegurarse de no eliminar 'Product' si no existe

    # Obtener el índice del producto seleccionado
    product_idx = get_product_index(products, product_name)

    # Calcular la matriz de similitudes
    similarity_matrix = calculate_similarity(products_numeric)

    # Obtener las recomendaciones (similitudes más altas)
    recommendations = similarity_matrix[product_idx]

    # Ordenar las recomendaciones por similitud (de mayor a menor)
    recommended_indices = recommendations.argsort()[-4:-1][::-1]  # Top 3 recomendaciones

    # Obtener los productos recomendados con toda su información
    recommended_products = products.iloc[recommended_indices]

    # Eliminar el producto seleccionado de las recomendaciones (si aparece)
    recommended_products = recommended_products[recommended_products['Product'] != product_name]

    return recommended_products
