<?php
    include("C:\xampp\htdocs\ajax_insert\db.php");

    if(isset($_POST['done'])){
        $title  = mysql_escape_string($_POST['Title']);
        $article  = mysql_escape_string($_POST['Article']);

        mysql_query("INSERT INTO articles(Title, Article) VALUES('{$title}', '{$article}')");
        exit();

    }
?>