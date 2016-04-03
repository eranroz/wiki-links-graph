<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
<title>Wikipedia connected components</title>

<!-- Bootstrap -->
<link href="css/bootstrap.min.css" rel="stylesheet">

<!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
<!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
<!--[if lt IE 9]>
<script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
<script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
<![endif]-->
<style>

</style>
</head>
<body>
<nav class="navbar navbar-inverse navbar-fixed-top">
<div class="container">
    <div class="navbar-header"><a class="navbar-brand" href="#">Connected Components</a></div>
    <div id="navbar" class="collapse navbar-collapse">
        <ul class="nav navbar-nav">
        <li class="active"><a href="#">Home</a></li>
        <li><a href="https://github.com/eranroz/wiki-links-graph">Source</a></li>
        <li><a href="#">About</a></li>
        </ul>
    </div>
</div>
</nav>
<div class="container">
<div class="starter-template" style="padding:40px 15px; text-align:center;">
<h1>Wikipedia connected components!</h1>
<p class="lead">
This page shows a report of connected components in Wikipedia links graph. The report is generated based on dumps. You can use it to find groups of orphan pages.
</p>
<table border="1" class="table table-hover table-striped">
<thead>
<tr>
<th>#</th>
<th>Members</th>
</tr>
</thead>
<tbody>
<?php 
include('hewiki_components.html');
?>
</tbody>
</table>
</div>
</div>
<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
<!-- Include all compiled plugins (below), or include individual files as needed -->
<script src="js/bootstrap.min.js"></script>
</body>
</html>
