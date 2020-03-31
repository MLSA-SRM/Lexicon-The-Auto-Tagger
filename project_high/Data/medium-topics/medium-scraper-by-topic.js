const axios = require('axios');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;

async function scrapePage(url) {
    let i=0;

    let response = await axios.get(url);
    let htmlString = response.data

    const dom = new JSDOM(htmlString)

    lst = dom.window.document.documentElement.querySelectorAll('h3');
    for (let l of lst) {
        let x = l.querySelector('a')
        if (x != null) {
            console.log(x.getAttribute('href'));
            i++;
        }
    }
    console.log(i);
}

scrapePage('https://medium.com/topic/art')
