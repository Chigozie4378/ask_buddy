<?php
include '../loader/init.php';
Session::Auth();
$ctr = new AuthController();
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <style>
        .form-label {
            margin-bottom: 0;
        }
    </style>
</head>

<body>
    <div class="container">
        <div class="row">
            <div class="offset-md-4 col-md-4">
                <ul class="nav nav-pills nav-justified mb-3" id="ex1" role="tablist">
                    <li class="nav-item" role="presentation">
                        <a class="nav-link" id="tab-login" data-mdb-pill-init href="index" role="tab"
                            aria-controls="pills-login" aria-selected="false">Login</a>
                    </li>
                    <li class="nav-item" role="presentation">
                        <a class="nav-link active" id="tab-register" data-mdb-pill-init href="signup" role="tab"
                            aria-controls="pills-register" aria-selected="true">Register</a>
                    </li>
                </ul>
                <div class="tab-content">
                    <div class="tab-pane fade show active" id="pills-register" role="tabpanel"
                        aria-labelledby="tab-register">
                        <form method="post" action="">
                            <div class="text-center mb-3">
                                <p>Sign up with:</p>
                                <button type="button" class="btn btn-link btn-floating mx-1" id="google-sign-in">
                                    <i class="fab fa-google"></i>
                                </button>
                            </div>

                            <p class="text-center">or:</p>
                            <div class="text-center"><b><i class="text-danger"><?php echo $ctr->register(); ?></i></b></div>
                            
                            <div data-mdb-input-init class="form-outline mb-4">
                                <label class="form-label" for="registerName">Name</label>
                                <input type="text" id="registerName" name="name" class="form-control" value="<?php echo OldInput::input('name')?>"/>
                            </div>

                            <div data-mdb-input-init class="form-outline mb-4">
                                <label class="form-label" for="registerEmail">Email</label>
                                <input type="email" id="registerEmail" name="email" class="form-control" value="<?php echo OldInput::input('email')?>"/>
                            </div>

                            <div data-mdb-input-init class="form-outline mb-4">
                                <label class="form-label" for="registerPassword">Password</label>
                                <input type="password" id="registerPassword" name="password" class="form-control" value="<?php echo OldInput::input('password')?>"/>
                            </div>

                            <div data-mdb-input-init class="form-outline mb-4">
                                <label class="form-label" for="registerRepeatPassword">Repeat password</label>
                                <input type="password" id="registerRepeatPassword" name="repeat_password"
                                    class="form-control" value="<?php echo OldInput::input('repeat_password')?>"/>
                            </div>

                            <button type="submit" data-mdb-button-init data-mdb-ripple-init
                                class="btn btn-primary btn-block mb-3">Sign up</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script src="https://apis.google.com/js/platform.js" async defer></script>
    <script>
        function onSignIn(googleUser) {
            var profile = googleUser.getBasicProfile();
            var id_token = googleUser.getAuthResponse().id_token;

            $.post("../controllers/AuthController", {
                google_id_token: id_token
            }, function (response) {
                if (response.status == 'success') {
                    window.location.href = '../chat';
                } else {
                    alert('Google Sign-In failed.');
                }
            }, 'json');
        }

        // Initialize Google Sign-In
        function initGoogleSignIn() {
            gapi.load('auth2', function () {
                auth2 = gapi.auth2.init({
                    client_id: '110663364009-51n287pnbpn1fl1o9ld4csclfad9fvqf.apps.googleusercontent.com'
                });

                document.getElementById('google-sign-in').addEventListener('click', function () {
                    auth2.signIn().then(function (googleUser) {
                        onSignIn(googleUser);
                    });
                });
            });
        }

        // Call init function when the page loads
        window.onload = initGoogleSignIn;
    </script>
</body>

</html>