# Manual de Uso - AutoGravity Analytics 2.0 🚀

Bienvenido a la versión 2.0 de AutoGravity Analytics. Esta herramienta ha sido rediseñada para ofrecer métricas de negocio precisas y dashboards de alto impacto visual sin depender de servicios de terceros ni IA.

## 🌟 Novedades v2.0
*   **Sin Dependencias de IA**: No requiere API Keys ni internet para funcionar.
*   **Bento Grid Interface**: Nuevo diseño moderno con tarjetas de KPIs y modo oscuro.
*   **Nuevas Métricas**: Tasa de Comprensión (AWT), Eficiencia de Formato, Mapa de Calor Regional.

## 🛠️ Instalación y Ejecución

1.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Iniciar Dashboard**:
    ```bash
    streamlit run app.py
    ```

## 📂 Formato de Datos (Excel)

El sistema espera un archivo Excel con una hoja llamada **"Dataset"**. 

### Columnas Requeridas
El sistema detecta automáticamente columnas en inglés o español.

| Métrica | Columnas Excel Reconocidas |
| :--- | :--- |
| **Tiempo Visto** | `watch_time`, `minutos_vistos`, `screentime` |
| **Usuario** | `user_id`, `usuario` |
| **Género** | `genre`, `genero` |
| **Formato Video** | `video_format`, `format`, `calidad`, `resolucion` (Ej: 'HD', '4K') |
| **Idioma Audio** | `audio_lang`, `language`, `idioma` (Ej: 'es', 'en') |
| **Región** | `region`, `zona` |
| **Dispositivo** | `device`, `dispositivo` |
| **Duración Content**| `duration`, `duracion`, `length` |

## 🖥️ Uso del Dashboard

### 1. KPIs Superiores
*   **Total Screentime**: Minutos totales consumidos.
*   **Active Users**: Clientes únicos detectados.
*   **Avg Completion**: Porcentaje promedio de video visto (Engagegement Score).

### 2. Pestañas de Análisis
*   **Content Intelligence**: Descubre qué formatos (HD/4K) e idiomas prefieren tus usuarios.
*   **Infrastructure**: Analiza fallas o preferencias por Dispositivo (Smart TV vs Móvil).
*   **Segmentation**: Clusters de usuarios basados en su comportamiento.

### 3. Filtros
Usa la barra lateral para filtrar TODA la data por Dispositivo, Región o Segmento.
