import streamlit as st
import pandas as pd
from helpers import load_products, recommend_product

def main():
    # Cargar los productos
    products = load_products('data/products.csv')

    # Título de la app
    st.title("Sistema de Recomendación de Tejidos")

    # Crear pestañas
    tab1, tab2 = st.tabs(["Buscar Producto", "Recomendaciones"])

    # Pestaña 1: Buscar Producto
    with tab1:
        st.header("Buscar Producto en la Base de Datos")

        product_name = st.selectbox("Selecciona un producto", products['Product'].unique())

        all_records = products[products['Product'] == product_name]
        product_category = st.selectbox(
            "Selecciona un material",
            all_records['Material'].unique()
        )

        filtered_records = all_records[all_records['Material'] == product_category]
        st.write("**Registros del producto:**")
        st.dataframe(filtered_records)

    # Pestaña 2: Recomendaciones
    with tab2:
        st.header("Recomendaciones de Productos")

        # Columnas disponibles para filtrar
        available_columns = [col for col in products.columns if col not in ['Price', 'Color']]

        # Crear checkboxes en columnas
        cols = st.columns(len(available_columns))
        selected_criteria = []

        for i, column in enumerate(available_columns):
            with cols[i]:
                if st.checkbox(column, key=f"check_{column}"):
                    selected_criteria.append(column)

        # Validar número de criterios
        if len(selected_criteria) > 3:
            st.warning("Por favor selecciona un máximo de 3 criterios")
        elif selected_criteria:
            # Crear selectores y generar recomendaciones
            selected_values = {}

            # Contenedor para los selectores
            with st.container():
                for criterion in selected_criteria:
                    unique_values = products[criterion].unique()
                    selected_values[criterion] = st.selectbox(
                        f"Selecciona {criterion}",
                        unique_values,
                        key=f"select_{criterion}"
                    )

            # Generar y mostrar recomendaciones
            if selected_values:
                recommended_products = recommend_product(
                    selected_criteria,
                    products,
                    criterion_values=selected_values
                )

                criteria_text = " Y ".join([f"{k}: {v}" for k, v in selected_values.items()])
                st.write(f"**Productos recomendados basados en {criteria_text}:**")

                # Mostrar recomendaciones con formato
                if 'Similitud' in recommended_products.columns:
                    recommended_products['Similitud'] = recommended_products['Similitud'].round(3)
                st.dataframe(recommended_products)

if __name__ == "__main__":
    main()