from PIL import Image, ImageDraw
from face import Face, Eye, Mouth, Nose, EyeBrow
import math
import uuid

COLOR_EMOJI_BACKGROUND = (255, 176, 46)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_LIP = (228, 92, 101)

IMAGE_SIZE = (512,512)
RESERVER_EDGE = (IMAGE_SIZE[0] * 0.1, IMAGE_SIZE[1] * 0.1)


class Color:
    def __init__(self,):
        self.skin = COLOR_EMOJI_BACKGROUND
        self.eye_brow = COLOR_BLACK
        self.nose = COLOR_BLACK
        self.mouth = COLOR_LIP


class Draw:

    def __init__(self,size = IMAGE_SIZE,background = COLOR_WHITE,color:Color = Color()):
        self._color = color
        self._background = background
        self._center = (size[0]/2,size[1]/2)
        self._scale = 1
        self._ts = [t/100.0 for t in range(101)]
        pass


    def get_color(self,):
        return self._color
    
    def set_color(self,color:Color):
        self._color = color
        pass

    def draw_face(self,face:Face,save=False,path=None):
        # img = Image.open(img_path)
        self._scale = 1
        self._face_center = face.get_center()
        face_size = face.get_face_size()
        self._scale = IMAGE_SIZE[0] / face_size[0] if face_size[0] > face_size[1] else IMAGE_SIZE[1] / face_size[1]
        self._scale = self._scale * 0.95        
        img = Image.new('RGB', IMAGE_SIZE, self._background)
        draw = ImageDraw.Draw(img)
        self._draw_face_background(face,draw)
        self._draw_eye_brow(face.left_eye_brow,draw)
        self._draw_eye_brow(face.right_eye_brow,draw)
        self._draw_eye(face.left_eye,draw)
        self._draw_eye(face.right_eye,draw)
        self._draw_mouth(face.mouth,draw)
        self._draw_nose(face.nose,draw)
        filename = None
        if save:
            filename = str(uuid.uuid4()) + '.png'
            if path is not None:
                img.save(f'{path}\\{filename}')
            else:
                img.save(f'{filename}')
        return img, filename 

    def _draw_eye_brow(self,eye_brow:EyeBrow,draw:ImageDraw):
        # draw left eye brow
        left_eye_brow_cords = [
            self._get_cord(eye_brow.left),
            self._get_cord(eye_brow.center),
            self._get_cord(eye_brow.right)
        ]
        bazier = self._make_bezier(left_eye_brow_cords)
        points = bazier(self._ts)
        draw.line(points,fill=self._color.eye_brow,width=3)

    def _draw_eye(self,eye:Eye,draw:ImageDraw):
        # draw left eye
        eye_up_cords = [
            self._get_cord(eye.left),
            self._get_cord(eye.top),
            self._get_cord(eye.right)
        ]
        bazier = self._make_bezier(eye_up_cords)
        points = bazier(self._ts)
        eye_top = points[len(points)//2]

        eye_bottom_cords = [
            self._get_cord(eye.right),
            self._get_cord(eye.bottom),
            self._get_cord(eye.left)
        ]
        bazier = self._make_bezier(eye_bottom_cords)
        temp_points = bazier(self._ts)
        points.extend(temp_points)
        eye_bottom = temp_points[len(temp_points)//2]

        draw.polygon(points,fill=COLOR_WHITE)
        draw.line(points,fill=COLOR_BLACK,width=3)

        if eye_top[0] > eye_bottom[0]:
            eye_ball_center = (abs(eye_top[0] - eye_bottom[0])/2 + eye_bottom[0],(eye_bottom[1]-eye_top[1])/2+eye_top[1])
        else:
            eye_ball_center = (abs(eye_top[0] - eye_bottom[0])/2 + eye_top[0],(eye_bottom[1]-eye_top[1])/2+eye_top[1])

        eye_ball_radius = abs((eye_top[1] - eye_bottom[1])/2)
        # sin45 = cost45 = math.sin(math.radians(45))
        sin45cos45 = math.sin(math.radians(45))
        x = eye_ball_radius * sin45cos45
        y = eye_ball_radius * sin45cos45

        eye_ball_top_left = (eye_ball_center[0] - x,eye_ball_center[1] - y)
        eye_ball_bottom_right = (eye_ball_center[0] + x,eye_ball_center[1] + y)

        draw.ellipse((eye_ball_top_left[0],eye_ball_top_left[1],
        eye_ball_bottom_right[0],eye_ball_bottom_right[1]),fill=COLOR_BLACK)

    def _draw_mouth(self,mouth:Mouth,draw:ImageDraw):
        # draw mouth
        mouth_up_cords = [
            self._get_cord(mouth.left),
            self._get_cord(mouth.top),
            self._get_cord(mouth.right)
        ]
        bazier = self._make_bezier(mouth_up_cords)
        points = bazier(self._ts)

        mouth_bottom_cords = [
            self._get_cord(mouth.right),
            self._get_cord(mouth.bottom),
            self._get_cord(mouth.left)
        ]
        bazier = self._make_bezier(mouth_bottom_cords)
        points.extend(bazier(self._ts))

        draw.polygon(points,fill=self._color.mouth)
        draw.line(points,fill=COLOR_BLACK,width=3)

        mouth_center_cords = [
            self._get_cord(mouth.left),
            self._get_cord(mouth.center),
            self._get_cord(mouth.right)
        ]
        bazier = self._make_bezier(mouth_center_cords)
        points = bazier(self._ts)
        draw.line(points,fill=COLOR_BLACK,width=2)

    def _draw_face_background(self,face:Face,draw:ImageDraw):
        # Calculate average distance to the center of the face
        total = [0,0]
        face_center = face.get_center()
        for cord in face.bounding:
            total[0] += abs(cord[0] - face_center[0])
            total[1] += abs(cord[1] - face_center[1])
        avg = (total[0]/len(face.bounding),total[1]/len(face.bounding))
        # [0] is the x distance, [1] is the y distance
        left_top = self._get_cord((face_center[0] - avg[0],face_center[1] - avg[1]))
        right_bottom = self._get_cord((face_center[0] + avg[0],face_center[1] + avg[1]))
        draw.ellipse((left_top[0],left_top[1],right_bottom[0],right_bottom[1]),fill=self._color.skin)

    def _draw_nose(self,nose:Nose,draw:ImageDraw):
        # draw nose
        nose_cords = [
            self._get_cord(nose.left),
            self._get_cord(nose.center),
            self._get_cord(nose.right)
        ]
        bazier = self._make_bezier(nose_cords)
        points = bazier(self._ts)
        draw.line(points,fill=self._color.nose,width=3)

        points = (nose_cords[0],self._get_cord(nose.top))
        # Line from middle of eye to nose
        draw.line(points,fill=self._color.nose,width=3)

    def _get_cord(self,old_cord:tuple) -> tuple:
        '''
        calculate the new cordinate according to the center in the image
        (0,0) upper left corner
        Parameters:
            old_cord: the old cordinate
            center: the center of the original image
        Returns:
            new_cord: the new cordinate
        '''
        return ((old_cord[0] - self._face_center[0])* self._scale + IMAGE_SIZE[0]/2,
         (old_cord[1] - self._face_center[1]) * self._scale + IMAGE_SIZE[1]/2)

    # Credit https://stackoverflow.com/questions/246525/how-can-i-draw-a-bezier-curve-using-pythons-pil
    def _make_bezier(self,xys):
        # xys should be a sequence of 2-tuples (Bezier control points)
        n = len(xys)
        combinations = self._pascal_row(n-1)
        def bezier(ts):
            # This uses the generalized formula for bezier curves
            # http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
            result = []
            for t in ts:
                tpowers = (t**i for i in range(n))
                upowers = reversed([(1-t)**i for i in range(n)])
                coefs = [c*a*b for c, a, b in zip(combinations, tpowers, upowers)]
                result.append(
                    tuple(sum([coef*p for coef, p in zip(coefs, ps)]) for ps in zip(*xys)))
            return result
        return bezier

    def _pascal_row(self,n, memo={}):
        # This returns the nth row of Pascal's Triangle
        if n in memo:
            return memo[n]
        result = [1]
        x, numerator = 1, n
        for denominator in range(1, n//2+1):
            # print(numerator,denominator,x)
            x *= numerator
            x /= denominator
            result.append(x)
            numerator -= 1
        if n&1 == 0:
            # n is even
            result.extend(reversed(result[:-1]))
        else:
            result.extend(reversed(result))
        memo[n] = result
        return result
    def _subtract_cord(self,cord1,coord2):
        return (cord1[0] - coord2[0],cord1[1] - coord2[1])
if __name__ == "__main__":
    d = Draw()
    img, fpath = d.draw_face(Face(),True)
    img.show()
    print(fpath)
        
