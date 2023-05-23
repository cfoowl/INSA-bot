let id = require('../data/id_insa.json');
const puppeteer = require('puppeteer');

function sleep(ms){
    return new Promise(resolve => setTimeout(resolve, ms));
}


(async () => {

    //Lance et set up le navigateur
    const browser = await puppeteer.launch({headless:true, executablePath: '/usr/bin/chromium-browser'});
    const page = await browser.newPage();
    await page.setViewport({width:1366, height: 768});

    //Page de connection à insa cvl hyperplanning
    await page.goto('https://cas.insa-cvl.fr/cas/login?service=https:%2F%2Fedt.insa-cvl.fr%2Fetudiant', {
        waitUntil: "domcontentloaded"
      });

    //Connection à hyperplanning
    await page.type('#username', id.login);
    await page.type('#password', id.mdp);
    await page.click('button[name="submitBtn"]');
    await page.waitForNavigation({waitUntil: 'networkidle2'});


    //Clique sur le bouton résultat
    await page.click('li.item-menu_niveau0:nth-child(2)');
    await sleep(500);

    //Clique sur le menu déroulant des semestres
    //await page.click('.ocb_bouton');
    //await sleep(500);

    //Clique sur le premier semestre
    //await page.click('.deroulant-conteneur-show-hide');
    //await sleep(500);

    //Clique sur "par ordre chronologique"
    await page.click('label.iecb.iecbrbgauche.m-left.as-chips');
    await sleep(500);

    //Récupère toutes les notes du semestre
    const nom_matieres = await page.$$eval('div.zone-principale', (divs) => {
      const results = [];

      divs.forEach((div) => {
        const content = div.querySelector('div.ie-ellipsis').textContent;
        results.push(content);
      });
    return results;
    });

    //console.log(nom_matieres);

    //Ecrit la liste des matières dans un json
    json = JSON.stringify(nom_matieres);
    const fs = require("fs")
    fs.writeFile("./data/notes.json", json, err=>{
        if(err){
          console.log("Error writing file" ,err)
        } else {
          //console.log('JSON data is written to the file successfully')
        }
       })
    await browser.close();
})();
