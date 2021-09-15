const siege = require('siege')

siege()
    .on('nodesdo.okeit.edu:8080')
    .for(100).times
    .get('/get_all_mo')
    .attack()
