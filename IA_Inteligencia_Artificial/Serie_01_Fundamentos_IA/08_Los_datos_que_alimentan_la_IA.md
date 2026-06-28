# Los datos que alimentan la IA
## Por qué los datos son el petróleo del siglo XXI y qué eso significa para ti

**Serie 1: Fundamentos de IA — Libro 8 de 10**

---

*Copyright © 2026 Enrique Padrón. Todos los derechos reservados. Ninguna parte de esta publicación puede ser reproducida, distribuida ni transmitida de ninguna forma ni por ningún medio sin el permiso previo por escrito del autor.*

---

> **Aviso legal:** El uso de la información de este libro es responsabilidad exclusiva del lector.

---

## Prólogo: El tesoro invisible de Isabel

La empresa de Isabel llevaba quince años registrando datos de empleados: evaluaciones de desempeño, tasas de rotación por departamento, resultados de encuestas de clima, patrones de asistencia, tiempo de permanencia en la empresa.

Quince años. Más de dos mil empleados. Decenas de variables por persona.

Cuando llegó el nuevo director de tecnología con la propuesta de "hacer algo con los datos de RRHH", Isabel entendió por primera vez lo que tenía entre manos. No era solo un archivo de historiales. Era un mapa del comportamiento organizacional acumulado durante quince años.

El problema: no sabía qué hacer con él. Ni siquiera sabía bien qué tenía.

---

## Capítulo 1: Por qué los datos son el ingrediente fundamental

Los sistemas de IA no se inventan el conocimiento: lo extraen de los datos.

Un modelo de diagnóstico médico aprende de millones de historiales clínicos. Un sistema de traducción aprende de miles de millones de pares de frases en distintos idiomas. Un LLM aprende de prácticamente todo el texto disponible en internet, libros y otras fuentes.

La calidad y cantidad de los datos de entrenamiento determina las capacidades del modelo resultante en formas que no pueden superarse solo con algoritmos mejores. Un algoritmo mediocre entrenado en datos excelentes supera a un algoritmo excelente entrenado en datos mediocres.

La expresión "los datos son el petróleo del siglo XXI" (atribuida a Clive Humby, matemático británico, 2006) captura algo real: los datos son el recurso estratégico que alimenta la economía de la IA, igual que el petróleo alimentó la economía industrial del siglo XX.

Con una diferencia importante: los datos, a diferencia del petróleo, no se consumen al usarlos. Se pueden copiar, combinar y reutilizar indefinidamente.

---

## Capítulo 2: Tipos de datos en IA

**Datos estructurados:** Organizados en tablas con filas y columnas. Bases de datos relacionales, hojas de cálculo, registros transaccionales. La IA clásica de predicción (machine learning tabular) es muy eficaz con este tipo de datos. Los datos de RRHH de Isabel son mayormente estructurados.

**Datos no estructurados:** Texto, imágenes, audio, vídeo. No tienen una organización tabular predefinida. El 80-90% de los datos generados en el mundo son no estructurados. Los LLMs y los modelos de visión operan principalmente con datos no estructurados.

**Datos semiestructurados:** JSON, XML, emails, páginas web. Tienen alguna organización (etiquetas, jerarquías) pero no el esquema rígido de las bases de datos relacionales.

**Datos sintéticos:** Generados por modelos de IA en lugar de por procesos del mundo real. Útiles cuando los datos reales son escasos, privados o costosos de obtener.

---

## Capítulo 3: Cómo se entrena un LLM: los datos en práctica

Para entrenar GPT-3, OpenAI uso aproximadamente:
- **Common Crawl:** 570 gigabytes de texto extraído de páginas web (después de filtrado)
- **WebText2:** Texto de páginas web enlazadas desde Reddit con alta valoración
- **Books1 y Books2:** Libros digitalizados
- **Wikipedia en inglés**

La cantidad total fue de aproximadamente 570 GB de texto, equivalente a cientos de miles de libros.

Los modelos más recientes usaron órdenes de magnitud más datos. El conjunto de entrenamiento de Llama 2 (Meta, 2023) fue de 2 billones de tokens. El de GPT-4 no ha sido revelado públicamente pero se estima en magnitudes similares o superiores.

