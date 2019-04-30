from zipfile import ZipFile 
import os 
  
def zipFiles(files, dir, file_name): 
    file_dir = os.path.join(dir, file_name)

    with ZipFile(file_dir,'w') as zip: 
        # writing each file one by one 
        for file in files: 
            zip.write(file)