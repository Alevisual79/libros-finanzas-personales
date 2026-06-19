# Los grandes modelos de lenguaje
## Por qué ChatGPT no sabe nada pero parece que sabe todo

**Serie 1: Fundamentos de IA — Libro 4 de 10**

---

## Prólogo: La pregunta de la analítica

Rubén llevaba semanas usando ChatGPT para sus propuestas de marketing. Un día le preguntó por las ventas de un producto específico de su cliente. El modelo respondió con cifras detalladas, tendencias, comparativas con el sector. Todo perfectamente redactado.

El problema: las cifras eran completamente inventadas. El modelo nunca había tenido acceso a los datos de ese cliente. Había generado texto plausible sobre ventas de ese tipo de producto.

Rubén casi envió esa propuesta a su cliente. Llegó a tiempo para verificar los datos.

Esa experiencia le hizo entender algo fundamental sobre los LLMs: no saben nada. Predicen texto.

---

## Capítulo 1: La arquitectura Transformer

Antes de los Transformers, los modelos de lenguaje procesaban el texto secuencialmente, palabra por palabra. Para textos largos, "olvidaban" el principio cuando llegaban al final.

El paper de 2017 "Attention is all you need" (Vaswani et al., Google) introdujo la arquitectura Transformer, que cambió radicalmente este enfoque.

La innovación clave: el mecanismo de **atención**. En lugar de procesar el texto secuencialmente, el Transformer puede "atender" a cualquier parte del texto al procesar cualquier otra parte. Al generar la palabra "él" en una oración larga, puede referirse directamente al sustantivo que está cuatro frases antes.

Esta capacidad de capturar dependencias de largo alcance, combinada con su paralelización eficiente, hizo que los Transformers dominaran el procesamiento de lenguaje natural.

---

## Capítulo 2: De GPT-1 a los modelos actuales

La familia GPT (Generative Pre-trained Transformer) de OpenAI ilustra la aceleración del campo:

**GPT-1 (2018):** 117 millones de parámetros. Primer modelo que demostró que pre-entrenar en texto general y ajustar para tareas específicas era más eficiente que entrenar desde cero para cada tarea.

**GPT-2 (2019):** 1.5 mil millones de parámetros. OpenAI inicialmente no lo publicó completo por miedo a su uso malicioso para generar desinformación. En perspectiva, era considerablemente menos capaz que los modelos actuales.

**GPT-3 (2020):** 175 mil millones de parámetros. El primer modelo que demostró capacidades emergentes sorprendentes: sin entrenamiento específico, podía realizar tareas que no estaban en su conjunto de entrenamiento.

**GPT-4 (2023):** Capacidades muy superiores. Supera a humanos en múltiples benchmarks académicos estandarizados.

En paralelo, Anthropic desarrolló Claude, Google desarrolló Gemini y PaLM, Meta publicó Llama (de código abierto), y decenas de empresas más entrenaron sus propios modelos.

---

## Capítulo 3: Cómo funciona la predicción de texto

Un LLM funciona prediciendo el siguiente token dado el contexto anterior.

Un **token** no es exactamente una palabra: es una unidad de texto que puede ser una palabra, parte de una palabra, o un signo de puntuación. GPT-4 tiene un vocabulario de aproximadamente 100,000 tokens.

Para cada token posible, el modelo produce una probabilidad. "The cat sat on the ___" podría producir: "mat" (0.25), "floor" (0.18), "couch" (0.12), "table" (0.09)... El siguiente token se selecciona de acuerdo a esas probabilidades (con parámetros que controlan el nivel de aleatoriedad).

Este proceso se repite recursivamente. El token generado se añade al contexto, y se predice el siguiente. Así hasta que el modelo genera el token de fin de secuencia o se alcanza la longitud máxima.

Todo el proceso es estadístico: el modelo no "decide" qué escribir; produce distribuciones de probabilidad sobre tokens.

---

## Capítulo 4: El pre-entrenamiento y el fine-tuning

Los LLMs modernos se entrenan en dos fases.

**Pre-entrenamiento:** El modelo aprende a predecir texto en cantidades masivas de datos: libros, artículos, páginas web, código, conversaciones. Aprende la estructura del lenguaje, los hechos del mundo, las convenciones de distintos géneros y estilos. Este entrenamiento cuesta decenas o cientos de millones de dólares.

**Fine-tuning y RLHF:** El modelo base pre-entrenado predice texto, pero no necesariamente de la forma útil para un asistente. El fine-tuning (ajuste fino) entrena el modelo con ejemplos de conversaciones de alta calidad, y el RLHF (Reinforcement Learning from Human Feedback) usa evaluadores humanos para guiar al modelo hacia respuestas más útiles, honestas y seguras.

Este segundo paso es el que convierte el modelo base en un asistente como ChatGPT o Claude.

---

## Capítulo 5: La ventana de contexto

Los LLMs tienen una **ventana de contexto**: la cantidad máxima de texto que pueden "ver" a la vez.

Los primeros GPT tenían ventanas de 2,048 tokens (aproximadamente 1,500 palabras). Los modelos actuales tienen ventanas de 128,000, 200,000 o incluso 1 millón de tokens.

La ventana de contexto determina qué puede usar el modelo para generar su respuesta: los mensajes anteriores de la conversación, los documentos que se le proporcionan, las instrucciones del sistema.

