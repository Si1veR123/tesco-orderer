function removeOrder(order, span) {
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == XMLHttpRequest.DONE) {   // XMLHttpRequest.DONE == 4
           if (xmlhttp.status == 200) {
               response = JSON.parse(xmlhttp.responseText)
               if (response["success"] === "y") {
                   span.parentElement.parentElement.remove()
               } else {
                   alert("Error: Tried to remove list not belonging to you")
               }
           }
           else if (xmlhttp.status == 400) {
              alert('There was an error 400');
           }
           else {
               alert('Something else other than status code 200 or 400 was returned');
           }
        }
    };

    xmlhttp.open("GET", "/removeorder/" + String(order), true);
    xmlhttp.send();
}