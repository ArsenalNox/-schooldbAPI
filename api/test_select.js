async function main(){
	const mysql = require('mysql2/promise')

	var con = await mysql.createConnection({
		database: 'schools',
		host:     '192.168.145.114',
		user:     'vlad',
		password: 'P@ssw0rd'
	})

	sql = "SELECT * FROM classes"

	var [result] = await con.execute(sql) 
	
	for(row_class of result){
		sql = `SELECT * FROM students WHERE cid = '${row_class['id']}'`
		const [rows] = await con.execute(sql)
		if (rows.length == 0){
			sql = `DELETE FROM classes WHERE id = ${row_class['id']}`
			const d_res = await con.execute(sql)
		}
	}
	console.log('Done')
	return 
}

main()
