from core.errors.face_exceptions import *
import numpy as np

class FaceModel:
    def __init__(self):
        self.encoding = []
        self.location = []
    
    def _encoding_string(encoding: list):
        try:
            process = ",".join(str(x) for x in encoding)
            return process
        
        except (Exception, ValueError) as e:
            raise FaceEncodingError(e)
        
    def _encoding_array(encoding: str):
        try:
            process = np.array([float(x) for x in encoding.split(',')])
            return process
        
        except (Exception, ValueError) as e:
            raise FaceEncodingError(e)
        
    def to_model(self, encoding: list, location: list):
        try:
            if not encoding:
               raise FaceEncodingError("encoding Vazio")
            
            if not location:
                raise FaceLocationError("location Vazio")
            
            new_model = FaceModel()
            new_model.encoding = encoding
            new_model.location = location

            return new_model
        
        except Exception as e:
           raise FaceModelError(e)
    
    def to_map(self, model: 'FaceModel'):
        try:
            return {
                "encoding": self._encoding_string(model.encoding),
                "location": model.location
            }
        except Exception as e:
            raise FaceModelError(e)
               