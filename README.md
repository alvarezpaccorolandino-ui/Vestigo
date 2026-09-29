# 🛍️ VESTIGO — Sistema de Ventas de Ropa con IA

Sistema de venta de ropa sin etiquetas de género, con un modelo de 
inteligencia artificial que recomienda la talla y silueta perfecta 
para cada cliente.

> **Proyecto Final** — Desarrollo de Sistemas Inteligentes II  
> Instituto — Ciclo 2025-2  
> Integrantes: **Ronal** y **Edwin**

---

## 🌐 URLs de Producción (Render)

| Servicio | URL |
| :--- | :--- |
| **Catálogo VESTIGO** | https://vestigo-web.onrender.com |
| **Admin Django** | https://vestigo-web.onrender.com/admin/ |
| **API IA (Swagger)** | https://vestigo-ia.onrender.com/docs |

---

## 📋 Descripción

VESTIGO es una aplicación web que permite:

- 🛒 Comprar ropa sin filtros binarios de género
- 🤖 Recibir recomendaciones de talla y silueta con IA
- 💳 Pagar con Yape, Plin, Tarjeta, Transferencia o Contraentrega
- 📦 Elegir entre recojo en tienda o delivery
- 📊 Administrar el inventario desde un panel Django

---

## 🏗️ Arquitectura del Sistema
┌─────────────────────────────────────────────────────────────┐
│ USUARIO (Navegador) │
│ Catálogo HTML + CSS + JavaScript │
└───────────────┬─────────────────────────┬───────────────────┘
│ │
│ (1) Productos │ (2) Predicción
│ Ventas │ de talla
▼ ▼
┌─────────────────────────┐ ┌─────────────────────────────┐
│ BACKEND DJANGO │ │ API IA (FastAPI) │
│ Render │ │ Render │
│ - Modelos (ORM) │ │ - Modelo de tallas │
│ - API REST (DRF) │ │ - Modelo de siluetas │
│ - Admin │ │ - Swagger Docs │
└───────────┬─────────────┘ └──────────────┬──────────────┘
│ │
▼ ▼
┌──────────────┐ ┌──────────────────┐
│ SQLite DB │ │ Modelos .pkl │
│ db.sqlite3 │ │ (Random Forest) │
└──────────────┘ └──────────────────┘

---

## 🧰 Tecnologías Utilizadas

### Backend
- **Python 3.13**
- **Django 6.1.1** — Framework web principal
- **Django REST Framework** — API REST
- **django-cors-headers** — CORS para el frontend
- **Gunicorn** — Servidor WSGI
- **Whitenoise** — Archivos estáticos

### Frontend
- **HTML5 + CSS3 + JavaScript (Vanilla)**
- Diseño responsive personalizado (negro + dorado)

### Inteligencia Artificial
- **scikit-learn** — Random Forest (100 árboles)
- **pandas + numpy** — Procesamiento de datos
- **joblib** — Serialización de modelos
- **FastAPI + Uvicorn** — API del modelo
- **Pydantic** — Validación de datos

### Base de Datos
- **SQLite** (desarrollo)

### Despliegue
- **Render** (plan gratuito)
- **GitHub** (control de versiones)

---

## 🚀 Instalación y Ejecución Local

### Requisitos Previos
- Python 3.10 o superior
- Git
- Navegador web (Chrome, Firefox o Edge)

### 1. Clonar el repositorio
```bash
git clone https://github.com/alvarezpaccorolandino-ui/Vestigo.git
cd Vestigo