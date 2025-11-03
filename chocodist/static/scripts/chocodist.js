/*
const paragraph = document.getElementById("myParagraph");
const button = document.getElementById("toggleButton");

button.addEventListener("click", function() {
    paragraph.classList.toggle("hidden");
});
*/

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookies = decodeURIComponent(document.cookie)
    console.log(decodedCookies)
    let ca = decodedCookies.split(';');
    for(let i = 0; i < ca.length; i++) {
        let c = ca[i];
        console.log("-" + c + "-")
        while(c.charAt(0) == ' ') { //eliminare spatii de la inceput
            c = c.substring(1)      //substring-ul de la poz 1 pana la sfarsit
            console.log(" *** -" + c + "-")
        }
        if(c.indexOf(name) == 0) {
            //console.log(c.substring(name.length));
            console.log("~"+c.substring(name.length, c.length)+"~");
            //substring-ul de dupa egal pana la sfarsit
            //la fel si daca ar i
            return c.substring(name.length, c.length); 
        }
    }
    return "";
}

function showHide(event) {
    //console.log(event)
    //console.log(event.target);
    //console.log(event.target.innerHTML);
    const text_div = event.target.innerHTML;
    const aria_controls = event.target.getAttribute("aria-controls");
    const controled_element = document.getElementById(aria_controls);
    //console.log(controled_element)
    let match_expand = text_div.match(/(.+) ►/)
    let match_compact = text_div.match(/(.+) ▼/)
    if(match_expand !== null) {
        console.log("fac vizibil");
        event.target.innerHTML = match_expand[1] + " " + "▼" //&#9660;
        controled_element.style.display = "block";
    } else if(match_compact !== null) {
        console.log("ascund");
        txt = match_compact[1]
        event.target.innerHTML = match_compact[1] + " " + "►"
        controled_element.style.display = "none";
    }

    /*
    if(text_div.indexOf("►") >= 0) { //&#9658;
        console.log("fac vizibil")
        if(aria_controls.substring("producer" >= 0)) {
            event.target.innerHTML = "Adauga producator ▼" //&#9660;
        } else {
            event.target.innerHTML = "Adauga produs ▼" //&#9660;
        }
        controled_element.style.display = "block"; //controled_element.style.visibility = "visible"
        
    } else if(text_div.indexOf("▼")) { //
        console.log("ascund")
        if(aria_controls.substring("producer" >= 0)) {
            event.target.innerHTML = "Adauga producator ►" //&#9660;
        } else {
            event.target.innerHTML = "Adauga produs ►"
        }
        controled_element.style.display = "none"; //controled_element.style.visibility = "hidden"
    }
    */
}

/*
genereaza_body = function(pagina, _this) {
    ret = ""

    if(pagina == "produse" || pagina == 'producatori') {
        ret = 'id=' + _this.attr('id') + "&valnoua=" +_this.html().trim()
    }
    
    return ret
}*/

genereaza_body = function() {
    let ret = ""
    for(let i = 0; i < arguments.length - 1; i = i + 2) {
        //console.log("i:", i, ", arg_name:", arguments[i], ", arg_val:", arguments[i+1]);
        ret += arguments[i] + "=" + arguments[i+1] + "&"
    }
    return ret.slice(0, -1); //to cut the last &
}


/*
Biblioteca (library) JQuery vine cu Bootstrap.
Permite acces mai usor la elementele interfetei grafice, asocierea de evenimente etc.

ex: $(body) - identifica corpul paginii: <body>...</body>
    $(body).on('focus', '[contenteditable]', function(event) {corp functie})
       - asociaza functia definita in blocul de mai sus cu evenimentul 'focus'
         pe elementele cu atributul [contenteditable] din 'body'

Pentru ca folosesc flask-bootstrap, am si JQuery.

Codul de mai jos folose


https://learn.jquery.com/events/introduction-to-events/
https://www.w3schools.com/jquery/default.asp
https://www.w3schools.com/jquery/jquery_chaining.asp
*/

$(window).on("load", function(event) {
    console.log("ON LOAD");
    const adauga = getCookie("adauga");
    
    //getCookie("modifica");
    //getCookie("sterge");
    
    let form_adauga = document.getElementById('add-form')
    /*if(form_adauga == null) {
        form_adauga = document.getElementById('add-producer-form')
    }*/

    if(form_adauga == null) {
        return; //nu avem pagina cu formular de adaugare
    } else {
        //$('add-product-form')
        console.log(form_adauga);
        console.log(form_adauga.getAttribute('style'))

        div_text = form_adauga.previousElementSibling;
        console.log(div_text);
        console.log(div_text.innerHTML)
        
        if(adauga == 1) {
            //daca am adaugat un element, las formularul vizibil
            //in urma adaugarii, se va primi un redirect cu un cookie care ne spune
            //ca s-a adaugat un element
            //div_text.innerHTML = "Adauga produs ▼" //&#9660;
            //controled_element.style.display = "block"; //controled_element.style.visibility = "visible"
            div_text.dispatchEvent(new Event('click'));
        }
    }
    
});



