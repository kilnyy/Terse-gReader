<?php
    function getNews($username, $passwd) {
        return system("python gReader.py $username $passwd"); 
    }
        
    $has_login = true;
    if (isset($_COOKIE['21INSIST_SESSION_ID'])) {
        $sid = $_COOKIE['21INSIST_SESSION_ID'];
        session_id($sid);
        session_start();
        if (isset($_SESSION['user']) && isset($_SESSION['passwd'])) {
            ;
        } else $has_login = false;
    } else $has_login = false;
    if (!$has_login) {
        if (isset($_POST['user']) && isset($_POST['passwd'])) {
            session_start();
            $_SESSION['user'] = $_POST['user'];
            $_SESSION['passwd'] = $_POST['passwd'];
            setcookie('21INSIST_SESSION_ID', session_id(), time() + 60*60*24*30, "/");
            $has_login = true;
        }
    }
?>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>gReader</title>
        <link rel=stylesheet href="style.css" type="text/css" /> 
    </head>
    <body>
<?php
    if ($has_login) {
        getNews($_SESSION['user'], $_SESSION['passwd']);
    } else {
?>
        <form method="post" action="index.php">
            <span>用户名：</span>
            <input type="text" name="user" />
            <span>密码：</span>
            <input type="password" name="passwd" />
            <input type="submit" name="submit" value="登录" />
        </form>
<?php
    }
?>
    </body>
</html>
