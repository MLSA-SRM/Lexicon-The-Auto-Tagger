const tagHead = document.getElementById("tag");
const loader = document.getElementById("loader");

function Disapp(){
    tagHead.style.display = "block"
}
function loaderDispl(){
    loader.style.display = "block"
}
function postTest() {   
    var result;
    chrome.tabs.executeScript({
        file: 'testRun.js'
    });
    chrome.runtime.onMessage.addListener(function(msg, sender, response){
        result = msg.tags;
        
        function appendData(data){

            var mainContainer = document.getElementById("incTags");
            for (var i = 0; i < data.length; i++) {
                var div = document.createElement("button");
                div.classList.add("tagStyle"); 
                div.innerHTML =  data[i];
                mainContainer.appendChild(div);
              }
            }
            loader.style.display = "none";
        appendData(result);
    });
    
}

document.getElementById("post-test").addEventListener("click", postTest);
document.getElementById("post-test").addEventListener("click", Disapp);


