;(function() {

    //Defino las variables globales que voy a utilizar.
    let totalTuplas = Number($("#id_form-TOTAL_FORMS").val());
    let initial = $("#id_form-INITIAL_FORMS").val();
    let min = Number($("#id_form-MIN_NUM_FORMS").val());
    let max = Number($("#id_form-MAX_NUM_FORMS").val());

    let $buttons = $("#buttons");//Tomo los botones para luego crear cada item antes de los botones.
    let template = $(`#item-${totalTuplas}`).html().replace(RegExp(`form-${totalTuplas - 1}`,"g"), `form-ITEM`);//Selecciono lo que es un item completo (producto+cantidad+checkBox).

    let $buttonAddPractica = $("#button-add-practica");

    let $inputDescuento = $("#id_descuento").on("input", function () {calcularTotal();});
    let $inputRecargo = $("#id_recargo").on("input", function () {calcularTotal();});
    //let $inputCliente = $("#select2-id_cliente-container").on("select", function () {console.log("AAA");});
    let $inputCliente = document.querySelector(`#id_cliente`);
    $inputCliente.onchange=function() {
      actualizarDescuento();
    };

    let $inputPractica = $("#id_practica");
    let divPractica = $inputPractica.parent().parent();
    divPractica.hide();//Oculto el input de la práctica.

    let iterador = 0;
    for (iterador ; iterador<totalTuplas; iterador++){//Este ciclo for es para darle comportamiento a todas las tuplas creadas por el formulario.
      let cantidad =$(`#id_form-${iterador}-cantidad`).on("input", function() { calcularTotal(); });//Obtengo la cantidad del item y le doy comportamiento (llama a la funcion calcularTotal cuando lo modifican).
      let producto = document.querySelector(`select[name="form-${iterador}-producto"]`);//Obtengo el producto del item y le doy comportamiento (llama a la funcion calcularTotal cuando cambia).
      producto.onchange=function(e) {
        calcularTotal();
      };
      let borrar = $(`#id_form-${iterador}-DELETE`).on("change", function() { calcularTotal(); });//Obtengo el checkBox eliminar del item y le doy comportamiento(llama a la funcion calcularTotal cuando cambia).
    }


    let actualizarDescuento = function (){
      let $cliente = $("#id_cliente");
      let identificador = $cliente.val();
      let myUrl = new String ("/GestionDeClientes/ver/" + identificador + "/");
      $.ajax({
        url: myUrl,
        data: {id: `${identificador}`},
        success: function(data){
          let $porcentajeDescuento =$(`#porcentajeDescuentoServicio`, data);//Consigo el porcentaje de descuentodel cliente, del ver.html traido por ajax.
          texto = $porcentajeDescuento[0].textContent;
          arrayTexto = texto.split(" ");
          let porcentajeDescuento=parseInt(arrayTexto[2]);//Obtengo el valor numérico del porcentaje de descuento del cliente.
          document.getElementById("id_descuento").value = porcentajeDescuento;//Seteo el porcentaje de descuento.
          calcularTotal();
        }
      });
    }


    //[TODO] FEATURE: calcularTotal no debería parsear un texto. Debería traer el .json con $ .ajax y extraer el precio de allí.

    let calcularTotal = function(){//Función que calcula el precio total de la factura y lo imprime en el input( input "total").
      let i=0;
      console.log("OBTENER TOTAL - entrando a la función.");
      let acumulador =0;//Esta variable acumuladora está para ir guardando los valores de las tuplas que se deben sumar. Sumando todos sus valores.

      for (i ; i<totalTuplas; i++){//Recalculo para todas las tuplas, para tener el valor real sin importar el cambio que se haga, sea un cambio de producto, de cantidad o que clickeen el checkBox eliminar.
        let item = $(`#item-${i+1}`);
        let $item = $(item);
        let inputCantidad =$(`#id_form-${i}-cantidad`, $item[0]);
        let inputSelect = $(`#id_form-${i}-producto`,$item[0]);
        let inputDelete = $(`#id_form-${i}-DELETE`, $item[0]);
        let $inputSelect = $(inputSelect);
        let borrar = inputDelete[0];
        let cantidad = inputCantidad[0].value;
        let texto = $inputSelect.find(":selected").text();

        if (borrar.checked == false){//Si el checkbox no está tildado, intento sumar el valor calculado de esta tupla al acumulador.
          if (cantidad < 0){ cantidad = 0;}//Si el usuario ingresa un valor negativo, lo ignoro y tomo la cantidad como 0.
          if ((texto != "---------") && (cantidad)) {//Si se ingresó tanto cantidad como producto, calculo el valor de la tupla.
            let varParseo = $inputSelect.find(":selected").text();//Obtengo el texto del input para parsearlo luego, y quedarme con su "precio".
            varParseo = varParseo.split(",");
            varParseo = varParseo[2];
            varParseo = varParseo.split(" ");
            varParseo = varParseo[2];
            let precioProducto = parseInt(varParseo);//Ya se consiguió el precio, pero está en cadena, lo transformo a entero.
            let precioFinalTupla = precioProducto * cantidad//Calculo el precio de la tupla.
            console.log("El precio de la tupla completa es: %s",precioFinalTupla);
            acumulador +=precioFinalTupla;//Sumo el total hasta ahora.
          }else{
            console.log("No se puede calcular el precio, falta llenar algún campo.");
          }
        }
      }

      document.getElementById("id_total").value = acumulador;//Escribo en el input "total" el precio calculado (imprimo el acumulador en el input "total").
      let $inputPractica = $("#id_practica");
      if ($inputPractica.is(":visible")){
        sumarPractica();//Llamo la función que incrementa el valor del input total con respecto al costo de la práctica seleccionada.
      }
      console.log("OBTENER TOTAL - finalizando la función.");
    }


    //Función que toma el valor del input total y le suma el costo de la práctica seleccionada.
    let sumarPractica = function(){
      let elementoSeleccionado = $inputPractica.find(":selected");//Consigo el elemento seleccionado.
      let texto = $inputPractica.find(":selected").text();
      let arrayTexto = texto.split(" ");//Parseo el __str__ de la práctica seleccionada.
      let tipo = arrayTexto[4];
      let identificador = parseInt(arrayTexto[2]);
      let $inputTotal = $("#id_total");//Obtengo el input Total.
      let precioInputTotal = parseInt($inputTotal[0].value);//Consigo el valor numérico del input total.
      let $descuento = $("#id_descuento");
      let porcentajeDescuento = parseInt($descuento.val());//Consigo el valor del porcentaje de descuento.
      let $recargo = $("#id_recargo");
      let porcentajeRecargo = parseInt($recargo.val());//Consigo el valor del porcentaje de recargo.
      console.log(porcentajeRecargo);

      //Si es una consulta, uso ajax con respecto a las url de consultas, sinó con respecto las url de cirugía.
      if (tipo == "consulta"){
        let myUrl = new String("/consultas/ver/" + identificador + "/");//Defino la url que voy a conseguir.
        $.ajax({
          url: myUrl,
          data: {id: `${identificador}`},
          success: function(data){
            let descuentoPractica = 0;
            let recargoPractica = 0;

            let $precio =$(`#id_precio`, data);//Consigo el precio de la práctica, del ver.html traido por ajax.
            texto = $precio[0].textContent;
            arrayTexto = texto.split("$");
            let precioPractica=parseInt(arrayTexto[1]);//Obtengo el valor numérico del costo de la práctica.
            if (porcentajeDescuento != 0){
              descuentoPractica = (precioPractica*porcentajeDescuento)/100;
            }
            if (porcentajeRecargo != 0){
              recargoPractica = (precioPractica*porcentajeRecargo)/100;
            }
            precioPractica -= descuentoPractica;
            precioPractica += recargoPractica;
            let nuevoPrecio = precioPractica + precioInputTotal;
            if (nuevoPrecio < 0){
              nuevoPrecio = 0;
            }
            document.getElementById("id_total").value = nuevoPrecio;//Seteo el precio total actualizado.
            //$itemTotal = $"(#id_total");
          }
        });
      }else{
        let myUrl = new String("/cirugias/ver/" + identificador +"/");//Defino la url que voy a conseguir.
        $.ajax({
          url: myUrl,
          data: {id: `${identificador}`},
          success: function(data){
            let descuentoPractica = 0;
            let recargoPractica = 0;

            let $precio =$(`#id_precio`, data);//Consigo el precio de la práctica, del ver.html traido por ajax.
            texto = $precio[0].textContent;
            arrayTexto = texto.split("$");
            let precioPractica=parseInt(arrayTexto[1]);//Obtengo el valor numérico del costo de la práctica.
            if (porcentajeDescuento != 0){
              descuentoPractica = (precioPractica*porcentajeDescuento)/100;
            }
            if (porcentajeRecargo != 0){
              recargoPractica = (precioPractica*porcentajeRecargo)/100;
            }
            precioPractica -= descuentoPractica;
            precioPractica += recargoPractica;
            let nuevoPrecio = precioPractica + precioInputTotal;
            if (nuevoPrecio <0){
              nuevoPrecio = 0;
            }
            document.getElementById("id_total").value = nuevoPrecio;//Seteo el precio total actualizado.
          }
        });
      }
    }

    let addPractica = function(){
      divPractica.show();
      $buttonAddPractica.hide();
      $inputPractica.on("change", function() { calcularTotal() });
    }


//Función que agrega un nuevo item (nueva tupla de selector de producto y cantidad). Asociandoles el comportamiento
//dinámico para calcular el total.
  	let add = function() {
  		console.log("ADD - Total al iniciar = %d",totalTuplas);
  		if (totalTuplas < max) {
        let id = totalTuplas;
        let field = template.replace(RegExp(`form-ITEM`,"g"), `form-${id}`);//Construyo el item  con el id que debe llevar dentro.
  			totalTuplas += 1;
  			field = `<div class="col-xs-7" id="item-${totalTuplas}">${field}</div>`;//Coloco el id que debe llevar el item en su cabecera.
  			$("#id_form-TOTAL_FORMS").val(totalTuplas);
        let $field = $(field);

        $buttons.before($field);
        let cantidad =$(`#id_form-${id}-cantidad`, $field).on("input", function() { calcularTotal(); });//Obtengo el input cantidad del elemento a agregar, dandole ademas dinamismo (que llame a la funcion calcularTotal al ser modificado).
        let producto = document.querySelector(`select[name="form-${id}-producto"]`, $field);//Obtengo el input producto del elemento a agregar, dondele ademas dinamismo (que llame a la funcion calcularTotal al cambiar).
        producto.onchange=function() {
          calcularTotal();
        };
        let borrar = $(`#id_form-${id}-DELETE`, $field).on("change", function() { calcularTotal(); });//Obtengo el checkBox del elemento a agregar, dandole ademas dinamismo (que llame a la funcion calcularTotal al cambiar).
  		} else{ console.log("Número máximo de productos alcanzado. NUMERO MAXIMO = %d",totalTuplas)}
  		console.log("ADD - Total al finalizar = %d",totalTuplas);
  	}

    let borrarTuplasVacias = function(){
      //[TODO]Función que coloca en verdadero el checkbox eliminar de las tuplas vacías.
    }




  	$("#button-add").click(add);
    $("#button-add-practica").click(addPractica);
})();

    $(function () {
        var today = new Date();
        var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
        var time = today.getHours() + ":" + today.getMinutes();
        var dateTime = date+' '+time;
        $("#id_fecha").datetimepicker({
            locale: 'es',
            format: 'L',
            maxDate: new Date()
        });

    });
