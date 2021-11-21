from face import Face
from google.cloud import vision
import os
from draw import Draw

class Respond:
    def __init__(self, img_path: list[str]):
        self.result_path = []
        self._img_path = img_path
        self._process()

        pass

    def _process(self):
        d = Draw()
        for img_path in self._img_path:
            if os.path.isfile(img_path):
                client = vision.ImageAnnotatorClient()
                with open(img_path, 'rb') as image_file:
                    content = image_file.read()
                image = vision.Image(content=content)
                response = client.face_detection(image=image)
                faces = response.face_annotations
                if len(faces) == 0:
                    raise ValueError('No face dected')
                face = Face(faces[0])
                _, filename =  d.draw_face(face, save=True,path = os.environ['IMAGE_FOLDER'] + '\\output\\')
                self.result_path.append(filename)
            else:
                raise ValueError(f'File ({img_path}) not found')
    def get_face(self):
        '''
        return a list of Face objects
        '''
        return self.face
    
    def __str__(self) -> str:
        pass

if __name__ == "__main__":
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\Users\\maich\\OneDrive\\University\\Hackathon\\Hack Western 8\\Backend\\western-hack-166656e05f61.json'
    imgs = ['sample1.jpg']
    r = Respond(imgs)
    print(r.result_path)