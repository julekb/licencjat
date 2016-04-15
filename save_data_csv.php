<!-- <?php
// the $_POST[] array will contain the passed in filename and data
// the directory "data" is writable by the server (chmod 777)
$date = "aaaaa";
$filename = "data/".$_POST["filename".$date];
$data = $_POST['filedata'];
// write the file to disk
file_put_contents($filename.$date, $data);
?> -->

<?php
// the $_POST[] array will contain the passed in filename and data
// the directory "data" is writable by the server (chmod 777)
$d = date("y-m-d-H:i:s");
$filename = "data/".$_POST['filename'].$d.".csv";
$data = $_POST['filedata'];
// write the file to disk
file_put_contents($filename, $data);
?>