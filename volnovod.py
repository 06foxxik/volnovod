from numpy import (sin, cos, tan, pi, exp, sqrt, arange, meshgrid, linspace, zeros)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import (clf, gcf, subplots_adjust, figure)
from tkinter.ttk import (Combobox, Radiobutton, Button, Style)
from tkinter import (Label, Entry, Tk, S, N, E, W, SE, SW, NE, NW, IntVar, font)
from sys import exit
import os

LARGE_FONT = ("Arial", 14)

def testVal(inStr, acttyp):
    if acttyp == '1': #insert
        if not inStr.isdigit():
            return False
        return True

def EXIT():
    os.abort()

#def time_minus():
#    global time
#    if time > 0:
#        time -= 1.0
#        time_label.configure(text = time)
#        plotting()

#def time_plus():
#    global time
#    time += 1.0
#    time_label.configure(text = time)
#    plotting()

def get(entry):
    value = entry.get()
    try:
        return int(value)
    except ValueError:
        return None

def plotting():
    global size_lines_entry
    global frequency
    global moda_n
    global moda_m
    global label
    global f_kr
    #global time_textbox
    clf()
    if (len(frequency.get()) == 0) or (len(a_x_size_entry.get()) == 0) or (len(b_x_size_entry.get()) == 0) or (len(size_lines_entry.get()) == 0) or (len(table_m.get()) == 0) or (len(table_n.get()) == 0):
        clf()
        label.configure(text = "Заполните все поля!", bg = "lightgray")
        label.place(x=590,y=255)
        #label.grid(row=0, column=4, columnspan=3, padx=10, pady=15, sticky=S+N)
        gcf().canvas.draw()
        return
    label.configure(text = " ")
    
    cc = 3e10 #Скорость света
    
    ff = get(frequency) #Частота в ГГц
    f = ff*1e9 #Перевод в Гц
    w = 2*pi*f
    lyam = cc/f
    hh = w//cc #Волновое число в волноводе
    #Параметры волновода
    n = get(table_n)
    m = get(table_m)
    a = get(a_x_size_entry) #размер волновода по x в см
    b = get(b_x_size_entry) #размер волновода по y в см
    c = lyam #размер волновода по z в см
    
    #Шаг сетки
    h = 0.01
    #время сечения
    if len(time_textbox.get()) != 0:
        tt = get(time_textbox)
    else:
        tt = 0
    
    t = tt/1e12
    #количество линий уровня
    k = get(size_lines_entry)
    
    kappa = sqrt(((pi*n/a)**2)+((pi*m/b)**2))
    kappaX = pi*n/a
    kappaY = pi*m/b
    f_kr = (cc*kappa)/(2*pi)
    
    #Алгоритм определения констант для проекций (где будет сдлеан срез)
    
    C1 = 0
    C2 = 0
    if n!=0 and m==0:
        if (n%2)!=0:
            C1 = a/2
        else:
            C1 = a/(2*n)
    elif n==0 and m!=0:
        if (m%2)!=0:
            C2 = b/2
        else:
            C2 = b/(2*m)
    
    
    ##TE##
    ##H
    def TE_H_XY(x,y):
        return ((abs(sin(kappaX*x)))/(abs(sin(kappaY*y))))*cos(w*t+pi/2)
    
    def TE_H_YZ(y,z):
        return (abs(sin(kappaY*y)))*cos(w*t-hh*z+pi/2)
    
    def TE_H_XZ(x,z):
        return (abs(sin(kappaX*x)))*cos(w*t-hh*z+pi/2)
    
    ##E
    def TE_E_XY(x,y):
        return abs(cos(kappaY*y))*abs(cos(kappaX*x))*cos(w*t)
    
    ##H10
    def TE10_H_XY(x,y):
        return abs(sin(kappaX*x-1.5))*exp(hh*tan(w*t)*y)
    
    def TE10_H_XZ(x,z):
        return abs(sin(kappaX*x))*cos(w*t-hh*z)
    
    def TE10_H_YZ(y,z):
        return exp(kappaX*(cos(kappaX*C1)/sin(kappaX*C1))*y)*cos(w*t-hh*z)
    
    ##E10
    def TE10_E_XY(x,y):
        return (w/(kappaX*cc))*abs(cos(kappaX*x))*sin(w*t)
    
    ##H01
    def TE01_H_XY(x,y):
        return abs(sin(kappaY*y+1.5))*exp(hh*tan(w*t)*x)
    
    def TE01_H_XZ(x,z):
        return exp(kappaY*(cos(kappaY*C2)/sin(kappaY*C2))*x)*cos(w*t-hh*z)
    
    def TE01_H_YZ(y,z):
        return abs(sin(kappaY*y))*cos(w*t-hh*z)
    
    ##E01
    def TE01_E_XY(x,y):
        return (w/(kappaY*cc))*abs(cos(kappaY*y))*sin(w*t)
    
    ###TM
    ##H
    def TM_H_XY(x,y):
        return abs(sin(kappaX*x))*abs(sin(kappaY*y))*cos(w*t+pi/2)
    
    ##E
    def TM_E_XY(x,y):
        return (abs(cos(kappaY*y)))/(abs(cos(kappaX*x)))*cos(w*t)
    
    def TM_E_XZ(x,z):
        return abs(cos(kappaX*x))*cos(w*t-hh*z)
    
    def TM_E_YZ(y,z):
        return abs(cos(kappaY*y))*cos(w*t-hh*z)
    
    def makeData(b1,b2):
        a1 = arange(0, b1, h)
        a2 = arange(0, b2, h)
        a1grid, a2grid = meshgrid(a1, a2)
        return a1grid, a2grid
    
    if f > f_kr:
        XY = fig.add_subplot(3, 1, 1)
        YZ = fig.add_subplot(3, 1, 2)
        XZ = fig.add_subplot(3, 1, 3)
        
        fig.set_figwidth(5)
        fig.set_figheight(5)
        
        x1, y1 = makeData(a,b)
        y2, z2 = makeData(b,c)
        x3, z3 = makeData(a,c)
        if var.get()==2:
            ###TE
            ##XY
            #H
            if n!=0 and m!=0:
                XY.contour(x1, y1, TE_H_XY(x1, y1), linspace(-1, 1, k), colors = 'b')
            elif n!=0 and m==0:
                XY.contour(x1, y1, TE10_H_XY(x1, y1), linspace(-1, 1, k), colors = 'r')
            elif n==0 and m!=0:
                XY.contour(x1, y1, TE01_H_XY(x1, y1), linspace(-1, 1, k), colors = 'r')
            XY.set_xlabel('x')
            XY.set_ylabel('y')
            
            #E
            if n!=0 and m!=0:
                XY.contour(x1, y1, TE_E_XY(x1, y1), linspace(-1, 1, k), colors = 'r')
            elif n!=0 and m==0:
                #XY.contour(x1, y1, TE10_E_XY(x1, y1), linspace(-1, 1, k), colors = 'r')
                for i in range(0,b,b//(k-2)):
                    XY.axhline(y=i, color = 'b')
            elif n==0 and m!=0:
                #XY.contour(x1, y1, TE01_E_XY(x1, y1), linspace(-1, 1, k), colors = 'r')
                for i in range(0,a,a//(k-2)):
                    XY.axvline(x=i, color = 'b')
            XY.set_xlabel('x')
            XY.set_ylabel('y')
            
            ##YZ
            #H
            if n!=0 and m!=0:
                YZ.contour(z2, y2, TE_H_YZ(y2, z2), linspace(-1, 1, k), colors = 'b')
                ary=linspace(0,b,k-2)
                arx1=zeros(k-2)
                for i in range(k-2):
                    arx1[i] = tt*0.015625*c
                YZ.scatter(arx1,ary, c='r', s=4)
                arx2=zeros(k-2)
                for i in range(k-2):
                    arx2[i] = c*0.525 + tt*0.015625*c
                YZ.scatter(arx2,ary, c='r', marker="x")
                YZ.set_xlim(0.0, c)
            elif n!=0 and m==0:
                YZ.contour(z2, y2, TE10_H_YZ(y2, z2), linspace(-1, 1, k), colors = 'r')
                for i in range(0,b,b//(k-2)):
                    YZ.axhline(y=i, xmin=0, xmax=0.22, color = 'b')
                    YZ.axhline(y=i, xmin=0.26, xmax=0.79, color = 'b', linestyle = '--')
                    YZ.axhline(y=i, xmin=0.82, xmax=1, color = 'b')
            elif n==0 and m!=0:
                YZ.contour(z2, y2, TE01_H_YZ(y2, z2), linspace(-1, 1, k), colors = 'b')
                ary=linspace(0,b,k-2)
                arx1=zeros(k-2)
                for i in range(k-2):
                    arx1[i]=c*0.2575
                YZ.scatter(arx1,ary, c='r', s=4)
                arx2=zeros(k-2)
                for i in range(k-2):
                    arx2[i]=c*0.786
                YZ.scatter(arx2,ary, c='r', marker="x")
                
            YZ.set_xlabel('y')
            YZ.set_ylabel('z')
            
            ##XZ
            #H
            if n!=0 and m!=0:
                XZ.contour(z3, x3, TE_H_XZ(x3, z3), linspace(-1, 1, k), colors = 'b')
                ary=linspace(0,a,k-2)
                arx1=zeros(k-2)
                for i in range(k-2):
                    arx1[i] = tt*0.015625*c
                XZ.scatter(arx1,ary, c='r', s=4)
                ary=linspace(0,a,k-2)
                arx2=zeros(k-2)
                for i in range(k-2):
                    arx2[i] = c*0.525 + tt*0.015625*c
                XZ.scatter(arx2,ary, c='r', marker="x")
                XZ.set_xlim(0.0, c)
            elif n!=0 and m==0:
                XZ.contour(z3, x3, TE10_H_XZ(x3, z3), linspace(-1, 1, k), colors = 'b')
                ary=linspace(0,a,k-2)
                arx1=zeros(k-2)
                for i in range(k-2):
                    arx1[i]=c*0.2575
                XZ.scatter(arx1,ary, c='r', s=4)
                arx2=zeros(k-2)
                for i in range(k-2):
                    arx2[i]=c*0.786
                XZ.scatter(arx2,ary, c='r', marker="x")
            elif n==0 and m!=0:
                XZ.contour(z3, x3, TE01_H_XZ(x3, z3), linspace(-1, 1, k), colors = 'r')
                for i in range(0,a,a//(k-2)):
                    XZ.axhline(y=i, xmin=0, xmax=0.22, color = 'b')
                    XZ.axhline(y=i, xmin=0.26, xmax=0.79, color = 'b', linestyle = '--')
                    XZ.axhline(y=i, xmin=0.82, xmax=1, color = 'b')
            XZ.set_xlabel('x')
            XZ.set_ylabel('z')
            
        elif var.get()==1:
            ###TM
            ##XY
            #H
            if n!=0 and m!=0:
                XY.contour(x1, y1, TM_H_XY(x1, y1), linspace(-1, 1, k), colors = 'b')
                XY.set_xlabel('x')
                XY.set_ylabel('y')
                
                #E
                XY.contour(x1, y1, TM_E_XY(x1, y1), linspace(-1, 1, k), colors = 'r')
                XY.set_xlabel('x')
                XY.set_ylabel('y')
                
                ##YZ
                #E
                YZ.contour(z2, y2, TM_E_YZ(y2, z2), linspace(-1, 1, k), colors = 'r')
                ary=[b//4,b*3//4]
                arx1=zeros(2)
                for i in range(2):
                    arx1[i] = c*0.2575 + tt*0.015625*c
                arx2=zeros(2)
                for i in range(2):
                    arx2[i] = c*0.786 + tt*0.015625*c
                YZ.scatter([arx1[0],arx2[1]],ary, c='b', s=8)   
                YZ.scatter([arx2[0],arx1[1]],ary, c='b', marker="x")
                YZ.set_xlim(0.0, c)
                YZ.set_xlabel('y')
                YZ.set_ylabel('z')
                
                ##XZ
                #E
                XZ.contour(z3, x3, TM_E_YZ(x3, z3), linspace(-1, 1, k), colors = 'r')
                ary=[a//4,a*3//4]
                arx1=zeros(2)
                for i in range(2):
                    arx1[i] = c*0.2575 + tt*0.015625*c
                arx2=zeros(2)
                for i in range(2):
                    arx2[i] = c*0.786 + tt*0.015625*c
                XZ.scatter([arx1[0],arx2[1]],ary, c='b', s=8)   
                XZ.scatter([arx2[0],arx1[1]],ary, c='b', marker="x")
                XZ.set_xlim(0.0, c)
                XZ.set_xlabel('x')
                XZ.set_ylabel('z')
                
    else:
        label = Label(window, text = "Частота ниже критической!", font = LARGE_FONT, bg = "white")
        label.place(x=590,y=255)
        #label.grid(row=5, column=4, columnspan=2, padx=30, sticky=SW)
    subplots_adjust(wspace=0.5, hspace=0.5)
    gcf().canvas.draw()
    w_label = Label(window, text = "Критическая частота (ГГц): ", font = LARGE_FONT, bg = "white")
    w_label.place(x=30,y=550)
    #w_label.grid(row=11, column=0, columnspan=4, padx=30, sticky=SW)
    wk_label = Label(window, text = f_kr/1e9, font = LARGE_FONT, bg = "white")
    wk_label.place(x=290,y=550)
    #wk_label.grid(row=11, column=3, columnspan=4, padx=30, sticky=SW)
    
# ИНТЕРФЕЙС

window = Tk()
window.title(" ")
window.protocol("WM_DELETE_WINDOW", EXIT)
window.attributes("-toolwindow", 0)
window.resizable(width = True, height = True)
window['bg'] = 'white'
#размер формы
window.geometry('1000x730')
default_font = font.nametofont("TkDefaultFont")
default_font.configure(size=14)

label_n = Label(window, text = "Тип волны:", font = LARGE_FONT, bg = "white")
label_n.place(x=30,y=20)

var = IntVar()
var.set(2)
rad_tm = Radiobutton(window, text='TM',variable=var, value=1)
rad_te = Radiobutton(window, text='TE',variable=var, value=2)
rad_tm.place(x=110,y=60)
rad_te.place(x=30,y=60)

moda_label = Label(window, text = "Мода:", font = LARGE_FONT, bg = "white")
moda_label.place(x=30,y=240)

label_m = Label(window, text = "m =", font = LARGE_FONT, bg = "white")
label_m.place(x=140,y=280)
table_m = Entry(window, width=7, bg="gainsboro", selectbackground='black', validate="key")
table_m['validatecommand'] = (table_m.register(testVal), '%P','%d')
table_m.place(x=180,y=280,width=48,height=30)

label_n = Label(window, text = "n =", font = LARGE_FONT, bg = "white")
label_n.place(x=30,y=280)
table_n = Entry(window, width=7, bg="gainsboro", selectbackground='black', validate="key")
table_n['validatecommand'] = (table_n.register(testVal), '%P','%d')
table_n.place(x=70,y=280,width=48,height=30)

label_f = Label(window, text = "Частота (ГГц) =", font = LARGE_FONT, bg = "white")
label_f.place(x=30,y=190)

frequency = Entry(window, width=7, bg="gainsboro", selectbackground='black', validate="key")
frequency['validatecommand'] = (frequency.register(testVal), '%P','%d')
frequency.place(x=170,y=190,width=48,height=30)

waveguide_size = Label(window, text = "Размеры волновода (см):", font = LARGE_FONT, bg = "white")
waveguide_size.place(x=30,y=100)

a_x_size = Label(window, text = "a =", font = LARGE_FONT, bg = "white")
a_x_size.place(x=30,y=140)
a_x_size_entry = Entry(window, width=7, bg="gainsboro", selectbackground='black', validate="key")
a_x_size_entry['validatecommand'] = (a_x_size_entry.register(testVal), '%P','%d')
a_x_size_entry.place(x=70,y=140,width=48,height=30)

b_x_size = Label(window, text = "b =", font = LARGE_FONT, bg = "white")
b_x_size.place(x=130,y=140)
b_x_size_entry = Entry(window, width=7, bg="gainsboro", selectbackground='black', validate="key")
b_x_size_entry['validatecommand'] = (b_x_size_entry.register(testVal), '%P','%d')
b_x_size_entry.place(x=170,y=140,width=48,height=30)

size_lines = Label(window, text = "Количество силовых линий поля =", font = LARGE_FONT, bg = "white")
size_lines.place(x=30,y=330)
size_lines_entry = Entry(window, width=7, bg="gainsboro", selectbackground='black', validate="key")
size_lines_entry['validatecommand'] = (size_lines_entry.register(testVal), '%P','%d')
size_lines_entry.place(x=340,y=330,width=48,height=30)

click = Button(window, text = "Построение", command = plotting)
click.place(x=30,y=470,width=124,height=46)

label = Label(window, font = LARGE_FONT, bg = "white")
#label.place(x=440,y=110)
#label.grid(row=10, column=14, columnspan=17, padx=10, pady=15, sticky=S+N)

#time = 0
label_time = Label(window, text = "Время: ", font = LARGE_FONT, bg = "white")
label_time.place(x=30,y=390)
time_textbox = Entry(window, width=7, bg="gainsboro", selectbackground='black', validate="key")
time_textbox['validatecommand'] = (time_textbox.register(testVal), '%P','%d')
time_textbox.place(x=110,y=390,width=48,height=30)
#time_label = Label(window, text = time, font = LARGE_FONT, bg = "white")
#time_label.place(x=230,y=390)
#time_plus = Button(window, text = "+", command = time_plus)
#time_plus.place(x=300,y=390,width=67,height=30)
#time_minus = Button(window, text = "-", command = time_minus)
#time_minus.place(x=120,y=390,width=67,height=30)

label_color1 = Label(window, text = "Магнитное поле", foreground="blue", font = LARGE_FONT, bg = "white")
label_color1.place(x=535, y=20)
label_color2 = Label(window, text = "Электрическое поле", foreground="red", font = LARGE_FONT, bg = "white")
label_color2.place(x=690,y=20)

fig = figure (figsize = (6,5), facecolor = "white")

canvas = FigureCanvasTkAgg(fig, master = window)
canvas.get_tk_widget().place(x=510, y=95)
label_warning = Label(window, text = "Сплошной линией показано движение по часовой стрелке \n Пунктирной линией показано движение против часовой стрелки", font = LARGE_FONT, bg = "white")
label_warning.place(x=400, y=490)

window.mainloop()