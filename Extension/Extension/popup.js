const tagHead = document.getElementById("tag");

function Disapp(){
    tagHead.style.display = "block"
}
function postTest() {   
    chrome.tabs.executeScript({
        file: 'testRun.js'
    });
    chrome.runtime.onMessage.addListener(function(msg, sender, response){
        document.write(msg.tags);
    })
}

document.getElementById("post-test").addEventListener("click", postTest);
document.getElementById("post-test").addEventListener("click", Disapp);


