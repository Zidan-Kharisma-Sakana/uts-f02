$(document).ready(function(){
	$('.show-form').click(function(){
		console.log("data is saved")
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
		});
	});
	$('#modal-note').on('submit','.create-form',function(){
		var form = $(this);	
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
					console.log("data is saved 5")
				} else{
					console.log("data is saved 4")
					$('#modal-note .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	})
});