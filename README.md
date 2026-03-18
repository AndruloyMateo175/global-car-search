# Car Finder Global

Buscador global de autos: specs técnicas, listings de venta y comparación de precios en más de 20 fuentes y 15+ países.

## Arquitectura

- **Backend**: Python + FastAPI
- **Frontend**: React + Vite
- **Deploy**: Docker → Railway

## Fuentes de datos incluidas

| Fuente | País/Región | Tipo |
|--------|-------------|------|
| CarQuery API | Global | Specs técnicas |
| AutoScout24 | Europa | Listings |
| Mobile.de | Alemania | Listings |
| Cars.com | USA | Listings |
| AutoTrader UK | Reino Unido | Listings |
| MercadoLibre | 8 países LATAM | Listings |
| CarGurus | USA/Canada/UK | Listings |
| Copart | Global | Subastas |
| BE FORWARD | Japón (export) | Listings |
| Cars.co.za | Sudáfrica | Listings |
| CarSales | Australia | Listings |
| OTOMOTO | Polonia | Listings |
| Dubizzle | Emiratos Árabes | Listings |

## Cómo agregar una nueva fuente

Editar `backend/services/listing_sources.py`:

```python
class MiNuevaFuente(ListingSource):
    name = "Mi Fuente"
    country = "País"
    country_code = "XX"
    base_url = "https://..."

    async def search(self, make, model, year=None):
        # Tu lógica de búsqueda
        return [CarListing(...)]

register_source(MiNuevaFuente())
```

---

## GUÍA PASO A PASO: Deploy en GitHub + Railway

### Paso 1: Crear cuenta en GitHub (si no tenés)
1. Ir a https://github.com
2. Click en "Sign up"
3. Seguir los pasos para crear tu cuenta

### Paso 2: Instalar Git (si no lo tenés)
1. Ir a https://git-scm.com/downloads
2. Descargar e instalar para tu sistema operativo
3. Abrir una terminal y verificar: `git --version`

### Paso 3: Subir el proyecto a GitHub
```bash
# 1. Abrir terminal en la carpeta del proyecto
cd car-finder-app

# 2. Inicializar repositorio Git
git init

# 3. Agregar todos los archivos
git add .

# 4. Hacer el primer commit
git commit -m "Car Finder Global - versión inicial"

# 5. Crear repositorio en GitHub:
#    - Ir a https://github.com/new
#    - Nombre: car-finder-global
#    - Dejarlo público o privado (como prefieras)
#    - NO marcar "Add a README" (ya tenemos uno)
#    - Click "Create repository"

# 6. Conectar y subir (reemplazar TU_USUARIO con tu usuario de GitHub):
git remote add origin https://github.com/TU_USUARIO/car-finder-global.git
git branch -M main
git push -u origin main
```

### Paso 4: Crear cuenta en Railway
1. Ir a https://railway.app
2. Click en "Login" → "Login with GitHub"
3. Autorizar Railway a acceder a tu GitHub

### Paso 5: Deploy en Railway
1. En Railway, click en **"New Project"**
2. Seleccionar **"Deploy from GitHub repo"**
3. Buscar y seleccionar **"car-finder-global"**
4. Railway detectará automáticamente el Dockerfile
5. Click en **"Deploy Now"**
6. Esperar 2-3 minutos a que compile y despliegue

### Paso 6: Obtener tu URL pública
1. Una vez deployado, ir a **Settings** del servicio
2. En la sección **"Networking"**, click en **"Generate Domain"**
3. Railway te dará una URL tipo: `car-finder-global-production.up.railway.app`
4. ¡Listo! Tu app está online

### Paso 7: Cada vez que hagas cambios
```bash
git add .
git commit -m "Descripción del cambio"
git push
```
Railway re-deploya automáticamente con cada push a GitHub.

---

## Desarrollo local

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend (en otra terminal)
cd frontend
npm install
npm run dev
```

La app estará en http://localhost:5173 (frontend) y http://localhost:8000 (API).

## API Endpoints

- `GET /api/search/?make=BMW&model=220i&year=2019` - Búsqueda completa
- `GET /api/specs/makes` - Listar marcas
- `GET /api/specs/models?make=BMW` - Listar modelos
- `GET /api/specs/detail?make=BMW&model=220i` - Specs técnicas
- `GET /api/sources/` - Ver fuentes disponibles
- `GET /api/health` - Health check
