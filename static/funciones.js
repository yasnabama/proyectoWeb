$(document).ready(function() {
	$("#containers").hide();
    $("#tipoTrago").change(function(){
    	var tipoT=$('#tipoTrago option:selected').val();
        alert(tipoT)
   		$.ajax({
	        url: '/tipo_Trago',
	        data: $('form').serialize(),
	        type: 'POST',
	        success: function(response) {
	        	console.log("Hoal");
	            console.log(response);

	        },
	        error: function(error) {
	            console.log('error',error);
        }
        });
    });


    $('#añadirItem').click(function(){
    	$("#containers").show();
		var tipoT=$('#tipoTrago option:selected').val();
		var cant=$('#cantidad option:selected').val();
    	if (tipoT!="--"):
 			alert("Debe seleccionar un Tipo de Trago");
 		if (cant!="--"):
 			alert("Debe seleccionar cantidad");
 		else:
 			row = "<tr>";
 			row += "<td>"+ tipoT + "</td>";
 			row += "<td>"+ cant+ "</td>";
 			row +="<td> <button type='button' class='btn btn-warning btnElimItem'> <span class='glyphicon glyphicon-pencil'></span></button>"
 			row += "</tr>";
 			$('#tabla_resumen').append(row);
 			alert("item añadido")

 	});
 	$('#confirmar').click(function(){
 		$("#containers").hide();
 		alert("Boton seleccionado")

 	});
	$('.btnListo').click(function(){
		console.log("boton seleccionado");
		var ID = $(this).parents('tr').attr("id");
		alert("Boton seleccionado", ID)
	});
	
});
