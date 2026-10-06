# Punteo electoral: carga y control de resultados

Proyecto final de la materia Seminario de Datos para Politólogos/as (DS4P).

**Autores:** Juan Ignacio Gonzalez Bracco y Mora Ottaviani

## De qué trata

El punteo es el seguimiento de los resultados de una elección. A medida que se conocen los resultados de cada mesa, se anotan los votos que obtuvo cada agrupación y después se van sumando para tener una idea del resultado general. Hoy ese proceso se hace de forma manual.

Elegimos este problema porque, en las elecciones de la facultad, vimos que el punteo se hace así: se van anotando y sumando a mano los resultados de las distintas mesas. Nos pareció un proceso bastante sencillo de sistematizar. No quisimos cambiar la forma en la que se hace, sino armar una herramienta que permita hacerlo de manera más ordenada, más rápida y con menos posibilidades de error.

La aplicación está pensada a partir de un caso concreto: la Facultad de Ciencias Sociales de la Universidad de Buenos Aires (FSOC-UBA). Usamos tres agrupaciones que participan ahí: La Ues, Alternativa Académica y La 15. Todos los datos son simulados, no son resultados reales.

## Quién la podría usar

Principalmente los fiscales o las agrupaciones que participan de la elección, para ir cargando los resultados de cada mesa y seguir el resultado general. Eventualmente también podría servir a quienes organizan o hacen el seguimiento de la elección. Nuestro objetivo es simplemente sistematizar el punteo que hoy se hace de forma manual.

## Qué hace

- Permite cargar una mesa: cuántos electores tiene y cuántos votos sacó cada agrupación.
- Muestra un tablero con todas las mesas, el total de votos y gráficos para ver cómo se reparten los votos.
- Marca automáticamente las mesas que conviene revisar, con tres controles: que no haya más votos que electores, que la participación no sea justo del 100 % y que una sola agrupación no tenga más del 70 % de los votos.
- Calcula con un modelo de Machine Learning si el riesgo de cada mesa es alto o bajo. El modelo lo entrenamos con datos simulados.
- Pide usuario y contraseña para entrar.
- 
## Aplicación publicada

La aplicación está en línea y se puede probar desde cualquier dispositivo:

- Pantalla de la aplicación: https://mvp-punteo-electoral.streamlit.app
- Servidor (API y documentación): https://TU-LINK.onrender.com/docs

Usuario de prueba: admin / ds4p2026

Aviso: usamos planes gratuitos, así que si nadie la usó en un rato puede tardar cerca de un minuto en despertar la primera vez.

## Usuario de prueba

- Usuario: admin
- Contraseña: ds4p2026

## Cómo se usa

La aplicación tiene cuatro pantallas. En la primera se inicia sesión. Después, en el menú de la izquierda, están el Dashboard (la tabla y los gráficos), Cargar Zona (el formulario para cargar una mesa) y Predicciones (el riesgo de cada mesa según el modelo).

## Cómo correrla en la computadora

1. Instalar las librerías:

```
   python -m pip install -r requirements.txt
```

2. Crear un archivo llamado `.env` en la carpeta del proyecto, con estas dos líneas:

```
   SECRET_KEY=una-clave-larga-que-elijas
   DATABASE_URL=la-direccion-de-la-base-de-datos
```

   La `DATABASE_URL` es opcional: si no se pone, el programa usa una base local en un archivo. La `SECRET_KEY` sí es obligatoria.

3. Cargar las mesas de ejemplo y crear el usuario de prueba:

```
   python seed_datos.py
   python crear_usuario.py
```

4. Prender el backend, en una terminal:

```
   python -m uvicorn main:app --reload
```

5. Prender la pantalla, en otra terminal:

```
   python -m streamlit run frontend.py
```

6. Abrir `http://localhost:8501` en el navegador e ingresar con el usuario de prueba.

## Con qué la hicimos

- Python como lenguaje.
- FastAPI para el backend (la parte que guarda y calcula).
- SQLAlchemy para trabajar con la base de datos, que está en PostgreSQL (Neon).
- Streamlit y Plotly para la pantalla y los gráficos.
- scikit-learn para el modelo de riesgo.

