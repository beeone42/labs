
function contractor_edit()
{
    $("#btn-valid").css("display", "block");
    $("#btn-edit").css("display", "none");
    
    $(".editable").each(function(index, value){
	var $input = $("<input>", {
            id: $(this).attr('id'),
            val: $(this).text(),
	    type: "text"
	});
	$(this).replaceWith($input);
    });
}

function contractor_valid()
{
    jQuery.ajax({
	type: 'POST',
	url: '/api/contractor/' + g_contractor_id,
	data: {
	    enterprise:   $('#f_enterprise').val(),
	    contact_name: $('#f_contact_name').val(),
	    contact_tel:  $('#f_contact_tel').val(),
	    contact_mail: $('#f_contact_mail').val(),
	},
	success: function(data, textStatus, jqXHR) {
	    //data = JSON.parse(data);
	    console.log("success", data);
	    if (data.success)
	    {
		$("#btn-valid").css("display", "none");
		document.location = "/contractor/" + data.res;
	    }
	    else
	    {
		return false;
	    }
	},
	error: function(jqXHR, textStatus, errorThrown) {
	    console.log(textStatus);
	}
    });
}

function callback()
{
    $("#btn-edit").click(function(){
	contractor_edit();
    });
    
    $("#btn-valid").click(function(){
	contractor_valid();
    });

    if (g_contractor_id == 0)
	contractor_edit();
}

