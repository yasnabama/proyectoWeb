$(document).ready(function() {
    $("#tipoTrago").change(function(){
    	var tipTrago=$('#tipoTrago option:selected').val();
        alert(tipTrago)
        console.log(tipTrago); 
   		$.ajax({
	        url: '/tipo_Trago',
	        data: $('form').serialize(),
	        type: 'POST',
	        success: function(response) {
	            console.log(response);
	        },
	        error: function(error) {
	            console.log(error);
        }
        });
    });

 
	$('.btnDelete').on("click",function(){
	var ID = $(this).parents('tr').attr("id");
	$.ajax({
		type:'POST',
		url:'/form',
		data: {id : ID},
		success: function() {
       		location.reload();
       		}
		});
	});
});
