
import os
class DataBase:
    def __init__(self, dataBasePath : str ) -> list[str]:
        
        self.dataBasePath = dataBasePath
        self.all_dir_imgs_paths = [dataBasePath+'/' + x for x in os.listdir(dataBasePath) ]
     
        
    def db_index_path(self, index: int)-> str: 
        """
            
        """
        
        return self.all_dir_imgs_paths[index]

if __name__ == '__main__':
   db =  DataBase('./Data-Base')
   print(db)
