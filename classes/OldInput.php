<?php
class OldInput{
    public static function input($field, $default = '') {
        return isset($_POST[$field]) ? htmlspecialchars($_POST[$field], ENT_QUOTES, 'UTF-8') : $default;
    }
}