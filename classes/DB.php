
<?php
class DB{
    private $host = 'localhost';
    private $server = 'root';
    private $password = '';
    private $dbname = 'chigzeai';

    protected function connect(){
        $conn = mysqli_connect($this->host,$this->server,$this->password,$this->dbname);
        if ($conn->connect_error){
            echo "Failed".$conn->connect_error;
        }
        return $conn;
    }

}
?>