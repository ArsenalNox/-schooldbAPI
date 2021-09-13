var express = require('express')
var cluster = require('cluster')
const { connect } = require('http2')
const { SSL_OP_EPHEMERAL_RSA } = require('constants')
var app = express()

const port = 8080

if (cluster.isMaster){
    console.log('Cluster master is starting...')
    var cpuCount = require('os').cpus().length
    
    for(let i = 0; i < cpuCount-2; i++){
        cluster.fork()
    }

} else {

    function connect_to_database(){
        var mysql = require('mysql')

        var con = mysql.createConnection({
            database: 'schools',
            host: 'localhost',
            user: 'root',
            password: 'root'
        })

        return con
    }

    app.get('/get_all_schools', (req, res) => {
        console.log(`cluster ${cluster.worker.id} responding to request`);
        
        con = connect_to_database()
        con.connect((err)=>{
            if (err) throw err;
            console.log(`Cluster ${cluster.worker.id} connected to database`)
            sql = 'SELECT * FROM `main`';
            con.query(sql, (err, result) => {
                if (err) throw err;
                
                res.send(result)
            })
        })
    })

    app.get('/get_inactive_school', (req, res) => {
        console.log(`cluster ${cluster.worker.id} responding to request`);
        
        con = connect_to_database()
        con.connect((err)=>{
            if (err) throw err;
            console.log(`Cluster ${cluster.worker.id} connected to database`)
            sql = 'SELECT * FROM `main` WHERE `main`.`isActive` = 0 LIMIT 1';
            con.query(sql, (err, result) => {
                if (err) throw err;
                
                res.send(result)
            })
        })
    })

    app.get('/activate_school/:id', (req, res) =>{
        const id = req.params.id 

        con = connect_to_database()
        con.connect((err) => {
            if (err) throw err;
            sql = "UPDATE `main` SET `main`.`isActive` = 1 WHERE `main`.`id` = "+id
            con.query(sql, (err, result) => {
                if (err) throw err;
                res.send(result)
            })
        })
    })

    app.listen(port)
    console.log(`New cluster (${cluster.worker.id}) fork app is listening on port ${port}`)
}
