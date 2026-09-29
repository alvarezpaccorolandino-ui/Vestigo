#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Crear superusuario automáticamente si no existe
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@vestigo.com', 'Vestigo2026!')
    print('✅ Superusuario "admin" creado')
else:
    print('ℹ️ Superusuario ya existe')
EOF

# Entrenar modelo si no existe
if [ ! -f "modelo_IA/artefactos/modelo_talla.pkl" ]; then
    python modelo_IA/entrenar_modelo.py
fi

echo "✅ Build completado con éxito"