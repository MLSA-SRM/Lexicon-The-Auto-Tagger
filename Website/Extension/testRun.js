function sendDataFromTab() {
    var titleData = document.getElementsByTagName('h3')[0]
    var articleData = document.getElementsByTagName('p')[0]
    options = {
        method: 'POST',
        header: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'title':titleData.innerText, 'article':articleData.innerText})
    }

    fetch('http://127.0.0.1:5000/extToModel', options)
    .then(response => response.json())
    .then(data => {chrome.runtime.sendMessage(data)})
}

sendDataFromTab();