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

    await sleep(1000);

    await page.type('#username', id.login);
    await page.type('#password', id.mdp);
    await page.click('button[name="submitBtn"]');

    await sleep(3000);
    await page.click('li.item-menu_niveau0:nth-child(2)');

    await sleep(1000);

    await page.click('.ocb_bouton');

    await sleep(1000);

    await page.click('.deroulant-conteneur-show-hide');

    await sleep(1000);

    await page.click('label.iecb:nth-child(2) > span:nth-child(2)');

    await sleep(1000);

    const arias = await page.evaluate(() => Array.from(
        document.querySelectorAll(".Espace"), 
        e => e.getAttribute("aria-label")
      ));
    
    arias.shift();
    console.log(arias);

    await sleep(5000);

    await browser.close();
})();