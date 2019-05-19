import glob
import os
from detection import Pola
from PIL import Image

path = os.path.join("..", "data", "matematika", "pola 1", "vr")

for pdf in glob.glob("../pdfs/matematika/pola 1/vr/*.pdf")[16:]:
	print("\nFilename:", os.path.basename(pdf))

	print("Genreating images...")
	pola = Pola(pdf)

	print("Genreating individual exercises...")
	pola.generate_exercises(skip=2)

	file_path = os.path.join(path, os.path.splitext(os.path.basename(pdf))[0])
	print("Saving to:", file_path)
	pola.save(file_path)
