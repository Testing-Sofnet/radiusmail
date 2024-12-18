 //change password user profile
$('#editPass').on('shown.bs.modal', function() {
    $('#passwdForm').bootstrapValidator('resetForm', true);
});


$(document).ready(function () {
	
	$('#id_municipio').change(function(event){
        $.post("/system/get_unidad/", {id_municipio:$('#id_municipio').val()}, function(data){
            var options = '<option value="">Selecciona una unidad</option>';
            for (var i = 0; i < data.length; i++){
                options += '<option value="'+data[i]["pk"]+'">' +data[i]["fields"]["trabajo_name"] +'</option>'
            }
            $('#id_trabajo').html(options)
            $("#id_trabajo option:first").attr('selected', 'selected');
        }, "json");
    });

    $('#passwd').keyup(function(e) {
        var strongRegex = new RegExp("^(?=.{8,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*\\W).*$", "g");
        var mediumRegex = new RegExp("^(?=.{7,})(((?=.*[A-Z])(?=.*[a-z]))|((?=.*[A-Z])(?=.*[0-9]))|((?=.*[a-z])(?=.*[0-9]))).*$", "g");
        var enoughRegex = new RegExp("(?=.{6,}).*", "g");
        if (false == enoughRegex.test($(this).val())) {
                $('#passstrength').html('<span class="badge bg-danger">Muy debil</span>');
        } else if (strongRegex.test($(this).val())) {
                $('#passstrength').html('<span class="badge bg-success">Fuerte</span>');
        } else if (mediumRegex.test($(this).val())) {
                $('#passstrength').html('<span class="badge bg-secondary">Media!</span>');
        } else {
                $('#passstrength').html('<span class="badge bg-warning">Débil!</span>');
        }
        return true;
    });


});

