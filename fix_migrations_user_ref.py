import os

# Carpeta donde buscar migraciones
apps = ["AUTENTICACION", "FE"]

old_ref = "to='AUTENTICACION.user'"
new_ref = "to='AUTENTICACION.User'"

for app in apps:
    mig_dir = os.path.join(app, "migrations")
    if not os.path.isdir(mig_dir):
        continue

    for fname in os.listdir(mig_dir):
        if fname.endswith(".py") and fname != "__init__.py":
            fpath = os.path.join(mig_dir, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()

            if old_ref in content:
                print(f"🔧 Corrigiendo {fpath} ...")
                new_content = content.replace(old_ref, new_ref)

                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(new_content)

print("✅ Corrección terminada. Ahora ejecuta: py manage.py migrate")
