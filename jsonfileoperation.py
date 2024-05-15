import json
import os.path

class JSONFileOperation():
    
    file_name:str
    file_path:str
    __data:any
    
    
    def __init__( self, file_name ) -> None  :
        
        self.file_name = file_name
        self.file_path = self.file_name + '.json'
        
    def get_data(self):
        return self.data
        
    def is_exist(self)-> bool:     
        if os.path.exists( self.file_path ):
            return True
        
        return False
    
    def read(self):
        with open( self.file_path , 'r') as fh:
            self.data = json.loads( fh.read() )
    
    def get(self,*args) -> list:
        
        values = []
        keys = args if len(args) > 0 else self.data.keys()
  
        for key in keys:
    
            if key in self.data:
                values.append(self.data[key])
                continue
            
            values.append(None)
        
        return values
  
    def write(self,data):
        
        with open( self.file_path , 'w') as fh:
            json.dump(data,fh)
        
            
            