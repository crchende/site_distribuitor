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
        print("Incerc sa ma conectez la serverul local MySQL/MariaDB si la baza de date flask_site1")
        cnx = mysql.connector.connect(**cfg)
      
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Probleme cu user-ul sau parola")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Baza de date nu exista")
        else:
            print(err)
        
        print("Verificati, va rog problema de conectare !!!")
        # programul se termina daca conexiunea esueaza
        exit()

    cursor = cnx.cursor()
    print("Conexiunea a reusit, returnare conexiune & cursor")
    return cnx, cursor

def cere_date(cmd_sql):
    global cnx, cursor, config
    
    if cnx.is_connected():
        cursor.execute(cmd_sql)
    else:
         cnx, cursor = conectare_si_generare_cursor(config)
         cursor.execute(cmd_sql)            

cnx, cursor = conectare_si_generare_cursor(config)

#print("Conexiune:", dir(cnx))
#print("Cursor:", dir(cursor))

#exit()

################################################################################
# Interogari SQL: SELECT, INSERT, UPDATE, DELETE
################################################################################

# SELECT
#q = "SHOW tables;"
q = "SELECT * from producatori;"

# Variante de citire rezultate interogara

print("\n1. Varianta cu fetchone si iterare rand cu rand")
#cursor.execute(q)
cere_date(q)
# c.rowcount nu functioneaza - arata -1
#print("cursor.stored_results:", cursor.stored_results())

print("Rezultat interogare: (fiecare rand este sub forma unui tuplu)")
while True:
    rand = cursor.fetchone()
    if not rand:
        break
    print(rand)

print("\n2. Varianta cu fetchall:")
cursor.execute(q)
# print(c.rowcount) - nu functioneaza. arata -1
randuri = cursor.fetchall();
for r in randuri:
    print(r)

print("\n3. Varianta 3 - cu iterare directa rezultat interogare")
cursor.execute(q)
for rand in cursor:
    print(rand)

############################################
# test eroare
# inchid cursorul si conexiunea
# - interogarea simpla esueaza
# - daca folosesc functia executa_comanda_sql functioneaza, detectez pierderea
#   conexiunii si o restabilesc
############################################
print("\n TEST Eroare conexiune - inchid cursorul si conexiunea\n")
cursor.close() # inchid si cursorul
cnx.close()

print("\nInterogare compusa, cu date din mai multe tabele:")
q_compus = "SELECT produse.id, producatori.nume, produse.nume \
            FROM producatori, produse \
            WHERE produse.id_producator = producatori.id;"

try:
    cursor.execute(q)
except Exception as e:
    
    print("EROARE la executare interogare dupa inchiderea conexiunii: ", e)

print("\nReiau interogarea cu functia care trateaza eroarea: \n")


cere_date(q_compus)
for p_id, prod_n, prds_n in cursor:
    frmt = "{:3} {:<10} {:30}"
    print(frmt.format(p_id, prod_n, prds_n))
 
    
################################################################################
# Terminare program - inchid conexiunea la server
################################################################################

cursor.close()
print("Inchid conexiunea la serverul MySQL")
cnx.close()

