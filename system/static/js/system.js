
//change password user profile
$('#passwd').on('shown.bs.modal', function() {
    $('#passwdProfileForm').bootstrapValidator('resetForm', true);
});

$('#passwdProfileForm').bootstrapValidator({
        feedbackIcons: {
            valid: 'fa fa-check',
            invalid: 'fa fa-times',
            validating: 'fas fa-spinner fa-pulse'
        },
        fields: {
            passwd: {
                validators: {
                    notEmpty: {
                        message: 'No puede estar vacio'
                    },
                    identical: {
                        field: 'passwd1',
                        message: 'Las contraseñas no coenciden'
                    }
                }
            },
            passwd1: {
                validators: {
                    notEmpty: {
                        message: 'No puede estar vacio'
                    },
                    identical: {
                        field: 'passwd',
                        message: 'Las contraseñas no coenciden'
                    }
                }
            }
        }
    });

function changePasswdProfile() {

    if ($('#passwdProfileForm').data('bootstrapValidator').isValid()) {

        var dataString = $('#passwdProfileForm').serialize();

        $.ajax({

            url: "/system/change_passwd/",
            type: "POST",
            data: dataString,
            dataType: "json",
            success: function (result) {
                if (result.status == true || result.status == 'true') {
                    $('#msg-body').html(result.msg);
                    $('#msg').addClass('in');
                    $('#msg').removeClass('hide');
                    $('#passwd').modal('toggle');
                }
                if (result.status == false || result.status == 'false') {
                    $('#msg-body').html(result.msg);
                    $('#msg').addClass('in');
                    $('#msg').removeClass('hide');

                }
            },
            error: function (jqXHR, status, error) {
                $('#msg-body').html("Ocurio un error inesperado, Error: " + error + ", discupe las molestias.");
                $('#msg').addClass('in');
                $('#msg').removeClass('hide');
            }
        });
    }
    else
    {
        $('#passwdProfileForm').data('bootstrapValidator').validate();
    }
};