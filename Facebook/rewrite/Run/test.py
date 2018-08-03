import zipfile

z = zipfile.ZipFile('new_fb.zip', mode='w')
z.write('new_fb.html')