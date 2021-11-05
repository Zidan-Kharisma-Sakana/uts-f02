$(document).ready(function(){
	var ShowForm = function(){
		var btn= $(this)
		$.ajax({
			url:btn.attr("data-url"),
			type:'get',
			dataType:'json',
			beforeSend: function(){
			
				$('#modal-note').modal('show');
			},
			success: function(data){
				$('#modal-note .modal-content').html(data.html_form);
			}
		});
	};
	var SaveForm =  function(){
		var form = $(this);	
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
					$('#modal-table ul').html(data.note_list)
					$('#modal-note').modal('hide');
				} else{
					
					$('#modal-note .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}

//delete
$('#modal-table').on("click",".show-form-delete",ShowForm);
$('#modal-note').on("submit",".delete-form",SaveForm)

//create
//delete
$('.show-form').click(ShowForm);
$('#modal-note').on("submit",".create-form",SaveForm)


});