$(function () {
    $("#form-login").submit(function () {
        var usuaurio = $("#username").val();
        var clave = $("#password").val();
        var dataString = $('#form-login').serialize();

        document.querySelector('#btnLogin').innerHTML = '<i class="fas fa-spinner fa-pulse" style="padding: 0; margin-right: 10px;"></i> Cargando...';
        $("#btnLogin").addClass('disabled');

        if (usuaurio == '' || clave == '') {
            var Toast = Swal.mixin({
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000,
                timerProgressBar: true,
              });
              document.querySelector("#btnLogin").innerHTML =
                '<i class="fas fa-sign-in-alt"></i> Acceder';
              $("#btnLogin").removeClass('disabled');
              Toast.fire({
                icon: "info",
                title: "Debe especificar un usuario y una contraseña",
              });
        }
        else {
            $.ajax
                ({
                    type: "POST",
                    url: "/",
                    data: dataString,
                    success: function (msg) {
                        if (msg == 1) {
                            window.location = "/dashboard/";
                        }
                        if (msg == 2) {
                            var Toast = Swal.mixin({
                                toast: true,
                                position: 'top-end',
                                showConfirmButton: false,
                                timer: 3000,
                                timerProgressBar: true,
                            });
                            document.querySelector('#btnLogin').innerHTML = '<i class="fas fa-sign-in-alt"></i> Acceder';
                            $("#btnLogin").removeClass('disabled');
                            Toast.fire({
                                icon: 'error',
                                title: 'Usuario y/o contraseña incorrecta.'
                            });
                        }
                        if (msg == 3) {
                            var Toast = Swal.mixin({
                                toast: true,
                                position: 'top-end',
                                showConfirmButton: false,
                                timer: 3000,
                                timerProgressBar: true,
                            });
                            document.querySelector('#btnLogin').innerHTML = '<i class="fas fa-sign-in-alt"></i> Acceder';
                            $("#btnLogin").removeClass('disabled');
                            Toast.fire({
                                icon: 'warning',
                                title: 'Usuario desactivado'
                            });
                        }
                        if (msg == 4) {
                            var Toast = Swal.mixin({
                                toast: true,
                                position: 'top-end',
                                showConfirmButton: false,
                                timer: 3000,
                                timerProgressBar: true,
                            });
                            document.querySelector('#btnLogin').innerHTML = '<i class="fas fa-sign-in-alt"></i> Acceder';
                            $("#btnLogin").removeClass('disabled');
                            Toast.fire({
                                icon: 'warning',
                                title: 'Está intentando entrar desde una IP no autorizada.'
                            });

                        }
                    }
                });
        }
        return false;
    });
});