$('body').on('focus', '[contenteditable]', function(event) {
    const _this = $(this);
    //console.log("this on Focus", _this)
    // https://stackoverflow.com/questions/12481439/jquery-this-keyword
    
    //$(this) will hold the element that you originally requested. 
    //It will attach all the jQuery prototype methods again, but will not have to search the DOM again.
    

    _this.data('before', _this.html()); //elementul din pagina unde se genereaza evenimentul - celula din tabel

    console.log("IN / FOCUS - this (elementul la care apare evenimentul): ", _this)
    //console.log("event.which:", event.which) - focus - cod eveniment 0
    //console.log("informatie colectata la acest eveniment", _this.data('before'))
    //console.log("_this.attr('producer-id')", _this.attr('producer-id'))
    //'blur keyup paste input'
    //Doar evenimentele blur, keydown duc la transfer de date a server
})


$('body').on('blur keydown', '[contenteditable]', function(event) {
    //event - evenimentul generat - de tip blur (iesire din element), keydown (apasare tasta) pe elemente cu 'contenteditable' din 'body'
    console.log("event.which blur / keydown:", event.which) //cod eveniment - event.which - la taste: 1: 49, 2: 50, a: 65, b: 66 ...
    console.log(csrf_token);
    //console.log("OUT - event", event)
    //console.log(event.view.location.host)
    const pathname = event.view.location.pathname
    //console.log("pathname din obiectul 'event':", pathname)
    //console.log("pathname din this:",$(this).context.ownerDocument.location.pathname)
    //Vreau ca doar apasarea tastei ENTER sa transfere date la server
    //Se trimit date si la click mouse in afara
    if(event.type === "keydown" && event.which != 13) { //ENTER - are cod eveniment 13
        //modificare continut
        //console.log("Tastat tasta cu codul:", event.which)
        return
    } else {
        //Nu merge 'paste' deoarece fac prevent default
        console.log("Tastat ENTER sau iesit din celula si dat click. cod: eveniment", event.which)
        event.preventDefault()
        const _this = $(this);
        //console.log(_this)
        console.log("*** _this.html:", _this.html())
        if (_this.data('before') !== _this.html()) {
            console.log("Modificare valoare: item-id:", _this.attr('item-id'), ", val: ", _this.html(), '(before: ', _this.data('before'),")")

            if(_this.attr('type') == "text") {
                const text_pattern = /^[a-zA-Z0-9\ ]+$/
                if(_this.html().match(text_pattern) == null) {
                    const msg = "Campul trebuie sa contina numele produsului!\nAti tastat:" + _this.html()
                    alert(msg)
                    _this.text(_this.data('before'))
                    return
                } 
            } else if(_this.attr('type') == "number") {
                const number_pattern = /^0$|^[1-9]([0-9]*)$/
                if(_this.html().match(number_pattern) == null) {
                    const msg = "Campul trebuie sa contina cantitatea un numar intreg >= 0!\nAti tastat: " + _this.html()
                    alert(msg);
                    _this.text(_this.data('before'))
                    return false;
                }
            }
            
            _this.data('orig', _this.data('before')) //am nevoie in caz ca am un duplicat de nume
            _this.data('before', _this.html()); //se salveaza noua valoare la cheia 'before': https://api.jquery.com/data/
            //metoda data are doua forme - cu un parametru - returneaza data de la cheie, cu doi parametrii
            //primul - cheia, al doilea valoarea
            
            body = genereaza_body('action', _this.attr('action'), 
                'item-id', _this.attr('item-id'), 
                'new-value', _this.html(), 
                'item-attr', _this.attr('item-attr'))
            console.log("body:", body)
            
            fetch(pathname, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": csrf_token
                },
                body: body,
            })
            .then(response => {
                console.log("response:", response)
                return response.text()
            })
            .then(data => {
                console.log("Rezultat modificare:", data);
                if(_this.data('orig') == data && _this.attr('item-attr') == "nume") { //doar la nume conteaza duplicatul, nu si la cantitate stoc
                    window.alert("Duplicat de nume, valoarea nu se va schimba!")
                }
                _this.html(data);
                console.log("_this.html():", _this.html());
                return data
            })
            .catch(error => console.log("EROARE fetch:", error));
        }
    }
});

