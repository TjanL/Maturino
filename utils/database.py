import os
import glob
import MySQLdb
import uuid


os.chdir("../data/matematika/")

resitve = ["https://www.ric.si/mma/M181-401-1-3/2018101013584331/",
"https://www.ric.si/mma/M182-401-1-3/2019041007463886/",
"https://www.ric.si/mma/M171-401-1-3/2017101014420056/",
"https://www.ric.si/mma/M172-401-1-3/2018040610455028/",
"https://www.ric.si/mma/M161-401-1-3/2016101211585831/",
"https://www.ric.si/mma/M162-401-1-3/2017040714252260/",
"https://www.ric.si/mma/M151-401-1-3/2015101412562730/",
"https://www.ric.si/mma/M152-401-1-3/2016041509451173/",
"https://www.ric.si/mma/M141-401-1-3/2014100714450191/",
"https://www.ric.si/mma/M142-401-1-3/2015100813182768/",
"https://www.ric.si/mma/M131-401-1-3/2013100914393879/",
"https://www.ric.si/mma/M132-401-1-3/2014100714381052/",
"https://www.ric.si/mma/M121-401-1-3/2012101507434059/",
"https://www.ric.si/mma/M122-401-1-3/2013100914335307/",
"https://www.ric.si/mma/M111-401-1-3/2011101400254649/",
"https://www.ric.si/mma/M112-401-1-3/2012101507514353/",
"https://www.ric.si/mma/M101-401-1-3/2010101313144501/",
"https://www.ric.si/mma/M102-401-1-3/2011101314102676/",
"https://www.ric.si/mma/M091-401-1-3/2009101211565384/",
"https://www.ric.si/mma/M092-401-1-3/2010100113562635/",
"https://www.ric.si/mma/M081-401-1-3/2008102208493007/",
"https://www.ric.si/mma/M082-401-1-3/2009101509575750/",
"https://www.ric.si/mma/M071-401-1-3/2007110907231563/",
"https://www.ric.si/mma/M072-401-1-3/2008100910014749/",
"https://www.ric.si/mma/M061-401-1-3/2006061313464373/",
"https://www.ric.si/mma/M062-401-1-3/2007110812331847/",
"https://www.ric.si/mma/M051-401-1-3/2007110507495450/",
"https://www.ric.si/mma/M052-401-1-3/2007110913592366/",
"https://www.ric.si/mma/M041-401-1-3/2011020210263155/",
"https://www.ric.si/mma/M041-402-1-4/2011020210273187/",
"https://www.ric.si/mma/M042-401-1-3/2011021813354385/",
"https://www.ric.si/mma/M042-402-1-4/2011021813363398/"]

db = MySQLdb.connect(host="127.0.0.1", user="admin", db="matura_naloge", charset="utf8")
cursor = db.cursor()

"""
for matura in glob.glob("pola 2/vr/jesen/*/dodatno*"):
	path = os.path.split(matura)[0]

	img_path = matura
	matura_name = os.path.split(path)[-1][:8]

	print(img_path, matura_name)
	stmt = 'INSERT INTO Dodatno (Path, UUID, Matura, Predmet) VALUES  (%s, %s, %s, 2)'

	cursor.execute(stmt, [img_path, uuid.uuid4(), matura_name])
	db.commit()
"""
"""
for url in resitve:
	matura = url.split("/")[-3][:8]
	print(url, matura)

	stmt = 'INSERT INTO Rešitve (Url, Matura) VALUES  (%s, %s)'

	cursor.execute(stmt, [url, matura])
	db.commit()
"""
#"""
for matura in glob.glob("pola 2/vr/jesen/*/[!dodatno]*"):
	path = os.path.split(matura)[0]

	img_path = matura
	matura_name = os.path.split(path)[-1][:8]
	nivo = matura.split("/")[1]
	rok = matura.split("/")[2]
	date = "20" + matura_name[1:3] + "-1-1"

	print(img_path, date, matura_name, nivo, rok)
	stmt = 'INSERT INTO Naloga (Predmet, Dodatno, Path, Rešitve, Date, Matura, Nivo, Rok, UUID) VALUES  (2, (SELECT d.ID from Dodatno d where d.Matura = %s), %s, (SELECT r.ID from Rešitve r where r.Matura = %s), %s, %s, %s, %s, %s)'

	cursor.execute(stmt, [matura_name, img_path, matura_name, date, matura_name, nivo, rok, uuid.uuid4()])
	db.commit()
#"""

db.close()