La curaduría de estos datos —decidir qué incluir y qué filtrar— es una de las decisiones más importantes y menos transparentes del proceso de entrenamiento.

---

## Capítulo 4: El problema de la calidad de los datos

No todos los datos son igual de valiosos para el entrenamiento.

El texto de Wikipedia es denso en hechos, bien estructurado y relativamente libre de errores. El texto de redes sociales tiene mucho ruido, argot, errores ortográficos y contexto efímero.

Los equipos de entrenamiento de los grandes modelos dedican enormes esfuerzos a:
- **Filtrado:** Eliminar contenido pornográfico, violento, spam o de baja calidad
- **Deduplicación:** Eliminar texto repetido (que haría que el modelo sobreaprendiera ciertos patrones)
- **Normalización:** Estandarizar codificaciones, formatos y caracteres
- **Muestreo ponderado:** Dar más peso a fuentes de alta calidad

Las decisiones de curaduría de datos tienen consecuencias profundas en el comportamiento del modelo, incluyendo sus sesgos, sus lagunas de conocimiento y su distribución de idiomas y perspectivas.

---

## Capítulo 5: El sesgo en los datos

Los datos de entrenamiento no son una muestra representativa del mundo: son una muestra de lo que existe en formato digital, con el sesgo de quién produce ese contenido.

**Sesgo de representación:** Internet y los libros digitalizados sobrerepresentan ciertas lenguas (inglés), culturas (occidentales), demografías (hombres, clases medias-altas) y perspectivas. Los modelos entrenados en estos datos heredan esas sobrerepresentaciones.

**Sesgo histórico:** Los datos reflejan el estado del mundo en el momento en que fueron creados, incluyendo las inequidades de ese mundo. Un modelo entrenado en textos históricos aprende las actitudes hacía género, raza y otras categorías presentes en esos textos.

**Sesgo de selección:** Las decisiones sobre qué datos incluir y cuáles excluir son tomadas por humanos con sus propios valores y puntos de vista.

**Amplificación del sesgo:** Los modelos no solo reproducen los sesgos de los datos: a veces los amplifican, especialmente en tareas de predicción.

---

## Capítulo 6: La propiedad intelectual y los datos de entrenamiento

Una de las controversias legales más importantes del momento: ¿pueden los modelos de IA entrenarse con contenido con copyright sin permiso o compensación a los autores?

**La posición de las empresas de IA:** El entrenamiento en texto protegido por copyright constituye "uso justo" (fair use) bajo la ley estadounidense, ya que el modelo aprende patrones, no memoriza contenido.

**La posición de los creadores:** Los modelos son entrenados con el trabajo de escritores, artistas, músicos y periodistas sin su consentimiento ni compensación, y luego compiten con ellos.

**El estado legal:** Hay docenas de litigios en curso. The New York Times demandó a OpenAI y Microsoft. Getty Images demandó a Stability AI. Escritores, músicos y artistas han presentado demandas colectivas.

El resultado legal determinará la arquitectura económica del ecosistema de IA para la próxima generación.

---

## Capítulo 7: Los datos propios como ventaja competitiva

Para las empresas, los datos propios —datos generados por sus propias operaciones, clientes y procesos— son una ventaja competitiva que los competidores no pueden replicar.

Un hospital con diez años de historiales clínicos de pacientes tiene una base de datos única para entrenar modelos de diagnóstico específicos para su población.

Una plataforma de e-commerce con el historial de compras de millones de usuarios puede entrenar sistemas de recomendación superiores a los de competidores con menos datos.

La empresa de Isabel tiene quince años de datos de RRHH que podrían usarse para predecir rotación, identificar empleados en riesgo de burnout, o correlacionar prácticas de gestión con resultados organizacionales.

El valor no está en los datos por sí mismos: está en la combinación de datos únicos con las preguntas correctas y las herramientas adecuadas.

---

## Capítulo 8: Privacidad y datos

Los datos más valiosos para la IA son frecuentemente los más privados: datos médicos, financieros, de comportamiento, de comunicaciones.

