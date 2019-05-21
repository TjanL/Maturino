import cherrypy
import MySQLdb
from random import choice


@cherrypy.expose
class Api(object):
	def __init__(self):
		self.db = Database()

	@cherrypy.tools.accept(media='text/plain')
	def GET(self, *vpath, **params):
		if params:
			subject = params.get("subject", "%")
			level = params.get("level", "%")
			year = params.get("year", "%")
			term = params.get("term", "%")
			return str(self.db.get_rendom_exercise(subject, level, year, term))

		return str([i for i in vpath])

class Database(object):
	def connect(self, user="admin"):
		db = MySQLdb.connect(host="127.0.0.1", user=user, db="matura_naloge", charset="utf8")
		cursor = db.cursor()
		return db, cursor

	def get_exercises(self, subject, level, year, term):
		db, cursor = self.connect()

		stmt = 'SELECT p.Naziv, n.Dodatno, CONCAT(p.Path, n.Path) as Path, n.Rešitve, n.Matura FROM Naloga n, Predmet p WHERE n.Predmet=p.ID AND p.naziv=%s AND n.nivo LIKE %s AND YEAR(n.Date) LIKE %s AND n.Rok LIKE %s'

		cursor.execute(stmt, [subject, level, year, term])
		db.close()

		columns = [col[0] for col in cursor.description]
		return [dict(zip(columns, row)) for row in cursor.fetchall()]

	def get_rendom_exercise(self, subject, level, year, term):
		return choice(self.get_exercises(subject, level, year, term))



if __name__ == '__main__':
	conf = {
		'/': {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			'tools.sessions.on': True,
			'tools.response_headers.on': True,
			'tools.response_headers.headers': [('Content-Type', 'text/plain'), ('charset', 'utf-8')],
		}
	}
	cherrypy.quickstart(Api(), '/', conf)
