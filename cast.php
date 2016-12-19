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

    <!-- Main -->
    <section class="wrapper style1">
        <div class="container">
            <div id="content">

                <!-- Content -->

                <article>
                    <header>
                        <h2>Cast Vote</h2>
                        <p>Vote for the candidate you want to elect.</p>
                    </header>
                </article>


                <section class="wrapper style1">
                    <div class="container">
                        <div class="row 200%">

                            <section class="4u 12u(narrower)">
                                <div class="box highlight">
                                    <i><img src="./images/bbo.png"/></i>
                                    <h3>1. Pororo</h3>
                                    <p>President of Korean childhood</p>
                                </div>
                            </section>
                            <section class="4u 12u(narrower)">
                                <div class="box highlight">
                                    <i><img src="./images/crong.png"/></i>
                                    <h3>2. Crong</h3>
                                    <p>Baby dinosaur raised by Pororo</p>
                                </div>
                            </section>
                            <section class="4u 12u(narrower)">
                                <div class="box highlight">
                                    <i><img src="./images/rupy.png"/></i>
                                    <h3>3. Roofy</h3>
                                    <p>Baby beaver who is very shy</p>
                                </div>
                            </section>
                        </div>
                    </div>
                </section>

                <div>
                    <form name="form" action="cast_insert.php" method="post">

                        <table>
                            <tr>
                                <th style="vertical-align : middle">Private Key<br></th>
                                <td><input type="text" name="input_id"></td>
                            </tr>

                            <tr>
                                <th style="vertical-align : middle">Candidate</th>
                                <td style="padding-top: 20px;">
                                    <input type="radio" name="input_ca" value="0"> 1. Pororo<br>
                                    <input type="radio" name="input_ca" value="1"> 2. Crong<br>
                                    <input type="radio" name="input_ca" value="2"> 3. Roofy
                                </td>
                            </tr>
                        </table>

                        <br>
                        <div>
                            <center><input style="vertical-align : middle;" type="submit" value="Voting"
                                           style="width: 70px; height: 36px; font-size : 14"></center>
                        </div>
                    </form>

                    <br>
                    <br>

                </div>
            </div>
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