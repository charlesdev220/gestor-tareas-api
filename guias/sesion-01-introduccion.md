# Sesión 01 — Introducción a Devin AI

**Duración total:** 3 horas (incluyendo 20 min de descanso)
**Audiencia:** Desarrolladores de Softtek de distintos lenguajes y seniorities
**Formato:** Presencial o remoto con pantalla compartida

---

## Objetivos de aprendizaje

Al terminar esta sesión el alumno será capaz de:

1. Explicar qué diferencia a Devin de un asistente de código convencional como GitHub Copilot.
2. Identificar qué tipos de tareas son adecuadas para delegar en Devin y cuáles no.
3. Describir cómo Devin planifica y ejecuta una tarea internamente.
4. Conectar Devin a un repositorio real y pedirle que analice un PR con bugs.

---

## Materiales necesarios antes de empezar

Antes de que lleguen los alumnos, tener abierto y listo:

- **Repositorio `gestor-tareas-api`** clonado localmente, rama `main`. La rama `escenario-1-bug-logico` ya pusheada y con un PR abierto contra `main` (PR #1: *bug: validaciones de negocio ausentes en tareas*).
- **Cuenta en [devin.ai](https://devin.ai)** con sesión iniciada. Tener listo el panel de nueva sesión para no perder tiempo.
- **Navegador con estas pestañas abiertas:**
  - PR #1 del repo en GitHub
  - Documentación de Devin: `docs.devin.ai`
  - Artículo de Gumroad / Sahil Lavingia sobre los 1500 PRs (o captura de pantalla del post original)
- **VS Code** con el repo abierto en `aplicacion/rutas/tareas.py`, visible pero sin zoom excesivo.
- Tener probado previamente que Devin puede acceder al repo (permisos de GitHub configurados).

---

## Timing general

| Bloque | Duración | Hora de inicio |
|---|---|---|
| Apertura y presentación | 10 min | 00:00 |
| B1 — Qué es Devin | 35 min | 00:10 |
| Caso real: Gumroad | 5 min | 00:45 |
| B2 — Arquitectura interna | 25 min | 00:50 |
| Demo en vivo | 20 min | 01:15 |
| **DESCANSO** | **20 min** | **01:35** |
| Actividad técnica | 35 min | 01:55 |
| Puesta en común | 10 min | 02:30 |
| Cierre y preview sesión 2 | 5 min | 02:40 |

---

## Apertura y presentación `[10 min — 00:00]`

*Mientras los alumnos se conectan o se sientan, tener en pantalla el título de la sesión.*

Buenos días a todos. Voy a empezar puntual porque tenemos mucho contenido.

Esta sesión es la primera de un curso sobre Devin AI, y el objetivo no es que salgáis convencidos de que Devin es la herramienta definitiva, sino que salgáis con una imagen realista: qué hace bien, qué hace mal, cómo encaja en un equipo de desarrollo real, y qué tenéis que cambiar en vuestra forma de trabajar para sacarle partido.

Vamos a trabajar sobre un repositorio concreto que ya conocéis o que vais a conocer hoy: una API de gestión de tareas en Python. No importa si no sois desarrolladores Python, porque lo que importa es la interacción con Devin, no el lenguaje.

La sesión tiene dos mitades separadas por un descanso. En la primera mitad: teoría y demo en vivo. En la segunda: vosotros mismos con Devin.

Antes de empezar, necesito que cada uno verifique que tiene cuenta en devin.ai. Levantad la mano si no tenéis acceso todavía.

*Resolver accesos pendientes. Máximo 3 minutos.*

Perfecto. Empezamos.

---

## B1 — Qué es Devin, capacidades y limitaciones `[35 min — 00:10]`

*Pantalla: VS Code con el repo abierto, minimizado. No mostrar Devin todavía.*

### Copilot vs agente autónomo

Llevamos años usando herramientas de asistencia al código. GitHub Copilot, ChatGPT, Cursor. Todas tienen algo en común: necesitan a un humano en el bucle para cada paso. Yo escribo, la herramienta sugiere, yo acepto o rechazo, yo ejecuto, yo leo el error, yo vuelvo a preguntar. El control sigue siendo mío en cada momento.

Devin es distinto en un aspecto fundamental: **puede ejecutar un ciclo completo de desarrollo sin que yo intervenga en cada paso**. Le doy una tarea, y él abre una terminal, lee el código, escribe cambios, ejecuta los tests, lee los errores, corrige, vuelve a ejecutar, y cuando considera que ha terminado, me entrega un resultado. Yo no tengo que estar mirando.

Eso tiene un nombre técnico: **agente autónomo**. Un agente es un sistema que percibe su entorno, toma decisiones y ejecuta acciones para alcanzar un objetivo, sin requerir instrucción humana en cada decisión intermedia.

La diferencia práctica es enorme. Con Copilot, si quiero que alguien arregle un bug, tengo que sentarme con él, describir el problema, copiar y pegar código, leer sugerencias, probar, volver a preguntar. El proceso sigue siendo mío. Con Devin, puedo escribirle "hay un bug en el endpoint de actualización de tareas, lee el código y corrígelo", y puedo irme a una reunión. Cuando vuelvo, tiene un PR preparado.

*Pausa de un segundo. Dejar que esto aterrice.*

Eso no significa que Devin sea mejor que vosotros. Significa que es un colaborador diferente, con un perfil diferente. Ahora vamos a ver cuál es ese perfil con honestidad.

### Capacidades reales

*Pantalla: mantener VS Code. No mostrar slides con listas, hablar directamente.*

Devin tiene cuatro capacidades que lo hacen útil en un contexto empresarial:

**Primera: leer y entender una codebase completa.** Cuando le das acceso a un repositorio, Devin no lee solo el archivo que le señalas. Navega el árbol de ficheros, lee la configuración, entiende las dependencias, traza las llamadas entre módulos. Es capaz de situarse en un proyecto desconocido con una velocidad que ningún desarrollador humano puede igualar, simplemente porque puede leer miles de líneas en segundos sin cansarse.

**Segunda: ejecutar y depurar.** Devin tiene acceso a una terminal real. Puede instalar paquetes, ejecutar tests, leer la salida de error, modificar el código, volver a ejecutar. Este ciclo lo hace solo, sin que yo tenga que copiar y pegar errores en un chat.

**Third: trabajar con contexto prolongado.** Mantiene el estado de la tarea a lo largo de docenas de pasos. Si en el paso 12 falla algo relacionado con una decisión tomada en el paso 3, puede retroceder y reconsiderar. Esto es muy distinto a un chat donde cada mensaje empieza casi desde cero.

**Cuarta: generar entregables completos.** No solo escribe código. Puede escribir los tests, actualizar la documentación, crear el PR con una descripción coherente y ejecutar la suite completa antes de entregarla.

### Limitaciones reales

*Esta parte es igual de importante. No pasarla rápido.*

Las limitaciones de Devin son reales y hay que conocerlas para no llevarse sorpresas en producción.

**Primera limitación: no tiene criterio de negocio.** Devin hace lo que le dices, no lo que necesitas. Si le pides que "mejore el rendimiento del endpoint de listado", puede añadir un índice en la base de datos, añadir caché, o simplemente añadir un parámetro de limit que no aplica. Las tres son "mejoras de rendimiento". Sin contexto de negocio preciso, Devin optimiza en la dirección que encuentra más obvia, que puede no ser la correcta.

**Segunda: se equivoca con lógica compleja.** En tareas de algorítmica no trivial, reglas de negocio entrelazadas o sistemas con muchos efectos laterales, la tasa de error de Devin sube. No es que no intente hacerlo bien; es que los errores de razonamiento sobre lógica compleja son el talón de Aquiles actual de los LLMs.

**Tercera: no puede reemplazar la revisión humana.** Todo lo que produce Devin tiene que pasar por code review. No como formalidad, sino porque comete errores sutiles: una condición invertida, un caso borde ignorado, una validación ausente. Veremos ejemplos de esto hoy.

**Cuarta: las instrucciones vagas producen resultados vagos.** Si el prompt es impreciso, Devin producirá algo que técnicamente responde al prompt pero que no es lo que querías. La calidad del output está directamente correlacionada con la calidad del input. Esto es una habilidad que hay que desarrollar.

*Hacer pausa aquí. Preguntar al grupo:* "¿Alguien ha usado ya Devin o algún agente similar en su trabajo? ¿Qué experiencia tuvo?" Escuchar una o dos respuestas, 1 minuto máximo.

### Casos de uso empresariales

*Pasar a casos concretos. No abstracciones.*

Los casos de uso donde Devin aporta más valor en entornos empresariales se agrupan en tres categorías.

**Deuda técnica y refactoring.** Cambiar nombres de variables en todo el repositorio, migrar una librería deprecated a su sucesor, convertir código síncrono a asíncrono en varios ficheros. Tareas que un desarrollador sénior haría bien pero que son lentas, mecánicas y aburridas. Devin las ejecuta rápido y con consistencia.

**Bugs bien definidos.** Si el bug está localizado y el comportamiento esperado está claro, Devin puede encontrarlo, corregirlo y añadir el test de regresión. El requisito es que alguien haya descrito bien el problema.

**Features pequeñas y repetitivas.** Añadir un nuevo endpoint que sigue el mismo patrón que los existentes, crear un nuevo campo en un modelo con su migración, añadir validaciones simples. Tareas donde el patrón ya existe en el repo y hay que replicarlo.

**Lo que no funciona bien:** arquitectura nueva desde cero, decisiones que requieren negociación con stakeholders, integraciones con APIs sin documentación clara, o cualquier tarea donde "el criterio" es más importante que "la ejecución".

---

## Caso real intercalado — Gumroad `[5 min — 00:45]`

*Pantalla: mostrar el post de Sahil Lavingia o la captura preparada.*

Voy a pausar un momento para hablar de un caso que probablemente es el más citado cuando se habla de Devin en producción.

Gumroad es una plataforma de comercio electrónico para creadores de contenido. No es una startup de cinco personas, tiene millones de usuarios y una codebase activa. Su CEO, Sahil Lavingia, publicó en 2024 que Devin se había convertido en el mayor contribuidor al repositorio de Gumroad, con más de **1.500 pull requests fusionados**.

Para poner eso en perspectiva: 1.500 PRs es una cantidad que un equipo de cuatro desarrolladores tardaría años en producir. Devin los produjo en meses, trabajando en paralelo con el equipo humano.

¿Qué hacía Devin exactamente? Principalmente tres cosas. Primero, implementar features pequeñas que seguían patrones ya establecidos en el código: nuevas opciones en formularios, ajustes en la lógica de pagos, mejoras en emails transaccionales. Segundo, corregir bugs reportados por usuarios con descripción clara del comportamiento incorrecto. Tercero, escribir tests para código existente que no tenía cobertura.

Lo relevante para nosotros no es el número. Es el modelo de trabajo que implica. El equipo de Gumroad no desapareció. Lo que cambió es que los desarrolladores humanos se enfocaron en las decisiones de producto y arquitectura, y delegaron en Devin la ejecución de lo que ya estaba decidido. Devin no inventó nada. Ejecutó con una velocidad y consistencia que un equipo pequeño no podía alcanzar por sí solo.

El segundo dato que vale la pena mencionar: Goldman Sachs ha reportado reducciones de tiempo significativas en procesos de sus mesas de operaciones usando agentes de IA para automatizar tareas repetitivas de análisis y generación de código de soporte. Y Visma, empresa europea de software de gestión empresarial, reportó en 2024 que había duplicado la productividad de algunos equipos de desarrollo tras integrar Devin en su flujo de trabajo.

Estos tres casos tienen algo en común: **ninguno eliminó desarrolladores, todos cambiaron qué hacen esos desarrolladores**. Eso es lo que tenéis que esperar si Devin entra en vuestros proyectos.

---

## B2 — Arquitectura interna de Devin `[25 min — 00:50]`

*Pantalla: abrir un documento en blanco o pizarra para dibujar mientras se habla. El diagrama ASCII de abajo sirve de referencia.*

### Cómo planifica una tarea

Cuando le enviáis una tarea a Devin, lo primero que hace no es escribir código. Lo primero es **leer**. Devin explora el repositorio: estructura de carpetas, archivos de configuración, dependencias declaradas, tests existentes. Construye un modelo mental del proyecto antes de tocar nada.

A continuación **planifica en pasos**. Genera una lista de subtareas ordenadas: "primero necesito entender cómo funciona el endpoint X, luego identificar dónde se valida Y, luego modificar Z, luego ejecutar los tests para verificar". Esta planificación es visible en la interfaz de Devin, en tiempo real. Podéis ver cómo piensa.

*Dibujar o mostrar el siguiente diagrama mientras se explica cada caja:*

```
┌──────────────────────────────────────────────────┐
│                  TAREA RECIBIDA                  │
│         (prompt del desarrollador)               │
└─────────────────────┬────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────┐
│              EXPLORACIÓN DEL REPO                │
│  Lee estructura · Identifica archivos clave      │
│  Entiende dependencias · Lee tests existentes    │
└─────────────────────┬────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────┐
│              PLANIFICACIÓN                       │
│  Divide la tarea en subtareas ordenadas          │
│  Estima qué archivos va a modificar              │
│  Decide por dónde empezar                        │
└─────────────────────┬────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────┐
│           CICLO DE EJECUCIÓN ITERATIVA           │
│                                                  │
│  ┌───────────┐  ┌───────────┐  ┌─────────────┐  │
│  │ Terminal  │  │  Editor   │  │  Navegador  │  │
│  │           │  │           │  │             │  │
│  │ Ejecuta   │  │ Lee y     │  │ Consulta    │  │
│  │ comandos  │  │ modifica  │  │ docs y      │  │
│  │ y tests   │  │ código    │  │ referencias │  │
│  └─────┬─────┘  └─────┬─────┘  └──────┬──────┘  │
│        └──────────────┴───────────────┘          │
│                       │                          │
│              ¿Tests pasan?                       │
│              /         \                         │
│            SÍ           NO                       │
│             │            │                       │
│             │      Analiza error                 │
│             │      Ajusta plan                   │
│             │      Vuelve a ejecutar             │
└─────────────┼────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────┐
│               ENTREGA                            │
│  Abre PR · Escribe descripción · Lista cambios   │
│  Reporta qué tests pasan y qué decisiones tomó  │
└──────────────────────────────────────────────────┘
```

### Las herramientas que usa Devin

Devin tiene acceso a tres herramientas principales que usa de forma coordinada.

**Terminal.** Puede ejecutar cualquier comando de shell. `git`, `pytest`, `pip install`, `curl`. Cuando un test falla, lee la salida de error y la usa para decidir el siguiente paso. Esto es lo que lo diferencia de un chatbot: no simula la ejecución, la hace de verdad.

**Editor de código.** Lee archivos completos, no fragmentos. Puede abrir cinco archivos a la vez y cruzar información entre ellos. Cuando modifica código, lo hace directamente sobre el árbol de ficheros, no sobre un snippet aislado.

**Navegador.** Puede acceder a documentación online, leer páginas de referencia de librerías, consultar Stack Overflow si lo necesita. También puede interactuar con interfaces web: abrir el PR en GitHub, leer los comentarios, añadir respuestas.

### Cómo itera cuando algo falla

Este punto es importante porque es donde Devin muestra su mayor diferencia respecto a un chatbot.

Cuando un test falla, Devin no para y te pregunta qué hacer. Lee el stack trace completo, identifica la línea exacta donde falla, vuelve al código, analiza la causa, modifica, vuelve a ejecutar. Este ciclo puede repetirse 10, 15, 20 veces en una tarea compleja. Cada iteración es una decisión autónoma.

Hay un límite, claro. Si después de muchas iteraciones no encuentra la solución, puede bloquearse o producir una solución incorrecta. Cuando eso pasa, necesita un humano que le dé más contexto o que reencamine el prompt. El rol del desarrollador en ese momento es de supervisor, no de ejecutor.

*Aquí hacer una pausa y preguntar si hay preguntas sobre la arquitectura antes de pasar a la demo.*

---

## Demo en vivo `[20 min — 01:15]`

*Pantalla: cambiar a navegador. Tener abierto el PR #1 del repo `gestor-tareas-api` en GitHub.*

Ahora vamos a ver esto en funcionamiento real. Voy a conectar Devin al repositorio y pedirle que analice el PR #1, que contiene bugs de validación que introdujimos deliberadamente para este ejercicio.

### Paso 1 — Revisar el PR antes de llamar a Devin `[2 min]`

*Mostrar el PR en GitHub. Navegar a la pestaña "Files changed".*

Primero voy a mostrarles el PR tal como lo vería cualquier revisor humano. El título es "bug: validaciones de negocio ausentes en tareas" y el cambio está en `aplicacion/rutas/tareas.py`.

*Mostrar el diff. Señalar específicamente:*
- El endpoint `create_task` no tiene ninguna validación de longitud de título.
- El endpoint `update_task` tiene una comprobación de estado, pero está mirando `payload.status` en lugar de `task.status`. La condición bloquea el caso equivocado.

Un revisor humano puede tardar varios minutos en detectar esto, especialmente la segunda parte, que es sutil. Vamos a ver qué hace Devin.

### Paso 2 — Abrir Devin y crear nueva sesión `[2 min]`

*Cambiar pestaña al panel de Devin.*

Abro una nueva sesión en Devin. Lo primero que hago es conectarlo al repositorio.

*Mostrar el proceso de conectar el repo de GitHub a Devin. Seguir los pasos de la interfaz.*

Una vez conectado, Devin ya tiene acceso de lectura al código. Podría darle acceso de escritura también, pero para esta demo voy a limitarlo a análisis, no a escritura automática.

### Paso 3 — Escribir el prompt inicial `[2 min]`

*Escribir el siguiente prompt en la caja de texto de Devin, despacio para que los alumnos puedan leerlo:*

```
Analiza el PR #1 del repositorio. Este PR introduce dos bugs
de validación en el archivo aplicacion/rutas/tareas.py.

Tu tarea es:
1. Identificar exactamente qué validaciones faltan o están mal implementadas.
2. Explicar en qué escenario concreto falla cada bug (qué petición HTTP
   produce el comportamiento incorrecto).
3. Proponer el código corregido para cada caso.

No hagas cambios en el repositorio todavía. Solo análisis y propuesta.
```

*Enviar. Mientras Devin empieza a trabajar, comentar al grupo:*

Fijaos en el prompt. He sido muy específico en tres cosas: qué tiene que hacer (identificar, explicar, proponer), qué no tiene que hacer (no modificar nada), y en qué fichero buscar. Cuanto más acotado es el prompt, más útil es la respuesta.

### Paso 4 — Leer y comentar la respuesta de Devin `[8 min]`

*Esperar a que Devin complete el análisis. Leer la respuesta en voz alta resumiendo, no leyendo literalmente.*

Devin ha encontrado los dos problemas. Vamos a ver qué dice sobre cada uno.

*Mostrar la parte de la respuesta sobre el primer bug:*

Sobre el primero, Devin identifica que `create_task` acepta un título de cualquier longitud, incluyendo un string vacío o de un carácter. Propone añadir una validación antes de persistir, devolviendo un 422 si `len(payload.title) < 3`.

*Mostrar la parte sobre el segundo bug:*

El segundo es más interesante. Devin detecta que la condición `if payload.status == TaskStatus.done` comprueba lo que el cliente quiere *poner*, no lo que la tarea *es* actualmente. Lo que queremos bloquear es modificar una tarea que ya está en `done`. La condición correcta sería `if task.status == TaskStatus.done`.

*Comentar al grupo:*

Este segundo bug es exactamente el tipo de error sutil que cuesta detectar en code review porque la lógica *parece* correcta a primera vista. Hay un `if`, hay una comparación, hay un `raise`. Pero la variable equivocada. Devin lo detectó leyendo el código completo, no solo la línea modificada.

### Paso 5 — Pedir el código corregido `[4 min]`

*Enviar un segundo mensaje a Devin:*

```
Perfecto. Ahora escribe el código completo corregido para la función
update_task y para la función create_task, con las dos validaciones
implementadas correctamente. Incluye también el test pytest para cada caso.
```

*Mientras Devin responde, comentar:*

Lo que estoy haciendo aquí es un flujo de trabajo típico: primero análisis, luego implementación. No todo de golpe. Esto permite validar que Devin entendió bien el problema antes de que escriba código.

*Mostrar la respuesta con el código propuesto. Señalar los cambios clave sin leerlos todos.*

Aquí está la corrección. Podéis ver que ha añadido la validación de longitud en `create_task` y ha corregido la variable en `update_task`. Y ha añadido los dos tests correspondientes que verifican exactamente el comportamiento esperado.

En un flujo real, ahora haría code review de esta propuesta y si es correcta, dejaría que Devin abra el PR.

---

## DESCANSO `[20 min — 01:35]`

*Anunciar el descanso claramente. Decir la hora exacta de regreso.*

Hacemos 20 minutos de descanso. Volvemos a las [hora exacta]. Cuando regresemos, vosotros vais a hacer exactamente lo que acabo de hacer yo, pero con vuestro propio prompt.

---

## Actividad técnica `[35 min — 01:55]`

### Enunciado

*Repartir o mostrar en pantalla las instrucciones. Leerlas en voz alta una vez.*

**Objetivo:** Usar Devin para identificar los bugs del PR #1 del repositorio `gestor-tareas-api` de forma autónoma, sin que el formador os diga dónde están.

**Instrucciones paso a paso:**

1. **Abrid Devin** y cread una nueva sesión.

2. **Conectad el repositorio.** Podéis usar el repo original si tenéis acceso, o el fork que hayáis hecho. Aseguraos de que el PR #1 (`escenario-1-bug-logico`) está visible.

3. **Escribid vuestro propio prompt** para pedirle a Devin que analice el PR y encuentre los problemas. No copiéis el prompt del formador. Redactadlo con vuestras palabras, siendo tan específicos o tan generales como queráis. Esto es parte del ejercicio.

4. **Leed la respuesta de Devin** y anotad:
   - ¿Encontró los dos bugs?
   - ¿Describió correctamente el escenario de fallo de cada uno?
   - ¿La corrección propuesta es la adecuada?

5. **Si Devin no encontró los dos bugs en el primer intento**, refinad el prompt y volved a intentarlo. Anotad qué cambió en vuestro segundo prompt respecto al primero.

6. **Pedid a Devin el código corregido** para uno de los dos bugs (el que prefiráis) y evaluar si la propuesta es correcta.

**Tiempo disponible:** 35 minutos.

### Criterios de éxito

El ejercicio está completo cuando podéis responder sí a estas tres preguntas:

- ¿Devin identificó que `create_task` no valida que el título tenga al menos 3 caracteres?
- ¿Devin identificó que `update_task` comprueba `payload.status` en lugar de `task.status`, permitiendo modificar tareas ya completadas?
- ¿La corrección propuesta por Devin para al menos uno de los dos bugs es técnicamente correcta?

### Solución esperada (para uso del formador al validar)

**Bug 1 — Validación de longitud de título ausente en `create_task`:**

Devin debe señalar que no existe ninguna comprobación sobre `len(payload.title)` antes de persistir la tarea. La corrección correcta añade:

```python
if len(payload.title) < 3:
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="El título debe tener al menos 3 caracteres",
    )
```

Y el test correspondiente verifica que una petición `POST /tasks/` con `{"title": "AB"}` devuelve 422.

**Bug 2 — Condición invertida en `update_task`:**

Devin debe señalar que la línea:
```python
if payload.status == TaskStatus.done:
```
debería ser:
```python
if task.status == TaskStatus.done:
```

El escenario de fallo concreto es: crear una tarea, cambiarla a `done`, y luego enviar un `PATCH` con `{"status": "in_progress"}`. Con el bug, la petición tiene éxito y modifica la tarea. Con la corrección, devuelve 400.

*Mientras los alumnos trabajan, circular por las mesas o monitorizar los chats de pantalla compartida. Observar qué prompts usan. No dar pistas a menos que alguien lleve más de 10 minutos bloqueado sin ningún avance.*

---

## Puesta en común `[10 min — 02:30]`

*Volver a pantalla compartida. Lanzar las preguntas una a una, no todas a la vez.*

Vamos a poner en común lo que habéis encontrado. Quiero escuchar respuestas concretas, no "funcionó bien" o "no funcionó".

**Pregunta 1:** ¿Cuántos de vosotros encontrasteis los dos bugs en el primer intento con Devin? ¿Cuántos necesitasteis refinar el prompt?

*Recoger manos o respuestas. Pedir a alguien que necesitó refinar que explique qué cambió en su segundo prompt.*

**Pregunta 2:** Comparad vuestro prompt con el que usé yo en la demo. ¿Qué diferencias encontráis? ¿Cuál fue más efectivo y por qué creéis que es así?

*Buscar diferencias concretas: si alguien fue más vago, si alguien fue más específico, si alguien añadió contexto que yo no añadí.*

**Pregunta 3:** Para los que encontrasteis los dos bugs, ¿la descripción que hizo Devin del bug número 2 (la condición invertida) fue suficientemente clara para que un desarrollador que no conoce el repo la entienda?

*Este punto abre la discusión sobre la calidad de la explicación de Devin, no solo si encontró el bug.*

**Pregunta 4:** ¿Alguien probó un prompt muy general, tipo "encuentra los bugs en este PR"? ¿Qué pasó?

*Si nadie lo probó, comentar qué suele pasar: Devin tiende a dar un análisis superficial o a enumerar posibles mejoras de estilo en lugar de localizar bugs de lógica específicos.*

---

## Cierre y preview de la sesión 2 `[5 min — 02:40]`

*Pantalla: volver al repo, rama `main`.*

Vamos a cerrar.

Lo que hemos visto hoy se resume en tres ideas que quiero que os llevéis.

**Primera:** Devin no es Copilot con esteroides. Es una categoría diferente de herramienta. Copilot os ayuda a escribir. Devin puede ejecutar. Esa diferencia cambia cómo lo usáis y qué tipo de tareas le dais.

**Segunda:** la calidad de vuestro prompt determina la calidad del resultado. No es magia y no adivina intenciones. Lo que le dais es lo que aprovecha. Hoy habéis visto la diferencia entre un prompt específico y uno vago. En las próximas sesiones vamos a trabajar esto de forma sistemática.

**Tercera:** Devin comete errores. La revisión humana no es opcional. Lo que cambia es dónde enfocáis esa revisión: en el criterio, la arquitectura, las decisiones de negocio, no en la mecánica de escritura.

En la **sesión 2** vamos a trabajar con los otros escenarios del repositorio: código duplicado, tests incompletos, endpoint con lógica incorrecta. Vais a ver cómo Devin aborda refactoring real y cómo se comporta cuando los tests que existen no cubren los casos de error. Traed el repo clonado y la cuenta de Devin activa.

Hasta la próxima.
