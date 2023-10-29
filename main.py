import random
import math
from math import radians,sin,cos,tan
from uimodel import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow,QMessageBox,QApplication,QGraphicsScene,QGraphicsPolygonItem
from PyQt5.QtGui import QPolygonF
from PyQt5.QtCore import Qt, QPointF
import sys

class classify_triangle_tradition():
    """function dict contain different function about triangle """
    def __init__(self,init_angle=None,function_dict=None):
        self.init_angle = init_angle
        if function_dict:
            self.function_dict = function_dict
        else:
            self.function_dict={
                "equilateral_triangle": self.equilateral_triangle,
                "isosceles_triangle": self.isosceles_triangle,
                "right_triangle": self.right_triangle,
                "right_isosceles_triangle": self.right_isosceles_triangle,
                "non_typical_triangle": self.non_typical_triangle
            }
        self.rename_dict= {
                "equilateral_triangle": '等边三角形',
                "isosceles_triangle": '等腰三角形',
                "right_triangle": '直角三角形',
                "right_isosceles_triangle": '等腰直角三角形',
                "non_typical_triangle": '非典型三角形'
            }
    def input_angle(self,a,b,c):
        """change angle"""
        self.init_angle=(a,b,c)

    def equilateral_triangle(self,x, y, z):
        # 等边三角形
        return 1 - (1 / 180) * max(x - y, y - z)

    def isosceles_triangle(self,x, y, z):
        # 等腰三角形
        return 1 - (1 / 60) * min(x - y, y - z)

    def right_triangle(self,x, y, z):
        # 直角三角形
        return 1 - (1 / 90) * abs(x - 90)

    def right_isosceles_triangle(self,x, y, z):
        # 等腰直角三角形
        return min(self.right_triangle(x, y, z), self.isosceles_triangle(x, y, z))

    def non_typical_triangle(self,x, y, z):
        # 非典型三角形
        return min(1 - self.isosceles_triangle(x, y, z), 1 - self.right_triangle(x, y, z), 1 - self.equilateral_triangle(x, y, z))

    def get_once(self):
        """choose max fitness value's and return that triangle """
        a,b,c = self.init_angle
        return {name:func(a,b,c) for name,func in self.function_dict.items()}

    def cal_res(self):
        res = self.get_once()
        value_list = sorted(res.items(),key=lambda x:x[1],reverse=True)
        res = value_list[0][0]
        return self.rename_dict[res]

class classify_triangle_exp(classify_triangle_tradition):
    def __init__(self):
        super(classify_triangle_exp, self).__init__()
        self.function_dict = {
            "equilateral_triangle": self.E_e,
            "isosceles_triangle": self.I_e,
            "right_triangle": self.R_e,
            "right_isosceles_triangle": self.IR_e,
            "non_typical_triangle": self.O_e,
        }

    def E_e(self,x, y, z):
        t = x - y
        return (1 - t / 180) ** t

    def I_e(self,x, y, z):
        t = min(x - y, y - z)
        return (1 - t / 60) ** t

    def R_e(self,x, y, z):
        t = x - 90
        return (1 - t / 90) ** t

    def IR_e(self,x, y, z):
        return min(self.I_e(x, y, z), self.R_e(x, y, z))

    def O_e(self,x, y, z):
        return min(1 - self.I_e(x, y, z), 1 - self.R_e(x, y, z), 1 - self.E_e(x, y, z))

class classify_triangle_tri(classify_triangle_tradition):
    def __init__(self):
        super(classify_triangle_tri, self).__init__()


    def transform_angle(self,x, y, z):
        return (radians(i) for i in [x, y, z])

    def equilateral_triangle(self,x, y, z):
        # 等边三角形
        x, y, z = self.transform_angle(x, y, z)
        b = radians(60)
        return max(0, (cos(x - b) + cos(y - b) + cos(z - b)) / 3)

    def isosceles_triangle(self,x, y, z):
        # 等腰三角形
        x, y, z = self.transform_angle(x, y, z)
        return max(cos(x - y), cos(y - z))

    def right_triangle(self,x, y, z):
        # 直角三角形
        x, y, z = self.transform_angle(x, y, z)
        return sin(x)

    def right_isosceles_triangle(self,x, y, z):
        # 等腰直角三角形
        return min(self.right_triangle(x, y, z), self.isosceles_triangle(x, y, z))

    def non_typical_triangle(self,x, y, z):
        # 非典型三角形
        return min(1 - self.isosceles_triangle(x, y, z), 1 - self.right_triangle(x, y, z), 1 - self.equilateral_triangle(x, y, z))

