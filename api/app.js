var express = require('express')
var cluster = require('cluster')
var app = express()

app.use(express.json())

const port = 8080

if (cluster.isMaster){
    console.log('Cluster master is starting...')
    var cpuCount = require('os').cpus().length
    
    for(let i = 0; i < cpuCount-2; i++){
        cluster.fork()
    }

    cluster.on('exit', (worker)=>{
        console.log(`Worker ${worker.id} died...\nCreating new worker...`)
   
        cluster.fork()
    })    

} else {

    function connect_to_database(){
        var mysql = require('mysql')

        var con = mysql.createConnection({
            database: 'schools',
            host: 'localhost',
            user: 'root',
            password: ''
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
        con = connect_to_database()
        con.connect((err)=>{
            if (err) throw err;
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

    //Получает все муниципалитеты 
    app.get('/get_all_mo', (req, res) => {
        con = connect_to_database()
        con.connect((err)=>{
            if (err) throw err;
            sql = "SELECT DISTINCT(mo) AS 'mo' FROM `main`"
            con.query(sql, (err, result) => {
                if (err) throw err;
                res.send(result)
            })
        })
    })


    //Получает все школы данного муниципалитета 
    app.get('/get_mo_schools', (req, res) => {
        if (!req.body.mo){
            res.status(400).send({err: "'mo' field is required"})
        }

        con = connect_to_database()
        con.connect((err) => {
            if (err) throw err;
            mo = req.body.mo
            sql = "SELECT id, name_full, name_short, type FROM `main` WHERE mo = '"+mo+"'"
            con.query(sql, (err, result) =>{
                if (err) throw err;
                res.status(200).send(result)
            })
        })  
    })

    app.get('/:school_id/classes', (req, res) => {
        const school_id = req.params.school_id
        con = connect_to_database()

        con.connect((err) => {
            if (err) throw err;
            sql = "SELECT * FROM `classes` WHERE `classes`.`sid` = '"+school_id+"'"

            con.query(sql, (err, result) => {
                if (err) throw err;
                res.status(200).send(result)
            })
        })
    })


    app.get('/:school_id/:class_id/students', (req, res) => {
        const school_id = req.params.school_id
        const class_id  = req.params.class_id
        con = connect_to_database()

        con.connect((err) => {
            if (err) throw err;
            sql = "SELECT * FROM `students` WHERE `students`.`sid` = '"+school_id+"' AND `students`.`cid`='"+class_id+"' " 

            con.query(sql, (err, result) => {
                if (err) throw err;
                res.status(200).send(result)
            })
        })
    })


    app.post('/:school_id/:class_id/:student_id/auth') 

    //Последующие три требуют токена аунтефикации для действий 
    app.post('/:school_id/:class_id/:student_id/logout')
    app.post('/:school_id/:class_id/:student_id/get_avaliable_tests')
	app.post('/:school_id/:class_id/:student_id/start_test/:test_id')
    app.post('/:school_id/:class_id/:student_id/end_test/')
    

    app.listen(port)
    console.log(`New cluster fork (${cluster.worker.id}) is listening on port ${port}`)
}