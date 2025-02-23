# Mi proyecto
1) Qué es, que aplicaciones tiene y como implemento en postgres Bases de Datos Vectoriales?
   
Una base de datos vectorial es un sistema diseñado para almacenar, gestionar y consultar datos representados como vectores numéricos (arrays de números) en un espacio multidimensional. Estos vectores suelen ser embeddings generados por modelos de machine learning, que codifican información compleja (como texto, imágenes o datos estructurados) en una forma numérica que captura similitudes semánticas o relaciones.

¿Que aplicaciones tiene las Bases de Datos Vectoriales?

Búsqueda semántica: En nuestro caso, se podría buscar CVEs con descripciones similares a una consulta (ej. "buffer overflow") sin depender de coincidencias exactas de palabras, sino de significado.
Análisis de ciberseguridad: Identificar patrones o agrupar vulnerabilidades relacionadas (ej. clustering de CVEs por tipo de ataque) basado en sus embeddings.
Recomendaciones: Sugerir medidas de mitigación basadas en similitudes entre CVEs históricos.
Detección de anomalías: Comparar nuevos CVEs con un conjunto existente para detectar outliers.

¿Cómo implemeto en postgres Base de Datos Vectoriales?

1. Instalando sentence-transformers: pip install sentence-transformers.
2. Asegurarse de que pgvector esté disponible en el PostgreSQL utilizado.

3) Qué es y que aplicaciones tienen los Datalakes?

Segun lo investigado un datalake es un repositorio centralizado que almacena grandes volúmenes de datos en su formato original (crudo), ya sean estructurados (como nuestro DataFrame de CVEs), semi-estructurados (JSON de la API) o no estructurados (logs de texto). A diferencia de una base de datos tradicional como PostgreSQL, un datalake no impone un esquema estricto al ingreso, lo que lo hace ideal para datos heterogéneos y análisis posteriores.

En nuestro deber un datalake podría almacenar no solo los datos procesados de CVEs, sino también las respuestas JSON crudas de la API, logs de solicitudes fallidas (como el 404 que obtuvimos), o incluso datos adicionales como capturas de tráfico de red.

¿Qué aplicaciones tienen los Datalakes?

Análisis de ciberseguridad: En nuestra tarea por ejemplo se podría guardar todas las respuestas de la API NIST (incluso las no procesadas) en un datalake para analizar tendencias a largo plazo, como la frecuencia de vulnerabilidades por año.
Big Data: Combinar los CVEs con otros datos (ej. logs de servidores, reportes de incidentes) para correlacionar eventos de seguridad.
Machine Learning: Usar los datos crudos del datalake para entrenar modelos que predigan severidad o clasifiquen vulnerabilidades.
Almacenamiento histórico: Mantener un archivo de todos los CVEs obtenidos sin preocuparte por estructurarlos inmediatamente, permitiendo consultas futuras.
