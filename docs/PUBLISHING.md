# Publicar el perfil flaco332/flaco332

Esta entrega está creada solamente en la carpeta local. No se inicializó Git,
no se creó un repositorio remoto y no se ejecutó ningún push.

## 1. Revisar la entrega

Abre `docs/preview.html` en tu navegador. Los botones Auto, Dark y Light permiten
comparar los temas sin conexión. Es una aproximación visual al layout de GitHub.

Para regenerar assets, actualizar la vista previa y validar los archivos:

```powershell
python scripts/build_assets.py
python scripts/preview.py
python scripts/validate.py
```

Los tres scripts usan solamente la biblioteca estándar de Python.
El README publicado funciona sin ejecutar scripts ni instalar dependencias.

## 2. Inicializar Git

Abre PowerShell dentro de la carpeta `github-profile` y ejecuta:

```powershell
git init -b main
git config user.name "flaco332"
git config user.email "crdeveloper@proton.me"
git add README.md assets docs scripts .gitignore .gitattributes
git diff --cached --stat
git commit -m "Create terminal-inspired GitHub profile"
```

La identidad del commit usa el alias y el email público autorizados.
También puedes sustituir el email por tu dirección noreply de GitHub,
disponible en Settings → Emails.

## 3. Crear el repositorio remoto

1. Inicia sesión en GitHub como **flaco332** y abre [New repository](https://github.com/new).
2. En **Owner**, selecciona **flaco332**.
3. En **Repository name**, escribe **flaco332**.
4. Selecciona **Public**.
5. Deja desactivada la inicialización con README, `.gitignore` y licencia: ya
   tienes los archivos localmente y necesitas un repositorio remoto vacío.
6. Haz clic en **Create repository**.

El repositorio público con nombre idéntico al usuario y un `README.md` no vacío
en la raíz habilita el README del perfil. Consulta la
[documentación oficial de GitHub](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme).

## 4. Subir por primera vez

Estos comandos son para ejecutarlos tú después de crear el repositorio vacío:

```powershell
git remote add origin https://github.com/flaco332/flaco332.git
git remote -v
git push -u origin main
```

Completa la autenticación de GitHub si Git Credential Manager la solicita.
Después abre [tu perfil](https://github.com/flaco332) y comprueba el README
en modo claro, oscuro y una ventana estrecha.

## 5. Cambios futuros

Edita `README.md` para cambiar textos y enlaces. Para cambiar los SVG, modifica
`scripts/build_assets.py` y ejecuta los tres scripts del paso 1.
La carpeta `.preview/` está excluida de Git y se reserva para capturas y auditorías locales.
