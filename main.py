import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
import PySimpleGUI as sg
import math
import matplotlib as mt
import numpy as np
h_w = 12
w_w = 2
q = 1.6
m = 1.67
n = 1000
a = 45
u = 30
v = 10
b = 0.5
z_0 = 0
class Canvas(FigureCanvasTkAgg):
  """
    Create a canvas for matplotlib pyplot under tkinter/PySimpleGUI canvas
    """

  def __init__(self, figure=None, master=None):
    super().__init__(figure=figure, master=master)
    self.canvas = self.get_tk_widget()
    self.canvas.pack(side='top', fill='both', expand=1)

def cm_to_inch(value):
  return value / 2.54

def plot_figure(v,a,u,q,m,n,b,z_0):
    a = math.radians(float(a))
    u = math.radians(float(u))
    q = float(q)*(10**(-19))
    # m = float(m)*(10**(-31)) #+8 знаков /////////////////////////////////////
    m = float(m)*(10**(-23))
    v = float(v)*(10**(6))
    n = float(n)
    b = float(b)
    z_0 = float(z_0)
    dt = 0.0001
    axes[0].cla()
    axes[1].cla()
    axes[2].cla()
    x = [0]
    y = [m*v/abs(q)*b*math.sin(a)]
    # y = [0]
    z = [z_0]
    vx = v * math.sin(a) * math.cos(u)
    vy = v * math.sin(a) * math.sin(u)
    vz = v * math.cos(a)
    # vz = 0
    i = 0

    if True:
    # try:
        while n > 0:
            ax = abs(q)*b/m*vy
            ay = -1*abs(q)*b/m*vx
            vx = vx + ax*dt
            vy = vy + ay*dt
            # print(vx,vy,vz)
            x.append(x[i]+vx*dt)
            y.append(y[i]+vy*dt)
            z.append(z[i]+vz*dt)
            # z_0 не изменяет?
            n = n - 1
            i = i + 1
            # if np.isnan(vx).any() or np.isinf(vx).any() or np.isnan(vy).any() or np.isinf(vy).any() or np.isnan(ax).any() or np.isinf(ay).any():
            #     print("Particle's position, velocity, or acceleration is NaN or Inf. Stopping simulation.")
            #     break
    # except:
    #     return
    # print(z)
    r = [x,y,z]
    axes[0].set_ylabel('ZX')
    axes[1].set_ylabel('ZY')
    axes[2].set_ylabel('XY')
    axes[0].plot(z,x)
    axes[1].plot(z,y)
    axes[2].plot(x,y,color='g')
    axes[2].set_xlabel('Time (s)')
    canvas.draw()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()
    return



layout = [
    [sg.Canvas(size=(640, 480), key='Canvas')],
    [sg.Text('q'), sg.Input(1.6,enable_events=True,k='-Q-',size=(5, 1)),sg.Text('^e-19  '),sg.Text('m'), sg.Input(1.67,enable_events=True,k='-M-',size=(5, 1)),sg.Text('^e-31  '), sg.Text('B'),sg.Input(0.5,enable_events=True,k='-B-',size=(5, 1)),sg.Text(text="   "),sg.Text('    v'),sg.Input(10,enable_events=True,k='-V-',size=(5, 1)),sg.Text(text="^e+6   "),sg.Text(text="n"),sg.Input(1000,enable_events=True,k='-N-',size=(5, 1))],
    # [[sg.Text('x0'), sg.Input(0,enable_events=True,k='-X-',size=(5, 1)),sg.Text('Vx'), sg.Input(1,enable_events=True,k='-VX-',size=(5, 1))]],
    # [[sg.Text('y0'), sg.Input(1,enable_events=True,k='-Y-',size=(5, 1)),sg.Text('Vy'), sg.Input(0,enable_events=True,k='-VY-',size=(5, 1))]],
    # [[sg.Text('z0'), sg.Input(0,enable_events=True,k='-Z-',size=(5, 1)),sg.Text('Vz'), sg.Input(0,enable_events=True,k='-VZ-',size=(5, 1))]],
    [sg.Text('a'), sg.Input(45,enable_events=True,k='-A-',size=(5, 1)),sg.Text('u'), sg.Input(30,enable_events=True,k='-U-',size=(5, 1)),sg.Text('z0'), sg.Input(0,enable_events=True,k='-Z0-',size=(5, 1))],
    [[sg.Push(), sg.Button('go'), sg.Push()]]
    ]
# sg.theme('DefaultNoMoreNagging')
window = sg.Window('Движение заряженной частицы в магнитном поле',
                   layout,
                   finalize=True,
                   resizable=True, size = (640, 520))
# plt.figure(figsize=(cm_to_inch(h_w), cm_to_inch(w_w)))
fig = Figure(figsize=(cm_to_inch(16), cm_to_inch(10.7)))
# fig, axes = plt.subplots(3, 1, sharex=True)
axes = fig.subplots(3, 1, sharex=True)
# ax_1 = fig.add_subplot(2, 1, 1)
# # fig.subplots_adjust(top=0.8, bottom=0.1)
# ax_2 = ax_1.twinx()
# ax_2 = fig.add_subplot(2, 1, 2)
canvas = Canvas(fig, window['Canvas'].Widget)
def launch():
    return plot_figure(v,a,u,q,m,n,b,z_0)
while True:
  event, values = window.read()
  # print(event)
  if event in (sg.WIN_CLOSED, 'Exit'):
    break
  elif event == '-A-':
      a = values[event]
      # launch()
  elif event == '-U-':
      u = values[event]
      # launch()
  elif event == '-Q-':
      q = values[event]
      # launch()
  elif event == '-M-':
      m = values[event]
      # launch()
  elif event == '-N-':
      n = values[event]
      # launch()
  elif event == '-B-':
    # print(values)
    b = values[event]
  elif event == '-Z0-':
    # print(values)
    z_0 = values[event]
  elif event == '-V-':
    # print(values)
    v = values[event]
  elif event == 'go':
      launch()
window.close()
exit()
