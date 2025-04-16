import dotenv
import os

K = os.environ.get("K")
Q_1 = os.environ.get("Q_1")
Q_2 = os.environ.get("Q_2")
M = os.environ.get("M")
T = os.environ.get("T")

CONST = K * Q_1 * Q_2 / M
alpha_x_prev = 0
def get_alpha_x(X, Y):
    alpha_x_prev = alpha_x
    alpha_x = CONST * X/(X**2+Y**2)^(3/2)
    
    return alpha_x_prev, alpha_x

def get_alpha_y(alpha_y):
    alpha_y_prev = alpha_y
    alpha_y = CONST * get_x/(get_x**2+get_y**2)^(3/2)

    return alpha_y_prev, alpha_y

def get_x(X, alpha_x):
    X_Prev = X
    X = X_Prev + get_speed_x() * T + (1/2)*get_alpha_x(alpha_x)[0] #probably an error with the [0] in the get alpha x

    return X_Prev, X

def get_y(Y, alpha_y):
    Y_Prev = Y
    Y = Y_Prev + get_speed_y() * T + (1/2)*get_alpha_y(alpha_y)[0]

    return None

def get_speed_x(V_x, alpha_x, alpha_x_prev):
    V_x_prev = V_x
    V_x = V_x_prev + (1/2) * (get_alpha_x(alpha_x) + get_alpha_x(alpha_x_prev)) * T

    return None

def get_speed_y(V_y, alpha_y, alpha_y_prev):
    V_y_prev = V_y
    V_y = V_y_prev + (1/2) * (get_alpha_y(alpha_y) + get_alpha_y(alpha_y_prev)) * T

    return None


# x = particle position (x)
# y = particle position (y)
# v_x = particle velocity (x)
# v_y = particle velocity (y)
# delta_t = time step
# alpha_x = given equation. Will contain q_1, q_2, k, m, and x and y. Note that the first four are given.
# alpha_y = same as above
# For alpha_x,y , mass is of the alpha particle

