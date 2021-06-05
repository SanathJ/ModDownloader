const fetch = require('node-fetch');
const fs = require('fs');
const prompt = require('prompt-sync')({ sigint: true });

// (async () => {
//     try {
//         var text = await main();
//         console.log(text);
//     } catch (e) {
//         // Deal with the fact the chain failed
//     }
// })();

main();


async function main() {
    const dir = prompt('Manifest.json directory: ');
    let manifest;
    try {
        manifest = JSON.parse(fs.readFileSync(dir + '/manifest.json'));
    }
    catch (error) {
        console.log(error);
        return;
    }
    const promiseArr = [];

    for (const mod of manifest.files) {
        promiseArr.push(findCDNLink(mod.projectID, mod.fileID));
    }
    const results = await Promise.all(promiseArr);

    fs.writeFileSync('links.csv', results.join(',\n'));
}

async function findCDNLink(projectID, fileID) {
    const res = await fetch(`https://addons-ecs.forgesvc.net/api/v2/addon/${projectID}/files`, {
        headers: {
            accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
        },
        referrerPolicy: 'strict-origin-when-cross-origin',
        body: null,
        method: 'GET',
        mode: 'cors',
    });

    const fileList = JSON.parse(await res.text());
    for (const file of fileList) {
        if(file.id == fileID) {
            return file.downloadUrl;
        }
    }
}
