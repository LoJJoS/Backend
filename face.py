from google.cloud.vision_v1.types.image_annotator import FaceAnnotation
from dataclasses import dataclass

@dataclass
class Eye:
    left: list[int]
    top: list[int]
    right: list[int]
    bottom: list[int]
    center: list[int]
    def __init__(self,data:list):
        self.left = data[0]
        self.top = data[1]
        self.right = data[2]
        self.bottom = data[3]
        self.center = data[4]

@dataclass
class Mouth:
    left: list[int]
    top: list[int]
    right: list[int]
    bottom: list[int]
    center: list[int]
    def __init__(self,data:list):
        self.left = data[0]
        self.top = data[1]
        self.right = data[2]
        self.bottom = data[3]
        self.center = data[4]

@dataclass
class EyeBrow:
    left: list[int]
    right: list[int]
    center: list[int]
    def __init__(self,data:list):
        self.left = data[0]
        self.right = data[1]
        self.center = data[2]

@dataclass
class Nose:
    tip: list[int]
    left: list[int]
    center: list[int]
    right: list[int]
    top: list[int]
    def __init__(self, data:list):
        self.tip = data[0]
        self.left = data[1]
        self.center = data[2]
        self.right = data[3]
        self.top = data[4]

class FaceException(Exception):
    def __init__(self, message=None):
        self.message = message

