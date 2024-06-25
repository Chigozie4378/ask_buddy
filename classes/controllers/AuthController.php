<?php
require '../vendor/autoload.php';

class AuthController extends UserModel
{
    public $error;

    public function register()
    {
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $name = trim($_POST['name']);
            $email = trim($_POST['email']);
            $password = trim($_POST['password']);
            $repeat_password = trim($_POST['repeat_password']);

            // Validate inputs
            if (empty($name) || empty($email) || empty($password) || empty($repeat_password)) {
                $error = "All fields are required.";
                return $error;
            }

            if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
                $error = "Invalid email format.";
                return $error;
            }

            if ($password !== $repeat_password) {
                $error = "Passwords do not match.";
                return $error;
            }

            if ($this->getUserByEmail($email)) {
                $error = "Email is already registered.";
                return $error;
            }

            if ($this->registerUser($name, $email, $password)) {
                $result = $this->getUserByEmail($email);
                $_SESSION['user_id'] = $result['id'];
                $_SESSION['name'] = $result['name'];
                $_SESSION['email'] = $result['email'];
                header("location: chat");
            } else {
                $error = "Error registering user.";
                return $error;
            }
        }
    }
    public function login()
    {
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $email = trim($_POST['email']);
            $password = trim($_POST['password']);
            
            if (empty($email) || empty($password)) {
                $error = "All fields are required.";
                return $error;
            }
            $hashed_password = md5($password);
            $result = $this->userLogin($email, $hashed_password);
            if ($result->num_rows > 0) {
                $row = $result->fetch_assoc();
                $_SESSION["name"] = $row['name'];
                $_SESSION["email"] = $row["email"];
                $_SESSION["user_id"] = $row["id"];
                pclose(popen("start /b C:\\xampp\\htdocs\\ask_buddy\\start_flask.bat", "r"));
                header("location:chat");
            } else {
                $error = "Invalid email or password.";
                return $error;
            }
        }
    }

    public function googleLogin()
    {
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $id_token = trim($_POST['google_id_token']);

            // Verify the ID token with Google
            $client = new Google_Client(['client_id' => '110663364009-51n287pnbpn1fl1o9ld4csclfad9fvqf.apps.googleusercontent.com']);
            $payload = $client->verifyIdToken($id_token);
            if ($payload) {
                $email = $payload['email'];
                $name = $payload['name'];

                $user = $this->getUserByEmail($email);

                if ($user) {
                    // User exists, log them in
                    session_start();
                    $_SESSION['user_id'] = $user['id'];
                    echo json_encode(['status' => 'success']);
                } else {
                    // User does not exist, register them
                    if ($this->registerUser($name, $email, '')) {
                        session_start();
                        $_SESSION['user_id'] = $this->getUserByEmail($email)['id'];
                        echo json_encode(['status' => 'success']);
                    } else {
                        echo json_encode(['status' => 'error', 'message' => 'Error registering user.']);
                    }
                }
            } else {
                // Invalid ID token
                echo json_encode(['status' => 'error', 'message' => 'Invalid ID token.']);
            }
        }
    }
    public function logout()
    {
        session_destroy();
        header("location:../index");
    }
}

if (isset($_POST['google_id_token'])) {
    $authController = new AuthController();
    $authController->googleLogin();
} else {
    $authController = new AuthController();
    $authController->register();
}
