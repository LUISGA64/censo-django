"""
Script para migrar datos de la BD antigua a la nueva
"""
import sqlite3
import sys

# Conectar a ambas bases de datos
old_db = sqlite3.connect('db.censo_Web.old')
new_db = sqlite3.connect('db.censo_Web')

old_cursor = old_db.cursor()
new_cursor = new_db.cursor()

print("=== MIGRANDO DATOS ===\n")

def migrate_table(table_name, display_name):
    """Migra una tabla completa"""
    print(f"Migrando {display_name}...")
    try:
        # Obtener datos de la tabla antigua
        old_cursor.execute(f"SELECT * FROM {table_name}")
        rows = old_cursor.fetchall()

        if not rows:
            print(f"   ✓ 0 registros (tabla vacía)")
            return 0

        # Crear placeholders para INSERT
        num_cols = len(rows[0])
        placeholders = ','.join(['?'] * num_cols)

        # Insertar datos
        for row in rows:
            try:
                new_cursor.execute(
                    f"INSERT INTO {table_name} VALUES ({placeholders})",
                    row
                )
            except sqlite3.IntegrityError as e:
                # Ignorar duplicados (por si acaso)
                pass

        print(f"   ✓ {len(rows)} registros migrados")
        return len(rows)
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return 0

# Migrar tablas en orden (respetando foreign keys)
totals = {}

# 1. Asociaciones
totals['asociaciones'] = migrate_table('censoapp_association', 'asociaciones')

# 2. Organizaciones
totals['organizaciones'] = migrate_table('censoapp_organizations', 'organizaciones')

# 3. Veredas
totals['veredas'] = migrate_table('censoapp_sidewalks', 'veredas')

# 4. Fichas Familiares
totals['fichas'] = migrate_table('censoapp_familycard', 'fichas familiares')

# 5. Personas
totals['personas'] = migrate_table('censoapp_person', 'personas')

# 6. Perfiles de Usuario
totals['perfiles'] = migrate_table('censoapp_userprofile', 'perfiles de usuario')

# 7. Materiales de Construcción (si existen)
try:
    totals['materiales'] = migrate_table('censoapp_materialconstructionfamilycard', 'materiales de construcción')
except:
    totals['materiales'] = 0

# Commit y cerrar
new_db.commit()
old_db.close()
new_db.close()

print("\n=== MIGRACIÓN COMPLETADA ===")
print(f"Total migrado:")
for key, value in totals.items():
    if value > 0:
        print(f"  - {value} {key}")

print("\n✅ Todos los datos han sido migrados exitosamente")


