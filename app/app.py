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
        product_category = st.selectbox("Selecciona un material", all_records['Material'].unique())
        all_records = all_records[all_records['Material'] == product_category]
        st.dataframe(all_records)  # Mostrar todos los registros del producto

    # Pestaña 2: Recomendaciones de Productos
    with tab2:
        st.header("Recomendaciones de Productos")

        # Crear checkboxes para seleccionar la columna de recomendación
        available_columns = [col for col in products.columns if col not in ['Price', 'Product']]

        # Contenedor horizontal para los checkboxes
        cols = st.columns(len(available_columns))
        selected_criterion = None

        # Crear un checkbox para cada columna
        for i, column in enumerate(available_columns):
            with cols[i]:
                if st.checkbox(column, key=f"check_{column}"):
                    # Desactivar los otros checkboxes
                    for other_col in available_columns:
                        if other_col != column and st.session_state.get(f"check_{other_col}"):
                            st.session_state[f"check_{other_col}"] = False
                    selected_criterion = column

        if selected_criterion:
            # Obtener valores únicos de la columna seleccionada
            unique_values = products[selected_criterion].unique()

            # Selector para elegir el valor específico
            selected_value = st.selectbox(
                f"Selecciona un valor de {selected_criterion}",
                unique_values
            )

            # Generar las recomendaciones basadas en el criterio y valor seleccionados
            recommended_products = recommend_product(
                selected_criterion,
                products,
                criterion_value=selected_value
            )

            # Mostrar los productos recomendados
            st.write(f"**Productos recomendados con {selected_criterion} = {selected_value}:**")
            st.dataframe(recommended_products)

# Ejecutar la app de Streamlit
if __name__ == "__main__":
    main()
