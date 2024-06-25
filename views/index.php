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
    <title>Login</title>
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
                <!-- Pills navs -->
                <ul class="nav nav-pills nav-justified mb-3" id="ex1" role="tablist">
                    <li class="nav-item" role="presentation">
                        <a class="nav-link active" id="tab-login" data-mdb-pill-init href="index" role="tab"
                            aria-controls="pills-login" aria-selected="true">Login</a>
                    </li>
                    <li class="nav-item" role="presentation">
                        <a class="nav-link" id="tab-register" data-mdb-pill-init href="signup" role="tab"
                            aria-controls="pills-register" aria-selected="false">Register</a>
                    </li>
                </ul>
                <!-- Pills navs -->

                <!-- Pills content -->
                <div class="tab-content">
                    <div class="tab-pane fade show active" id="pills-login" role="tabpanel" aria-labelledby="tab-login">
                        <form action="" method="post">
                            <div class="text-center mb-3">
                                <p>Sign in with:</p>
                                <button type="button" data-mdb-button-init data-mdb-ripple-init
                                    class="btn btn-link btn-floating mx-1">
                                    <i class="fab fa-google"></i>
                                </button>
                            </div>
                            <div class="text-center"><b><i class="text-danger"><?php echo $ctr->login(); ?></i></b></div>

                            <p class="text-center">or:</p>

                            <!-- Email input -->
                            <div data-mdb-input-init class="form-outline mb-4">
                                <label class="form-label" for="email">Email</label>
                                <input type="email" id="email" class="form-control" name="email"  value="<?php echo OldInput::input('email')?>"/>
                            </div>

                            <!-- Password input -->
                            <div data-mdb-input-init class="form-outline mb-4">
                                <label class="form-label" for="loginPassword">Password</label>
                                <input type="password" id="loginPassword" class="form-control" name="password"  value="<?php echo OldInput::input('password')?>"/>
                            </div>

                            <!-- 2 column grid layout -->
                            <div class="row mb-4 d-flex justify-content-center">
                                    <!-- Simple link -->
                                    <a href="#!">Forgot password?</a>
                              
                            </div>

                            <!-- Submit button -->
                            <button type="submit" data-mdb-button-init data-mdb-ripple-init
                                class="btn btn-primary btn-block mb-4">Sign in</button>

                            <!-- Register buttons -->
                            <div class="text-center">
                                <p>Not a member? <a href="signup">Register</a></p>
                            </div>
                        </form>
                    </div>
                </div>
                <!-- Pills content -->
            </div>
        </div>
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>

</html>
