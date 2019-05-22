import os
import glob
import MySQLdb
import uuid


os.chdir("../data/slovenscina/")

resitve = ["https://www.ric.si/mma/M181-103-1-4/2018101013572982/",
"https://www.ric.si/mma/M182-103-1-4/2019041007453826/",
"https://www.ric.si/mma/M171-103-1-4/2017101014404852/",
"https://www.ric.si/mma/M172-103-1-4/2018040610444205/",
"https://www.ric.si/mma/M161-103-1-4/2016101211573430/",
"https://www.ric.si/mma/M162-103-1-4/2017040714241858/",
"https://www.ric.si/mma/M151-103-1-4/2015101412442268/",
"https://www.ric.si/mma/M152-103-1-4/2016041509441383/",
"https://www.ric.si/mma/M141-103-1-4/2014100714435093/",
"https://www.ric.si/mma/M142-103-1-4/2015100813171131/",
"https://www.ric.si/mma/M131-103-1-4/2013100914382712/",
"https://www.ric.si/mma/M132-103-1-4/2014100714370493/",
"https://www.ric.si/mma/M121-103-1-4/2012101112422018/",
"https://www.ric.si/mma/M122-103-1-4/2013100914325476/",
"https://www.ric.si/mma/M111-101-1-4/2011101323421198/",
"https://www.ric.si/mma/M112-103-1-4/2012101112381837/",
"https://www.ric.si/mma/M101-103-1-4/2010101114004496/",
"https://www.ric.si/mma/M102-103-1-4/2011101313145350/",
"https://www.ric.si/mma/M091-103-1-4/2009101211024383/",
"https://www.ric.si/mma/M092-103-1-4/2010100109151452/",
"https://www.ric.si/mma/M081-103-1-4/2008102013530900/",
"https://www.ric.si/mma/M082-103-1-4/2009101509275887/",
"https://www.ric.si/mma/M071-103-1-4/2007110814243485/",
"https://www.ric.si/mma/M072-103-1-4/2008100608444604/",
"https://www.ric.si/mma/M061-103-1-4/2006061309154122/",
"https://www.ric.si/mma/M062-103-1-4/2007110614000954/",
"https://www.ric.si/mma/M051-103-1-4/2007102915011809/",
"https://www.ric.si/mma/M052-103-1-4/2007110509472543/",
"https://www.ric.si/mma/M041-103-1-6/2011013113094112/",
"https://www.ric.si/mma/M042-103-1-6/2011021812375823/"]

db = MySQLdb.connect(host="127.0.0.1", user="admin", db="matura_naloge", charset="utf8")
cursor = db.cursor()

for matura in glob.glob("pola 2/vr/pomlad/*/[!dodatno]*"):
	path = os.path.split(matura)[0]

	img_path = matura
	matura_name = os.path.split(path)[-1][:8]
	nivo = matura.split("/")[1]
	rok = matura.split("/")[2]
	date = "20" + matura_name[1:3] + "-1-1"

	print(img_path, date, matura_name, nivo, rok)
	stmt = 'INSERT INTO Naloga (Predmet, Dodatno, Path, Rešitve, Date, Matura, Nivo, Rok, UUID) VALUES  (1, (SELECT d.ID from Dodatno d where d.Matura = %s), %s, (SELECT r.ID from Rešitve r where r.Matura = %s), %s, %s, %s, %s, %s)'

	cursor.execute(stmt, [matura_name, img_path, matura_name, date, matura_name, nivo, rok, uuid.uuid4()])
	db.commit()

"""
for url in resitve:
	matura = url.split("/")[-3][:8]
	print(url, matura)

	stmt = 'INSERT INTO Rešitve (Url, Matura) VALUES  (%s, %s)'

	cursor.execute(stmt, [url, matura])
	db.commit()
"""


db.close()