/*
Ambele variante de mai jos ataseaza functii de tratare eviment elementului cu clasa .submit-with-icon
Nu sunt foarte utile insa pentru a bloca stergerea ...
Asta se rezolva prin tratarea evenimentului la nivelul formularului, nu la nivalul glyphicon-ului 'trash'

$(function() {
    $('.submit-with-icon').click(function(event) {
        //elementul unde are loc evenimentul - asupra caruia se actioneaza
        const _this = $(this)
        console.log("Apasat delete. _this:", _this)
        if(window.confirm("Chiar doriti sa stergeti produsul selectat?") == true) {
            alert("Produsul selectat va fi sters!");
            return true;
        } else {
            alert("Stergere anulata!")
            event.stopPropagate;
            return false;
        }
    })
})


$('.submit-with-icon').on(s'click', function(event) {
    //elementul unde are loc evenimentul - asupra caruia se actioneaza
    const _this = $(this)
    console.log("Apasat delete. _this:", _this)
    if(window.confirm("Chiar doriti sa stergeti produsul selectat?") == true) {
        alert("Produsul selectat va fi sters!");
        return true;
    } else {
        alert("Stergere anulata!")
        event.stopPropagate();
        return false;
    }
})
*/ 


/* 
    Construire tabel Comanda la producator.
    De fiecare data cand selectez un element din oferta, adaug linie intr-un tabel
    cu sumarul comenzii.
*/

function construiesteSumarComanda(event) {
    console.log("construiesteSumarComanda")
    //console.log(event)
    //console.log(event.target)
    const atribute_produs = event.target.parentNode.parentNode.children; //celulele dintr-un rand din oferta
    console.log(atribute_produs)

    /*
        Metoda de a cauta obiectele nu este optima
        Daca adaug au modific elemente in pagina, trebuie modificat aici
        Cea mai buna metoda este sa identific elementele dupa ID.
    */
    //const div_sumar = event.target.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.nextSibling.nextSibling;
    //const tabel_sumar = event.target.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.nextSibling.nextSibling.childNodes[1];
    const div_sumar = document.getElementById("div-sumar-comanda");
    const tabel_sumar = document.getElementById("tabel-sumar-comanda");
    const body_tabel_sumar = tabel_sumar.childNodes[1]
    const total_sumar_comanda = document.getElementById("total-sumar-comanda")


    console.log("div_sumar:", div_sumar);
    console.log("tabel_sumar:", tabel_sumar);

    div_sumar.style.display = "block";
    
    const nume_produs = atribute_produs[0].textContent;
    const pret_unitar = atribute_produs[1].textContent;
    const input = atribute_produs[3].getElementsByTagName("input")[0];

    let total = Number(total_sumar_comanda.textContent);
    let total_produs_anterior = 0;
    let total_produs = 0;
    
    console.log("input:", input, ", valoare input:", input.value);

    const rand_existent = document.getElementById(nume_produs)
    if(rand_existent) {
        total_produs_anterior = rand_existent.children[3].textContent;
        if(input.value == 0) {
            //total = total - Number(input.value);
            total -= total_produs_anterior;
            body_tabel_sumar.removeChild(rand_existent);
        } else {
            rand_existent.children[2].textContent = input.value;
            total_produs = pret_unitar * input.value;
            rand_existent.children[3].textContent = total_produs;
            total += total_produs - total_produs_anterior;
        }
    } else {
        if(input.value == 0) {
            return null;
        }
        const tr = document.createElement("tr");
        tr.id = nume_produs;
        tr.class = "produs";

        let i = 0;
        let pret = 0;

        for (const element of atribute_produs) {
            //console.log(element.textContent)
            console.log("firstChild:", element.firstChild);
            const input = element.getElementsByTagName("input")[0]
            
            let txt = "";
            if(input) {
                txt = input.value;
                console.log("input:", txt)
            } else {
                txt = element.textContent;
            }
            console.log("data:", txt);
            if(i != 2) {
                const td = document.createElement("td")
                if(i == 0) {
                    td.style.textAlign = "left";
                }
                td.textContent = txt;
                tr.appendChild(td);
            }
            i++;
        }
        const td_pret = document.createElement("td")
        total_produs = Number(pret_unitar) * Number(input.value);
        td_pret.textContent = total_produs;
        total += total_produs;
        tr.appendChild(td_pret)
        body_tabel_sumar.appendChild(tr);
    }
    total_sumar_comanda.textContent = total;
}