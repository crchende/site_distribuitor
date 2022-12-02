# cip_chende@yahoo.com
# 2022/07/30
#
# API simplu pentru MySQL - fara OOP
#
# Server DB folosit: MySQL Distrib 8.0.30, for Linux (x86_64)
#                    (nu am testat pe Windows dar cel mai probabil functioneaza)
#
# NOTA:
# Sunt anumite diferente intre MySQL si MariaDB. 
# Posibil sa fie probleme la importul bazei de date de mai jos in MariaDB.
# Daca nu merge, recomand folosirea MySQL
# 
# baza date: site_distribuitor
# fisier SQL git: 
#
# Comanda instalare DB:
# mysql -u utilizator -p  site_distribuitor < site_distribuitor_base_mysql_cu_db_20220728_01.sql
#
# NOTA: Trebuie sa aveti instalat pe calculator clientul si serverul MySQL.
#       Puteti folosi varianta 'community' de pe site-ul: 
#       Dupa instalare ar trebui sa puteti rula din consola comanda de mai sus.
#
#       In caz ca nu functioneaza, verificati unde aveti instalat mysql-ul
#       Adaugati in PATH calea catre mysql.
#

import mysql.connector
from mysql.connector import errorcode


################################################################################
# Informatii pentru conectarea la baza de date:
################################################################################
config = {
  'user': 'flaskdev',
  'password': 'parolaflask',
  'host': '127.0.0.1',
  'database': 'site_distribuitor',
  'raise_on_warnings': True,
  'autocommit': True,
}

# initializare variabila conexiune - cnx
cnx = None

################################################################################
# Conectare la baza serverul de baze de date si la baza de date flask_site1
################################################################################
def conectare(cfg):
    try:
        print(f"Incerc sa ma conectez la serverul local MySQL si la baza de date: {config['database']}")
        cnx = mysql.connector.connect(**cfg)
      
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print(f"EROARE conectare la baza de date: Probleme cu user-ul si/sau parola")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"EROARE conectare la baza de date: Baza de date: {config['database']}, nu exista")
        else:
            print(f"EROARE conectare la baza de date: {err}")
        
        print("Rezolvati, va rog, problema de conectare si reincercati!")
        exit()

    print(f"SUCCES: Conexiunea la {config['host']}:port_default si Baza Date: {config['database']} a reusit.")
    return cnx

def _interogare_db(cmd_sql, parametrii):
    global cnx, config
    ok_commit = 0
    cmd = cmd_sql.split()[0]
    #print(cmd)
    if cmd != "SELECT" and cmd != "SHOW":
        ok_commit = 1
        
    print("DBG: cmd_sql:     ", cmd_sql)
    print("DBG: paramertrii: ", parametrii)
        
    ok_db = 0
    
    ret = []
    
    if cnx.is_connected():         
        ok_db = 1
    else:
        print("selecteaza - probleme conexiune db, reconectare")
        cnx = conectare_si_generare_cursor(config)
        if cnx.is_connected():
            ok_db = 1
        else:
            print("EROARE Conexiune:")
            print(f"DBG: parametrii: host: {config['host']}; port: default; user: {config['user']}")
            print("Verificati configuratia / serverul DB, legatura la net si reincercati!")
            return "EROARE Conexiune"
                
    if ok_db:
        with cnx.cursor() as cursor:
            try:
                if parametrii:          
                    cursor.execute(cmd_sql, parametrii)
                else:
                    cursor.execute(cmd_sql)
                # UPDATE, DELETE, INSERT
                if ok_commit:
                    cnx.commit()
                ret = cursor.fetchall()
            except Exception as e:
                print(f"EROARE {cmd}")
                print(f"DBG: interogare SQL:", cmd_sql)
                print(f"DBG: eroare:", e)
                ret = f"EROARE {cmd}, eroare = {e}"

    return ret 

def selecteaza(cmd_sql, *parametrii):
    return _interogare_db(cmd_sql, parametrii)               

def insereaza(cmd_sql, *parametrii):
    return _interogare_db(cmd_sql, parametrii)
    
def sterge(cmd_sql, *parametrii):
    return _interogare_db(cmd_sql, parametrii)

def modifica(cmd_sql, *parametrii):
    return _interogare_db(cmd_sql, parametrii)

def deconectare():
    global cnx
    print("\nInchid conexiunea la serverul MySQL")
    cnx.close()

# Creere conexiune - se va face cand se importa modulul in site_distribuitor
cnx = conectare(config)