## Los archivos principales

- `main.py`: el backend, con las rutas y los controles.
- `frontend.py`: la pantalla de la aplicación.
- `models.py` y `database.py`: las tablas y la conexión a la base de datos.
- `esquemas.py`: revisa que los datos cargados tengan sentido.
- `seguridad.py`: contraseñas encriptadas y tokens de sesión.
- `entrenar_almodelo.py` y `modelo_riesgo.pkl`: el modelo de riesgo y su entrenamiento.
- `seed_datos.py` y `crear_usuario.py`: cargan los datos de ejemplo y el usuario de prueba.

## Lo que más nos costó y lo que aprendimos

Esta fue la parte que más nos costó del proyecto, y por eso la contamos con detalle.

**Arrancar de cero.** Al principio no sabíamos ni dónde escribir el código ni cómo ejecutarlo. Tuvimos errores muy básicos: guardar un archivo sin la extensión `.py`, escribir un comando de instalación (`pip install`) dentro del código en vez de la terminal, definir una función después de usarla y errores de indentación (los espacios al principio de las líneas, que en Python importan). Cada uno nos hizo entender cómo se lee y cómo se ejecuta un programa.

**La configuración de la computadora.** Fue lo que más tiempo nos llevó. Teníamos Python instalado dos veces y la terminal no encontraba comandos como `uvicorn`, así que aprendimos a llamarlos a través de Python (`python -m uvicorn`). También nos pasó que la terminal estaba parada en una carpeta equivocada, y entonces la base de datos y el modelo se guardaban en otro lugar o el programa no encontraba los archivos. Aprendimos a abrir siempre la carpeta del proyecto completa en el editor y a revisar en qué carpeta estamos antes de ejecutar algo.

**Entender cómo se conectan las partes.** Nos costó entender que la base de datos, el backend y la pantalla son programas separados, y que los dos últimos tienen que estar prendidos al mismo tiempo, cada uno en su terminal. Tampoco entendíamos por qué el link `127.0.0.1` no funcionaba si no estaba prendido el servidor: es una dirección que solo existe dentro de la computadora donde corre el programa. Eso lo entendimos del todo cuando llegamos a publicar la aplicación.

**Armar el código sin romperlo.** Varias veces pegamos bloques de código duplicados o en un lugar equivocado, y el programa dejaba de arrancar. Aprendimos a pegar funciones completas, una por vez, y a leer los mensajes de error de abajo para arriba, porque la última línea es la que dice qué falló.

**Detalles que nos trabaron.** Las librerías de encriptación de contraseñas no se llevaban bien entre ciertas versiones, y tuvimos que instalar una versión específica. También confundimos el número interno de cada mesa (el que usa la base) con el número que aparece en su nombre: la "Mesa 22" internamente es la 2. Al pasar a la base en la nube (PostgreSQL) tuvimos que avisarle desde qué número seguir numerando las mesas nuevas, porque si no iba a intentar repetir uno que ya existía.

**El modelo de riesgo.** Al principio le pasábamos los votos y los electores por separado y no detectaba bien una mesa con más votos que electores. Cuando le pasamos directamente la participación (votos dividido electores), mejoró bastante en nuestras pruebas con datos simulados. Aprendimos que no alcanza con darle datos a un modelo: importa cuáles y cómo se los damos.

**Lo que nos queda.** Aprendimos a validar los datos que se cargan, a guardar las contraseñas encriptadas, a proteger las rutas con un token de sesión, a usar variables de entorno para no subir claves a GitHub y a conectar una base de datos en la nube. Y, sobre todo, a no asustarnos con los errores: casi todos se resuelven leyendo con calma qué dice el mensaje.

## Qué le agregaríamos con más tiempo

- Que las agrupaciones se puedan elegir y no estén fijas en el formulario.
- Poder corregir o borrar una mesa cargada por error.
- Usuarios con distintos permisos, por ejemplo fiscales y organizadores.
- Exportar los resultados a Excel.
- Probarla con datos reales de una elección.
