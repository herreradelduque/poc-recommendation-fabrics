import pandas as pd
import random

# Diccionario con valores ficticios para las nuevas columnas
new_columns_data = {
    'Material': ['Algodón', 'Lino', 'Seda', 'Poliéster', 'Yute'],  # Ejemplo de materiales
    'Color': ['Rojo', 'Azul', 'Verde', 'Negro', 'Blanco'],  # Ejemplo de colores
    'Calidez_Color': ['Alta', 'Baja', 'Alta', 'Media', 'Baja'],  # Ejemplo de calidez del color
    'Textura': ['Suave', 'Grueso', 'Lisa', 'Rugoso', 'Aterciopelado']  # Ejemplo de texturas
}

# Función para generar precios basados en material y textura
def generate_price(material, texture):
    base_price = 100  # Precio base
    material_price = {
        'Algodón': 10, 'Lino': 15, 'Seda': 20, 'Poliéster': 5, 'Yute': 8
    }
    texture_price = {
        'Suave': 5, 'Grueso': 10, 'Lisa': 3, 'Rugoso': 8, 'Aterciopelado': 7
    }
    return base_price + material_price.get(material, 0) + texture_price.get(texture, 0)

# Crear combinaciones únicas de Producto, Categoría, Material y Textura
product_combinations = pd.DataFrame({
    'Product': ['Tejido A', 'Tejido B', 'Tejido C', 'Tejido D', 'Tejido E'],
    'Category': ['Ropa', 'Ropa', 'Accesorios', 'Accesorios', 'Mobiliario'],
    'Material': random.choices(new_columns_data['Material'], k=5),
    'Textura': random.choices(new_columns_data['Textura'], k=5),
    'Color': [random.sample(new_columns_data['Color'], 3) for _ in range(5)],  # Cada producto tiene 3 colores
    'Price': [generate_price(material, texture) for material, texture in zip(random.choices(new_columns_data['Material'], k=5), random.choices(new_columns_data['Textura'], k=5))]
})

# Expandir la lista de colores para hacer múltiples registros por combinación de producto, categoría, material y textura
expanded_data = []
for _, row in product_combinations.iterrows():
    for color in row['Color']:
        expanded_data.append({
            'Product': row['Product'],
            'Category': row['Category'],
            'Material': row['Material'],
            'Textura': row['Textura'],
            'Color': color,
            'Price': row['Price']
        })

# Crear un DataFrame final con las combinaciones únicas
final_products_df = pd.DataFrame(expanded_data)

# Guardar el CSV actualizado
csv_file = 'data/products.csv'  # Ruta para el nuevo archivo CSV
final_products_df.to_csv(csv_file, index=False)

print(f"CSV generado y guardado como: {csv_file}")
