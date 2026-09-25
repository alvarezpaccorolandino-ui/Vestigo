"""
Modelo de IA: Recomendador de Tallas para VESTIGO
==================================================
Entrena un clasificador que predice la talla y silueta recomendada
a partir de las medidas corporales del cliente.

Autor: Ronal + equipo VESTIGO
Fecha: Septiembre 2026
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# ============================================================
# 1. CONFIGURACIÓN
# ============================================================
np.random.seed(42)

TALLAS = ['XS', 'S', 'M', 'L', 'XL', 'XXL']

# ============================================================
# 2. GENERAR DATASET SINTÉTICO
# ============================================================
def generar_dataset(n_muestras=2000):
    """Genera un dataset sintético de medidas corporales."""
    datos = []

    for _ in range(n_muestras):
        talla_real = np.random.choice(TALLAS)

        rangos = {
            'XS':  {'pecho': (76, 82),  'cintura': (58, 64),  'cadera': (82, 88),  'altura': (150, 160)},
            'S':   {'pecho': (82, 88),  'cintura': (64, 70),  'cadera': (88, 94),  'altura': (155, 165)},
            'M':   {'pecho': (88, 94),  'cintura': (70, 76),  'cadera': (94, 100), 'altura': (160, 170)},
            'L':   {'pecho': (94, 102), 'cintura': (76, 84),  'cadera': (100, 108),'altura': (165, 175)},
            'XL':  {'pecho': (102, 110),'cintura': (84, 92),  'cadera': (108, 116),'altura': (170, 180)},
            'XXL': {'pecho': (110, 120),'cintura': (92, 102), 'cadera': (116, 126),'altura': (175, 185)},
        }

        r = rangos[talla_real]

        pecho = np.random.uniform(*r['pecho']) + np.random.normal(0, 1.5)
        cintura = np.random.uniform(*r['cintura']) + np.random.normal(0, 1.5)
        cadera = np.random.uniform(*r['cadera']) + np.random.normal(0, 1.5)
        altura = np.random.uniform(*r['altura']) + np.random.normal(0, 2)

        ratio = cintura / cadera
        if ratio < 0.75:
            silueta = 'Entallado'
        elif ratio < 0.85:
            silueta = 'Recto'
        elif ratio < 0.95:
            silueta = 'Holgado'
        else:
            silueta = 'Oversize'

        datos.append({
            'pecho': round(pecho, 1),
            'cintura': round(cintura, 1),
            'cadera': round(cadera, 1),
            'altura': round(altura, 1),
            'talla': talla_real,
            'silueta': silueta
        })

    return pd.DataFrame(datos)


print("=" * 60)
print("PASO 1: Generando dataset sintético...")
print("=" * 60)
df = generar_dataset(2000)
print(f"✓ Dataset creado: {len(df)} muestras")
print("\nPrimeras 5 filas:")
print(df.head())
print("\nDistribución de tallas:")
print(df['talla'].value_counts())

# ============================================================
# 3. PREPARAR DATOS
# ============================================================
print("\n" + "=" * 60)
print("PASO 2: Preparando datos para entrenamiento...")
print("=" * 60)

X = df[['pecho', 'cintura', 'cadera', 'altura']].values
y_talla = df['talla'].values
y_silueta = df['silueta'].values

X_train, X_test, y_talla_train, y_talla_test, y_silueta_train, y_silueta_test = train_test_split(
    X, y_talla, y_silueta, test_size=0.2, random_state=42
)

print(f"✓ Entrenamiento: {len(X_train)} muestras")
print(f"✓ Prueba: {len(X_test)} muestras")

# ============================================================
# 4. ENTRENAR
# ============================================================
print("\n" + "=" * 60)
print("PASO 3: Entrenando modelos...")
print("=" * 60)

modelo_talla = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
modelo_talla.fit(X_train, y_talla_train)
print("✓ Modelo de talla entrenado")

modelo_silueta = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
modelo_silueta.fit(X_train, y_silueta_train)
print("✓ Modelo de silueta entrenado")

# ============================================================
# 5. EVALUAR
# ============================================================
print("\n" + "=" * 60)
print("PASO 4: Evaluando modelos...")
print("=" * 60)

y_talla_pred = modelo_talla.predict(X_test)
acc_talla = accuracy_score(y_talla_test, y_talla_pred)
print(f"\n📊 MODELO TALLA - Accuracy: {acc_talla:.4f} ({acc_talla*100:.2f}%)")
print(classification_report(y_talla_test, y_talla_pred, zero_division=0))

y_silueta_pred = modelo_silueta.predict(X_test)
acc_silueta = accuracy_score(y_silueta_test, y_silueta_pred)
print(f"\n📊 MODELO SILUETA - Accuracy: {acc_silueta:.4f} ({acc_silueta*100:.2f}%)")
print(classification_report(y_silueta_test, y_silueta_pred, zero_division=0))

# ============================================================
# 6. GUARDAR
# ============================================================
print("\n" + "=" * 60)
print("PASO 5: Guardando modelos...")
print("=" * 60)

os.makedirs('modelo_ia/artefactos', exist_ok=True)
joblib.dump(modelo_talla, 'modelo_ia/artefactos/modelo_talla.pkl')
joblib.dump(modelo_silueta, 'modelo_ia/artefactos/modelo_silueta.pkl')
print("✓ modelo_talla.pkl guardado")
print("✓ modelo_silueta.pkl guardado")

# ============================================================
# 7. PROBAR
# ============================================================
print("\n" + "=" * 60)
print("PASO 6: Probando el modelo...")
print("=" * 60)

ejemplos = [
    {'pecho': 92, 'cintura': 74, 'cadera': 98, 'altura': 168, 'descripcion': 'Persona promedio'},
    {'pecho': 80, 'cintura': 62, 'cadera': 86, 'altura': 155, 'descripcion': 'Persona pequeña'},
    {'pecho': 108, 'cintura': 90, 'cadera': 114, 'altura': 178, 'descripcion': 'Persona grande'},
    {'pecho': 96, 'cintura': 68, 'cadera': 92, 'altura': 170, 'descripcion': 'Persona atlética'},
]

for ej in ejemplos:
    entrada = np.array([[ej['pecho'], ej['cintura'], ej['cadera'], ej['altura']]])
    talla_pred = modelo_talla.predict(entrada)[0]
    silueta_pred = modelo_silueta.predict(entrada)[0]
    print(f"\n👤 {ej['descripcion']}:")
    print(f"   Medidas: Pecho {ej['pecho']}cm, Cintura {ej['cintura']}cm, Cadera {ej['cadera']}cm, Altura {ej['altura']}cm")
    print(f"   → Talla: {talla_pred}")
    print(f"   → Silueta: {silueta_pred}")

print("\n" + "=" * 60)
print("✅ ¡MODELO ENTRENADO Y EVALUADO CON ÉXITO!")
print("=" * 60)