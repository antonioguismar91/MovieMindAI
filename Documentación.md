# 📘 Documentación del Proyecto - MovieMind IA

Este documento detalla desde el uso básico para el usuario final hasta los desafíos técnicos superados durante el desarrollo de **MovieMind IA**.

---

## 📖 1. Manual de Usuario (Guía Rápida)

Para disfrutar de la mejor experiencia con el recomendador, sigue estos pasos:

### Uso Básico:
1.  **Búsqueda:** Introduce tu consulta en lenguaje natural (ej: *"películas de suspense psicológico con finales inesperados"*).
2.  **Exploración:** Analiza las 3 tarjetas generadas. Cada una incluye su género, nota de IMDb y una sinopsis optimizada.
3.  **Gestión de Biblioteca:** Si decides ver una película o ya la has visto, marca el checkbox **"La veré"**. Esto la registrará en tu historial para no volver a recomendarla.
4.  **Feedback:** Califica la recomendación con el sistema de estrellas. Este paso es vital para que la IA entienda tus gustos futuros.

### Sección de Estadísticas:
En la parte inferior, encontrarás tu **"Perfil Cinéfilo"**, donde el sistema analiza tus tendencias y muestra un resumen de tus géneros más votados.

---

## 📋 2. Instalación y Puesta en Marcha

Para ejecutar este proyecto en local, sigue estas instrucciones:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/MovieMindAI.git](https://github.com/tu-usuario/MovieMindAI.git)
    cd MovieMindAI
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configurar la API Key:**
    Edita el archivo `app.py` e introduce tu `API_KEY` de Groq en la sección de configuración inicial.

4.  **Ejecutar la aplicación:**
    ```bash
    streamlit run app.py
    ```

---

## 🛠️ 3. Stack Tecnológico

El proyecto utiliza un conjunto de herramientas modernas para garantizar velocidad y precisión:

* **Lenguaje:** Python 3.14 (Versión de desarrollo).
* **Framework:** Streamlit (Interfaz de usuario interactiva).
* **IA:** Groq Cloud API (Modelo Llama-3.3-70b-versatile).
* **Persistencia de datos:** Pandas & CSV (Almacenamiento local ligero).

---

## 🏗️ 4. Arquitectura del Proyecto

El sistema opera bajo un ciclo de vida de datos circular:

1.  **Entrada:** Captura de la consulta del usuario.
2.  **Contextualización:** Lectura de `historial.csv` para recuperar la "lista negra" de películas vistas y el contexto de votos previos.
3.  **Prompt Engineering:** Generación de un *System Prompt* dinámico con instrucciones de prohibición y formato.
4.  **Inferencia:** Procesamiento de la consulta mediante el modelo Llama 3.3.
5.  **Parsing (Extracción):** Uso de **Regex** para desglosar la respuesta de la IA en componentes visuales.
6.  **Persistencia:** Registro de la interacción y actualización de la biblioteca del usuario.

---

## 🚀 5. Retos Técnicos y Soluciones

Durante el desarrollo nos enfrentamos a desafíos críticos que moldearon la app actual:

### A. El problema de la "Memoria a Corto Plazo"
**Reto:** La IA recomendaba títulos redundantes que el usuario ya conocía.
**Solución:** Inyección de una "lista negra" dinámica en el mensaje del sistema, extrayendo los valores únicos de la columna `Vistas` del CSV.

### B. Diseño Visual Mediante Parsing
**Reto:** La respuesta de la IA era un bloque de texto difícil de leer.
**Solución:** Se implementó un extractor basado en expresiones regulares que busca patrones de iconos (`🎭`, `⭐`, `📝`) para mapear la información en tarjetas HTML con bordes dorados y altura simétrica.

### C. Colisiones de ID en Streamlit
**Reto:** Errores de `DuplicateElementId` al generar múltiples componentes dinámicos.
**Solución:** Uso de `keys` únicas combinando el índice del bucle con fragmentos del título de la película.

---

## 📈 6. Informe de Proyecto y Mejoras Futuras

MovieMind IA ha evolucionado de un simple script de chat a una herramienta de gestión personal de cine con interfaz premium.

**Próximos pasos previstos:**
* **Posters Reales:** Conexión con la API de TMDB para mostrar imágenes de las películas.
* **Tráilers:** Botones directos a YouTube mediante búsqueda automatizada.
* **Escalabilidad:** Migración del almacenamiento CSV a una base de datos SQLite.
