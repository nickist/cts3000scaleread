  // function WebSocketTest() {
    $(document).ready(function() {
        if ("WebSocket" in window) {    
             // Let us open a web socket
             var ws = new WebSocket("ws://127.0.0.1:9000");
            $(document).on("click", "#startbutton", function() {
                 var i;
                 i++;
                    // Web Socket is connected, send data using send()
                    ws.send("Start");
                    
                
                    ws.onmessage = function (evt) { 
                    var received_msg = evt.data;
                      $(".status").text(received_msg);
                    };
                
                    ws.onclose = function() {                     
                    // websocket is closed.
                      $(".status").text("Stopped");
                    };
             });

             $(document).on("click", "#stopbutton", function() {
                 
              // Web Socket is connected, send data using send()
              ws.send("Stop");
              
          
              ws.onmessage = function (evt) { 
              var received_msg = evt.data;
                $(".status").text(received_msg);
              };
          
              ws.onclose = function() { 
              
              // websocket is closed.
              alert("Connection is closed..."); 
              };
       });
        } else {
          // The browser doesn't support WebSocket
          alert("WebSocket NOT supported by your Browser!");
       }

   });
      
    
         
       
        
    