class Face:
    
    _LEFT_EYE = [
    'LEFT_EYE_LEFT_CORNER',
    'LEFT_EYE_TOP_BOUNDARY',
    'LEFT_EYE_RIGHT_CORNER',
    'LEFT_EYE_BOTTOM_BOUNDARY',
    'LEFT_EYE'
    ]
    _RIGHT_EYE = [
    'RIGHT_EYE_LEFT_CORNER',
    'RIGHT_EYE_TOP_BOUNDARY',
    'RIGHT_EYE_RIGHT_CORNER',
    'RIGHT_EYE_BOTTOM_BOUNDARY',
    'RIGHT_EYE'
    ]
    _MOUTH = [
    'MOUTH_LEFT',
    'UPPER_LIP',
    'MOUTH_RIGHT',
    'LOWER_LIP',
    'MOUTH_CENTER',


    ]
    _LEFT_EYE_BROW = [
    'LEFT_OF_LEFT_EYEBROW',
    'RIGHT_OF_LEFT_EYEBROW',
    'LEFT_EYEBROW_UPPER_MIDPOINT'
    ]
    _RIGHT_EYE_BROW = [
    'RIGHT_OF_RIGHT_EYEBROW',
    'LEFT_OF_RIGHT_EYEBROW',
    'RIGHT_EYEBROW_UPPER_MIDPOINT'
    ]
    _NOSE = [
        'NOSE_TIP',
        'NOSE_BOTTOM_LEFT',
        'NOSE_BOTTOM_CENTER',
        'NOSE_BOTTOM_RIGHT',
        'MIDPOINT_BETWEEN_EYES'
    ]
    _VALIDSET = {
        'left_eye':_LEFT_EYE,
        'right_eye':_RIGHT_EYE,
        'mouth':_MOUTH,
        'left_eye_brow':_LEFT_EYE_BROW,
        'right_eye_brow':_RIGHT_EYE_BROW,
        'nose':_NOSE
        }

    def __init__(self,data: FaceAnnotation = None):
        if data is None:
            self.__build_sample_face()
        else:
            # 
            self.bounding = []
            self.landmarks = {}
            self.emotions = {}

            self.__process_bounding(data.bounding_poly)
            self.__process_landmarks(data.landmarks)
            
            # TODO Emotions
        self.__valid()
        
        self.left_eye = Eye([self.landmarks[key] for key in self._LEFT_EYE])
        self.right_eye = Eye([self.landmarks[key] for key in self._RIGHT_EYE])
        self.mouth = Mouth([self.landmarks[key] for key in self._MOUTH])
        self.left_eye_brow = EyeBrow([self.landmarks[key] for key in self._LEFT_EYE_BROW])
        self.right_eye_brow = EyeBrow([self.landmarks[key] for key in self._RIGHT_EYE_BROW])
        self.nose = Nose([self.landmarks[key] for key in self._NOSE])
        
    def __valid(self):
        '''
        Check if the Face is valid
        '''
        if (len(self.bounding) != 4):
            raise Exception('Invalid bounding polygon')
        for key, value in self._VALIDSET.items():
            for v in value:
                if v not in self.landmarks:
                    raise FaceException(f'{key} missing feature')
        

    def __process_bounding(self, bounding):
        for loc in bounding.vertices:
            self.bounding.append((loc.x,loc.y))

    def __process_landmarks(self,landmarks: list[dict]):
        '''
        Convert the list of landmarks into a dictionary
        '''
        for landmark in landmarks:
            self.landmarks[landmark.type_.name] = (round(landmark.position.x),round(landmark.position.y))

    def __build_sample_face(self):
        self.landmarks = {'LEFT_EYE': (284.9124755859375, 1309.3321533203125, -0.0020694732666015625), 'RIGHT_EYE': (446.2580261230469, 1281.4495849609375, -8.306976318359375), 'LEFT_OF_LEFT_EYEBROW': (228.46725463867188, 1280.206787109375, 23.173765182495117), 'RIGHT_OF_LEFT_EYEBROW': (318.0321960449219, 1260.216064453125, -22.98845672607422), 'LEFT_OF_RIGHT_EYEBROW': (387.4114685058594, 1248.365966796875, -26.84813690185547), 'RIGHT_OF_RIGHT_EYEBROW': (485.5850524902344, 1241.4969482421875, 8.853046417236328), 'MIDPOINT_BETWEEN_EYES': (358.29803466796875, 1283.0272216796875, -32.59511947631836), 'NOSE_TIP': (369.9129638671875, 1365.04248046875, -91.79908752441406), 'UPPER_LIP': (380.7168273925781, 1424.639892578125, -68.7232894897461), 'LOWER_LIP': (385.7512512207031, 1476.9293212890625, -67.70095825195312), 'MOUTH_LEFT': (313.4258117675781, 1459.7589111328125, -27.971691131591797), 'MOUTH_RIGHT': (448.0027770996094, 1439.4422607421875, -36.33673095703125), 'MOUTH_CENTER': (384.2515563964844, 1447.4434814453125, -61.86162185668945), 'NOSE_BOTTOM_RIGHT': (419.12774658203125, 1374.964599609375, -41.57756805419922), 'NOSE_BOTTOM_LEFT': (332.0458984375, 1392.3614501953125, -37.739898681640625), 'NOSE_BOTTOM_CENTER': (375.672607421875, 1392.3155517578125, -63.31429672241211), 'LEFT_EYE_TOP_BOUNDARY': (281.5674133300781, 1295.160400390625, -5.71929931640625), 'LEFT_EYE_RIGHT_CORNER': (316.1492004394531, 1304.819580078125, -1.9501953125), 'LEFT_EYE_BOTTOM_BOUNDARY': (285.931640625, 1320.6292724609375, -3.634002685546875), 'LEFT_EYE_LEFT_CORNER': (252.79281616210938, 1317.3634033203125, 14.95335578918457), 'RIGHT_EYE_TOP_BOUNDARY': (443.45013427734375, 1266.238037109375, -13.708322525024414), 'RIGHT_EYE_RIGHT_CORNER': (477.5195007324219, 1279.8143310546875, 3.136659622192383), 'RIGHT_EYE_BOTTOM_BOUNDARY': (447.56414794921875, 1293.05810546875, -12.186840057373047), 'RIGHT_EYE_LEFT_CORNER': (412.027099609375, 1285.26416015625, -6.427745819091797), 'LEFT_EYEBROW_UPPER_MIDPOINT': (269.3301086425781, 1254.96240234375, -6.208339691162109), 'RIGHT_EYEBROW_UPPER_MIDPOINT': (433.83770751953125, 1229.5753173828125, -15.533979415893555), 'LEFT_EAR_TRAGION': (186.94569396972656, 1400.71484375, 177.44464111328125), 'RIGHT_EAR_TRAGION': (569.2662963867188, 1338.9342041015625, 159.49269104003906), 'FOREHEAD_GLABELLA': (351.24786376953125, 1249.5872802734375, -29.153038024902344), 'CHIN_GNATHION': (400.17645263671875, 1554.4091796875, -60.738643646240234), 'CHIN_LEFT_GONION': (242.75875854492188, 1516.1268310546875, 90.88097381591797), 'CHIN_RIGHT_GONION': (547.9943237304688, 1457.8026123046875, 76.58969116210938), 'LEFT_CHEEK_CENTER': (268.21826171875, 1412.8404541015625, -1.9492511749267578), 'RIGHT_CHEEK_CENTER': (488.372802734375, 1376.7060546875, -13.912138938903809)}
        for key, value in self.landmarks.items():
            self.landmarks[key] = (round(value[0]),round(value[1])) 
        self.emotions = {'joyLikelihood': 'VERY_LIKELY', 'sorrowLikelihood': 'VERY_LIKELY', 'angerLikelihood': 'VERY_LIKELY', 'surpriseLikelihood': 'VERY_LIKELY', 'underExposedLikelihood': 'VERY_LIKELY', 'blurredLikelihood': 'VERY_LIKELY', 'headwearLikelihood': 'VERY_LIKELY'}
        self.bounding = [(116, 1020), (635, 1020), (635, 1476), (116, 1476)]

    def get_bounding(self) -> list[tuple]:
        return self.bounding

    def get_left_eye(self)->Eye:
        return self.left_eye

    def get_right_eye(self)->Eye:
        return self.right_eye

    def get_mouth(self)->Mouth:
        return self.mouth
    
    def get_left_eye_brow(self)->EyeBrow:
        return self.left_eye_brow
    
    def get_right_eye_brow(self)->EyeBrow:
        return self.right_eye_brow

    def get_nose(self)->Nose:
        '''
        Get Nose from the face
        '''
        return self.nose

    def get_center(self):
        '''
        Return the nose tip as the center of the face
        '''
        return self.nose.tip

    def get_face_size(self):
        '''
        Return the size of the face
        '''
        return (
            max(self.bounding, key=lambda x: x[0])[0] - min(self.bounding, key=lambda x: x[0])[0],
            max(self.bounding, key=lambda x: x[1])[1] - min(self.bounding, key=lambda x: x[1])[1]
            )


    def __str__(self) -> str:
        return f'Left eye:{self.get_left_eye()}\n' + \
        f'Right eye:{self.get_right_eye()}\n'+ \
        f'Mouth:{self.get_mouth()}\n'+ \
        f'Left eye brow:{self.get_left_eye_brow()}\n'+ \
        f'Right eye brow:{self.get_right_eye_brow()}\n' + \
        f'Nose:{self.get_nose()}\n'
        

if __name__ == "__main__":
    face = Face()
    print(face)

