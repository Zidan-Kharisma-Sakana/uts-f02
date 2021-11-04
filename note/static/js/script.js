$(document).ready(function(){
	$('.show-form').click(function(){
		$.ajax({
			url:'add_message',
			type:'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-note').modal('show');
			},
			success: function(data){
				$('#modal-note .modal-content').html(data.html_form);
			}
		})
	})
})