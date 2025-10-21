import sys
import os
import sqlite3
import csv

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_database_file(db_version):

    if not os.path.exists(f'database/{db_version}'):
        print(f"Folder {db_version} in folder database/ does not exist.")
        return
    if not os.path.exists(f'database/{db_version}/Datamodel_Sections_v{db_version}.csv') or not os.path.exists(f'database/{db_version}/Datamodel_Registers_v{db_version}.csv'):
        print(f"CSV files for version {db_version} are missing.")
        return
    if os.path.exists(f"database/{db_version}/Datamodel_v{db_version}.db"):
        print(f"Database file for version {db_version} already exists, delete the file before regenerating.")
        return

    conn = sqlite3.connect(f"database/{db_version}/Datamodel_v{db_version}.db")
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    major, minor = db_version.split(".")
    cursor.execute("CREATE TABLE IF NOT EXISTS Version (Id INTEGER PRIMARY KEY, Version INTEGER, Revision INTEGER)")
    cursor.execute("INSERT INTO Version (Version, Revision) VALUES (?, ?)", (int(major), int(minor)))

    cursor.execute("CREATE TABLE IF NOT EXISTS Section_List (Id INTEGER PRIMARY KEY, Name TEXT, Block TEXT, Address INTEGER)")

    with open(f'database/{db_version}/Datamodel_Sections_v{db_version}.csv', 'r') as f:
        data = csv.DictReader(f)
        to_db = [(i['Name'], i['Block'], i['Address']) for i in data]
        cursor.executemany("INSERT INTO Section_List (Name, Block, Address) VALUES (?, ?, ?)", to_db)
    
    conn.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS Register_List (ID INTEGER PRIMARY KEY, Name TEXT, Class TEXT, Type TEXT, Size INTEGER, Offset INTEGER, Section TEXT, EnumID INTEGER, MapType TEXT, MapLen INTEGER, MUID INTEGER, OutType INTEGER, ExtractExpr TEXT, InjectExpr TEXT, FormatString TEXT, Writable INTEGER, TranslateID INTEGER, DefUserLevel INTEGER, ReferenceID INTEGER)
                   """)
    
    with open(f'database/{db_version}/Datamodel_Registers_v{db_version}.csv', 'r') as f:
        data = csv.DictReader(f, delimiter=';')
        to_db = [(i['Name'], i['Class'], i['Type'], i['Size'], i['Offset'], i['Section'], i['EnumID'], i['MapType'], i['MapLen'], i['MUID'], i['OutType'], i['ExtractExpr'], i['InjectExpr'], i['FormatString'], i['Writable'], i['TranslateID'], i['DefUserLevel'], i['ReferenceID']) for i in data]
        cursor.executemany("INSERT INTO Register_List (Name, Class, Type, Size, Offset, Section, EnumID, MapType, MapLen, MUID, OutType, ExtractExpr, InjectExpr, FormatString, Writable, TranslateID, DefUserLevel, ReferenceID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", to_db)

    # Commit the changes
    conn.commit()

if __name__ == "__main__":
    version_availabes = os.listdir('database')
    print("Versions found in database folder:")
    for db_version in enumerate(version_availabes):
        if not os.path.exists(f"database/{db_version[1]}/Datamodel_v{db_version[1]}.db"):
            print(f"{db_version[0]}) {db_version[1]}*")
        else:
            print(f"{db_version[0]}) {db_version[1]}")
    print("* means that database file is missing.")
    version_selected = int(input("Select database version to generate: "))
    create_database_file(version_availabes[version_selected])
