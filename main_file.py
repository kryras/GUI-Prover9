from proverdict import dictionary, rm_list

import os
import _thread
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog

# zmienne globalne (stan programu)
file_name = ''
file_path = ''
fof_prover9_rb = False
prover9_rb = False


class GuiMain:
    def open_file(self):
        self.main_changing_status_label.config(text='Wczytywanie pliku wejściowego.')
        txt_file = tkinter.filedialog.askopenfilename(filetypes=(("Wejście Prover9", "*.in"),
                                                                 ("Pliki tekstowe", "*.txt"),
                                                                 ("Wszystkie pliki", "*.*")),
                                                      initialdir='Przykłady')
        if txt_file:

            self.input_text1.delete(1.0, tk.END)
            self.input_text2.delete(1.0, tk.END)
            self.input_text3.delete(1.0, tk.END)
            with open(txt_file) as _file:
                self.input_text1.insert(1.0, _file.read())
                global file_name
                file_name = txt_file[txt_file.rfind('/') + 1:txt_file.rfind('.'):]
                global file_path
                file_path = txt_file[:txt_file.rfind('/') + 1:]
                self.input_text1.edit_modified(False)
                _file.close()
                status_label = 'Wczytano plik wejściowy "' + file_name + '".'
                self.main_changing_status_label.config(text=status_label)
        else:
            self.main_changing_status_label.config(text='')

        file_name2 = file_name + '2.in'
        file2_path = file_path + file_name2
        txt_file2 = Path(file2_path)
        if txt_file2.is_file():
            txt_file2 = open(file2_path, 'r')
            if txt_file2 is not None:
                self.input_text2.insert(1.0, txt_file2.read())
                self.input_text2.edit_modified(False)
                txt_file2.close()

        file_name3 = file_name + '3.in'
        file3_path = file_path + file_name3
        txt_file3 = Path(file3_path)
        if txt_file3.is_file():
            txt_file3 = open(file3_path, 'r')
            if txt_file3 is not None:
                self.input_text3.insert(1.0, txt_file3.read())
                self.input_text3.edit_modified(False)
                txt_file3.close()

    def save_file_output(self):
        self.main_changing_status_label.config(text='Zapisywanie wyjścia jako...')
        file = tkinter.filedialog.asksaveasfile(mode='w',
                                                initialdir='Przykłady',
                                                defaultextension="*.*",
                                                initialfile='nazwa_pliku.out',
                                                filetypes=(("Wyjście Prover9", "*.out"),
                                                           ("Plik tekstowy", "*.txt")))
        if file is not None:
            data = self.output_text.get('1.0', tk.END + '-1c')
            file_output_path = file.name
            file_name_output = file_output_path[file_output_path.rfind('/') + 1:file_output_path.rfind('.'):]
            file_output_path = file_output_path[:file_output_path.rfind('/') + 1:]
            file.write(data)
            file.close()
            status_label = 'Zapisano wyjście jako "' + file_name_output + '".'
            self.main_changing_status_label.config(text=status_label)

            if len(self.output_text_2.get('1.0', tk.END + '-1c')) != 0:
                file_name_output2 = file_name_output + '_DOWÓD.out'
                file2_output_path = file_output_path + file_name_output2
                file2 = open(file2_output_path, 'w')
                if file2 is not None:
                    data2 = self.output_text_2.get('1.0', tk.END + '-1c')
                    file2.write(data2)
                    file2.close()
        else:
            self.main_changing_status_label.config(text='')

    def save_file_as_input(self):
        self.main_changing_status_label.config(text='Zapisywanie wejścia jako...')
        file = tkinter.filedialog.asksaveasfile(mode='w',
                                                defaultextension="*.*",
                                                initialfile='nazwa_pliku.in',
                                                filetypes=(("Wejście Prover9", "*.in"),
                                                           ("Plik tekstowy", "*.txt")))
        if file is not None:
            data = self.input_text1.get('1.0', tk.END + '-1c')
            file.write(data)
            global file_name
            file_name_tmp = file.name
            global file_path
            file_path = file_name_tmp[:file_name_tmp.rfind('/') + 1:]
            file_name = file_name_tmp[file_name_tmp.rfind('/') + 1:file_name_tmp.rfind('.'):]
            self.input_text1.edit_modified(False)
            file.close()
            status_label = 'Zapisano wejście jako "' + file_name + '".'
            self.main_changing_status_label.config(text=status_label)
        else:
            self.main_changing_status_label.config(text='')

        if len(self.input_text2.get('1.0', tk.END + '-1c')) != 0:
            file2_name = file_name + '2.in'
            file2_path = file_path + file2_name
            file2 = open(file2_path, 'w')
            if file2 is not None:
                data2 = self.input_text2.get('1.0', tk.END + '-1c')
                file2.write(data2)
                self.input_text2.edit_modified(False)
                file2.close()

        if len(self.input_text3.get('1.0', tk.END + '-1c')) != 0:
            file3_name = file_name + '3.in'
            file3_path = file_path + file3_name
            file3 = open(file3_path, 'w')
            if file3 is not None:
                data3 = self.input_text3.get('1.0', tk.END + '-1c')
                file3.write(data3)
                self.input_text3.edit_modified(False)
                file3.close()

    def save_changes_input(self):
        if len(file_name) != 0:
            if self.input_text1.edit_modified() == 1:
                file1_name = file_name + '.in'
                file1_path = file_path + file1_name
                file1 = open(file1_path, 'w')
                if file1 is not None:
                    data1 = self.input_text1.get('1.0', tk.END + '-1c')
                    file1.write(data1)
                    self.input_text1.edit_modified(False)
                    file1.close()
                    status_label = 'Zapisano zmiany w pliku "' + file1_name + '".'
                    self.main_changing_status_label.config(text=status_label)

            if self.input_text2.edit_modified() == 1:
                file2_name = file_name + '2.in'
                file2_path = file_path + file2_name
                if len(self.input_text2.get('1.0', tk.END + '-1c')) != 0:
                    file2 = open(file2_path, 'w')
                    if file2 is not None:
                        data2 = self.input_text2.get('1.0', tk.END + '-1c')
                        file2.write(data2)
                        self.input_text2.edit_modified(False)
                        file2.close()
                else:
                    self.input_text2.edit_modified(False)
                    file2 = Path(file2_path)
                    if file2.is_file():
                        os.remove(file2_path)

            if self.input_text3.edit_modified() == 1:
                file3_name = file_name + '3.in'
                file3_path = file_path + file3_name
                if len(self.input_text3.get('1.0', tk.END + '-1c')) != 0:
                    file3 = open(file3_path, 'w')
                    if file3 is not None:
                        data3 = self.input_text3.get('1.0', tk.END + '-1c')
                        file3.write(data3)
                        self.input_text3.edit_modified(False)
                        file3.close()
                else:
                    self.input_text3.edit_modified(False)
                    file3 = Path(file3_path)
                    if file3.is_file():
                        os.remove(file3_path)

        else:
            self.create_window_save_warning()

    def translate_input(self, input_text):
        tr_input = input_text.get('1.0', tk.END + '-1c')
        tr_input = tr_input.lower()
        tr_input = tr_input.split()

        for i in tr_input:
            if i in dictionary:
                tr_input[tr_input.index(i)] = dictionary[i]

        tr_input = [el for el in tr_input if el not in rm_list]

        for i, el in enumerate(tr_input):

            if el == '.':
                tr_input.insert(i + 1, '\n')

            if tr_input[i] == ' > ' and tr_input[i + 1] == ' | ' and tr_input[i + 2] == ' = ':
                tr_input[i] = ' >'
                tr_input[i + 1] = ''
                tr_input[i + 2] = '= '

            if tr_input[i] == ' < ' and tr_input[i + 1] == ' | ' and tr_input[i + 2] == ' = ':
                tr_input[i] = ' <'
                tr_input[i + 1] = ''
                tr_input[i + 2] = '= '

            if tr_input[i] == "." and i < len(tr_input) - 2 and tr_input[i + 2] == ' exist ':
                tr_input[i + 2] = 'exist '

            if tr_input[i] == "." and i < len(tr_input) - 2 and tr_input[i + 2] == ' all ':
                tr_input[i + 2] = 'all '

        tr_input = ''.join(tr_input)

        return tr_input

    def run_prover(self):
        if prover9_rb is False and fof_prover9_rb is False:
            self.create_window_select_prover()
            _thread.exit()
        else:
            self.run_prover_button.config(state='disable')
            self.main_changing_status_label.config(text='Przygotowywanie do uruchomienia provera.')
            global file_name
            tmp_file_name1 = ''
            tmp_file_name2 = ''
            tmp_file_name3 = ''
            file1_used = False
            file2_used = False
            file3_used = False
            self.output_text.delete(1.0, tk.END)
            self.output_text_2.delete(1.0, tk.END)

            prover_args = []
            if prover9_rb is True:
                prover_args = ['prover9', '-f']
            if fof_prover9_rb is True:
                prover_args = ['fof-prover9', '-f']

            if len(self.input_text1.get('1.0', tk.END + '-1c')) != 0:
                self.choose_prover_1.config(state='disable')
                self.choose_prover_2.config(state='disable')
                tmp_file_name1 = 'tmp1' + file_name + '.in'
                tmp_file1 = open(tmp_file_name1, 'w')
                if tmp_file1 is not None:
                    if self.is_checked.get() == 1:
                        input_tmp1 = self.translate_input(self.input_text1)
                    else:
                        input_tmp1 = self.input_text1.get('1.0', tk.END + '-1c')

                    tmp_file1.write(input_tmp1)
                    tmp_file1.close()
                    prover_args.append(tmp_file_name1)
                    file1_used = True
                else:
                    self.create_window_run_prover_file_err()

                if len(self.input_text2.get('1.0', tk.END + '-1c')) != 0:
                    tmp_file_name2 = 'tmp2' + file_name + '2.in'
                    tmp_file2 = open(tmp_file_name2, 'w')
                    if tmp_file2 is not None:
                        if self.is_checked.get() == 1:
                            input_tmp2 = self.translate_input(self.input_text2)
                        else:
                            input_tmp2 = self.input_text2.get('1.0', tk.END + '-1c')

                        tmp_file2.write(input_tmp2)
                        tmp_file2.close()
                        prover_args.append(tmp_file_name2)
                        file2_used = True
                    else:
                        self.create_window_run_prover_file_err()

                if len(self.input_text3.get('1.0', tk.END + '-1c')) != 0:
                    tmp_file_name3 = 'tmp3' + file_name + '3.in'
                    tmp_file3 = open(tmp_file_name3, 'w')
                    if tmp_file3 is not None:
                        if self.is_checked.get() == 1:
                            input_tmp3 = self.translate_input(self.input_text3)
                        else:
                            input_tmp3 = self.input_text3.get('1.0', tk.END + '-1c')

                        tmp_file3.write(input_tmp3)
                        tmp_file3.close()
                        prover_args.append(tmp_file_name3)
                        file3_used = True
                    else:
                        self.create_window_run_prover_file_err()

                self.main_changing_status_label.config(text='Uruchomiono prover. Trwa udowadnianie twierdzeń...')
                proc = subprocess.Popen(prover_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                output = proc.stdout.read()
                self.output_text.insert(1.0, output)

                tmp_output_file_name = 'tmp_out' + file_name + '.out'
                tmp_output_file = open(tmp_output_file_name, 'w')
                if tmp_output_file is not None:

                    output = self.output_text.get('1.0', tk.END + '-1c')
                    tmp_output_file.write(output)
                    tmp_output_file.close()
                else:
                    self.create_window_run_prover_file_err()

                proof_args = ['prooftrans', 'renumber', 'parents_only', '-f', str(tmp_output_file_name)]
                proc2 = subprocess.Popen(proof_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                output2 = proc2.stdout.read()
                self.output_text_2.insert(1.0, output2)

                os.remove(tmp_output_file_name)

                if file1_used is True:
                    os.remove(tmp_file_name1)
                if file2_used is True:
                    os.remove(tmp_file_name2)
                if file3_used is True:
                    os.remove(tmp_file_name3)

                self.choose_prover_1.config(state='enable')
                self.choose_prover_2.config(state='enable')
                self.run_prover_button.config(state='enable')
                self.main_changing_status_label.config(text='Prover zakończył działanie.')
                _thread.exit()
            else:
                self.create_window_run_prover_file_err()
                self.run_prover_button.config(state='enable')
                _thread.exit()

    def create_window_question(self):
        t = tk.Toplevel()
        t.resizable(0, 0)
        t.wm_title("Podstawowe informacje")
        img = tk.PhotoImage(file='prover9icon.png')
        t.tk.call('wm', 'iconphoto', t._w, img)
        lbl = ttk.Label(t,
                        text="Korzystając z translacji należy trzymać sie niżej wymienionych reguł"
                             "\n\n*Każda linia powinna być zakończona spacją i kropką"
                             "\n*Po każdym nawiasie (otwierającym i zamykającym) należy użyć spacji np.: ( x lub y )"
                             "\n*Wyrażenia opisujące założenia muszą znajdować się w wyrażenia ( założenia )"
                             "\n*Wyrażenia opisujące cele powinny znajdować się w wyrażenia ( cele )"
                             "\n*Tekst wpropwadzany w jezyku naturalnym może, ale nie musi zawierać polskich znaków."
                             "\nWymagana jest konsekwencja w pisowni - słowa zawierające kilka polskich znaków muszą"
                             " być w całości"
                             "\nnapisane z nimi, lub w całości napisane bez nich - błędne wprowadzenie: x równowazne "
                             "y", style='my.Label')
        lbl.pack(side="top", fill="both", expand=True, padx=100, pady=10)
        self.question_mark.config(state='disable')
        self.main_changing_status_label.config(text='Otwarto okno \"Podstawowe informacje\".')

        def quit_win():
            t.destroy()
            self.question_mark.config(state='normal')
            self.main_changing_status_label.config(text='')

        zamknij_button = ttk.Button(t, text='Zamknij', command=quit_win, style='my.TButton')
        zamknij_button.pack()
        t.protocol("WM_DELETE_WINDOW", quit_win)

    def create_window_table(self):
        t = tk.Toplevel()
        t.resizable(0, 0)
        t.wm_title("Tabela translacji")
        photo = tk.PhotoImage(file="tabela2.png")
        img = tk.PhotoImage(file='prover9icon.png')
        t.tk.call('wm', 'iconphoto', t._w, img)
        lbl = ttk.Label(t, image=photo)
        lbl.image = photo
        lbl.pack()
        self.table.config(state='disable')
        self.main_changing_status_label.config(text='Otwarto okno \"Tabela translacji\".')

        def quit_win():
            t.destroy()
            self.table.config(state='normal')
            self.main_changing_status_label.config(text='')

        zamknij_button = ttk.Button(t, text='Zamknij', command=quit_win, style='my.TButton')
        zamknij_button.pack()
        t.protocol("WM_DELETE_WINDOW", quit_win)

    def create_window_save_warning(self):
        t = tk.Toplevel()
        t.resizable(0, 0)
        t.wm_title("Błąd przy próbie zapisu")
        img = tk.PhotoImage(file='prover9icon_error.png')
        t.tk.call('wm', 'iconphoto', t._w, img)
        lbl = ttk.Label(t,
                        text="Aby zapisać zmiany najpiew musisz utworzyć plik wejściowy (opcja \"Zapisz jako...\")"
                             "\nlub wczytać istniejący plik (opcja \"Wczytaj\").", style='my.Label')
        lbl.pack(side="top", fill="both", expand=True, padx=100, pady=10)
        self.main_changing_status_label.config(text='Wystąpił problem przy zapisie.')

        def quit_win():
            t.destroy()

        zamknij_button = ttk.Button(t, text='Zamknij', command=quit_win, style='my.TButton')
        zamknij_button.pack()
        t.protocol("WM_DELETE_WINDOW", quit_win)

    def create_window_select_prover(self):
        t = tk.Toplevel()
        t.resizable(0, 0)
        t.wm_title("Nie wybrano metody przeprowadzania dowodu")
        img = tk.PhotoImage(file='prover9icon_warning.png')
        t.tk.call('wm', 'iconphoto', t._w, img)
        lbl = ttk.Label(t,
                        text="Zaznacz opcję \"1. Prover9\", aby skorzystać ze standardowego trybu Prover9"
                             "\nlub opcję \"2. FOF-Prover9\", aby skorzysać z trybu redukcji do wyrażeń "
                             "pierwszego rzędu",
                        style='my.Label')
        lbl.pack(side="top", fill="both", expand=True, padx=100, pady=10)

        def quit_win():
            t.destroy()

        zamknij_button = ttk.Button(t, text='Zamknij', command=quit_win, style='my.TButton')
        zamknij_button.pack()
        t.protocol("WM_DELETE_WINDOW", quit_win)

    def create_window_run_prover_file_err(self):
        t = tk.Toplevel()
        t.resizable(0, 0)
        t.wm_title("Błąd przy próbie uruchomienia Prover9")
        img = tk.PhotoImage(file='prover9icon_error.png')
        t.tk.call('wm', 'iconphoto', t._w, img)
        lbl = ttk.Label(t,
                        text="Nie udało się otworzyć plików wejściowych Prover9 lub brak formuł wejściowych. "
                             "\n\nSprawdź czy masz dostęp do tworzenia plików w katalogu z tą aplikacją"
                             "\nlub czy okno wprowadzania formuł jest wypełnione.", style='my.Label')
        lbl.pack(side="top", fill="both", expand=True, padx=100, pady=10)
        self.main_changing_status_label.config(text='Uruchamianie provera nie powiodło się.')

        def quit_win():
            t.destroy()

        zamknij_button = ttk.Button(t, text='Zamknij', command=quit_win, style='my.TButton')
        zamknij_button.pack()
        t.protocol("WM_DELETE_WINDOW", quit_win)

    def create_preview(self):
        if self.is_checked.get() == 1:
            self.main_changing_status_label.config(text='Otwarto podgląd translacji.')
            self.preview_button.config(state='enable')

            t = tk.Toplevel()
            t.resizable(0, 0)
            t.wm_title("Podgląd")
            img = tk.PhotoImage(file='prover9icon.png')
            t.tk.call('wm', 'iconphoto', t._w, img)

            # miejsce na zakladki
            tabs_preview = ttk.Notebook(t)
            tabs_preview.grid(row=0, column=0, sticky='news')

            # zakladka 1
            page1 = ttk.Frame(tabs_preview)
            tabs_preview.add(page1, text='Plik główny')
            podglad_text1 = tk.Text(page1, width=80, height=10)
            podglad_text1.grid(column=0, row=2, sticky="news")
            podglad_scroll1 = ttk.Scrollbar(page1, command=podglad_text1.yview)
            podglad_scroll1.grid(column=3, row=2, sticky='news')
            podglad_text1['yscrollcommand'] = podglad_scroll1.set

            # zakladka 2
            page2 = ttk.Frame(tabs_preview)
            tabs_preview.add(page2, text='Plik 2')
            podglad_text2 = tk.Text(page2, width=80, height=10)
            podglad_text2.grid(column=0, row=2, sticky="news")
            podglad_scroll2 = ttk.Scrollbar(page2, command=podglad_text2.yview)
            podglad_scroll2.grid(column=3, row=2, sticky='news')
            podglad_text2['yscrollcommand'] = podglad_scroll2.set

            # zakladka 3
            page3 = ttk.Frame(tabs_preview)
            tabs_preview.add(page3, text='Plik 2')
            podglad_text3 = tk.Text(page3, width=80, height=10)
            podglad_text3.grid(column=0, row=2, sticky="news")
            podglad_scroll3 = ttk.Scrollbar(page3, command=podglad_text3.yview)
            podglad_scroll3.grid(column=3, row=2, sticky='news')
            podglad_text3['yscrollcommand'] = podglad_scroll3.set

            self.preview_button.config(state='disable')
            self.translate_checkbutton.config(state='disabled')

            def quit_win():
                t.destroy()
                self.preview_button.config(state='normal')
                self.translate_checkbutton.config(state='active')
                self.main_changing_status_label.config(text='')

            preview_button_close = ttk.Button(t, text='Zamknij', command=quit_win, style='my.TButton')
            preview_button_close.grid(column=0, row=3, pady=5)
            t.protocol("WM_DELETE_WINDOW", quit_win)

            tr_input1 = self.translate_input(self.input_text1)
            podglad_text1.delete(1.0, tk.END)
            podglad_text1.insert(tk.END, tr_input1)

            tr_input2 = self.translate_input(self.input_text2)
            podglad_text2.delete(1.0, tk.END)
            podglad_text2.insert(tk.END, tr_input2)

            tr_input3 = self.translate_input(self.input_text3)
            podglad_text3.delete(1.0, tk.END)
            podglad_text3.insert(tk.END, tr_input3)

    def create_window_about_program(self):
        t = tk.Toplevel()
        t.resizable(0, 0)
        t.wm_title("O programie")
        img = tk.PhotoImage(file='prover9icon.png')
        t.tk.call('wm', 'iconphoto', t._w, img)
        lbl = ttk.Label(t,
                        text="Program został stworzony na potrzeby laboratorium: Techniki kompilacji"
                             "\nDo stworzenia programu użyto Python 3.6 oraz Prover9"
                             "\n\nAutorzy: Kacper Onak, Krystian Rasławski"
                             , style='my.Label')
        lbl.pack(side="top", fill="both", expand=True, padx=100, pady=10)
        self.main_changing_status_label.config(text='Otwarto okno \"O programie\".')

        def quit_win():
            t.destroy()

        zamknij_button = ttk.Button(t, text='Zamknij', command=quit_win, style='my.TButton')
        zamknij_button.pack()
        t.protocol("WM_DELETE_WINDOW", quit_win)
        
    def click(self):
        if self.is_checked.get() == 1:
            self.preview_button.config(state='enable')
        else:
            self.preview_button.config(state='disable')

    def click_radio(self):
        global fof_prover9_rb
        global prover9_rb
        if self.is_checked_radio.get() == 1:  # wybor pelnej wersji
            self.main_changing_status_label.config(text="Wybrano opcję Prover9")
            prover9_rb = True
            fof_prover9_rb = False

        else:  # wybor wersji skroconej
            self.main_changing_status_label.config(text="Wybrano opcję FOF-Prover9")
            prover9_rb = False
            fof_prover9_rb = True

    def click_radio_prover9(self):
        global fof_prover9_rb
        global prover9_rb
        self.is_checked_radio.set(1)
        self.main_changing_status_label.config(text="Wybrano opcję Prover9")
        prover9_rb = True
        fof_prover9_rb = False

    def click_radio_fofprover9(self):
        global fof_prover9_rb
        global prover9_rb
        self.is_checked_radio.set(2)
        self.main_changing_status_label.config(text="Wybrano opcję FOF-Prover9")
        prover9_rb = False
        fof_prover9_rb = True

    def __init__(self, root):
        root.title('GUI Prover9')
        root.geometry('860x600')
        root.resizable(0, 0)

        # ikonka na linuxie
        img = tk.PhotoImage(file='prover9icon.png')
        root.tk.call('wm', 'iconphoto', root._w, img)

        s = ttk.Style()
        s.configure('my.TButton', font=('Helvetica', 12), width=12)
        s.configure('my.Label', font=('Helvetica', 12))
        s.configure('myB.Label', font=('Helvetica', 14))

        frame_top = ttk.Frame(root, width='800', height='10')
        frame_top.pack(side='top')

        frame_left = ttk.Frame(root, width='800', height='540')
        frame_left.pack(side='left', padx=20, pady=20)

        frame_right = ttk.Frame(root, width='470', height='540')
        frame_right.pack(side='right', padx=20)

        # menu
        menubar = tk.Menu(root)
        # tworzenie wysuwanego menu i dodanie do paska menu
        filemenu = tk.Menu(menubar, tearoff=0, disabledforeground='black')
        filemenu.add_command(label="Wejście provera", state='disabled')
        filemenu.add_command(label="   Wczytaj plik(i)", command=self.open_file)
        filemenu.add_command(label="   Zapisz jako...", command=self.save_file_as_input)
        filemenu.add_command(label="   Zapisz zmiany", command=self.save_changes_input)
        filemenu.add_separator()
        filemenu.add_command(label="Wyjście provera", state='disabled')
        filemenu.add_command(label="   Zapisz jako...", command=self.save_file_output)
        filemenu.add_separator()
        filemenu.add_command(label="Zamknij...", command=root.quit)
        menubar.add_cascade(label="Plik", menu=filemenu)

        editmenu = tk.Menu(menubar, tearoff=0, disabledforeground='black')
        editmenu.add_command(label="Uruchom", command=lambda: _thread.start_new_thread(self.run_prover, ()))
        editmenu.add_radiobutton(label="Prover9", command=self.click_radio_prover9)
        editmenu.add_radiobutton(label="FOF-Prover9", command=self.click_radio_fofprover9)
        editmenu.add_separator()
        editmenu.add_command(label="Podgląd wejścia", command=self.create_preview)
        menubar.add_cascade(label="Uruchom", menu=editmenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Pomoc programu GUI Prover 9", command=self.create_window_question)
        helpmenu.add_command(label="Tabela translacji", command=self.create_window_table)
        helpmenu.add_separator()
        helpmenu.add_command(label="O programie...", command=self.create_window_about_program)
        menubar.add_cascade(label="Pomoc", menu=helpmenu)

        # wyświetlenie menu
        root.config(menu=menubar)

        # miejsce na zakladki (pliki wejściowe)
        tabs = ttk.Notebook(frame_left)
        tabs.grid(row=2, column=0, columnspan=4, sticky='news')

        # zakladka 1
        page1 = ttk.Frame(tabs)
        tabs.add(page1, text='Plik główny')

        self.input_text1 = tk.Text(page1, width=100, height=12)
        self.input_text1.grid(column=0, row=2, sticky="news")

        self.input_scroll1 = ttk.Scrollbar(page1, command=self.input_text1.yview)
        self.input_scroll1.grid(column=3, row=2, sticky='news')
        self.input_text1['yscrollcommand'] = self.input_scroll1.set

        # zakladka 2
        page2 = ttk.Frame(tabs)
        tabs.add(page2, text='Plik 2')

        self.input_text2 = tk.Text(page2, width=100, height=12)
        self.input_text2.grid(column=0, row=2, sticky="news")

        self.input_scroll2 = ttk.Scrollbar(page2, command=self.input_text2.yview)
        self.input_scroll2.grid(column=3, row=2, sticky='news')
        self.input_text2['yscrollcommand'] = self.input_scroll2.set

        # zakladka 3
        page3 = ttk.Frame(tabs)
        tabs.add(page3, text='Plik 3')

        self.input_text3 = tk.Text(page3, width=100, height=12)
        self.input_text3.grid(column=0, row=2, sticky="news")

        self.input_scroll3 = ttk.Scrollbar(page3, command=self.input_text3.yview)
        self.input_scroll3.grid(column=3, row=2, sticky='news')
        self.input_text3['yscrollcommand'] = self.input_scroll3.set

        # miejsce na zakladki (pliki wyjsciowe)
        tabs_out = ttk.Notebook(frame_left)
        tabs_out.grid(row=5, column=0, columnspan=4, sticky='news')

        # wyjscie provera
        page1_out = ttk.Frame(tabs_out)
        tabs_out.add(page1_out, text='Pełne wyjście provera')

        self.output_text = tk.Text(page1_out, width=100, height=12)
        self.output_text.grid(column=0, row=5, sticky="news")

        self.output_scroll = ttk.Scrollbar(page1_out, command=self.output_text.yview)
        self.output_scroll.grid(column=3, row=5, sticky='news')
        self.output_text['yscrollcommand'] = self.output_scroll.set

        # skrocone wyjscie
        page2_out = ttk.Frame(tabs_out)
        tabs_out.add(page2_out, text='Skrócone wyjście - dowód')

        self.output_text_2 = tk.Text(page2_out, width=100, height=12)
        self.output_text_2.grid(column=0, row=5, sticky="news")

        self.output_scroll_2 = ttk.Scrollbar(page2_out, command=self.output_text_2.yview)
        self.output_scroll_2.grid(column=3, row=5, sticky='news')
        self.output_text_2['yscrollcommand'] = self.output_scroll_2.set

        # przyciski pod napisem "Wejscie prover"
        self.load_input_button = ttk.Button(root, text='Wczytaj', command=self.open_file, style='my.TButton')
        self.load_input_button.place(x=20, y=28)
        self.save_as_input_button = ttk.Button(root, text='Zapisz jako...', command=self.save_file_as_input,
                                               style='my.TButton')
        self.save_as_input_button.place(x=140, y=28)
        self.save_changes_button = ttk.Button(root, text='Zapisz zmiany', command=self.save_changes_input,
                                              style='my.TButton')
        self.save_changes_button.place(x=260, y=28)

        # przycisk pod wyjsciem provera
        self.save_as_output_button = ttk.Button(root, text='Zapisz jako...', command=self.save_file_output,
                                                style='my.TButton')
        self.save_as_output_button.place(x=720, y=550)

        # Podglad
        self.preview_button = ttk.Button(root, text='Podgląd', command=self.create_preview, style='my.TButton',
                                         state='disable')
        self.preview_button.place(x=525, y=54)

        # Radiobuttony
        self.is_checked_radio = tk.IntVar()
        self.choose_prover_1 = ttk.Radiobutton(root, text='1. Prover9', variable=self.is_checked_radio, value=1,
                                               command=self.click_radio)
        self.choose_prover_1.place(x=426, y=10)
        self.choose_prover_2 = ttk.Radiobutton(root, text='2. FOF-Prover9', variable=self.is_checked_radio, value=2,
                                               command=self.click_radio)
        self.choose_prover_2.place(x=426, y=30)

        # Checkbox do podgladu
        self.is_checked = tk.IntVar()
        self.translate_checkbutton = tk.Checkbutton(root, variable=self.is_checked, command=self.click)
        self.translate_checkbutton.place(x=446, y=57, anchor='ne')
        self.checkbutton_text = ttk.Label(root, text="Tłumacz", style='my.Label')
        self.checkbutton_text.place(x=510, y=59, anchor='ne')

        # Tabela
        self.table = ttk.Button(root, command=self.create_window_table)
        self.table.place(x=831, y=0, anchor="ne")

        self.image_table = tk.PhotoImage(file="tabela.png")
        self.table.config(image=self.image_table)
        self.table.image = self.image_table

        # Uruchom prover
        self.run_prover_button = ttk.Button(root, text='Uruchom',
                                            command=lambda: _thread.start_new_thread(self.run_prover, ()),
                                            style='my.TButton')
        self.run_prover_button.place(x=720, y=54)

        # pytajnik >>
        self.question_mark = ttk.Button(root, command=self.create_window_question)
        self.question_mark.place(x=860, y=0, anchor="ne")

        self.image_question_mark = tk.PhotoImage(file="pytajnik2.png")
        self.question_mark.config(image=self.image_question_mark)
        self.question_mark.image2 = self.image_question_mark

        # napisy nad oknami
        self.main_input_label = ttk.Label(root, text="Wejście provera", style='myB.Label')
        self.main_input_label.place(x=20, y=4)

        self.main_output_label = ttk.Label(frame_left, text="Wyjście provera", style='myB.Label')
        self.main_output_label.grid(column=0, row=4, sticky="news", pady=10)

        # Status
        self.main_status_label = ttk.Label(root, text="Status: ")
        self.main_status_label.place(x=0, y=580)

        self.main_changing_status_label = ttk.Label(root, text="")
        self.main_changing_status_label.place(x=45, y=580)


def main():
    root = tk.Tk()
    app = GuiMain(root)
    root.mainloop()


