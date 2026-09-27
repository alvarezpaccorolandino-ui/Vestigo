#!/usr/bin/env bash
# build.sh — Script de construcción para Render

set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Entrenar modelo si no existe
if [ ! -f "modelo_ia/artefactos/modelo_talla.pkl" ]; then
    python modelo_ia/entrenar_modelo.py
fi

echo "✅ Build completado con éxito"