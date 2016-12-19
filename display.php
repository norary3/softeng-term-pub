<!DOCTYPE HTML>

<html>
<head>
    <title>Cast Vote</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <!--[if lte IE 8]>
    <script src="assets/js/ie/html5shiv.js"></script><![endif]-->
    <link rel="stylesheet" href="assets/css/main.css"/>
    <!--[if lte IE 8]>
    <link rel="stylesheet" href="assets/css/ie8.css"/><![endif]-->
    <!--[if lte IE 9]>
    <link rel="stylesheet" href="assets/css/ie9.css"/><![endif]-->
    <style>
        .aa {

        }
    </style>

</head>

<style>
    @media screen and (max-width: 840px) {
        .box.highlight i img {
            width: 50%;
        }
    }
</style>
<style>
    @media screen and (max-width: 840px) {
        .box.highlight h3 {
            padding-top: 15px;
        }
    }
</style>

<style>
    @media screen and (max-width: 430px) {
        section.wrapper.style1 div.aa {
            padding-left: 0px;
        }
    }
</style>

<style>
    @media screen and (max-width: 430px) {
        section div div p {
            width: 250px;
            line-height: 200%
        }
    }
</style>


<body>
<div id="page-wrapper">

    <!-- Header -->
    <div id="header" style="padding-top: 0px;">

        <!-- Nav -->
        <nav id="nav">
            <ul style="height: 50px;">
                <li class="#"><a href="index.php">Home</a></li>
                <li><a href="cast.php">Cast Vote</a></li>
                <li><a href="display.php">Display Result</a></li>
                <li><a href="advantage.php">Advantages</a></li>
                <li><a href="https://github.com/chaeheum3/softeng-term-pub">Clean Vote</a></li>
            </ul>
        </nav>

    </div>

    <?php

    include "config.php";
    include "util.php";

    $connect = dbconnect($host, $dbid, $dbpass, $dbname);

    $query = "select * from candidate";

    $result = mysql_query($query, $connect);

    mysql_data_seek($result, 0);
    $can = mysql_fetch_array($result);
    $first_candidate = $can['public_key'];

    mysql_data_seek($result, 1);
    $can = mysql_fetch_array($result);
    $second_candidate = $can['public_key'];

    mysql_data_seek($result, 2);
    $can = mysql_fetch_array($result);
    $third_candidate = $can['public_key'];

    $query = "select * from ballot";

    $result = mysql_query($query, $connect);

    $row_num = mysql_num_rows($result);


    $first_count = 0;
    $second_count = 0;
    $third_count = 0;


    for ($i = 1; $i <= $row_num; $i++) {
        $row = mysql_fetch_array($result);
        if ($row["candidate"] == $first_candidate) {
            $first_count += 1;
        } else if ($row["candidate"] == $second_candidate) {
            $second_count += 1;
        } else if ($row["candidate"] == $third_candidate) {
            $third_count += 1;
        }
    }

    ?>

    <!-- Main -->
    <section class="wrapper style1">
        <div class="container">
            <div id="content">

                <!-- Content -->

                <article>
                    <header>
                        <h2>Display Result</h2>
                        <p style="margin-bottom: 70px;">Check out the results.</p>
                    </header>
                </article>
            </div>
            <div>

                <?php
                $max = $first_count;
                if ($second_count > $max) {
                    $max = $second_count;
                }
                if ($third_count > $max) {
                    $max = $third_count;
                }

                if ($first_count == $max) {
                    $cnt += 1;
                }
                if ($second_count == $max) {
                    $cnt += 1;
                }
                if ($third_count == $max) {
                    $cnt += 1;
                }

                if ($cnt == 1) {
                    if ($max == $first_count) {
                        $max_name = "1. Pororo";
                    } else if ($max == $second_count) {
                        $max_name = "2. Crong";
                    } else {
                        $max_name = "3. Roofy";
                    }
                }

                echo "<p style = 'font-size : 1.5em;'>The person who has the most vote : <font color ='#ff5b60' style = 'font-weight: bold; font-size : 1.6em;'>$max_name</font></p>";
                ?>


    </section>


    <section class="wrapper style1">
        <div class="container">
            <div class="row 200%">

                <section class="4u 12u(narrower)">
                    <div class="box highlight">
                        <i><img src="./images/bbo.png"/></i>
                        <h3 style="margin-bottom: 40px;">1. Pororo</h3>
                        <p style="font-size : 1.5em;"><?= $first_count ?> vote</p>
                    </div>
                </section>
                <section class="4u 12u(narrower)">
                    <div class="box highlight">
                        <i><img src="./images/crong.png"/></i>
                        <h3 style="margin-bottom: 40px;">2. Crong</h3>
                        <p style="font-size : 1.5em;"><?= $second_count ?> vote</p>
                    </div>
                </section>
                <section class="4u 12u(narrower)">
                    <div class="box highlight">
                        <i><img src="./images/rupy.png"/></i>
                        <h3 style="margin-bottom: 40px;">3. Roofy</h3>
                        <p style="font-size : 1.5em;"><?= $third_count ?> vote</p>
                    </div>
                </section>
            </div>
        </div>


        <div class="container">
            <?php


            $query = "select * from ballot";

            $result = mysql_query($query, $connect);
            $row_num = mysql_num_rows($result);


            echo "<table>";
            echo "<tr style = 'font-size :22px; font-weight : 800; border-color:black; border-width : 2px; border-bottom-style:solid;text-align:center;'><td style = 'border-bottom-style:solid; width: 100px;'>No</td><td style='width: 300px;'>ID</td><td style='width: 100px;height: 30px;text-align:center;'>Candidate</td></tr>";

            for ($i = 1; $i <= $row_num; $i++) {
                $array = mysql_fetch_array($result);
                echo "<tr style = 'text-align:center;height: 30px;font-weight:bold;'>";
                echo "<td>$i</td>";

                echo "<td style = 'font-family: Consolas;'>";
                echo "$array[2]";
                echo "</td>";


                echo "<td style = 'font-weight:bold;'>";
                if ($array[3] == $first_candidate) {
                    echo "Pororo";
                } else if ($array[3] == $second_candidate) {
                    echo "Crong";
                } else if ($array[3] == $third_candidate) {
                    echo "Roofy";
                }
                echo "</td>";

                echo "</tr>";
            }
            echo "</table>";


            mysql_close($connect);
            ?>
        </div>

    </section>

    <!-- Copyright -->
    <div class="copyright">
        <ul class="menu" style="text-align:center">
            <li>&copy; CleanVote. All rights reserved</li>
        </ul>
    </div>


</div>


<!-- Scripts -->
<script src="assets/js/jquery.min.js"></script>
<script src="assets/js/jquery.dropotron.min.js"></script>
<script src="assets/js/skel.min.js"></script>
<script src="assets/js/util.js"></script>
<!--[if lte IE 8]>
<script src="assets/js/ie/respond.min.js"></script><![endif]-->
<script src="assets/js/main.js"></script>

</body>
</html>