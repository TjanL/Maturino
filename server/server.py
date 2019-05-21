import cherrypy
import MySQLdb
import os
import glob
import json
from random import choice


class Root(object):
	def __init__(self, html_dir):
		# Preload html files to RAM
		self.html_dir = html_dir
		self.html_files = {}
		for file in glob.glob(os.path.join(self.html_dir, "*.html")):
			self.html_files[os.path.basename(file)] = open(file, encoding="utf8").read()

	@cherrypy.expose
	def index(self):
		return self.html_files["index.html"]


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
			return json.dumps(self.db.get_rendom_exercise(subject, level, year, term), ensure_ascii=False).encode("utf-8")
		return []

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
	api_conf = {
		'/': {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
		}
	}

	root_conf = {
	   '/': {
			'tools.sessions.on': True,
		},
		'/assets': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': os.path.abspath('../website/assets')
		}
	}

	cherrypy.tree.mount(Api(), '/api', api_conf)
	cherrypy.tree.mount(Root("../website"), '/', root_conf)
	cherrypy.server.socket_host = "127.0.0.1"
	cherrypy.engine.start()
