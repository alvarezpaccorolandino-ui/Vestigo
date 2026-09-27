"""
Pruebas Funcionales de la API de IA VESTIGO
=============================================
Verifica que los endpoints de la API FastAPI funcionen correctamente.
Requiere que la API esté corriendo en http://127.0.0.1:8001

Ejecutar: python api_IA/test_api.py

Autor: Ronal + equipo VESTIGO
Fecha: Septiembre 2026
"""

import requests
import time
import json

# Configuración
API_URL = "http://127.0.0.1:8001"

print("=" * 60)
print("PRUEBAS FUNCIONALES DE LA API - VESTIGO")
print("=" * 60)

resultados = []


def ejecutar_prueba(nombre, funcion):
    """Ejecuta una prueba y registra el resultado."""
    print(f"\n{'─' * 60}")
    print(f"🧪 {nombre}")
    print(f"{'─' * 60}")
    try:
        exito = funcion()
        resultados.append((nombre, exito))
        if exito:
            print(f"✅ PASÓ")
        else:
            print(f"❌ FALLÓ")
    except Exception as e:
        print(f"❌ FALLÓ: {e}")
        resultados.append((nombre, False))


# ============================================================
# TEST 1: Endpoint raíz
# ============================================================
def test_endpoint_raiz():
    """Verifica que el endpoint raíz / responda correctamente."""
    respuesta = requests.get(f"{API_URL}/")
    print(f"   Status: {respuesta.status_code}")
    print(f"   Respuesta: {json.dumps(respuesta.json(), indent=2, ensure_ascii=False)}")

    assert respuesta.status_code == 200, "Debe responder 200"
    data = respuesta.json()
    assert data["api"] == "VESTIGO IA", "Debe ser VESTIGO IA"
    assert data["estado"] == "funcionando", "Debe estar funcionando"
    return True


# ============================================================
# TEST 2: Health check
# ============================================================
def test_health():
    """Verifica que el modelo esté cargado."""
    respuesta = requests.get(f"{API_URL}/health")
    print(f"   Status: {respuesta.status_code}")
    print(f"   Respuesta: {json.dumps(respuesta.json(), indent=2)}")

    assert respuesta.status_code == 200, "Debe responder 200"
    data = respuesta.json()
    assert data["modelo_talla_cargado"] is True, "El modelo de talla debe estar cargado"
    assert data["modelo_silueta_cargado"] is True, "El modelo de silueta debe estar cargado"
    return True


# ============================================================
# TEST 3: Predicción exitosa
# ============================================================
def test_prediccion_exitosa():
    """Verifica que la predicción funcione con datos válidos."""
    datos = {
        "pecho": 92,
        "cintura": 74,
        "cadera": 98,
        "altura": 168
    }
    respuesta = requests.post(f"{API_URL}/predecir-talla", json=datos)
    print(f"   Datos enviados: {datos}")
    print(f"   Status: {respuesta.status_code}")
    print(f"   Respuesta: {json.dumps(respuesta.json(), indent=2, ensure_ascii=False)}")

    assert respuesta.status_code == 200, "Debe responder 200"
    data = respuesta.json()
    assert "talla" in data, "Debe incluir talla"
    assert "silueta" in data, "Debe incluir silueta"
    assert data["talla"] in ["XS", "S", "M", "L", "XL", "XXL"], "Talla válida"
    return True


# ============================================================
# TEST 4: Predicción con múltiples casos
# ============================================================
def test_multiples_predicciones():
    """Verifica predicciones con diferentes tipos de cuerpo."""
    casos = [
        {"pecho": 78, "cintura": 60, "cadera": 84, "altura": 155, "esperada": "XS"},
        {"pecho": 92, "cintura": 74, "cadera": 98, "altura": 168, "esperada": "M"},
        {"pecho": 115, "cintura": 96, "cadera": 120, "altura": 182, "esperada": "XXL"},
    ]
    for caso in casos:
        esperada = caso.pop("esperada")
        respuesta = requests.post(f"{API_URL}/predecir-talla", json=caso)
        data = respuesta.json()
        print(f"   {caso} → {data['talla']} (esperado: {esperada})")
        assert respuesta.status_code == 200, "Debe responder 200"
        assert data["talla"] == esperada, f"Esperaba {esperada}, obtuve {data['talla']}"
    return True


