date_distribuitor = {
    "producatori": [
        {"id": 1, "nume": "Poiana"},
        {"id": 2, "nume": "Kandia"},
        {"id": 3, "nume": "Milka"},
    ],

    "produse": [
        {"id": 1, "id_producator": 1, "nume": "Ciocolata cu lapte"},
        {"id": 2, "id_producator": 1, "nume": "Ciocolata cu alune"},
        {"id": 3, "id_producator": 2, "nume": "Ciocolata cu iaurt"},
        {"id": 4, "id_producator": 2, "nume": "Ciocolata cu caramel sarat"},
        {"id": 5, "id_producator": 2, "nume": "Ciocolata cu biscuiti"},
        {"id": 6, "id_producator": 2, "nume": "Ciocolata cu amaruie"},
        {"id": 7, "id_producator": 3, "nume": "Ciocolata cu fructe de padure"},
        {"id": 8, "id_producator": 3, "nume": "Ciocolata cu lapte"}
    ],
    
    "comenzi_la_producatori": [
        {"id": 1, "id_producator": 1},
        {"id": 2, "id_producator": 2},
        {"id": 3, "id_producator": 3},
    ],
    
    "continut_comenzi_la_producatori": [
        {"id_comanda": 1, "id_produs": 1, "cantitate": 100},
        {"id_comanda": 1, "id_produs": 2, "cantitate": 150},
        {"id_comanda": 2, "id_produs": 3, "cantitate": 200},
        {"id_comanda": 2, "id_produs": 4, "cantitate": 250},
        {"id_comanda": 3, "id_produs": 7, "cantitate": 50}, 

    ],
        
    "clienti": [],
    
    "comenzi_de_la_clientii": [],
}
