import matplotlib.pyplot as plt
from random import uniform
from math import sqrt

def check_collision(new_circle, circle_list):
    for c in circle_list:
        d = sqrt((new_circle.center[0] - c.center[0])**2 +
                 (new_circle.center[1] - c.center[1])**2)
        if d < (c.radius + new_circle.radius):
            return True
    return False

def draw_circles(n_circle, name):
    min_r, max_r = 0.5, 8.0
    size = 300

    circle_list = []

    fig = plt.gcf()

    while len(circle_list) < n_circle:
       pos = (uniform(max_r, size-max_r), uniform(max_r, size-max_r))
       circle = plt.Circle(pos, uniform(min_r, max_r), color="black")
       if check_collision(circle, circle_list):
            continue
       fig.gca().add_artist(circle)
       circle_list.append(circle)

    plt.xlim(0, size)
    plt.ylim(0, size)   
    plt.axis('off')
    #plt.show()
    fig.savefig(name)
    plt.close("all")

    return True

# min = 100
# max = 200
# for i in range(min, max+1, 3):
#     if i<10:
#         draw_circles(i, 'img/cirles00'+str(i)+'.png')
#     elif i<100:
#         draw_circles(i, 'img/circles0'+str(i)+'.png')
#     else:
#         draw_circles(i, 'img/circles'+str(i)+'.png')