Lo que está fuera de la ventana de contexto, el modelo no lo "sabe". No tiene memoria entre conversaciones (a menos que se implemente explícitamente). Cada conversación empieza desde cero.

Este es uno de los factores que explican por qué los LLMs dan respuestas inconsistentes en diferentes conversaciones.

---

## Capítulo 6: Capacidades emergentes

Una de las observaciones más sorprendentes en el desarrollo de los LLMs es la aparición de **capacidades emergentes**: habilidades que aparecen de repente en modelos más grandes sin estar presentes en modelos más pequeños.

Modelos pequeños fallan en aritmética de varios dígitos. En un umbral de tamaño, los modelos más grandes lo resuelven casi perfectamente. No hubo entrenamiento específico para eso: emergió del escala.

El razonamiento en cadena (chain-of-thought), la aritmética, la traducción de idiomas de baja frecuencia, la escritura de código: todas son capacidades que emergieron con el escalado.

Esto hace que predecir qué podrán hacer los modelos futuros sea extraordinariamente difícil. Hay capacidades que no existen hoy que podrían emerger con el próximo escalado.

---

## Capítulo 7: Por qué alucinan los LLMs

Las alucinaciones —generar información falsa con confianza— son el problema más conocido de los LLMs.

La causa es estructural: el objetivo de entrenamiento es predecir texto plausible, no texto verdadero. No hay un mecanismo interno que distinga entre "texto que refleja hechos reales" y "texto que suena como si reflejara hechos reales".

Cuando el modelo llega a una pregunta sobre la que tiene información en sus datos de entrenamiento, produce texto consistente con esa información. Cuando llega a una pregunta sobre la que no tiene información —o sobre eventos posteriores a su fecha de corte—, produce texto plausible en el mismo estilo con confianza similar.

Los factores que reducen las alucinaciones incluyen: el fine-tuning para admitir ignorancia, el acceso a fuentes externas en tiempo real (retrieval-augmented generation), y la instrucción explícita de citar fuentes.

Pero las alucinaciones no se eliminan completamente con los sistemas actuales. Son una característica estructural del enfoque, no un bug que se pueda parchear.

---

## Capítulo 8: El problema de la fecha de corte

Los LLMs tienen una **fecha de corte**: la fecha hasta la que tienen datos de entrenamiento. Después de esa fecha, no tienen conocimiento de eventos.

GPT-4 tiene una fecha de corte en 2023. Preguntas sobre eventos de 2024 o 2025 solo pueden ser respondidas correctamente si el modelo tiene acceso a búsqueda web en tiempo real.

Sin acceso a internet, los modelos responden preguntas sobre eventos recientes de dos formas: admitiendo que no saben (comportamiento deseable) o inventando información plausible (comportamiento indeseable que ocurre).

La solución más común es RAG (Retrieval-Augmented Generation): conectar el modelo a una base de datos o al internet para recuperar información actualizada antes de generar la respuesta.

---

## Capítulo 9: Modelos propietarios vs. modelos abiertos

El ecosistema de LLMs tiene dos grandes categorías:

**Modelos propietarios:** GPT-4 (OpenAI), Claude (Anthropic), Gemini (Google). Solo accesibles a través de APIs de pago. Las compañías no revelan sus arquitecturas, datos de entrenamiento o parámetros completos. Tienden a ser los modelos más capaces.

**Modelos de código abierto:** Llama (Meta), Mistral, Falcon, Qwen. Disponibles para descargar y ejecutar localmente o modificar. La transparencia permite auditorías independientes y personalización, pero la responsabilidad de su uso se traslada al operador.

La brecha de capacidad entre los mejores modelos propietarios y los mejores modelos abiertos se ha reducido significativamente. Llama 3.1 (405B parámetros) es competitivo con GPT-4 en muchas tareas.

---

## Capítulo 10: Cómo usarlos bien

El error más común al usar LLMs es tratarlos como bases de datos de hechos. No lo son. Son generadores de texto plausible.

Las tareas en que los LLMs brillan:
- Redacción, edición y mejora de texto
- Síntesis de documentos proporcionados al modelo
- Generación de borradores, ideas, estructuras
- Explicación de conceptos
- Transformación de formato o estilo
- Código (con verificación externa)

Las tareas que requieren cautela:
- Verificación de hechos (siempre verificar externamente)
- Información actualizada (comprobar fecha de corte o usar acceso web)
- Cálculos matemáticos complejos (usar herramientas de cálculo)
- Información médica, legal o financiera de alta importancia (consultar profesionales)

Rubén aprendió su lección. A partir de entonces, cuando pedía datos al modelo, siempre añadía la instrucción: "Si no tienes información verificada sobre esto, dímelo en lugar de inventar cifras." Una instrucción simple que cambió la calidad de sus outputs.

---

## Epílogo: La paradoja de la competencia

Un LLM puede explicar la teoría cuántica de campos mejor que la mayoría de físicos. Y puede equivocarse en que el Papa actual es Benedicto XVI.

Esta paradoja —competencia extraordinaria combinada con errores básicos y predecibles— es la característica más importante de los LLMs para quien los usa.

No son omniscientes ni estúpidos. Son herramientas estadísticas entrenadas en texto humano, con las fortalezas y limitaciones que eso implica.

Entender esto no los hace menos útiles. Los hace útiles de la forma correcta.

---

*Este es el Libro 4 de la colección Inteligencia Artificial Aplicada, Libro 4 de 10 de la Serie 1: Fundamentos de IA.*
