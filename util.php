<meta name="generator" content="Namo WebEditor(Trial)">
<?php
function dbconnect($host, $id, $pass, $db)  //데이터베이스 연결
{
    $connect = @mysql_connect($host, $id, $pass);
    mysql_select_db($db);
    return $connect;
}

function msg($msg) // 경고 메시지 출력 후 이전 페이지로 이동
{
    echo "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=euc-kr\" />
        <script>
             window.alert('$msg');
             history.go(-1);
        </script>";
    exit;
}

function s_msg($msg) //일반 메시지 출력
{
    echo "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=euc-kr\" />
        <script>
            window.alert('$msg');
        </script>";
}

function check_pass($pass, $c_pass) //패스워드 일치 여부 검사
{
    $ret = strcmp($pass, $c_pass);
    return $ret;
}

?>