# ============================================================
# TEST 5: Validación de inputs (rechaza datos inválidos)
# ============================================================
def test_validacion_inputs():
    """Verifica que la API rechace datos fuera de rango."""
    print("   Probando datos inválidos...")

    # Caso 1: pecho muy pequeño
    datos = {"pecho": 30, "cintura": 74, "cadera": 98, "altura": 168}
    respuesta = requests.post(f"{API_URL}/predecir-talla", json=datos)
    print(f"   Pecho=30 (inválido) → Status {respuesta.status_code}")
    assert respuesta.status_code == 422, "Debe rechazar pecho < 50"

    # Caso 2: altura fuera de rango
    datos = {"pecho": 92, "cintura": 74, "cadera": 98, "altura": 300}
    respuesta = requests.post(f"{API_URL}/predecir-talla", json=datos)
    print(f"   Altura=300 (inválido) → Status {respuesta.status_code}")
    assert respuesta.status_code == 422, "Debe rechazar altura > 220"

    # Caso 3: campos faltantes
    datos = {"pecho": 92}
    respuesta = requests.post(f"{API_URL}/predecir-talla", json=datos)
    print(f"   Solo pecho (incompleto) → Status {respuesta.status_code}")
    assert respuesta.status_code == 422, "Debe rechazar datos incompletos"

    return True


# ============================================================
# TEST 6: Rendimiento (tiempo de respuesta)
# ============================================================
def test_rendimiento():
    """Verifica que la API responda en menos de 500ms."""
    datos = {"pecho": 92, "cintura": 74, "cadera": 98, "altura": 168}

    tiempos = []
    for i in range(10):
        inicio = time.time()
        requests.post(f"{API_URL}/predecir-talla", json=datos)
        fin = time.time()
        tiempos.append((fin - inicio) * 1000)

    promedio = sum(tiempos) / len(tiempos)
    maximo = max(tiempos)
    minimo = min(tiempos)

    print(f"   10 peticiones realizadas:")
    print(f"   - Tiempo promedio: {promedio:.1f} ms")
    print(f"   - Tiempo mínimo: {minimo:.1f} ms")
    print(f"   - Tiempo máximo: {maximo:.1f} ms")

    assert promedio < 500, f"El promedio debe ser < 500ms (fue {promedio:.1f}ms)"
    return True


# ============================================================
# EJECUTAR TODAS LAS PRUEBAS
# ============================================================
ejecutar_prueba("TEST 1: Endpoint raíz (/)", test_endpoint_raiz)
ejecutar_prueba("TEST 2: Health check (/health)", test_health)
ejecutar_prueba("TEST 3: Predicción exitosa", test_prediccion_exitosa)
ejecutar_prueba("TEST 4: Múltiples predicciones", test_multiples_predicciones)
ejecutar_prueba("TEST 5: Validación de inputs", test_validacion_inputs)
ejecutar_prueba("TEST 6: Rendimiento (tiempo de respuesta)", test_rendimiento)

# ============================================================
# RESUMEN FINAL
# ============================================================
print("\n" + "=" * 60)
print("RESUMEN DE PRUEBAS FUNCIONALES")
print("=" * 60)

aprobadas = sum(1 for _, exito in resultados if exito)
total = len(resultados)

for nombre, exito in resultados:
    estado = "✅ PASÓ" if exito else "❌ FALLÓ"
    print(f"{estado}  {nombre}")

print(f"\n📊 Total: {aprobadas}/{total} pruebas aprobadas ({(aprobadas/total)*100:.1f}%)")

if aprobadas == total:
    print("\n🎉 ¡TODAS LAS PRUEBAS FUNCIONALES PASARON!")
else:
    print(f"\n⚠ Hay {total - aprobadas} prueba(s) fallida(s).")

print("=" * 60)