class Triangle_window(Ui_MainWindow,QMainWindow):
    # 首先进行初始化 初始化各个部件
    def __init__(self):
        super(Triangle_window, self).__init__()
        self.setupUi(self)
        # 将各个按钮关联
        self.setWindowTitle('第23组展示程序')
        self.scene = QGraphicsScene()
        self.plot_triangle.setScene(self.scene)


        self.input_angle.clicked.connect(self.cal_result)
        self.random_angle.clicked.connect(self.rand_res_cal)


    def get_angel(self):
        """get the angel"""
        # 排序
        try:
            angles = sorted([int(i.text()) for i in [self.IX,self.IY,self.IZ]],reverse=True)
            if sum(angles)!=180:
                # 弹出一个窗口并且停止计算 , 弹出窗口并且返回0
                alert = QMessageBox()
                alert.setText('请重新输入!!!')
                alert.show()
                alert.exec_()
                return None

            return angles
        except Exception:
            alert = QMessageBox()
            alert.setText('输入不合法!!!')
            alert.show()
            alert.exec_()
            return None

    def cal_result(self):
        tri = classify_triangle_tri()
        exp = classify_triangle_exp()
        tra = classify_triangle_tradition()

        angels = self.get_angel()
        if angels:
            tri.input_angle(*angels)
            exp.input_angle(*angels)
            tra.input_angle(*angels)

            tri_res = tri.cal_res()
            exp_res = exp.cal_res()
            tra_res = tra.cal_res()

            self.D1.setText(tra_res)
            self.D2.setText(exp_res)
            self.D3.setText(tri_res)
            self.draw_tri()

        else:
            res = 'NA'
            self.D1.setText(res)
            self.D2.setText(res)
            self.D3.setText(res)

    def rand_res_cal(self):
         x,y,z= rand_angles()
         self.IX.setText(str(x))
         self.IY.setText(str(y))
         self.IZ.setText(str(z))
         self.cal_result()

    def draw_tri(self):
        # geometry x,y 宽度 高度
        # self.plot_triangle = QtWidgets.QGraphicsView(self.centralwidget)

        # 重置scene
        self.scene = QGraphicsScene()
        self.plot_triangle.setScene(self.scene)

        a = .5
        angles = self.get_angel()
        pos_x,pos_y =  cal_pos(*angles)
        x, y, width, height = self.plot_triangle.frameGeometry().getRect()


        vertices = [
            QPointF(0,0),
            QPointF(width * a, 0),
            QPointF(width * a * pos_x,height * a * pos_y),
        ]
        polygon = QPolygonF(vertices)

        triangle_item = QGraphicsPolygonItem(polygon)
        self.scene.addItem(triangle_item)


def rand_angles():
    while True:
        # 生成随机的三个角度
        angle1 = random.randint(1, 178)  # 1到178度之间
        angle2 = random.randint(1, 179 - angle1)  # 第二个角度的范围取决于前两个
        angle3 = 180 - angle1 - angle2  # 第三个角度是为了确保和为180

        if angle3 >= 10:
            # 有效的三角形，返回三个角度
            return angle1, angle2, angle3

def cal_pos(x,y,z):
    """calculate the triangle's position according to the angle"""
    z,y,x = x,y,z
    low = tan(x) + tan(y)
    return (tan(y)/low,tan(x)*tan(y)/low)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    windows = Triangle_window()
    windows.show()
    sys.exit(app.exec_())
