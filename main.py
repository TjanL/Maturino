import glob
import os
from detection import Pola
from PIL import Image


for pdf in glob.glob("*.pdf"):
	print("\nFilename:", pdf)

	print("Genreating imgs...")
	pola = Pola(pdf)

	print("Genreating individual exercises...")
	pola.generate_exercises()

	print("Saving to:", os.path.splitext(pdf)[0])
	pola.save(os.path.splitext(pdf)[0])

