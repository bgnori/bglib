import os
import Image

for filename in os.listdir('.'):
  if filename.endswith("cut.jpg"):
    savename = filename[:-8]+'.jpg'
    i = Image.open(filename)
    if filename.startswith('bar'):
      j = i.resize((25, 88), resample=1)
    else:
      j = i.resize((19, 88), resample=1)
    f = file(savename, 'w+b')
    j.save(f)



    
  






