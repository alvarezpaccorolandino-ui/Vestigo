#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

if [ ! -f "modelo_IA/artefactos/modelo_talla.pkl" ]; then
    python modelo_IA/entrenar_modelo.py
fi

echo "✅ Build completado con éxito"