from Robot import Robot
from Communication import Communication
import math

class go_to:
    def __init__(self, id, team, val_x, val_y) -> None:
        self.id = id
        self.team = team
        self.val_x = val_x
        self.val_y = val_y
        self.car = Robot(id, team)
        self.de = 10
        self.kr = 10

        self.car_x = self.car.x()
        self.car_y = self.car.y()

        self.diff_x = self.val_x - self.car_x
        self.diff_y = self.val_y - self.car_y

        self.comm = Communication()

    def __theta(self):
        return math.atan(self.diff_y/self.diff_x)


    def __dist(self):
        return math.sqrt( self.diff_x * self.diff_x + self.diff_y * self.diff_y)

    
    def __err_orientation(self):
        return self.__theta() - self.car.orient()

#######################################   Campo Repulsivo   #######################################

    def __enemies(self):
        if self.team == True:
            return False
        else:
            return True

    def __obstacles(self):
        enemie_team = self.__enemies()

        enemie_0 = Robot(0,enemie_team)
        enemie_1 = Robot(1,enemie_team)
        enemie_2 = Robot(2,enemie_team)
        

        return [(enemie_0.x(), enemie_0.y()), (enemie_1.x(), enemie_1.y()), (enemie_2.x(), enemie_2.y())]


    def calculate_obstacle_field(self):
        obs = self.__obstacles()
        force_x = 0
        force_y = 0

        contador = 0

        while contador < 3:
            enemie = obs[contador]

            diff_x = self.car_x - enemie[0]
            diff_y = self.car_y - enemie[1]

            p_point = math.sqrt( diff_x*diff_x * diff_y*diff_y)
            
            cos = diff_x/p_point
            sen = diff_y/p_point

            force_x += cos/p_point
            force_y += sen/p_point

            contador += 1
        a = math.sqrt(force_x*force_x + force_y*force_y)
        auf = math.atan2( force_x/a, force_y/a)

        return auf

#######################################   Campo Atrativo   #######################################

    def calculate_free_fiel(self):
        pr = (self.val_x, self.val_y - self.de)
        pl = (self.val_x, self.val_y + self.de)

        if self.val_y > self.de:
            TUF = self.__hs_ccw(pr)
            return TUF

        else:
            TUF = self.__hs_cw(pl)
            return TUF

    def __hs_cw(self, pl):
        r = math.sqrt(pl[0]*pl[0]  + pl[1]*pl[1])
        theta = math.atan2(pl[1]/pl[0])
        
        if r > self.de:
            HS_CW = theta + math.radians(90)*((self.de + self.kr)/(r + self.kr))
            return (math.cos(HS_CW), math.sen(HS_CW))

        else:
            HS_CW = theta + math.radians(90)*math.sqrt(r / self.de)
            return (math.cos(HS_CW), math.sen(HS_CW))


    def __hs_ccw(self, pr):
        r = math.sqrt(pr[0]*pr[0]  + pr[1]*pr[1])
        theta = math.atan2(pr[1]/pr[0])
        
        if r > self.de:
            HS_CCW = theta - math.radians(90)*((self.de + self.kr)/(r + self.kr))
            return (math.cos(HS_CCW), math.sen(HS_CCW))
        else:
            HS_CCW = theta - math.radians(90)*math.sqrt(r / self.de)
            return (math.cos(HS_CCW), math.sen(HS_CCW))

##################################################################################################
    def go_to(self):
        robot_speed = 25
        orientation_kp = 25
        if self.__dist() < 0.1:
            self.comm.move(self.id, self.team, 0,0)
        else:
            velocidade = self.__err_orientation() * orientation_kp
            if self.diff_x > 0.0:
                self.comm.move(self.id, self.team, -velocidade + robot_speed, velocidade + robot_speed)
            else:
                self.comm.move(self.id, self.team, -velocidade - robot_speed, velocidade - robot_speed)