El equilibrio entre la utilidad de los datos y la privacidad de las personas es una de las tensiones más importantes de la era de la IA.

Las aproximaciones técnicas incluyen:
- **Federated learning:** El modelo se entrena en los dispositivos de los usuarios sin que los datos salgan del dispositivo.
- **Differential privacy:** Se añade ruido matemático a los datos de entrenamiento para proteger la privacidad individual mientras se preservan los patrones estadísticos.
- **Synthetic data:** Se generan datos artificiales que tienen las mismas propiedades estadísticas que los datos reales sin contener información personal real.

El marcó regulatorio europeo (GDPR) y sus equivalentes globales establecen restricciones sobre cómo los datos personales pueden ser usados para entrenamiento de IA.

---

## Capítulo 9: El futuro: ¿escasez de datos?

Hay una pregunta que inquieta a los investigadores: ¿hay suficiente texto de calidad en internet para entrenar la próxima generación de modelos?

Algunos análisis sugieren que el texto de alta calidad disponible en internet podría ser insuficiente para los modelos del futuro sin reutilización masiva.

Las respuestas del campo incluyen:
- **Datos sintéticos:** Usar modelos actuales para generar datos de entrenamiento para modelos futuros (hay debates sobre si esto funciona o produce "degeneración del modelo")
- **Datos multimodales:** Entrenar en imágenes, vídeo y audio además de texto
- **Datos propietarios:** Acuerdos con editoriales, plataformas y otras fuentes de datos de calidad
- **Eficiencia:** Entrenar modelos más pequeños y eficientes que requieran menos datos

La escasez de datos podría ser el próximo cuello de botella del escalado de la IA, después de la potencia computacional.

---

## Capítulo 10: Lo que Isabel hizo con sus datos

El director de tecnología de Isabel le propuso un proyecto piloto: analizar los datos de RRHH para identificar predictores de rotación involuntaria.

El primer paso no fue la IA: fue entender qué datos existían realmente, qué calidad tenían, qué variables faltaban y cuáles eran fiables. Tres semanas de trabajo de limpieza y documentación antes de entrenar el primer modelo.

El resultado: un modelo que predecía con un 73% de precisión qué empleados tenían alta probabilidad de abandonar la empresa en los próximos seis meses. No perfecto. Pero suficientemente bueno para enfocar las conversaciones de retención donde más importaban.

La lección de Isabel: los datos ya estaban ahí. El valor no estaba en tenerlos, sino en saber qué preguntar y cómo preparar los datos para responder esas preguntas.

Eso es cierto para cualquier organización. Los datos son el recurso. El criterio es la ventaja.

---

## Epílogo: El mundo como datos

Cada clic, cada búsqueda, cada compra, cada mensaje, cada imagen capturada por una cámara urbana: el mundo moderno genera datos continuamente.

Esta generación masiva de datos no fue diseñada para entrenar modelos de IA. Fue el resultado de digitalizar procesos que antes eran analógicos.

Que ese subproducto de la digitalización resulte ser el combustible de la mayor transformación tecnológica de la historia es una de las ironías más interesantes del siglo XXI.

Y la próxima vez que aceptes los términos y condiciones de una aplicación, recuerda: estás contribuyendo al corpus.

---

*Este es el Libro 8 de la colección Inteligencia Artificial Aplicada, Libro 8 de 10 de la Serie 1: Fundamentos de IA.*

---

*Si este libro te ha resultado útil, considera dejar una reseña en Amazon. Solo lleva un minuto y marca una gran diferencia para los autores independientes.*

---

## Sobre el Autor

Enrique Padrón nació en las Islas Canarias, España. Veinticinco años en distintas empresas le enseñaron algo que pocos se atreven a decir: las personas no fracasan por falta de información, fracasan porque nadie les dio las herramientas correctas en el momento exacto. Esta colección existe para cambiar eso. Cada libro destila lo que realmente funciona, sin relleno, sin teoría vacía. Desarrollada con el apoyo de inteligencia artificial para llevar ese conocimiento más lejos de lo que cualquier autor podría alcanzar solo.