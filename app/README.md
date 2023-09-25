# Continut:

1. INITIALIZARE
1. Interogari SQLAlchemy

Vezi si directorul doc

# Initializare / resetare baza de date.

## Pornire flask shell:

Din app executa comanda 

    porneste_flask_shell        (linux) sau 
    porneste_flask_shell.bat    (windows)

Creare baza de date si populare cu datele din dateinitiale.date

## Executa din shell:

    >>> modele.BazaDateBaza.init_db()

pentru stergerea tuturor datelor executa:

    >>> modele.BazaDateBaza.sterge_continut_db()


# Interogari SQLAlchemy


## Interogare text - similar cu SQL

    db.session.execute(q) - intoarce un cursor

    db.session.execute('SELECT * FROM produse').all()
    [(1, 1, 'Ciocolata cu lapte'), 
    (2, 1, 'Ciocolata cu alune'),
    ...
    (8, 3, 'Ciocolata cu lapte')]

Recomandat ca sirul SQL sa fie construit ca 'text' din sqlalchemy.sql

    from sqlalchemy.sql import text
    q = text('SELECT * from produse')

## Interogare simpla - pe un tabel:

    x = modele.ModelProduse.query.with_entities(modele.ModelProduse.id, modele.ModelProduse.nume)

va selecta doar id-ul si numele din tabelul produse

    x = modele.ModelProduse.query.all()

va selecta toate campurile

    x = modele.ModelProduse.query.filter(modele.ModelProduse.id_producator == 1).all()

    #lista de obiecte:
    #(daca folosesc with_entities pentru a selecta doar anumite campuri, rezultatul
    #va fi o lista de tupluri)
    [Produse(id=1, id_producator=1 nume='Ciocolata cu lapte'), 
    Produse(id=2, id_producator=1 nume='Ciocolata cu alune')]

    x[1]
    Produse(id=2, id_producator=1 nume='Ciocolata cu alune')
    x[1].id
    2

## Interogare compusa - JOIN intre mai multe tabele

    Echivalent SQL
        SELECT producatori.nume, produse.nume FROM producatori, produse
            WHERE produse.id_producator = producatori.id

    SQLAlchemy:
    x = db.session.query(modele.ModelProduse, modele.ModelProducatori)\
            .join(modele.ModelProducatori, modele.ModelProduse.id_producator == \
                modele.ModelProducatori.id)\
            .with_entities(modele.ModelProducatori.nume, modele.ModelProduse.nume)\
            .all()
    
    print(x)
         
       [('Poiana', 'Ciocolata cu lapte'), 
        ('Poiana', 'Ciocolata cu alune'), 
        ('Kandia', 'Ciocolata cu iaurt'), 
        ('Kandia', 'Ciocolata cu caramel sarat'), 
        ('Kandia', 'Ciocolata cu biscuiti'), 
        ('Kandia', 'Ciocolata cu amaruie'), 
        ('Milka', 'Ciocolata cu fructe de padure'), 
        ('Milka', 'Ciocolata cu lapte')]

## Exemplu interogare care afiseaza continutul comenzilor cu numele produsului si producatorului:

- Varianta cu `WHERE`

        SELECT continut_comenzi_la_producatori.id_comanda, producatori.nume, produse.nume, continut_comenzi_la_producatori.cantitate 
        FROM continut_comenzi_la_producatori, producatori, produse
        WHERE continut_comenzi_la_producatori.id_produs = produse.id 
        AND produse.id_producator = producatori.id

- Aceeasi interogare dar cu `JOIN`

        SELECT continut_comenzi_la_producatori.id_comanda, producatori.nume, produse.nume, continut_comenzi_la_producatori.cantitate 
        FROM continut_comenzi_la_producatori 
        JOIN produse ON continut_comenzi_la_producatori.id_produs = produse.id 
        JOIN producatori ON producatori.id = produse.id_producator

- Aceeasi interogare - FLASK SQLAlchemy

    TBD


# Inserare / Adaugare

    # Tabalul avand id-ul de tip autoincrement, nu este nevoie sa configuram
    # si id-ul. Acesta va fi stabilit in mod automat la adaugare in baza de 
    # date.

    # se creaza un obiect nou si se adauga cu add.
    producator_nou = ModelProducatori(nume = <nume nou>)
    x = db.session.add(producator_nou)

    # doar pentru a confirma ca x nu primeste nici o valoare
    print('x =', x)

    # pas necesar pentru a face modificarea in baza de date
    db.session.commit()

# Modificare

    # identificare producator de modificat si generare obiect corestpunzator
    producator = ModelProducatori.query.filter_by(id=id_prod).first()
    # modificare atributul obiectului la noua valoare
    producator.nume = nume_nou

    # se foloseste tot 'add' doar ca pentru o inregistrare existenta, transformata
    # in obiect prin apelul de mai sus.
    db.session.add(producator)
    db.session.commit()

# Stergere:

    del_obj = modele.ModelProducatori.query.filter_by(nume='Heidi').first()
    db.session.delete(del_obj)
    db.session.commit()

Verificare
    modele.ModelProducatori.query.all()
    [Producatori(id=1, nume='Poiana'), 
    Producatori(id=2, nume='Kandia'), 
    Producatori(id=3, nume='Milka')] 


