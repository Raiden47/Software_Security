<?php
// Function to create a sql connection.
function getDB() {
  $dbhost="10.9.0.6";
  $dbuser="seed";
  $dbpass="dees";
  $dbname="sqllab_users";

  // Create a DB connection
  $conn = new mysqli($dbhost, $dbuser, $dbpass, $dbname);
  if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error . "\n");
  }
  return $conn;
}

// filtering
$input_uname = $msqli->real_escape_string ($_GET['username']);
$input_pwd = $msqli->real_escape_string ($_GET['Password']);
$hashed_pwd = sha1($input_pwd);

// create a connection
$conn = getDB();

// do the query
$result = $conn->query("SELECT id, name, eid, salary, ssn
                        FROM credential
                        WHERE name= ? and Password= ?");
                
// statement        
$stmt = $conn -> prepare($result);
$stmt = $conn -> $bind_param("ss", $input_name, $hashed_pwd);
$stmt -> execute();
$stmt -> $bind_result($id, $name, $eid, $salary, $ssn);

if ($stmt->num_rows > 0) {
  // only take the first row 
  $firstrow = $stmt->fetch();
  $id     = $firstrow["id"];
  $name   = $firstrow["name"];
  $eid    = $firstrow["eid"];
  $salary = $firstrow["salary"];
  $ssn    = $firstrow["ssn"];
}

// close the sql connection
$conn->close();
?>
