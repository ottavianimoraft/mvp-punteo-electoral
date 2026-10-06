import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

random.seed(42)

def generar_mesa_simulada():
    electores = random.randint(20, 100)
    porcentaje_participacion = random.uniform(0.3, 1.1)
    votos_totales = int(electores * porcentaje_participacion)
    concentracion_max = random.uniform(0.2, 1.0)

    es_riesgo = 1 if (votos_totales > electores or porcentaje_participacion >= 1.0 or concentracion_max > 0.70) else 0

    participacion = votos_totales / electores
    return [participacion, concentracion_max], es_riesgo

X = []
y = []

for _ in range(300):
    features, etiqueta = generar_mesa_simulada()
    X.append(features)
    y.append(etiqueta)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

precision = modelo.score(X_test, y_test)
print(f"Precisión del modelo: {precision:.0%}")

joblib.dump(modelo, "modelo_riesgo.pkl")
print("Modelo guardado en modelo_riesgo.pkl")