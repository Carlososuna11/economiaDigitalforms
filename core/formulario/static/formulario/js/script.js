var limit = 3;
var tengo = 0;

function checkbox_button(boton,valor){
    var clase = boton.className;
    var checkbox = document.getElementById(valor);
    if (clase == 'black'){
        if (tengo < limit ){
            tengo++;
            boton.classList.remove("black");
            boton.classList.add("orange");
            checkbox.checked = true;
        }else{
            alert('La seleccion Maxima es de 3');
        }
    }else{
        tengo--;
        boton.classList.remove("orange");
        boton.classList.add("black");
        checkbox.checked = false;
    }
}

function reportar_seleccion(url){
    // Swal.fire({
    //     title: 'Espere Por favor!',
    //     html: 'Espera mientras se procesa el pago',
    //     didOpen: () => {
    //         Swal.showLoading()
    //     }
    // });
    var checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    var activos= [];
    console.log(checkboxes)
    if (checkboxes.length == limit){
        for (var checkbox of checkboxes) {
            activos.push(checkbox.value);
        }
        fetch(url,{
            method: 'POST',
            headers: {
            'content-type': 'application/json',
            'X-CSRFToken':csrftoken
            },
            body: JSON.stringify({
                activos:activos
            })
        })
        .then(function(res) {
            return res.json();
        })
        .then(function(res){
            Swal.fire({
                position: 'center',
                icon: 'success',
                title: 'Se Envio la Solicitud',
                showConfirmButton: false,
                timer: 1500
                }).then((res) => {window.close();});
        })
    } else{
        Swal.fire({
            icon: 'error',
            title: 'Ups...',
            text: 'Selecciona 3 Activos',
        })
    }
}