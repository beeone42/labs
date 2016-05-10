
function deal_edit()
{
//    $("#btn-edit").css("visibility", "hidden");
//    $("#btn-valid").css("visibility", "visible");
    
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
    
    $(".selectable.site").each(function(index, value){
	v = $(this).text();
	var $input = $("<select>", {
            id: $(this).attr('id')
	});
	
   	for (var key in g_sites)
	{
	    var o = new Option(g_sites[key], key);
	    $(o).html(g_sites[key]);
	    $input.append(o);
	    if ($(this).attr('bid') == key)
	    {
		$(o).attr("selected", true);
	    }
	}
	$input.on("change", function(){
	    var id = $(this).val();
	    $("#site_pic").attr("src", g_sites_pic[id]);


	    jQuery.ajax({
		type: 'GET',
		url: '/api/deals/nextid/' + id,
		success: function(data, textStatus, jqXHR) {
		    $("#f_bdcid").val(data.data);
		    console.log("success", data);
		},
		error: function(jqXHR, textStatus, errorThrown) {
		    console.log(textStatus);
		}
	    });
	});
	$(this).replaceWith($input);
    });
    
    $(".selectable.user").each(function(index, value){
	v = $(this).text();
	var $input = $("<select>", {
            id: $(this).attr('id')
	});
	
   	for (var key in g_users)
	{
	    var o = new Option(g_users[key], key);
	    $(o).html(g_users[key]);
	    $input.append(o);
	    if ($(this).attr('bid') == key)
	    {
		$(o).attr("selected", true);
	    }
	}
	$(this).replaceWith($input);
	
    });
    
    $(".selectable.deal_state").each(function(index, value){
	v = $(this).text();
	var $input = $("<select>", {
            id: $(this).attr('id')
	});
	for (i = 0; i < g_deal_states.length; i++)
	{
	    var o = new Option(g_deal_states[i]);
	    $(o).html(g_deal_states[i]);
	    $input.append(o);
	    if (v == g_deal_states[i])
	    {
		$(o).attr("selected", true);
	    }
	}
	$(this).replaceWith($input);
	
    });
}

function deal_valid()
{
    jQuery.ajax({
	type: 'POST',
	url: '/api/deal/' + g_deal_id,
	data: {
	    bdcid: $('#f_bdcid').val(),
	    description: $('#f_description').val(),
	    creator_id: $('#f_creator_name').val(),
	    validator_id: $('#f_validator_name').val(),
	    state: $('#f_state').val(),
	    site_id: $('#f_site_name').val()
	},
	success: function(data, textStatus, jqXHR) {
	    //data = JSON.parse(data);
	    console.log("success", data);
	    if (data.success)
	    {
		$("#btn-valid").css("display", "none");
		document.location = "/deal/" + data.res;
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
	deal_edit();
    });
    
    $("#btn-valid").click(function(){
	deal_valid();
    });

    if (g_deal_id == 0)
	deal_edit();
}

