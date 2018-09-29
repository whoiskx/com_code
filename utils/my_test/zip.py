

import zipfile

zip_file = zipfile.ZipFile('file_name.zip', 'w')
zip_file.write('/tmp/hello.txt')
zip_file.close()