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

        # Agregar botón de limpiar filtros
        if st.button("Limpiar Filtros"):
            # Reset session state for all filters
            for key in st.session_state.keys():
                if key.startswith("filter_"):
                    del st.session_state[key]
            #st.experimental_rerun()

        # Definir las columnas de filtrado disponibles (excluyendo Price y Color)
        filter_columns = [col for col in products.columns if col not in ['Price', 'Color']]

        # Crear filtros dinámicos
        filters = {}
        current_data = products.copy()

        for column in filter_columns:
            if len(current_data) > 0:  # Verificar si hay datos para filtrar
                # Usar session state para mantener el estado de los filtros
                key = f"filter_{column}"
                filters[column] = st.selectbox(
                    f"Selecciona {column}",
                    ['Todos'] + list(current_data[column].unique()),
                    key=key
                )

                # Aplicar filtro si se selecciona un valor específico
                if filters[column] != 'Todos':
                    current_data = current_data[current_data[column] == filters[column]]

        # Mostrar los resultados filtrados una sola vez al final
        if len(current_data) > 0:
            st.write("### Resultados encontrados")
            st.write(f"Se encontraron {len(current_data)} productos que coinciden con los filtros:")
            st.dataframe(current_data)
        else:
            st.warning("No se encontraron productos que coincidan con los filtros seleccionados.")
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