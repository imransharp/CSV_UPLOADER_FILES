<?php
$host = "172.21.163.160";
$dbname = "gcssbi_dashboard_adi";
$username = "GCSSBI";
$password = "Engineer@7070";

// Create connection
$conn = new mysqli($host, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
