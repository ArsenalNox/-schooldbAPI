var express = require('express')
var cors    = require('cors')
var cluster = require('cluster')
var app = express()

app.use(express.json())
app.use(cors())
app.options('*', cors())


const port = 8080

if (cluster.isMaster){
    //Инициализация всей движухи
    var cpuCount = require('os').cpus().length

    console.log('Cluster master is starting.\nCore count: '+cpuCount)
    
    for(let i = 0; i < cpuCount; i++){ //Создание потоков 
        cluster.fork()
    }

    cluster.on('exit', (worker)=>{
        console.log(`Worker ${worker.id} died...\nCreating new worker...`)
   
        cluster.fork()
    })    

} else {

    function shuffleArray(array) { //Нагло украл 
        let curId = array.length;
        // There remain elements to shuffle
        while (0 !== curId) {
            // Pick a remaining element
            let randId = Math.floor(Math.random() * curId);
            curId -= 1;
            // Swap it with the current element.
            let tmp = array[curId];
            array[curId] = array[randId];
            array[randId] = tmp;
        }
        return array;
    } 

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
    
    function random_number(a, b){
        return Math.round(Math.random()*(b-a)+a)
    }
    
    async function check_if_token_expired(token){
        var con = connect_to_database()
        con.connect((err) => {
            if (err) {
                throw err
            }
                
            sql = "SELECT * FROM students WHERE token = ? LIMIT 1"
            result = con.query(sql, [token], (err, result) => {
                if (err) {
                    throw err
                }
                if (result.length == 0){
                    console.log('Faied to find user')
                    result = true 
                    return 
                }

                exipre_date_sql = result[0].expires 
                var edt = exipre_date_sql
                expire_date_js = new Date(edt)
                console.log('test')
                console.log(edt)
                console.log(expire_date_js)
                let d = new Date()
                let date_now = new Date(
                    d.getFullYear(),
                    d.getMonth(),
                    d.getDay(),
                    d.getHours(),
                    d.getSeconds(),
                    d.getMilliseconds
                )
                console.log(date_now.toString() < expire_date_js.toString())
                console.log(date_now.toString() > expire_date_js.toString())
                if (date_now.toString() < expire_date_js.toString()){
                    console.log('token is not expired')
                    result = false
                } else {
                    result = true
                }

                return result
            })
            return result
        })
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
            sql = "SELECT * FROM `munipals`"
            con.query(sql, (err, result) => {
                if (err) throw err;
                res.send(result)
            })
        })
    })


    //Получает все школы данного муниципалитета 
    app.get('/get_mo_schools/:mo_id', (req, res) => {

        con = connect_to_database()
        con.connect((err) => {
            if (err) throw err;
            mo = req.params.mo_id
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

    //Аунтефикация ученика 
    app.get('/:school_id/:class_id/:student_id/auth', (req, res) => {
        const school_id  = req.params.school_id
        const class_id   = req.params.class_id
        const student_id = req.params.student_id

        con = connect_to_database()
        con.connect((err) => {
            if (err) throw err;
            sql = "SELECT * FROM students WHERE sid = ? AND cid = ? AND id = ?"
            
            con.query(sql, [school_id, class_id, student_id], (err, result) => {
                if (err) throw err;
                if (result.token == null && result.expires == null){
                    console.log('User has not logged in')
                } else {
                    console.log('User is already logged in, resetting token')
                }
                
                let d = new Date()
                let expiration_date = new Date(
                    d.getFullYear(),
                    d.getMonth(),
                    d.getDay(),
                    (d.getHours()+12),
                    d.getSeconds(),
                    d.getMilliseconds()
                )
                let mySqlTimestamp = expiration_date.toISOString().slice(0, 19).replace('T', ' ')
                let newAccessToken = 
                    + Math.random().toString(36).substr(2, 20) 
                    + Math.random().toString(36).substr(2, 20)
                
                console.log(expiration_date, mySqlTimestamp, newAccessToken)

                sql = "UPDATE students SET token = ?, expires = ? WHERE sid = ? AND cid = ? AND id = ?"
                con.query(sql, [newAccessToken, mySqlTimestamp, school_id, class_id, student_id], (err, result) => {
                    if (err) {
                        res.status(500).send({error: "Неудалось выполнить вход"})
                        throw err
                    } 
                    
                    res.status(200).send({token: newAccessToken, exp_date: expiration_date})
                })  

            })
        })
    }) 


    //Последующие три требуют токена аунтефикации для действий 
    app.post('/:school_id/:class_id/:student_id/logout', (req, res) => {
        if (!req.body.token) {
            res.status(403).send({error: "Необходимо поле token"})
            return
        }

        const token      = req.body.token
        const school_id  = req.params.school_id
        const class_id   = req.params.class_id
        const student_id = req.params.student_id
        
        console.log(`User ${student_id} attempts logout`)
       
        con = connect_to_database()
        con.connect((err) => {
            if (err) throw err;

            //Проверяем есть ли этот токен 
            sql = "SELECT * FROM `students` WHERE token=? LIMIT 1"
            con.query(sql, [token], (err, result) => {
                if (err) throw err;
                
                if (result.length == 0) {
                    res.status(301).send({message: "nothing found"})
                    return 
                } 

                sql = "UPDATE students SET token = null, expires = null WHERE id = ? AND token = ? "
                con.query(sql, [student_id, token], (err, result) => {
                    if (err) {
                        res.status(500).send({error: "error"})
                        return 
                    }

                    if (result){
                        res.status(200).send({success: true})
                        return 
                    }
                })
            })
        })
    })


    app.post('/:school_id/:class_id/:student_id/get_avaliable_tests', (req, res) => {
        if (!req.body.token) {
                res.status(403).send({error: "Необходимо поле token"})
                return
            }

        const token      = req.body.token
        const school_id  = req.params.school_id
        const class_id   = req.params.class_id
        const student_id = req.params.student_id
     
        con = connect_to_database()
        con.connect((err) => {
            if (err) throw err;
            sql = "SELECT * FROM students WHERE id = ? AND token = ? LIMIT 1"
            con.query(sql, [student_id, token], (err, result) => {
                if (err) throw err;

                if (result.len == 0) { 
                    res.status(403).send({error: "user is not authorised"})
                    return 
                }
                
                sql = "SELECT * FROM classes WHERE id = ? LIMIT 1"
                con.query(sql, [class_id], (err, result) => {
                    if (err) throw err;
                    if (result.length == 0){
                        res.status(500).send({error: "class not found"})
                        return 
                    }

                    student_class_year = result[0].year
                    sql = "SELECT modules.*, subjects.name as 'sbj' FROM modules LEFT JOIN subjects ON modules.subject=subjects.id WHERE isActive = 1 AND targeted_class = ?"
                    console.log(`Selecting modules for student ${student_id} in class ${class_id} year ${student_class_year}`)
                    con.query(sql, [student_class_year], (err, result) => { 
                        if (err) throw err;
                        res.status(200).send(result)
                    })
                })
            })
        })
    })      

    app.post('/:school_id/:class_id/:student_id/start_test/:test_id', (req, res) => {
        if (!req.body.token) {
            res.status(403).send({error:'Необходимо поле token'})
            return 
        }
 
        const token      = req.body.token
        const school_id  = req.params.school_id
        const class_id   = req.params.class_id
        const student_id = req.params.student_id
        const test_id    = req.params.test_id

        con = connect_to_database()
        con.connect((err) => {
            if (err) throw err;
            sql = "SELECT modules.*, subjects.name as 'sbj' FROM modules LEFT JOIN subjects ON modules.subject=subjects.id WHERE modules.id = ?"
            con.query(sql, [test_id], (err, result) => {
                if (err) throw err;
                if(result.length == 0){
                    res.status(500).send({error:"Could not find module"})
                }
                module = result[0]
                sql = "SELECT * FROM modules_questions WHERE mid = ? ORDER BY q_num ASC"
                con.query(sql, [test_id], (err, result) => {
                    if (err) throw err;
                    if (result.length == 0){
                        res.send(500).send({error: "Could not find questions"})
                        return 
                    }
                    
                    num_questions = 0
                    //К каждому вопросу создать объкт, содержащий варианты данного вопроса 
                    current_qustion = 1
                    questions = []
                    tmp_questions = []

                    /*
                     *  Составляем массив сгруппированных по вариантам вопросов 
                     * */
                    for (question of result) { //Проходимся по все вопросам 
                        if (question.q_num > num_questions){
                            num_questions = question.q_num
                        }
                        if (current_qustion == question.q_num){
                            tmp_questions.push(question)
                        } else {
                            questions.push(tmp_questions)
                            tmp_questions = []
                            current_qustion = question.q_num
                            tmp_questions.push(question)
                        }
                    }
                    
                    finilized_questions = [] //подготовка финального массива для отправки
                    for (question of questions){
                        if (question.len == 1){ //Если у вопроса нет вариантов 
                            qtmp = question[0]
                        } else {
                            qtmp = question[random_number(0, question.length-1)] //выбор случайного варианта 
                        }

                        finilized_questions.push({ //Записываем
                            number:  qtmp.q_num,
                            variant: qtmp.q_variant,
                            text:    qtmp.q_text,
                            image:   qtmp.q_image,
                            answ1:   qtmp.answ1,
                            answ2:   qtmp.answ2,
                            answ3:   qtmp.answ3,
                            answ4:   qtmp.answ4
                        })
                    }

                    shuffled = shuffleArray(finilized_questions) //Перемешиваем 
                    res.status(200).send({header: module, questions: shuffled})
                })
            })
        })    
    })


    app.post('/:school_id/:class_id/:student_id/end_test/', (req, res) => {
        if (!req.body.header.student_token) {
            res.status(403).send({error:'Необходимо поле token'})
            return 
        }
        if (!req.body.header.module_id) {
            res.status(403).send({error:'Необходимо поле module_id'})
            return
        }

        const school_id  = req.params.school_id
        const class_id   = req.params.class_id
        const student_id = req.params.student_id
        const token      = req.body.header.student_token
        const test_id    = req.body.header.module_id
        const answeres   = req.body.arr

        con = connect_to_database()
        con.connect((err) => {
            if (err) throw err;

            sql = "SELECT modules.*, subjects.name as 'sbj' FROM modules LEFT JOIN subjects ON modules.subject=subjects.id WHERE modules.id = ?"
            con.query(sql, [test_id], (err, result) => {
                if (err) throw err;
                if (result.length == 0){
                    res.status(500).send({error:'could not find module'})
                    return
                }

                module_data = result[0]
                sql = "SELECT modules_questions.*, question_types.id as 'qtp', question_types.name as 'qtn' FROM modules_questions LEFT JOIN question_types ON modules_questions.q_type=question_types.id WHERE modules_questions.mid = ?"
                con.query(sql, [test_id], (err, result) => {
                    if (err) throw err;
                    test_uuid = 'UUID' 
                    + Math.random().toString(36).substr(2, 20) 
                    + Math.random().toString(36).substr(2, 20)
                        
                    results_to_write = []


                    for (answer of answeres){ //Итерируемся через все ответы 
                        var tmp = {}
                        tmp.test_uid = test_uuid
                        tmp.mid      = test_id
                        tmp.sid      = school_id
                        tmp.a_given  = answer.answers
                        answ_g = answer.answers

                        found = false 

                        //Ищем, какому вопросу принадлежит этот ответ 
                        for (question of result){
                            if(
                                (question.q_num == answer.number)
                                &&
                                (question.q_variant == answer.variant)
                            ){
                                found = true
                                console.log('нашел')
                                tmp.qid = question.id

                                if (question.correct_answ == 1){
                                    a_corr = question.answ1
                                } else if (question.correct_answ == 2){
                                    a_corr = question.answ2
                                } else if (question.correct_answ == 3){
                                    a_corr = question.answ3
                                } else if (question.correct_answ == 4){
                                    a_corr = question.answ4
                                } //ELSE??????

                                if (answ_g == a_corr){
                                    tmp.isCorrect = true 
                                } else {
                                    tmp.isCorrect = false
                                }
                                console.log(a_corr, answ_g)
                                    
                                results_to_write.push([
                                    tmp.test_uid,
                                    tmp.qid,
                                    tmp.a_given,
                                    tmp.isCorrect,
                                    tmp.mid,
                                    tmp.sid,
                                    student_id
                                ])
                            }
                        }

                        if (!found) {
                            console.log(`У ${student_id} НЕУДАЛОСЬ НАЙТИ ${answer.number}:${answer.variant}`)
                        }
                    }
                    console.log(results_to_write)
                    sql = "INSERT INTO results(test_uid, qid, a_given, isCorrect, mid, sid, student) VALUES ?"
                    con.query(sql, [results_to_write], (err, result) => {
                        if (err) throw err;
                        if (result) {
                            res.status(200).send({success: true})
                            return
                        } 

                        res.status(500).send({error: 'could not write results'})
                        return 
                    })
                })
            })
        })
        console.log(req.body)
    })
    

    app.listen(port)
    console.log(`New cluster fork (${cluster.worker.id}) is listening on port ${port}`)
}
