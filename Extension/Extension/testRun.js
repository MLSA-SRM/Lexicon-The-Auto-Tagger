function sendDataFromTab() {
    var titleData = document.getElementsByTagName('h3')[0];
    var nodes = document.querySelectorAll("p");
    var str1 = "";
      nodes.forEach((node)=>{
        str1 = str1 + node.innerText;
    });
    options = {
        method: 'POST',
        header: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'title':titleData.innerText, 'article':str1})
    }

    fetch('https://projecthigh.herokuapp.com/extToModel', options)
    .then(response => response.json())
    .then(data => {chrome.runtime.sendMessage(data)})
}

sendDataFromTab();