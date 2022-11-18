<!DOCTYPE html>
<html lang="sv">
<head>
  <title>Room Calendar</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-+0n0xVW2eSR5OomGNYDnhzAbDsOXxcvSN1TPprVMTNDbiYZCxYbOOl7+AMvyTG2x" crossorigin="anonymous">
  <link rel="stylesheet" type="text/css" href="style.css">
  <link href="https://fonts.googleapis.com/css?family=Poppins:300,400,700,900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.3.1/css/all.css" integrity="sha384-mzrmE5qonljUremFsqc01SB46JvROS7bZs3IO2EmfFsd15uHvIt+Y8vEf7N7fWAU" crossorigin="anonymous">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.0/jquery.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-gtEjrD/SeCtmISkJkNUaaKMoLD0//ElJ19smozuHV6z3Iehds+3Ulb9Bn9Plx0x4" crossorigin="anonymous"></script>
  
  <script>
  $(document).ready(function() {
      $(".divkl").load("https://mickekring.se/stats/room/b212a/kl.php");
      var refreshId = setInterval(function() {
          $(".divkl").load("https://mickekring.se/stats/room/b212a/kl.php");
      }, 5000);
      $(".divday").load("https://mickekring.se/stats/room/b212a/day.php");
      var refreshId3 = setInterval(function() {
          $(".divday").load("https://mickekring.se/stats/room/b212a/day.php");
      }, 5000);
  });
  </script>

</head>

<body>


<div class="container-fluid">
    
   <div class="row">
    
      <div class="col-md-4">
      
        <div class="row">
        <div class="div1-half-top">
        <h2 class="calheading">B212A</h2>
        <div class="divkl"></div></div></div>
        
        <div class="row">
          <div class="div1-half-bottom">
          <video id="videoBG" autoplay muted loop>
          <source src="micke.mp4" type="video/mp4"></video>
          <div class="divprofile">
            <h3>Micke Kring</h3>
            <p>IT-PEDAGOG</p>
            <p>micke.kring@edu.stockholm.se</p>
          <div class="divstatus"></div></div></div></div>
     
      </div>
    
      <div class="col-md-8">
        
        <div class="row">
        <div class="div1-half">
        <h2 class="calheading"><i class="far fa-calendar-alt" aria-hidden="true"></i> Kalender</h2>
        <div class="divday"></div>
        </div>
        </div>
        </div>
   
      </div>

  </div>


</div>

</body>
</html>