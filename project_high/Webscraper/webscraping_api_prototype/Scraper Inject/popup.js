
const btn = document.getElementById("btn");

function postTest() {
    var result;
    chrome.tabs.executeScript({
        file: 'testRun.js'
    });    
}

document.getElementById("post-test").addEventListener("click", postTest);


