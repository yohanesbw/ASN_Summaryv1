<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

<?php

$servername = "localhost";
$username = "root";
$password = "test123";

// Create connection
$conn = new mysqli($servername, $username, $password);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$sql = "SELECT html_detail from asn_summary.report_summary WHERE report_id='" . $_GET['report_id']."'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo $row["html_detail"];
    }
} else {
    echo "Please select the report";
}

$conn->close();

?>
