import string
import this
import time
import tkinter as tk

from click import command
from matplotlib.pyplot import text
import datetime as dt

from Controllers.AerationController import AerationController


class MainWindow(tk.Frame):
    def __init__(self, top):
        super().__init__()
        self.aeration_controller = None

        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        top.geometry("600x460+565+183")
        top.minsize(120, 1)
        top.maxsize(3844, 3221)
        top.resizable(1,  1)
        top.title("TP 1")
        top.configure(background="#172A3A")
        top.configure(cursor="arrow")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.top = top

        self.title = tk.Label(self.top)
        self.title.place(relx=0.05, rely=0.043, height=32, width=534)
        self.title.configure(activebackground="#f9f9f9")
        self.title.configure(activeforeground="black")
        self.title.configure(background="#172A3A")
        self.title.configure(compound='center')
        self.title.configure(disabledforeground="#a3a3a3")
        self.title.configure(font="-family {Ubuntu Mono} -size 18")
        self.title.configure(foreground="#74B3CE")
        self.title.configure(highlightbackground="#d9d9d9")
        self.title.configure(highlightcolor="black")
        self.title.configure(text='''Contrôle d’une porte d’aération d’une serre''')

        self.menubar = tk.Menu(top,font="TkMenuFont",bg='#ff4242',fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.temp_ambi_label = tk.Label(self.top)
        self.temp_ambi_label.place(relx=0.05, rely=0.196, height=22, width=204)
        self.temp_ambi_label.configure(activebackground="#f9f9f9")
        self.temp_ambi_label.configure(activeforeground="black")
        self.temp_ambi_label.configure(anchor='w')
        self.temp_ambi_label.configure(background="#172A3A")
        self.temp_ambi_label.configure(compound='left')
        self.temp_ambi_label.configure(disabledforeground="#a3a3a3")
        self.temp_ambi_label.configure(font="-family {Ubuntu Mono} -size 13 -weight bold")
        self.temp_ambi_label.configure(foreground="#74B3CE")
        self.temp_ambi_label.configure(highlightbackground="#d9d9d9")
        self.temp_ambi_label.configure(highlightcolor="black")
        self.temp_ambi_label.configure(text='''Température ambiante:''')

        self.dist_ouvert_label = tk.Label(self.top)
        self.dist_ouvert_label.place(relx=0.05, rely=0.261, height=22, width=314)

        self.dist_ouvert_label.configure(activebackground="#f9f9f9")
        self.dist_ouvert_label.configure(activeforeground="black")
        self.dist_ouvert_label.configure(anchor='w')
        self.dist_ouvert_label.configure(background="#172A3A")
        self.dist_ouvert_label.configure(compound='left')
        self.dist_ouvert_label.configure(disabledforeground="#a3a3a3")
        self.dist_ouvert_label.configure(font="-family {Ubuntu Mono} -size 13 -weight bold")
        self.dist_ouvert_label.configure(foreground="#74B3CE")
        self.dist_ouvert_label.configure(highlightbackground="#d9d9d9")
        self.dist_ouvert_label.configure(highlightcolor="black")
        self.dist_ouvert_label.configure(text='''Distance d’ouverture de la porte :''')

        self.controle_label = tk.Label(self.top)
        self.controle_label.place(relx=0.05, rely=0.348, height=22, width=204)
        self.controle_label.configure(activebackground="#f9f9f9")
        self.controle_label.configure(activeforeground="black")
        self.controle_label.configure(anchor='w')
        self.controle_label.configure(background="#172A3A")
        self.controle_label.configure(compound='left')
        self.controle_label.configure(disabledforeground="#a3a3a3")
        self.controle_label.configure(font="-family {Ubuntu Mono} -size 13 -weight bold -underline 1")
        self.controle_label.configure(foreground="#74B3CE")
        self.controle_label.configure(highlightbackground="#d9d9d9")
        self.controle_label.configure(highlightcolor="black")
        self.controle_label.configure(text='''Contrôle :''')

        self.motor_direction_label = tk.Label(self.top)
        self.motor_direction_label.place(relx=0.05, rely=0.717, height=22
                , width=104)
        self.motor_direction_label.configure(activebackground="#f9f9f9")
        self.motor_direction_label.configure(activeforeground="black")
        self.motor_direction_label.configure(anchor='w')
        self.motor_direction_label.configure(background="#172A3A")
        self.motor_direction_label.configure(compound='left')
        self.motor_direction_label.configure(disabledforeground="#a3a3a3")
        self.motor_direction_label.configure(font="-family {Ubuntu Mono} -size 13 -weight bold")
        self.motor_direction_label.configure(foreground="#74B3CE")
        self.motor_direction_label.configure(highlightbackground="#d9d9d9")
        self.motor_direction_label.configure(highlightcolor="black")
        self.motor_direction_label.configure(text='''Direction:''')

        self.motor_direction_text = tk.Label(self.top)
        self.motor_direction_text.place(relx=0.217, rely=0.717, height=22
                , width=154)
        self.motor_direction_text.configure(activebackground="#f9f9f9")
        self.motor_direction_text.configure(activeforeground="black")
        self.motor_direction_text.configure(anchor='w')
        self.motor_direction_text.configure(background="#172A3A")
        self.motor_direction_text.configure(compound='left')
        self.motor_direction_text.configure(disabledforeground="#a3a3a3")
        self.motor_direction_text.configure(font="-family {Ubuntu Mono} -size 13 -weight bold")
        self.motor_direction_text.configure(foreground="#74B3CE")
        self.motor_direction_text.configure(highlightbackground="#d9d9d9")
        self.motor_direction_text.configure(highlightcolor="black")
        self.motor_direction_text.configure(text='''MOTOR_DIRECTION''')

        self.pourcentage_ouvert_porte_label = tk.Label(self.top)
        self.pourcentage_ouvert_porte_label.place(relx=0.517, rely=0.348
                , height=62, width=134)
        self.pourcentage_ouvert_porte_label.configure(activebackground="#f9f9f9")
        self.pourcentage_ouvert_porte_label.configure(activeforeground="black")
        self.pourcentage_ouvert_porte_label.configure(background="#172A3A")
        self.pourcentage_ouvert_porte_label.configure(compound='left')
        self.pourcentage_ouvert_porte_label.configure(disabledforeground="#a3a3a3")
        self.pourcentage_ouvert_porte_label.configure(font="-family {Ubuntu Mono} -size 11 -weight bold")
        self.pourcentage_ouvert_porte_label.configure(foreground="#74B3CE")
        self.pourcentage_ouvert_porte_label.configure(highlightbackground="#d9d9d9")
        self.pourcentage_ouvert_porte_label.configure(highlightcolor="black")
        self.pourcentage_ouvert_porte_label.configure(justify='left')
        self.pourcentage_ouvert_porte_label.configure(text='''Pourcentage d'ouverture de la porte:''')
        self.pourcentage_ouvert_porte_label.configure(wraplength="120")

        self.pourcentage_ouvert_porte_text = tk.Label(self.top)
        self.pourcentage_ouvert_porte_text.place(relx=0.65, rely=0.457, height=52
                , width=150)
        self.pourcentage_ouvert_porte_text.configure(activebackground="#f9f9f9")
        self.pourcentage_ouvert_porte_text.configure(activeforeground="black")
        self.pourcentage_ouvert_porte_text.configure(background="#172A3A")
        self.pourcentage_ouvert_porte_text.configure(compound='left')
        self.pourcentage_ouvert_porte_text.configure(disabledforeground="#a3a3a3")
        self.pourcentage_ouvert_porte_text.configure(font="-family {Ubuntu Mono} -size 20 -weight bold")
        self.pourcentage_ouvert_porte_text.configure(foreground="#74B3CE")
        self.pourcentage_ouvert_porte_text.configure(highlightbackground="#d9d9d9")
        self.pourcentage_ouvert_porte_text.configure(highlightcolor="black")
        self.pourcentage_ouvert_porte_text.configure(justify='left')
        self.pourcentage_ouvert_porte_text.configure(text='''0%''')
        self.pourcentage_ouvert_porte_text.configure(wraplength="150")

        self.motor_speed_label = tk.Label(self.top)
        self.motor_speed_label.place(relx=0.583, rely=0.717, height=52, width=84)

        self.motor_speed_label.configure(activebackground="#f9f9f9")
        self.motor_speed_label.configure(activeforeground="black")
        self.motor_speed_label.configure(anchor='w')
        self.motor_speed_label.configure(background="#172A3A")
        self.motor_speed_label.configure(compound='left')
        self.motor_speed_label.configure(disabledforeground="#a3a3a3")
        self.motor_speed_label.configure(font="-family {Ubuntu Mono} -size 13 -weight bold")
        self.motor_speed_label.configure(foreground="#74B3CE")
        self.motor_speed_label.configure(highlightbackground="#d9d9d9")
        self.motor_speed_label.configure(highlightcolor="black")
        self.motor_speed_label.configure(text='''Vitesse:''')

        self.motor_speed_text = tk.Label(self.top)
        self.motor_speed_text.place(relx=0.717, rely=0.717, height=22, width=154)

        self.motor_speed_text.configure(activebackground="#f9f9f9")
        self.motor_speed_text.configure(activeforeground="black")
        self.motor_speed_text.configure(anchor='w')
        self.motor_speed_text.configure(background="#172A3A")
        self.motor_speed_text.configure(compound='left')
        self.motor_speed_text.configure(disabledforeground="#a3a3a3")
        self.motor_speed_text.configure(font="-family {Ubuntu Mono} -size 13 -weight bold")
        self.motor_speed_text.configure(foreground="#74B3CE")
        self.motor_speed_text.configure(highlightbackground="#d9d9d9")
        self.motor_speed_text.configure(highlightcolor="black")
        self.motor_speed_text.configure(text='''0 tour/min''')

        self.show_log_button = tk.Button(self.top)
        self.show_log_button.place(relx=0.4, rely=0.804, height=44, width=127)
        self.show_log_button.configure(activebackground="#ffffff")
        self.show_log_button.configure(activeforeground="#000000")
        self.show_log_button.configure(background="#508991")
        self.show_log_button.configure(compound='left')
        self.show_log_button.configure(cursor="hand2")
        self.show_log_button.configure(disabledforeground="#a3a3a3")
        self.show_log_button.configure(font="-family {Segoe UI} -size 10 -weight bold")
        self.show_log_button.configure(foreground="#172A3A")
        self.show_log_button.configure(highlightbackground="#d9d9d9")
        self.show_log_button.configure(highlightcolor="black")
        self.show_log_button.configure(pady="0")
        self.show_log_button.configure(text='''Afficher les logs''')
        self.show_log_button.configure(command=self.on_click_show_logs)


        self.auto_button = tk.Button(self.top)
        self.auto_button.place(relx=0.15, rely=0.413, height=34, width=117)
        self.auto_button.configure(activebackground="#ffffff")
        self.auto_button.configure(activeforeground="#000000")
        self.auto_button.configure(background="#508991")
        self.auto_button.configure(compound='left')
        self.auto_button.configure(cursor="hand2")
        self.auto_button.configure(disabledforeground="#a3a3a3")
        self.auto_button.configure(font="-family {Segoe UI} -size 8 -weight bold")
        self.auto_button.configure(foreground="#172A3A")
        self.auto_button.configure(highlightbackground="#d9d9d9")
        self.auto_button.configure(highlightcolor="black")
        self.auto_button.configure(pady="0")
        self.auto_button.configure(text='''Automatique''')
        self.auto_button.configure(command=self.on_click_automatic)

        self.manual_button = tk.Button(self.top)
        self.manual_button.place(relx=0.15, rely=0.5, height=34, width=77)
        self.manual_button.configure(activebackground="#ffffff")
        self.manual_button.configure(activeforeground="#000000")
        self.manual_button.configure(background="#508991")
        self.manual_button.configure(compound='left')
        self.manual_button.configure(cursor="hand2")
        self.manual_button.configure(disabledforeground="#a3a3a3")
        self.manual_button.configure(font="-family {Segoe UI} -size 8 -weight bold")
        self.manual_button.configure(foreground="#172A3A")
        self.manual_button.configure(highlightbackground="#d9d9d9")
        self.manual_button.configure(highlightcolor="black")
        self.manual_button.configure(pady="0")
        self.manual_button.configure(text='''Manuel''')
        self.manual_button.configure(command=self.on_click_manual)

        self.open_door_button = tk.Button(self.top)
        self.open_door_button.place(relx=0.05, rely=0.587, height=34, width=97)
        self.open_door_button.configure(activebackground="#ffffff")
        self.open_door_button.configure(activeforeground="#000000")
        self.open_door_button.configure(background="#508991")
        self.open_door_button.configure(compound='left')
        self.open_door_button.configure(cursor="hand2")
        self.open_door_button.configure(disabledforeground="#a3a3a3")
        self.open_door_button.configure(font="-family {Segoe UI} -size 8 -weight bold")
        self.open_door_button.configure(foreground="#172A3A")
        self.open_door_button.configure(highlightbackground="#d9d9d9")
        self.open_door_button.configure(highlightcolor="black")
        self.open_door_button.configure(pady="0")
        self.open_door_button.configure(text='''Ouvrir la porte''')
        self.open_door_button.configure(command=self.open_full_door)

        self.close_door_button = tk.Button(self.top)
        self.close_door_button.place(relx=0.283, rely=0.587, height=34
                , width=97)
        self.close_door_button.configure(activebackground="#ffffff")
        self.close_door_button.configure(activeforeground="#000000")
        self.close_door_button.configure(background="#508991")
        self.close_door_button.configure(compound='left')
        self.close_door_button.configure(cursor="hand2")
        self.close_door_button.configure(disabledforeground="#a3a3a3")
        self.close_door_button.configure(font="-family {Segoe UI} -size 8 -weight bold")
        self.close_door_button.configure(foreground="#172A3A")
        self.close_door_button.configure(highlightbackground="#d9d9d9")
        self.close_door_button.configure(highlightcolor="black")
        self.close_door_button.configure(pady="0")
        self.close_door_button.configure(text='''Fermer la porte''')
        self.close_door_button.configure(command=self.close_full_door)

        self.manual_percentage_input = tk.Entry(self.top)
        self.manual_percentage_input.place(relx=0.3, rely=0.5, height=30
                , relwidth=0.09)
        self.manual_percentage_input.configure(background="#74B3CE")
        self.manual_percentage_input.configure(borderwidth="3")
        self.manual_percentage_input.configure(disabledforeground="#a3a3a3")
        self.manual_percentage_input.configure(font="-family {Ubuntu Mono} -size 11")
        self.manual_percentage_input.configure(foreground="#000000")
        self.manual_percentage_input.configure(highlightbackground="#d9d9d9")
        self.manual_percentage_input.configure(highlightcolor="black")
        self.manual_percentage_input.configure(insertbackground="black")
        self.manual_percentage_input.configure(selectbackground="blue")
        self.manual_percentage_input.configure(selectforeground="white")

        self.temp_ambi_text = tk.Label(self.top)
        self.temp_ambi_text.place(relx=0.383, rely=0.196, height=22, width=154)
        self.temp_ambi_text.configure(activebackground="#f9f9f9")
        self.temp_ambi_text.configure(activeforeground="black")
        self.temp_ambi_text.configure(anchor='w')
        self.temp_ambi_text.configure(background="#172A3A")
        self.temp_ambi_text.configure(compound='left')
        self.temp_ambi_text.configure(disabledforeground="#a3a3a3")
        self.temp_ambi_text.configure(font="-family {Ubuntu Mono} -size 13 -weight bold")
        self.temp_ambi_text.configure(foreground="#74B3CE")
        self.temp_ambi_text.configure(highlightbackground="#d9d9d9")
        self.temp_ambi_text.configure(highlightcolor="black")
        self.temp_ambi_text.configure(text='''99 °C''')

        self.motor_distance_text = tk.Label(self.top)
        self.motor_distance_text.place(relx=0.583, rely=0.261, height=22
                , width=154)
        self.motor_distance_text.configure(activebackground="#f9f9f9")
        self.motor_distance_text.configure(activeforeground="black")
        self.motor_distance_text.configure(anchor='w')
        self.motor_distance_text.configure(background="#172A3A")
        self.motor_distance_text.configure(compound='left')
        self.motor_distance_text.configure(disabledforeground="#a3a3a3")
        self.motor_distance_text.configure(font="-family {Ubuntu Mono} -size 13 -weight bold")
        self.motor_distance_text.configure(foreground="#74B3CE")
        self.motor_distance_text.configure(highlightbackground="#d9d9d9")
        self.motor_distance_text.configure(highlightcolor="black")
        self.motor_distance_text.configure(text='''999 cm''')

        self.set_manual_percentage_button = tk.Button(self.top)
        self.set_manual_percentage_button.place(relx=0.417, rely=0.5, height=34
                , width=47)
        self.set_manual_percentage_button.configure(activebackground="#ffffff")
        self.set_manual_percentage_button.configure(activeforeground="#000000")
        self.set_manual_percentage_button.configure(background="#508991")
        self.set_manual_percentage_button.configure(compound='left')
        self.set_manual_percentage_button.configure(cursor="hand2")
        self.set_manual_percentage_button.configure(disabledforeground="#a3a3a3")
        self.set_manual_percentage_button.configure(font="-family {Segoe UI} -size 8 -weight bold")
        self.set_manual_percentage_button.configure(foreground="#172A3A")
        self.set_manual_percentage_button.configure(highlightbackground="#d9d9d9")
        self.set_manual_percentage_button.configure(highlightcolor="black")
        self.set_manual_percentage_button.configure(pady="0")
        self.set_manual_percentage_button.configure(text='''Définir''')
        self.set_manual_percentage_button.configure(command=self.on_click_set_manual_percentage)

    # methode pour afficher les logs
    def open_log_window(self):
        self.new = tk.Toplevel(self.top)
        self.new.geometry("600x300")
        self.new.title("Logs")

        self.dateText = dt.datetime.now()
        self.timeText= time.strftime('%H:%M:%S')

        logs = self.aeration_controller.get_logs()

        print(len(logs))

        self.date_Log= tk.Label(self.new, text=f"{self.dateText:%A, %B %d, %Y} " + self.timeText, font=('-family {Ubuntu Mono} -size 13 -weight bold'))
        self.date_Log.place(relx=.05, rely=.15)

        '''
        self.labelframe_Logs= tk.LabelFrame(self.new, text=logs, fg="black", font="none 10 bold")\
            .grid(row=1, column=0, ipadx=230, ipady=200, sticky=tk.W)
        self.date_Log= tk.Label(self.new, text=f"{self.dateText:%A, %B %d, %Y} " + self.timeText, font=('-family {Ubuntu Mono} -size 13 -weight bold'))
        self.date_Log.place(relx=.05, rely=.15)
        self.distance_Log = tk.Label(self.new, text="Distance: %.2f cm"%self.distance, font=('-family {Ubuntu Mono} -size 13 -weight bold'))
        self.distance_Log.place(relx=.05, rely=.20)
        self.pourcentage_Log = tk.Label(self.new, text="Pourcentage d'ouverture de la porte: " + self.pourc + " %", font=('Helvetica 8 bold'))
        self.pourcentage_Log.place(relx=.05, rely=.25)
        self.temp_Log = tk.Label(self.new, text="Temperature: " + str(round(self.tempC))+ "°C", font=('Helvetica 8 bold'))
        self.temp_Log.place(relx=.05, rely=.30)
        self.mode_Log = tk.Label(self.new, text="Mode: " + self.modeMsg, font=('Helvetica 8 bold'))
        self.mode_Log.place(relx=.05, rely=.35)
        '''

    
    def set_controller(self, controller) -> None:
        """
        Set the controller
        :param controller:
        :return:
        """
        self.aeration_controller: AerationController = controller


    def on_click_manual(self) -> None:
        """
        Handle manual button click event
        :return:
        """
        self.aeration_controller.set_state('manual')

        self.aeration_controller.log('Door in manual mode.')


    def on_click_automatic(self):
        """
        Handle automatic button click event
        :return:
        """
        self.aeration_controller.set_state('automatic')

        self.aeration_controller.log('Door in automatic mode.')

    def on_click_set_manual_percentage(self):
        percentage = float(self.manual_percentage_input.get())
        self.aeration_controller.set_manual_percentage(percentage)

    def on_click_open_door(self):
        self.aeration_controller.set_manual_percentage(100)

    def on_click_open_door(self):
        self.aeration_controller.set_manual_percentage(0)

    def on_click_show_logs(self):
        self.open_log_window()

    def set_temp(self, temp):
        self.temp_ambi_text.configure(text= str(round(temp, 2)) + ' °C')

    def set_distance(self, distance):
        self.motor_distance_text.configure(text= str(round(distance, 2)) + ' cm')

    def set_open_door_percentage(self, percentage):
        self.pourcentage_ouvert_porte_text.configure(text= str(round(percentage, 2)) + ' %')

    def set_motor_direction(self, direction):
        self.motor_direction_text.configure(text=direction)

    def set_motor_speed(self, motor_speed: string):
        self.motor_speed_text.configure(text=motor_speed)

    def set_user_percentage_input(self, percentage: float):
        self.manual_percentage_input.delete(0, tk.END)
        self.manual_percentage_input.insert(0, str(percentage))
        
        if(self.aeration_controller):
            self.aeration_controller.log('Door in manual mode set to ' + str(percentage) + '.')

    def open_full_door(self):
        self.aeration_controller.set_manual_percentage(100)
        self.manual_percentage_input.delete(0, tk.END)
        self.manual_percentage_input.insert(0, 100)

        self.aeration_controller.log('Door full opened.')

    def close_full_door(self):
        self.aeration_controller.set_manual_percentage(55)
        self.manual_percentage_input.delete(0, tk.END)
        self.manual_percentage_input.insert(0, 55)

        self.aeration_controller.log('Door full closed.')
