<?php
class Session{
    public static function AuthViews(){
        if (!isset($_SESSION['user_id'])) {
            header("Location: ../index");
        }
    }
    public static function Auth(){
        if (isset($_SESSION['user_id'])) {
            header('location:chat');
        }
    }
    
}