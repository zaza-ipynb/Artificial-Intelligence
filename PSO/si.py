import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import random
import math
import plotly.graph_objs as go
import plotly.offline as py

def f(x):
    x1 = x[0]
    x2 = x[1]
    obj1 = 0
    obj2 = 0
    for i in range(1,6):
      obj1 = obj1+i*math.cos((i+1)*x1+1)
      obj2 = obj2+i*math.cos((i+1)*x2+1)
    obj = -obj1*obj2
    return obj

def configure_plotly_browser_state():
  import IPython
  display(IPython.core.display.HTML('''
        <script src="/static/components/requirejs/require.js"></script>
        <script>
          requirejs.config({
            paths: {
              base: '/static/base',
              plotly: 'https://cdn.plot.ly/plotly-1.5.1.min.js?noext',
            },
          });
        </script>
        '''))

configure_plotly_browser_state()
py.init_notebook_mode(connected=False)

xx=np.linspace(-50, 50, 100)
yy=np.linspace(-50, 50, 100)
x,y=np.meshgrid(xx, yy)
z = np.zeros(x.shape)
for i in range(x.shape[0]):
    for j in range(y.shape[1]):
        z[i][j] = f([x[i][j],y[i][j]])


colorscale=[[0.0, 'rgb(20,29,67)'],
           [0.1, 'rgb(28,76,96)'],
           [0.2, 'rgb(16,125,121)'],
           [0.3, 'rgb(92,166,133)'],
           [0.4, 'rgb(182,202,175)'],
           [0.5, 'rgb(253,245,243)'],
           [0.6, 'rgb(230,183,162)'],
           [0.7, 'rgb(211,118,105)'],
           [0.8, 'rgb(174,63,95)'],
           [0.9, 'rgb(116,25,93)'],
           [1.0, 'rgb(51,13,53)']]

textz = [['x: '+'{:0.5f}'.format(x[i][j])+'<br>y: '+'{:0.5f}'.format(y[i][j])+
        '<br>z: '+'{:0.5f}'.format(z[i][j]) for j in range(z.shape[1])] for i in range(z.shape[0])]

trace1= go.Surface(
    x=tuple(x),
    y=tuple(y),
    z=tuple(z),
    colorscale=colorscale,
    text=textz,
    hoverinfo='text',
)

axis = dict(
showbackground=True,
backgroundcolor="rgb(230, 230,230)",
showgrid=False,
zeroline=False,
showline=False)

ztickvals=list(range(-6,4))
layout = go.Layout(title="Projections" ,
                autosize=False,
                width=700,
                height=600,
                scene=dict(xaxis=dict(axis, range=[-50, 50]),
                            yaxis=dict(axis, range=[-50, 50]),
                            zaxis=dict(axis , range=[-200,200]),
                            aspectratio=dict(x=1,
                                             y=1,
                                             z=1)
                           )
                )

data=[go.Surface(
    opacity=1,
    x=x,
    y=y,
    z=z,
    contours=go.surface.Contours(
        x=go.surface.contours.X(
            highlight=True,
            highlightcolor="#41a7b3",
        ),
        y=go.surface.contours.Y(highlight=False),
        z=go.surface.contours.Z(highlight=False),
    )
)]
fig = go.Figure(data=data, layout=layout)
py.iplot(fig)

def k():
  x = 2/abs(2-4.1-math.sqrt(4.1**2-4*4.1))
  return x

def v(vid,pid,xid,pgd):
  r = np.random.random()
  a = vid + 2.8*r*(pid-xid) + 1.3*r*(pgd-xid)
  vel = abs(a)*k()
  return vel

max = 50
min = -50
p = np.random.uniform(low=-50, high=50, size=(5,2))
q = np.zeros((5,3))
for i in range(1,100):
  for a in range(p.shape[1]):
    q[0][a] = f([p[0][a],p[1][a]])
  for a in range(p.shape[3]):
    if i == 0:
      q[3][a] = v(1,)

#problem modelling
def fitness_function(position):
    return f(position)

#Counting/calculate the velocity
W = 0.5
c1 = 0.5
c2 = 0.9
target = 1

n_iterations = int(1000)
target_error = float(1000000)
n_particles = int(100)

particle_position_vector = np.array([np.array([(-1) ** (bool(random.getrandbits(1))) * random.random()*50, (-1)**(bool(random.getrandbits(1))) * random.random()*50]) for _ in range(n_particles)])
pbest_position = particle_position_vector
pbest_fitness_value = np.array([float('-inf') for _ in range(n_particles)])
gbest_fitness_value = float('-inf')
gbest_position = np.array([float('-inf'), float('-inf')])

velocity_vector = ([np.array([0, 0]) for _ in range(n_particles)])
iteration = 0
while iteration < n_iterations:
    for i in range(n_particles):
        fitness_cadidate = fitness_function(particle_position_vector[i])

        if(pbest_fitness_value[i] < fitness_cadidate):
            pbest_fitness_value[i] = fitness_cadidate
            pbest_position[i] = particle_position_vector[i]

        if(gbest_fitness_value < fitness_cadidate):
            gbest_fitness_value = fitness_cadidate
            gbest_position = particle_position_vector[i]



    for i in range(n_particles):
        new_velocity = (W*velocity_vector[i]) + (c1*random.random()) * (pbest_position[i] - particle_position_vector[i]) + (c2*random.random()) * (gbest_position-particle_position_vector[i])
        new_position = new_velocity + particle_position_vector[i]
        particle_position_vector[i] = new_position

    iteration = iteration + 1

print("The best position : ", gbest_position, "of iteration number : ", f(gbest_position))
