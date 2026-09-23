# Brief para el chat de LinkedIn — `stack-canon`

> **Tu rol al leer esto:** especialista en SEO y desarrollador senior de skills de IA.
> No eres el autor del proyecto: eres quien decide cómo se cuenta para que un lector
> técnico de LinkedIn entienda el valor en los primeros ocho segundos.
>
> Este documento es autocontenido. No hace falta historial previo.

---

## 1. Qué es, en una frase

Un plugin de código abierto para Claude Code que obliga a que el código generado por IA
siga la arquitectura que publica el equipo de cada framework, tenga pruebas de verdad, y
deje la lógica de negocio documentada en un solo sitio.

Repo: `github.com/rjla-developer/stack-canon` · MIT · v1.1.0

## 2. El problema que ataca

Cuando le pides a una IA que construya algo, improvisa la estructura. No porque sea mala:
porque **la arquitectura recomendada de cada framework es información externa que ningún
modelo tiene de forma fiable**. Flutter publica una guía de arquitectura. Astro publica
que corras las pruebas contra el build de producción. Nada de eso está garantizado en los
pesos del modelo, y sale distinto cada vez que preguntas.

La skill lleva ese conocimiento en un catálogo verificado contra la documentación oficial
de nueve stacks, y lo descarga en vivo.

## 3. Las tres reglas

1. **Arquitectura del equipo del framework, no del gusto del modelo.** Lee un catálogo de
   nueve stacks verificado contra la documentación primaria.
2. **Pruebas de reglas de negocio y de presentación, en el límite exacto** — y después
   levantar la app y mirar la pantalla. Una suite verde sólo prueba lo que se te ocurrió
   afirmar.
3. **La lógica de negocio vive en un documento del grupo**, no repartida entre el repo del
   back y el del front. Cuando un cambio altera una regla, ese documento se actualiza en
   la misma tarea.

Antes tenía nueve capacidades. Siete se borraron porque las mediciones no las sostuvieron.

---

## 4. Los números (todos verificables en el repo)

**Método:** misma app Astro construida dos veces desde el mismo prompt literal, y después
la misma funcionalidad añadida a las dos. Una sola variable: la skill activada o no.

**El detalle que da credibilidad:** la baseline no es "Claude a secas". Los dos lados
corren con las mismas 57 skills personales. Mide valor marginal sobre un montaje que ya
era bueno.

| Criterio | Sin skill | Con skill |
|---|---|---|
| `CLAUDE.md` del proyecto | no existe | 208 líneas, escrito **antes** del código |
| Casos de prueba | 54 | **127** |
| Defectos visuales encontrados | 2 | **5** |
| Assets servidos | 2,1 MB | **1,0 MB** |
| Función más larga | **197** | 258 ← *pierde* |
| Archivo más grande | **545** | 627 ← *pierde* |

## 5. Los dos momentos que valen como historia

**Una decisión pasada restringiendo una futura.** En la segunda funcionalidad, la skill se
negó a usar la librería pedida y lo justificó citando una regla del `CLAUDE.md` — *regla
que había escrito ella misma en la primera funcionalidad*. Nadie se la recordó. Eso es
memoria arquitectónica funcionando, y hasta esa corrida sólo existía como teoría.

**El mejor hallazgo lo produjo el lado que perdió.** La baseline entregó el hero sin
pruebas. Al pedírselas, **una falló de verdad**: 180° no son un número entero de cuadros
de 8°, así que la animación tenía cuatro grados de desvío sistemático, invisible a ojo.
Moraleja: las pruebas no se escriben para que pasen, se escriben para que una falle.

---

## 6. El ángulo que yo usaría, y por qué

**Recomendado: "Medí mi propia herramienta y perdió en dos de siete métricas. Publiqué las
dos."**

En LinkedIn todo el mundo publica que su cosa de IA funciona. Casi nadie publica dónde
pierde. La honestidad medida es el diferenciador escaso, y además es cierta — el repo
publica cinco predicciones fallidas y seis defectos propios.

Alternativas, por si el chat prefiere otro tono:

- **"La IA no sabe la arquitectura de tu framework, y no te lo va a decir."** Ataca un
  dolor concreto. Más técnico, menos personal.
- **"Borré siete de las nueve funciones de mi propia herramienta."** Habla de criterio de
  producto, no de código. Alcance más amplio, técnico más flojo.

**Lo que NO recomiendo:** el ángulo de productividad ("construí X en Y horas"). Está
saturado, y no es lo que hace interesante a este proyecto.

## 7. Estructura del post

**Gancho (2 líneas).** LinkedIn corta en ~140–210 caracteres en móvil; todo lo que importa
va antes del *ver más*. Sin preámbulo, sin "hace unos meses me propuse".

**Cuerpo.** Un número concreto por párrafo, párrafos de 1–3 líneas. Los muros de texto
mueren. El momento del `CLAUDE.md` citándose a sí mismo es el clímax: colócalo a dos
tercios, no al final.

**Cierre.** Una pregunta real, no "¿qué opinas?". Algo como: *¿cuántas de las reglas de
arquitectura de tu equipo están escritas en algún sitio que una IA pueda leer?*

## 8. SEO y mecánica de LinkedIn

**LinkedIn tiene dos buscadores encima:** el suyo propio y Google, que indexa los posts
públicos. Ambos leen el texto del cuerpo, no las imágenes.

- **Palabras clave literales, en el cuerpo, en las primeras líneas.** Los términos que
  alguien escribiría de verdad: *Claude Code*, *agent skills*, *arquitectura*, *testing*,
  *IA para desarrollo*. Sin relleno — si una palabra clave no cabe con naturalidad, fuera.
- **3–5 hashtags específicos** al final. `#ClaudeCode` `#AgentSkills` `#TestingDeSoftware`
  rinden más que `#Tecnología` o `#Innovación`, que compiten con millones.
- **El enlace al repo, en el primer comentario.** Es práctica común porque se reporta que
  los enlaces externos reducen alcance. *No lo tengo verificado contra datos públicos de
  LinkedIn* — trátalo como convención del gremio, no como hecho.
- **La señal que sí está clara es el tiempo de lectura.** Un post que retiene treinta
  segundos gana a uno que consigue un like rápido. Eso premia números concretos y
  párrafos cortos, que es exactamente lo que este material tiene.
- **Idioma:** decide uno y mantenlo. Mezclar parte en español, parte en inglés, parte los
  dos, divide la audiencia y ensucia la indexación. Si el público es hispanohablante,
  español con los términos técnicos en inglés tal cual.

**Formato:** texto nativo antes que carrusel. El material es numérico y narrativo; un
carrusel obligaría a partir el argumento y el momento del `CLAUDE.md` pierde fuerza.

## 9. Lo que no se puede decir

El repo tiene una regla desde el día uno: *ningún dato inventado*. El post hereda eso.

- **Una corrida por lado.** Es una comparación controlada, no una medición estadística.
  Hacen falta tres por lado para publicar cualquier tasa. No escribir "X% mejor".
- **La regla 3 no tiene evidencia.** Se agregó porque hacía falta para equipos
  multi-repositorio, no porque un experimento la sostenga. Está marcada así en el propio
  repo. Si el post la menciona, tiene que mencionar eso también.
- **La skill no mejora el diseño.** Los dos sitios salieron prácticamente idénticos. Lo
  dice el registro de evidencias.
- **No hay capturas de los proyectos de Astro.** Si el post pide imagen, o se capturan
  primero, o se va sin ella.
