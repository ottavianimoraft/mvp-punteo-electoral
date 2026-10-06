# Detección de punteo en elecciones universitarias

Plataforma web que detecta irregularidades en los resultados de mesas de votación de elecciones universitarias, entre ellas el "punteo". Combina reglas de control fijas con un modelo de Machine Learning que predice el riesgo de cada mesa. Trabaja con datos simulados de una sola facultad.

**Autores:** Juan Ignacio Gonzalez Bracco y Mora Ottaviani
**Materia:** Seminario de Datos para Politólogos/as (DS4P)

## Qué hace

- **Carga de mesas:** el usuario ingresa electores y votos por agrupación de cada mesa.
- **Detector de irregularidades**, con tres reglas:
  - Más votos que electores → alerta.
  - Votos igual a electores (100 % de participación) → revisar.
  - Una agrupación con más del 70 % de los votos → concentración anómala.
- **Dashboard:** métricas, tabla de mesas y gráficos interactivos de votos y participación.
- **Predicción de riesgo:** un modelo Random Forest clasifica cada mesa en riesgo ALTO o BAJO a partir de su participación y su concentración de votos.
- **Login con JWT:** todas las consultas de datos requieren iniciar sesión.

## Credenciales de prueba

| Usuario | Contraseña |
|---------|------------|
| admin   | ds4p2026   |

## Arquitectura

```
Navegador  →  Frontend (Streamlit)  →  API (FastAPI)  →  Base de datos (PostgreSQL en Neon)
                                           ↓
                                  Modelo de ML (modelo_riesgo.pkl)
```

- **Backend:** FastAPI, SQLAlchemy (ORM), Pydantic (validación), JWT (python-jose) y bcrypt (passlib).
- **Base de datos:** PostgreSQL en la nube (Neon). Sin configuración usa un archivo SQLite local.
- **Machine Learning:** scikit-learn (Random Forest), guardado con joblib.
- **Frontend:** Streamlit con cuatro pantallas (Login, Dashboard, Cargar Zona y Predicciones) y gráficos con Plotly.

## Estructura del proyecto

| Archivo | Para qué sirve |
|---------|----------------|
| `main.py` | API: endpoints, login y reglas de detección |
| `database.py` | Conexión a la base de datos |
| `models.py` | Tablas (Mesa, Voto, Usuario) como clases |
| `esquemas.py` | Validación de los datos de entrada (Pydantic) |
| `seguridad.py` | Encriptación de contraseñas y tokens JWT |
| `entrenar_almodelo.py` | Entrenamiento del modelo de riesgo |
| `modelo_riesgo.pkl` | Modelo entrenado |
| `seed_datos.py` | Carga las 6 mesas simuladas |
| `crear_usuario.py` | Crea el usuario de prueba |
| `frontend.py` | Aplicación en Streamlit |
| `requirements.txt` | Librerías necesarias |

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/login` | Devuelve un token JWT |
| GET | `/mesas` | Lista de mesas (requiere token) |
| POST | `/mesas` | Carga una mesa nueva y devuelve su estado (requiere token) |
| GET | `/alertas` | Mesas con irregularidades (requiere token) |
| GET | `/resumen` | Datos para el dashboard (requiere token) |
| GET | `/prediccion/{mesa_id}` | Riesgo predicho por el modelo (requiere token) |

La documentación interactiva de la API está en `/docs`.

## Cómo correrlo en tu computadora

1. Instalar las librerías:

```
   python -m pip install -r requirements.txt
```

2. Crear un archivo `.env` en la carpeta del proyecto, con estas variables:

```
   SECRET_KEY=una-clave-larga-y-secreta
   DATABASE_URL=postgresql://usuario:clave@host/base
```

   `DATABASE_URL` es opcional: si no está, se usa un archivo SQLite local. `SECRET_KEY` es obligatoria.

3. Cargar los datos y crear el usuario de prueba:

```
   python seed_datos.py
   python crear_usuario.py
```

4. Prender el backend (primera terminal):

```
   python -m uvicorn main:app --reload
```

5. Prender el frontend (segunda terminal):

```
   python -m streamlit run frontend.py
```

6. Abrir `http://localhost:8501` e ingresar con las credenciales de prueba.

Para que el frontend apunte a un backend publicado, se define la variable de entorno `API_URL`.

## Aplicación publicada

- **Frontend (Streamlit Community Cloud):** pendiente
- **API (Render):** pendiente