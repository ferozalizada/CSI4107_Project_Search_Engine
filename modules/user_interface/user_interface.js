var relevanceList = [];
var relevanceQueryList = [];
var query;
var suggestions = [];

window.onload = function(){
    var searchInput = document.getElementById("searchInput");

    searchInput.addEventListener("keydown", function(e){
        var value = searchInput.value.trim();
        if(e.keyCode == 32 && value != ""){ // spacebar is pressed
            getSuggestions(value);
        }
    });

    searchInput.addEventListener("keyup", function(e){
        if(searchInput.value.trim() == ""){ // spacebar is pressed
            document.getElementById("suggestions").style.display = "none";
        }
    });

    document.addEventListener("click", function(e){
        if(e.target.className != "suggestion" && e.target != searchInput){
            document.getElementById("suggestions").style.display = "none";
        }
    });

    searchInput.addEventListener("focus", function(e){
        if(searchInput.value.trim() != "" && suggestions.length > 0){ // spacebar is pressed
            document.getElementById("suggestions").style.display = "block";
        }
    });
};

function search() {
    query = document.getElementById("searchInput").value;
    var model = document.querySelector('input[name="model"]:checked').value;
    var collection = document.querySelector('input[name="collection"]:checked').value;

    document.getElementById("suggestions").style.display = "none";

    relevanceList = [];

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        var docs = JSON.parse(this.responseText);
        
        var content = "";
        for(var i = 0; i < docs.length; i++){
            var test = docs[i]["description"].replace(/[<>]/g, '');
            var excerpt = test.split(".")[0] + ".";
            updateUnrelevant(docs[i]["docID"]);

            var doc = "<div class='docs' id='" + docs[i]["docID"] + "'>" +
                            "<div class='header'>" +
                                "<div class='docTitle'>" + 
                                    docs[i]["title"] +
                                    "<img src='/modules/user_interface/description.svg' class='linkToDoc' onclick=\"viewFullDoc('" + docs[i]["title"] + "','" + test.trim() + "')\" />" +
                                "</div>" +
                                "<div class='score'>Score: " + docs[i]["score"].toFixed(2) + "</div>" +
                            "</div>" +
                            "<div class='excerpt'>" + excerpt + "</div>" +
                            "<div class='docRelevant'>" +
                                "<input type='checkbox' id='r" + docs[i]["docID"] + "' name='relevantDoc' value='" + docs[i]["docID"] + "' onclick='updateRelevance(this.value)' />" +
                                "<label for='relevantDoc'> Relevant</label>" +
                            "</div>" +
                        "</div>";
            content += doc;
        }

        document.getElementById("result").innerHTML = content;
        }
    };
    
    xhttp.open("POST", "user_interface.py", true);
    xhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xhttp.send("query=" + query + "&model=" + model + "&collection=" + collection);
}

function viewFullDoc(title, description){
    myWindow = window.open("", title, "resizable=yes,top=150,left=300,width=800,height=400");
    myWindow.document.write("<h1>" + title + "</h1><p style='text-align:justify;'>" + description.replace(/\$/g, "\'") + "</p>");
    // https://www.w3schools.com/jsref/met_win_open.asp
}

function updateRelevance(docID){
    if(relevanceList[docID] == 0){
        relevanceList[docID] = 1; // make a new entry or update it
    }else{
        relevanceList[docID] = 0;
    }
    
    relevanceQueryList[query] = relevanceList;
}

function updateUnrelevant(docID){
    relevanceList[docID] = 0; // make a new entry or update it

    relevanceQueryList[query] = relevanceList;
}

function getSuggestions(suggestion_query){
    var model = document.querySelector('input[name="model"]:checked').value;
    var collection = document.querySelector('input[name="collection"]:checked').value;

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            suggestions = JSON.parse(this.responseText);

            if(suggestions.length > 0){
                displaySuggestions(suggestions);
                document.getElementById("suggestions").style.display = "block";
            }
        }
    };

    xhttp.open("POST", "", true);
    xhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xhttp.send("suggestion_query=" + suggestion_query + "&model=" + model + "&collection=" + collection + "&more_results=" + false);
}

function displaySuggestions(suggestions){
    var sArea = document.getElementById("suggestions");
    var content = "";

    // assuming suggestions is an array of string
    for(i in suggestions){
        content += "<div class='suggestion' onclick='selectSuggestion(this.innerHTML)'>" + suggestions[i] + "</div>";
    }

    sArea.innerHTML = content;
}

function selectSuggestion(_query){
    document.getElementById("searchInput").value = _query;
    document.getElementById("suggestions").style.display = "none";
}