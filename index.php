<?php
// index.php
session_start();
if (isset($_SESSION['user_id'])) {
    header('location:chat');
} else {
    header("Location: views/index");
}
