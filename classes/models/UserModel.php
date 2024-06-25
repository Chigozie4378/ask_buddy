<?php
class UserModel extends DB{
    private $db;
    public function __construct(){
        $this->db =  $this->connect();
    }
    protected function registerUser($name, $email, $password) {
        $stmt = $this->db->prepare("INSERT INTO users (name, email, password) VALUES (?, ?, ?)");
        $hashed_password = md5($password);
        $stmt->bind_param('sss', $name, $email, $hashed_password);
        return $stmt->execute();
    }

    protected function getUserByEmail($email) {
        $stmt = $this->db->prepare("SELECT * FROM users WHERE email = ?");
        $stmt->bind_param('s', $email);
        $stmt->execute();
        $result = $stmt->get_result();
        return $result->fetch_assoc();
    }
    
    protected function userLogin($username, $hashed_password)
    {
        $dbconn = $this->connect();
        $query = "SELECT * FROM users WHERE email = ? AND password = ? ";
        $stmt = $dbconn->prepare($query);
        $stmt->bind_param("ss", $username, $hashed_password);
        $stmt->execute();
        $result = $stmt->get_result();
        return $result;
    }
    
}

