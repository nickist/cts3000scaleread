if(typeof(EventSource) !== "undefined") {
  var source = new EventSource("submit.php");
  source.onmessage = function(event) {
    document.getElementById("result").innerHTML = event.data;
    if(event.data === "Running"){
      document.getElementById("result").style.color = "Green";
    }else if (event.data === "Stopped" ||
    event.data === "Error" ||
    event.data === "Tripped"){
      document.getElementById("result").style.color = "Red"; 
    }else {
      document.getElementById("result").style.color = "Blue";
    }
  };
} else {
  document.getElementById("result").innerHTML = "Sorry, your browser does not support server-sent events...";
}