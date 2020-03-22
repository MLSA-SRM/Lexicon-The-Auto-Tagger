<pre><?php
    $title = $_POST['title'];
    $article = $_POST['article'];

    if(!isset($_POST['submit'])){
        echo 'Thank you for your sumbission';
        die();
    }

    $bridge = mysqli_connect('localhost', 'root', '','highdb');

    $query = "INSERT INTO articles (Title, Article) VALUES ('$title', '$article')";

    if($bridge->query($query)){
        echo 'wew';
    }
?>
</pre>