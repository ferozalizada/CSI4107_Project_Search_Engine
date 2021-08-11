window.onload = () => {
  searchBtn = document.getElementById("searchBtn");
  searchBtn.addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
      event.preventDefault();
      search();
    }
  });
  function search() {
    var query = document.getElementById("searchInput").value;
    var model = document.querySelector('input[name="model"]:checked').value;
    var collection = document.querySelector('input[name="collection"]:checked')
      .value;

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        var docs = JSON.parse(this.responseText);

        var content = "";
        for (var i = 0; i < docs.length; i++) {
          var excerpt = docs[i]["description"].split(".")[0] + ".";

          var doc =
            "<div class='docs' id='" +
            docs[i]["docID"] +
            "'>" +
            "<div class='header'>" +
            "<div class='docTitle'>" +
            docs[i]["title"] +
            "<img src='/modules/user_interface/description.svg' class='linkToDoc' onclick=\"viewFullDoc('" +
            docs[i]["title"] +
            "','" +
            docs[i]["description"].trim().replace(/'/g, "$") +
            "')\" />" +
            "</div>" +
            "<div class='score'>Score: " +
            docs[i]["score"].toFixed(2) +
            "</div>" +
            "</div>" +
            "<div class='excerpt'>" +
            excerpt +
            "</div>" +
            "</div>";
          content += doc;
        }

        document.getElementById("result").innerHTML = content;
      }
    };
    xhttp.open("POST", "user_interface.py", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send(
      "query=" + query + "&model=" + model + "&collection=" + collection
    );
  }

  function viewFullDoc(title, description) {
    myWindow = window.open(
      "",
      title,
      "resizable=yes,top=150,left=300,width=800,height=400"
    );
    myWindow.document.write(
      "<h1>" +
        title +
        "</h1><p style='text-align:justify;'>" +
        description.replace(/\$/g, "'") +
        "</p>"
    );
    // https://www.w3schools.com/jsref/met_win_open.asp
  }
};
