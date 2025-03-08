import streamlit as st
import pandas as pd
from helpers import load_products, recommend_product

def main():
    # Cargar los productos
    products = load_products('data/products.csv')

    # Título de la app en Streamlit
    st.title("Sistema de Recomendación de Tejidos")

    # Crear las pestañas
    tab1, tab2 = st.tabs(["Buscar Producto", "Recomendaciones"])

    # Pestaña 1: Buscar Producto
    with tab1:
        st.header("Buscar Producto en la Base de Datos")

        # Selector para elegir el producto
        product_name = st.selectbox("Selecciona un producto", products['Product'].unique())

        # Mostrar todos los registros del producto seleccionado
        st.write("**Todos los registros de este producto:**")
        all_records = products[products['Product'] == product_name]
        st.dataframe(all_records)  # Mostrar todos los registros del producto

    # Pestaña 2: Recomendaciones de Productos
    with tab2:
        st.header("Recomendaciones de Productos")

        # Selector para elegir el producto para recomendaciones
        product_name_for_recommendations = st.selectbox("Selecciona un producto para recomendaciones", products['Product'].unique())

        # Generar las recomendaciones
        recommended_products = recommend_product(product_name_for_recommendations, products)

        # Mostrar los productos recomendados
        st.write("**Productos recomendados:**")
        st.dataframe(recommended_products)

# Ejecutar la app de Streamlit
if __name__ == "__main__":
    main()
