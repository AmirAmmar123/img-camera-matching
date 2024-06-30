
import os
class DataBase:
    """
    Initializes the database with the specified database path.

    Args:
        dataBasePath: The path to the database.

    Returns:
        A list of all directory paths containing training images within the database.
    """

    def __init__(self, dataBasePath : str ) -> list[str]:
        
        self.dataBasePath = dataBasePath
        self.all_dir_imgs_paths = [
            f'{dataBasePath}/{x}/training/' for x in os.listdir(dataBasePath)
        ]
     
        
    def imgDirIndexPath(self, index: int)-> str: 
        """
        Returns the image directory path at the specified index.

        Args:
            index: The index of the image directory path to retrieve.

        Returns:
            The image directory path at the specified index.
        """

        return self.all_dir_imgs_paths[index]

if __name__ == '__main__':
   db =  DataBase('./Data-Base')
   print(db)
