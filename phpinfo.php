<?php
$info = [
    "version" => phpversion(),
    "ini_path" => php_ini_loaded_file(),
];

echo json_encode($info);