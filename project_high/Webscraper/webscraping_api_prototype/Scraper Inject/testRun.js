function sendDataFromTab() {
    var lst = document.documentElement.querySelectorAll('h3');
    var link_list = []
    for (let l of lst) {
        let x = l.querySelector('a')
        if (x != null) {
            var link = x.getAttribute('href');
            if (link.substring(0, 5) != 'https') {
                link = 'https://medium.com' + link;
            }
            if (!link_list.includes(link)) {
                link_list.push(link);
            }
        }
    }

    options = {
        method: 'POST',
        header: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'link': link_list})
    }

    fetch('http://127.0.0.1:5000/scrapeDataMaster', options)
    .then(response => response.json())
    .then(data => {chrome.runtime.sendMessage(data)})
}

sendDataFromTab();