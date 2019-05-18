import os
import pytesseract
from PIL import Image
from pytesseract import Output
from pdf2image import convert_from_path


class Letter(object):
	def __init__(self, letter, x1, y1, x2, y2):
		self.letter = letter
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2

class Naloga(object):
	def __init__(self, st, img):
		self.st = st
		self.img = img

class Pola(object):
	def __init__(self, path):
		self.imgs = convert_from_path(path)
		self.naloge = []

	def generate_exercises(self):
		for img in self.imgs:
			self.naloge.extend(self._get_exercises(img))

	def save(self, path):
		if not os.path.isdir(path):
			os.makedirs(path)
		for naloga in self.naloge:
			naloga.img.save(os.path.join(path, naloga.st.strip(".") + ".png"), "PNG")

	def _get_right_coords(self, img, params):
		tmp = []
		size = img.size
		img_search = img.crop(params)
		tes_data = pytesseract.image_to_data(img_search, config="--psm 6", lang="slv", output_type=Output.DICT)

		whitelist = ["točke)", "točki)", "točk)", "točka)", "tocke)", "tocki)", "tock)", "tocka)"]
		for i in range(len(tes_data["level"])):
			if tes_data["text"][i] in whitelist:
				tmp.append(
					Letter(
						tes_data["text"][i],
						tes_data['left'][i] + params[0],
						tes_data['top'][i] + params[1],
						tes_data['left'][i] + tes_data['width'][i] + params[0],
						tes_data['top'][i] + tes_data['height'][i] + params[1]
						)
					)
		return tmp

	def _get_left_coords(self, img, params):
		tmp = []
		size = img.size
		img_search = img.crop(params)
		tes_data = pytesseract.image_to_data(img_search, config="--psm 6", lang="slv", output_type=Output.DICT)

		for i in range(len(tes_data["level"])):
			if "." in tes_data["text"][i] or "," in tes_data["text"][i]:
				tmp.append(
					Letter(
						tes_data["text"][i],
						tes_data['left'][i] + params[0],
						tes_data['top'][i] + params[1],
						tes_data['left'][i] + tes_data['width'][i] + params[0],
						tes_data['top'][i] + tes_data['height'][i] + params[1]
						)
					)
		return tmp

	def _get_exercises(self, img, padding=20):
		size = img.size

		params_left = (185,180,245,size[1])
		top_left = self._get_left_coords(img, params_left)

		params_right = (size[0]-310,180,size[0]-190,size[1])
		bottom_right = self._get_right_coords(img, params_right)

		tmp = []
		for i in range(min(len(top_left), len(bottom_right))):
			tmp.append(
				Naloga(
					top_left[i].letter,
					img.crop(
						(
							top_left[i].x1-padding,
							top_left[i].y1-padding,
							bottom_right[i].x2+padding,
							bottom_right[i].y2+padding)
						)
					)
				)

		return tmp


if __name__ == '__main__':
	pola = Pola("M062-401-1-1.pdf")
	pola.generate_exercises()
	pola.save("test1")
