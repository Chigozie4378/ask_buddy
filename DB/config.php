<?php

define('DB_SERVER', 'localhost');
define('DB_USERNAME', 'root');
define('DB_PASSWORD', '');
define('DB_NAME', 'chigzeai');

/* Attempt to connect to MySQL database */
$link = new mysqli(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);


if($link === false){
    die("ERROR: Could not connect. " . mysqli_connect_error());
} else {
    echo('Connected to database successfully.');
}


