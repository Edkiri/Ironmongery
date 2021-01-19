import sqlite3

try:
    conn = sqlite3.connect('comercial_guerra.db')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE ventas (
            fecha TEXT NOT NULL,
            tasa REAL NOT NULL,
            punto_de_venta REAL DEFAULT 0,
            pago_movil REAL DEFAULT 0,
            bolivares_efectivo REAL DEFAULT 0,
            dolares_efectivo REAL DEFAULT 0,
            zelle REAL DEFAULT 0,
            vuelto_bolivares REAL DEFAULT 0,
            vuelto_dolares REAL DEFAULT 0,
            total_dolares REAL NOT NULL);""")
    
    conn.commit()

except sqlite3.Error as error:
    print("Error while working with SQLite.", error)
finally:
    conn.close()