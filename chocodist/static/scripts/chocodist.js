/*
const paragraph = document.getElementById("myParagraph");
const button = document.getElementById("toggleButton");

button.addEventListener("click", function() {
    paragraph.classList.toggle("hidden");
});
*/

function showHide(event) {
    //console.log(event)
    //console.log(event.target);
    //console.log(event.target.innerHTML);
    const text_div = event.target.innerHTML;
    const aria_controls = event.target.getAttribute("aria-controls");
    const controled_element = document.getElementById(aria_controls);
    //console.log(controled_element)

    if(text_div.indexOf("►") >= 0) { //&#9658;
        console.log("fac vizibil")
        event.target.innerHTML = "Adauga produs ▼" //&#9660;
        controled_element.style.display = "block"; //controled_element.style.visibility = "visible"
        
    } else if(text_div.indexOf("▼")) { //
        console.log("ascund")
        event.target.innerHTML = "Adauga produs ►"
        controled_element.style.display = "none"; //controled_element.style.visibility = "hidden"
    }
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

$('body').on('focus', '[contenteditable]', function(event) {
    const _this = $(this);
    // https://stackoverflow.com/questions/12481439/jquery-this-keyword
    /*
    $(this) will hold the element that you originally requested. 
    It will attach all the jQuery prototype methods again, but will not have to search the DOM again.
    */

    _this.data('before', _this.html());

    console.log("IN / FOCUS - event: ", event)
    console.log("informatie colectata la acest eveniment", _this.data('before'))
    console.log("_this.attr('producer-id')", _this.attr('producer-id'))
    //'blur keyup paste input'
    //Doar evenimentele blur, keydown duc la transfer de date a server
}).on('blur keydown', '[contenteditable]', function(event) {
    console.log("event.which:", event.which)
    console.log("OUT - event", event)
    //console.log(event.view.location.host)
    const pathname = event.view.location.pathname
    console.log(pathname)
    //Vreau ca doar apasarea tastei ENTER sa transfere date la server
    //Se trimit date si la click mouse in afara
    if(event.type === "keydown" && event.which != 13) {
        //modificare continut
        //console.log("Tastat tasta cu codul:", event.which)
        return
    } else {
        //Nu merge 'paste' deoarece fac prevent default
        console.log("Tastat ENTER sau iesit din celula. cod:", event.which)
        event.preventDefault()
        const _this = $(this);
        //console.log("_this.attr('producer-id')", _this.attr('producer-id'));
        //console.log("this.id:", $this.attr('id'))
        if (_this.data('before') !== _this.html()) {
            console.log("Modificare valoare: producer-id:", _this.attr('producer-id'), ", val: ", _this.html())

            _this.data('before', _this.html()); //se salveaza noua valoare la cheia 'before': https://api.jquery.com/data/
            //metoda data are doua forme - cu un parametru - returneaza data de la cheie, cu doi parametrii
            //primul - cheia, al doilea valoarea

            
            body = genereaza_body('producer-id', _this.attr('producer-id'), 'new-value', _this.html())
            console.log("body:", body)
            
            fetch(pathname, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: body,
            })
            .then(response => {
                console.log("response:", response)
                return response.text()
            })
            .then(data => {
                console.log("Rezultat modificare:", data);
                _this.html(data);
                console.log("_this.html():", _this.html());
                return data
            })
            .catch(error => console.log("EROARE fetch:", error));
        }
    }
});
