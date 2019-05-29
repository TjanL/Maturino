import cherrypy
import MySQLdb
import os
import glob
import json
from random import choice
from PIL import Image
from io import BytesIO


class Root(object):
	def __init__(self, html_dir):
		# Preload html files to RAM
		self.html_dir = html_dir
		self.html_files = {}
		for file in glob.glob(os.path.join(self.html_dir, "*.html")):
			self.html_files[os.path.basename(file)] = open(file, encoding="utf8").read()

	def error_page(status, message, traceback, version):
		return status

	@cherrypy.expose
	def index(self, *vpath, **params):
		return self.html_files["index.html"]

	@cherrypy.expose
	def about(self, *vpath, **params):
		return self.html_files["about.html"]


class Api(object):
	def __init__(self):
		self.db = Database()

	def error_page(status, message, traceback, version):
		return status

	@cherrypy.expose
	@cherrypy.tools.allow(methods=["GET"])
	@cherrypy.tools.accept(media='text/plain')
	def naloga(self, **params):
		cherrypy.response.headers['Content-Type'] = "application/json"
		if params:
			subject = params.get("subject", "%")
			pola = params.get("pola", "%")
			level = params.get("level", "%")
			year = params.get("year", "%")
			term = params.get("term", "%")
			return json.dumps(self.db.get_rendom_exercise(subject, pola, level, year, term), ensure_ascii=False).encode("utf-8")
		return str([]).encode("utf-8")

	@cherrypy.expose
	@cherrypy.tools.allow(methods=["GET"])
	@cherrypy.tools.accept(media='text/plain')
	def image(self, **params):
		if params:
			img_id = params.get("i")
			if img_id:
				path = self.db.get_img_path(img_id)
				if path:
					bytes_io = BytesIO()
					img = Image.open(path)
					img.save(bytes_io, 'PNG')

					cherrypy.response.headers['Content-Type'] = "image/png"
					return bytes_io.getvalue()
		return None


class Database(object):
	def connect(self, user="admin"):
		db = MySQLdb.connect(host="127.0.0.1", user=user, db="matura_naloge", charset="utf8")
		cursor = db.cursor()
		return db, cursor

	def get_exercises(self, subject, pola, level, year, term):
		db, cursor = self.connect()

		stmt = 'SELECT p.Naziv as predmet, n.Pola as pola, n.Nivo as raven, YEAR(n.Date) as leto, n.Rok as rok, d.UUID as dodatno, n.UUID as img, r.Url as rešitve FROM Naloga n, Rešitve r, Dodatno d, Predmet p WHERE n.Predmet=p.ID AND n.Dodatno=d.ID and n.Rešitve=r.ID and p.naziv=%s AND n.Pola LIKE %s AND n.nivo LIKE %s AND YEAR(n.Date) LIKE %s AND n.Rok LIKE %s'

		cursor.execute(stmt, [subject, level, year, term])
		db.close()

		columns = [col[0] for col in cursor.description]
		return [dict(zip(columns, row)) for row in cursor.fetchall()]

	def get_rendom_exercise(self, subject, pola, level, year, term):
		return choice(self.get_exercises(subject, pola, level, year, term))

	def get_img_path(self, img_id):
		db, cursor = self.connect()

		stmt = 'SELECT CONCAT(p.Path, t.Path) as Path FROM Predmet p, (SELECT n.Predmet, n.Path, n.UUID FROM Naloga n UNION SELECT d.Predmet, d.Path, d.UUID FROM Dodatno d) as t WHERE p.ID = t.Predmet and t.UUID = %s'

		cursor.execute(stmt, [img_id])
		db.close()

		row = cursor.fetchone()[0]
		return row


if __name__ == '__main__':
	api_conf = {
		'/': {
			'error_page.default': Api.error_page
		}
	}

	root_conf = {
	   '/': {
			'tools.sessions.on': True,
			'error_page.default': Root.error_page
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
