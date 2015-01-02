$(document).ready(function() {
	$("#containers").hide();
    $("#tipoTrago").change(function(){
    	var tipoT=$('#tipoTrago option:selected').val();
   		$.ajax({
	        url: '/tipo_Trago',
	        data: $('form').serialize(),
	        type: 'POST',
	        success: function(response) {
	            //console.log(response);
	            segSelec(response);
	        },
	        error: function(error) {
	            console.log('error',error);
        }
        });
    });




	
});
function segSelec(data){
	//vaciar el select cuando consulta de nuevo.
	var sel = document.getElementById("seleccionTrago");
	for(i=(sel.length-1); i>=0; i--){
	   aBorrar = sel.options[i];
	   aBorrar.parentNode.removeChild(aBorrar);
	}
	opciones=data.split("-");
	largo=opciones.length;
	console.log(largo);
	for (i=0; i<largo; i++){
		var row="<option>"+opciones[i]+"</option>";
		$('#seleccionTrago').append(row);
	}
}

function añadItem(){
	$("#containers").show();
	var mesa=$('#mesa option:selected').val();
	var trago=$('#seleccionTrago option:selected').text(); 
	var cant=$('#cantidad option:selected').val();
	console.log(cant+"-");
	var n = $('tr:last td', $("#tablamon")).length;
	console.log(n); //numero de items de la tabla.
	var row = "<tr>";
	row += "<td >"+ mesa + "</td>";
	row += "<td >"+ trago + "</td>";
	row += "<td>"+ cant+ "</td>";
	row +="<td> <button type='button' class='btn btn-warning btnElimItem' onclick='ElimItem(this.parentNode.parentNode.rowIndex)'> <span class='glyphicon glyphicon-pencil'></span></button>"
	row += "</tr>";
	$('#tabla_resumen').append(row);
	alert("item añadido")
	
}
function ElimItem(i){
	var r = confirm("¿Esta seguro que desea eliminar este item?");
	if (r == true) {
		x = "Eliminado";
	    document.getElementsByTagName("table")[0].setAttribute("id","tabla_resumen");
	    document.getElementById("tabla_resumen").deleteRow(i);

	}

}


function confirmar(){
	var i=0;
	$('#tabla_resumen tr').each(function () {
		var mesa = $(this).find("td").eq(0).html();
		var trago = $(this).find("td").eq(1).html();
		var c = $(this).find("td").eq(2).html();
		i=i+1;
		trago=trago.replace(" ","_");
		var data= mesa+"-"+trago+"-"+c+"-"+i;
		
		$.ajax({
	        url:'/confirmarP/'+data,
	        data: data,
	        type: 'POST',
	        success: function(response) {
	            console.log(response);
	            location.reload();
	        },
	        error: function(error) {
	            console.log('error',error);
        }
        });
	});
}

function botonListo(){
	console.log("!!!boton seleccionado");
	fila = document.getElementById('id');
	console.log(fila);
	
	var ID = $(this).parents('tr').attr("id");
}