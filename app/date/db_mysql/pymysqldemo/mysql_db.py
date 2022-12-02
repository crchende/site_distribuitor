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



################################################################################
# Conectare la baza serverul de baze de date si la baza de date flask_site1
################################################################################
def conectare_si_generare_cursor(cfg):
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

def interogare_db(cmd_sql):
    global cnx, config
    ok_commit = 0
    cmd = cmd_sql.split()[0]
    #print(cmd)
    if cmd != "SELECT" and cmd != "SHOW":
        ok_commit = 1
        
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

def selecteaza(cmd_sql):
    return interogare_db(cmd_sql)               

def insereaza(cmd_sql):
    return interogare_db(cmd_sql)
    
def sterge(cmd_sql):
    return interogare_db(cmd_sql)

def modifica(cmd_sql):
    return interogare_db(cmd_sql)


cnx = conectare_si_generare_cursor(config)

#print("Conexiune:", dir(cnx))
#print("Cursor:", dir(cursor))

#exit()

################################################################################
# Interogari SQL: SELECT, INSERT, UPDATE, DELETE
################################################################################

###################
# SHOW
###################
print("\n'SHOW DATABASES'. Afisare baze de date disponibile pe server:")
q = "SHOW databases;"
print(interogare_db(q))

print(f"\n'SHOW TABLES'. Afisare tabele in baza de date {config['database']}")
q = "SHOW tables;"
print(interogare_db(q))


###################
# Operatii CRUD
#          Create, Read, Update, Delete
###################

###################
# SELECT (R ead)
###################
print("\nSELECT compus produse, cu afisare nume produator, nu id:")
q_compus = "SELECT produse.id, producatori.nume, produse.nume \
            FROM producatori, produse \
            WHERE produse.id_producator = producatori.id;"
print(selecteaza(q_compus))

###################
# Verificare refacere automata conexiune
###################
print("\nTEST Eroare conexiune - inchid conexiunea")
cnx.close()
print("apelez selecteaza - care incearca sa refaca conexiunea")
print(selecteaza(q_compus))

print("\nSELECT producatori:")
q = "SELECT * from producatori;"
print(interogare_db(q))
 
##################### 
# INSERT - adaugare (exemplu): (C reate)
#####################
#INSERT INTO `site_distribuitor`.`producatori` (`id`, `nume`) VALUES ('4', 'Heidi');
# cum coloana 'id' a fost configurata cu auto-increment, nu este necesar sa
# dam valoarea ID-ului. Baza de date va face increment
print("\nADAUARE: producator - Heidi")
q = "INSERT INTO `site_distribuitor`.`producatori` (`nume`) VALUES ('Heidi');"
insereaza(q)

print("\nVERIFICARE_INSERT")
q = "SELECT * from producatori;"
print(interogare_db(q))

print("\nVerific ca nu pot adauga de doua ori acelasi producator - nume unic")
print("\nADAUARE: producator - Heidi")
q = "INSERT INTO `site_distribuitor`.`producatori` (`nume`) VALUES ('Heidi');"
insereaza(q)

print("\nVERIFICARE ca nu avem doi producatori Heidi")
q = "SELECT * from producatori;"
print(interogare_db(q))

######################
# UPDATE - modificare (exemplu) (U pdate)
######################
print("\nMODIFICARE: Heidi -> Heidi123")
q = "UPDATE `site_distribuitor`.`producatori` SET `nume` = 'Heidi123' WHERE (`nume` = 'Heidi');"
modifica(q)
print("VERIFICARE MODIFICARE")
q = "SELECT * from producatori;"
print(interogare_db(q))

print("\nVerificare MODIFICARE: inregistrare inexistenta (Heidi care acum este Heidi123):")
q = "UPDATE `site_distribuitor`.`producatori` SET `nume` = 'Heidi123' WHERE (`nume` = 'Heidi');"
modifica(q)
print("VERIFICARE ca nu s-a modificat nimic")
q = "SELECT * from producatori;"
print(interogare_db(q))

######################
# Interogare DELETE - stertere (exemplu) (D elete)
######################
print("\nSTERGERE: Heidi123")
q = "DELETE FROM `site_distribuitor`.`producatori` WHERE (`nume` = 'Heidi123');"
sterge(q)
print("VERIFICARE STERGERE")
q = "SELECT * from producatori;"
print(interogare_db(q))

print("\nVerificare STERGERE inregistrare inexistenta: Heidi123")
q = "DELETE FROM `site_distribuitor`.`producatori` WHERE (`nume` = 'Heidi123');"
sterge(q)
print("VERIFICARE ca nu s-a sters nimic")
q = "SELECT * from producatori;"
print(interogare_db(q))

print("\nDe observat id-ul producatorului 'Heidi'. Va fi incrementat la fiecare")
print("rulare a programului. Acesta a fost configurat de tip 'autoincrement'")
    
################################################################################
# Terminare program - inchid conexiunea la server
################################################################################


print("\nInchid conexiunea la serverul MySQL")
cnx.close()

