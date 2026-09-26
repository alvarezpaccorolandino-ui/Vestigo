"""
Pruebas Unitarias del Modelo de IA VESTIGO
===========================================
Verifica que el modelo de recomendación de tallas y siluetas
funcione correctamente con casos conocidos.

Ejecutar: python -m pytest modelo_ia/test_modelo.py -v
O simplemente: python modelo_ia/test_modelo.py

Autor: Ronal + equipo VESTIGO
Fecha: Septiembre 2026
"""

import joblib
import numpy as np
import os
import sys

# Agregar la raíz del proyecto al path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# Cargar los modelos
RUTA_MODELO_TALLA = os.path.join(BASE_DIR, 'modelo_ia', 'artefactos', 'modelo_talla.pkl')
RUTA_MODELO_SILUETA = os.path.join(BASE_DIR, 'modelo_ia', 'artefactos', 'modelo_silueta.pkl')

print("=" * 60)
print("PRUEBAS UNITARIAS DEL MODELO DE IA - VESTIGO")
print("=" * 60)

# Verificar que existan los archivos
assert os.path.exists(RUTA_MODELO_TALLA), f"No existe: {RUTA_MODELO_TALLA}"
assert os.path.exists(RUTA_MODELO_SILUETA), f"No existe: {RUTA_MODELO_SILUETA}"
print("✓ Los archivos de modelos existen")

# Cargar modelos
modelo_talla = joblib.load(RUTA_MODELO_TALLA)
modelo_silueta = joblib.load(RUTA_MODELO_SILUETA)
print("✓ Modelos cargados correctamente")


# CASOS DE PRUEBA

casos_prueba = [
    # (pecho, cintura, cadera, altura, talla_esperada_min, descripcion)
    {"pecho": 78, "cintura": 60, "cadera": 84, "altura": 155, "talla": "XS", "desc": "Persona muy pequeña"},
    {"pecho": 85, "cintura": 66, "cadera": 90, "altura": 160, "talla": "S", "desc": "Persona pequeña"},
    {"pecho": 90, "cintura": 73, "cadera": 96, "altura": 167, "talla": "M", "desc": "Persona mediana"},
    {"pecho": 97, "cintura": 80, "cadera": 103, "altura": 172, "talla": "L", "desc": "Persona grande"},
    {"pecho": 105, "cintura": 88, "cadera": 111, "altura": 177, "talla": "XL", "desc": "Persona extra grande"},
    {"pecho": 115, "cintura": 96, "cadera": 120, "altura": 182, "talla": "XXL", "desc": "Persona doble extra grande"},
]

print("\n" + "=" * 60)
print("EJECUTANDO PRUEBAS")
print("=" * 60)

aprobadas = 0
falladas = 0

for i, caso in enumerate(casos_prueba, 1):
    entrada = np.array([[caso["pecho"], caso["cintura"], caso["cadera"], caso["altura"]]])
    talla_pred = modelo_talla.predict(entrada)[0]
    silueta_pred = modelo_silueta.predict(entrada)[0]

    exito = talla_pred == caso["talla"]

    if exito:
        aprobadas += 1
        estado = "✅ PASÓ"
    else:
        falladas += 1
        estado = "❌ FALLÓ"

    print(f"\nTest #{i}: {caso['desc']}")
    print(f"   Entrada: pecho={caso['pecho']}, cintura={caso['cintura']}, cadera={caso['cadera']}, altura={caso['altura']}")
    print(f"   Esperado: {caso['talla']}")
    print(f"   Obtenido: {talla_pred} (silueta: {silueta_pred})")
    print(f"   {estado}")


# PRUEBAS DE VALIDACIÓN (casos límite)
print("\n" + "=" * 60)
print("PRUEBAS DE VALIDACIÓN (casos límite)")
print("=" * 60)

# Test: predicción con valores extremos
casos_limite = [
    {"pecho": 50, "cintura": 40, "cadera": 50, "altura": 120, "desc": "Mínimo permitido"},
    {"pecho": 200, "cintura": 200, "cadera": 200, "altura": 220, "desc": "Máximo permitido"},
]

for i, caso in enumerate(casos_limite, len(casos_prueba) + 1):
    try:
        entrada = np.array([[caso["pecho"], caso["cintura"], caso["cadera"], caso["altura"]]])
        talla_pred = modelo_talla.predict(entrada)[0]
        silueta_pred = modelo_silueta.predict(entrada)[0]
        print(f"\nTest #{i}: {caso['desc']}")
        print(f"   Predicción: Talla {talla_pred}, Silueta {silueta_pred}")
        print(f"   ✅ PASÓ (no lanza error)")
        aprobadas += 1
    except Exception as e:
        print(f"\nTest #{i}: {caso['desc']}")
        print(f"   ❌ FALLÓ: {e}")
        falladas += 1

# RESULTADOS
print("\n" + "=" * 60)
print("RESULTADOS DE LAS PRUEBAS")
print("=" * 60)
print(f"✅ Pruebas aprobadas: {aprobadas}")
print(f"❌ Pruebas falladas: {falladas}")
total = aprobadas + falladas
print(f"📊 Tasa de éxito: {aprobadas}/{total} ({(aprobadas/total)*100:.1f}%)")

if falladas == 0:
    print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
else:
    print(f"\n⚠ Hay {falladas} prueba(s) fallida(s) que requieren atención.")

print("=" * 60)