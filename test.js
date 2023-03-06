var id = require('./data/id_insa.json');
const puppeteer = require('puppeteer');

function sleep(ms){
    return new Promise(resolve => setTimeout(resolve, ms));
}


(async () => {
    const browser = await puppeteer.launch({headless:false});
    const page = await browser.newPage();
    await page.setViewport({width:1366, height: 768});

    await page.goto('https://cas.insa-cvl.fr/cas/login?service=https:%2F%2Fedt.insa-cvl.fr%2Fetudiant');

    await sleep(500);

    await page.type('#username', id.login);
    await page.type('#password', id.mdp);
    await page.click('button[name="submitBtn"]');

    await sleep(2000);
    await page.click('li.item-menu_niveau0:nth-child(2)');

    await sleep(500);

    await page.click('.ocb_bouton');

    await sleep(500);

    await page.click('.deroulant-conteneur-show-hide');

    await sleep(500);

    await page.click('label.iecb:nth-child(2) > span:nth-child(2)');

    await sleep(500);

    const arias = await page.evaluate(() => Array.from(
        document.querySelectorAll(".Espace"), 
        e => e.getAttribute("aria-label")
      ));
    
    arias.shift();
    test = [];

    for (let i in arias) {
        var k = "";
        for(let j in arias[i]) {
            if (!"0123456789".includes(arias[i][j])) {
                k+=arias[i][j];
            } else {
                break;
            }
        }
        test.push(k);
    }
    json = JSON.stringify(test);

    var fs = require("fs")
    fs.writeFile("./notes.json", json, err=>{
        if(err){
          console.log("Error writing file" ,err)
        } else {
          console.log('JSON data is written to the file successfully')
        }
       })

    await sleep(5000);

    await browser.close();
})();