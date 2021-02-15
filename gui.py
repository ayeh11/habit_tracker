from tkinter import *
import datetime
from calendar import monthrange
import csv
from tkinter import messagebox

root = Tk()
root.geometry("1000x800")

datatxt = "data.txt"
topictxt = "topics.txt"
fieldnames = ["date", "t1", "t2", "t3", "t4", "t5"]
datas = []

num_topics = 5
topic_choices = ["choice", "text", "number", "y/n"]
days = ["Sun", "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat"]
themes = ["modern", "cute", "greenery"]
theme = "modern"
colors = ["lightgrey", "lightblue", "white"]
emojis = []
emojitxt = "emojist.txt"

def read_topics():
    f = open(topictxt, "r")
    lines = []
    for line in f:
        li = line.replace("\n", "")
        lines.append(li)
    l = [line.split(",") for line in lines]
    ttypes = l[0]
    tnames = l[1]
    tformat = l[2]
    tinfo = []
    for i in range(len(l)-3):
        i += 3
        tinfo.append(l[i])
    f.close()

    return ttypes, tnames, tformat, tinfo


topictypes, topicsnames, topicformat, topicinfo = read_topics()


def update_topics():
    f = open(topictxt, "w")
    lines = []
    lists = [topictypes, topicsnames, topicformat]
    for l in lists:
        line = ",".join(l)
        lines.append(line)
    for s in topicinfo:
        line = ",".join(s)
        lines.append(line)
    for line in lines:
        f.write("{}\n".format(line))
    f.close()


def get_emojis():
    f = open(emojitxt, "r")
    for line in f:
        l = line.replace("\n", "")
        emojis.append(l)
    f.close()


def read_data():
    with open(datatxt, 'r') as f:
        reader = csv.DictReader(f)
        for line in reader:
            datas.append(line)


def update_data():
    with open(datatxt, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for thing in datas:
            writer.writerow(thing)


def is_int(n):
    try:
        int(n)
        return True
    except ValueError:
        return False


def reset(frame, rowscols):
    for child in frame.winfo_children():
        child.destroy()

    if rowscols:
        for i in range(10):
            frame.grid_rowconfigure(i, weight=0)
            frame.grid_columnconfigure(i, weight=0)


def get_today():
    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day
    return month, day, year


def get_first_and_total_days(year, month):
    dayofweek, totdays = monthrange(year, month)
    return dayofweek, totdays


def create_top_header(frame, month):
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=5)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=10)
    frame.grid_columnconfigure(2, weight=1)

    settings_but = Button(frame, text='settings', command=settings)
    settings_but.grid(row=0, column=2, sticky='nsew')

    x = datetime.datetime(2000, month, 1)
    Label(frame, text=x.strftime("%B"), font=("Arial", 40), anchor='w').grid(row=1, column=1, sticky='nsew')

    botframe = Frame(frame)
    botframe.grid(row=2, column=0, columnspan=3, sticky="ew")
    for d in range(len(days)):
        Label(botframe, text=days[d]).grid(row=0, column=d)
        botframe.grid_columnconfigure(d, weight=1)


def create_days(main_frame, first_day_of_month, totdays, today, boxwid):
    frames = []
    for t in range(1, totdays + 1):
        c = (t + first_day_of_month) % 7
        r = (t + first_day_of_month) // 7
        f = Frame(main_frame, width=boxwid, highlightbackground=colors[0], highlightthickness="1", bg=colors[2])
        f.grid(row=r, column=c, sticky='nsew')
        frames.append(f)
        f.grid_columnconfigure(0, weight=1)
        Label(f, text=t, anchor='n').grid(row=0, column=0, columnspan=4)

    frames[today - 1]["bg"] = colors[1]
    widgets_in_frames(frames)


# TODO: display the date data
def widgets_in_frames(frames):
    done = False
    fontsize = 15
    nspace = []
    cspace = []
    ynspace = []
    for d in range(len(datas)):
        for tf in range(len(topicformat)):
            if topicformat[tf] == "T":
                topicnum = int(topicformat[1])
                day = datas[d]['date'].split("-")
                reset(frames[int(day[1]) - 1], False)
                Label(frames[int(day[1])-1], text=day[1], anchor='n').grid(row=0, column=0, columnspan=4)
                text = "{}...".format(datas[d]['t{}'.format(topicnum+1)][0:20])
                Label(frames[int(day[1])-1], text=text, bg=topicinfo[topicnum]).grid(columnspan=4, rowspan=2)
                done = True
            elif not done:
                allminis = mini_frames(frames)
                if is_int(topicformat[tf]):
                    num = int(topicformat[tf])
                    type = topictypes[num]
                    if type == "number":
                        nspace.append((num, tf, d))
                    elif type == "choice":
                        cspace.append((num, tf, d))
                    elif type == "y/n":
                        ynspace.append((num, tf, d))

    for n in range(len(nspace)):
        num, space, d = nspace[n]
        text = datas[d]['t{}'.format(num + 1)]
        Label(allminis[d][space], text=text, font=("Arial", fontsize)).grid(sticky='e')
        Label(allminis[d][space + 1], text=topicinfo[num], font=("Arial", fontsize)).grid(sticky='w')

    for c in range(len(cspace)):
        num, space, d = cspace[c]
        text = datas[d]['t{}'.format(num + 1)]
        Label(allminis[d][space], text=text, font=("Arial", fontsize)).grid()

    for y in range(len(ynspace)):
        num, space, d = ynspace[y]
        text = datas[d]['t{}'.format(num + 1)]
        if text == "1":
            Label(allminis[d][space], text=topicinfo[num], font=("Arial", fontsize)).grid()


def mini_frames(frames):
    allminis = []
    for d in range(len(datas)):
        minis = []
        splitdate = datas[d]['date'].split("-")
        frame = frames[int(splitdate[1]) - 1]
        for r in range(2):
            frame.grid_rowconfigure(r + 1, weight=1)
            for c in range(4):
                frame.grid_columnconfigure(c, weight=1)
                f = Frame(frame)
                f.grid(row=r + 1, column=c, sticky='nsew')
                f.grid_columnconfigure(0, weight=1)
                f.grid_rowconfigure(0, weight=1)
                minis.append(f)
        allminis.append(minis)

    return allminis


def settings():
    reset(root, False)

    topframe = Frame(root)
    frame = Frame(root)
    leftframe = Frame(frame, highlightbackground=colors[0], highlightthickness="2")
    rightframe = Frame(frame, highlightbackground=colors[0], highlightthickness="2")

    root.grid_rowconfigure(1, weight=10)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=2)
    leftframe.grid_columnconfigure(0, weight=1)
    topframe.grid_columnconfigure(0, weight=1)
    topframe.grid_columnconfigure(1, weight=1)

    topframe.grid(row=0, column=0, sticky='nsew')
    frame.grid(row=1, column=0, sticky='nsew')
    leftframe.grid(row=0, column=0, sticky='nsew')
    rightframe.grid(row=0, column=1, sticky='nsew')

    Button(topframe, text="Home", padx=10, pady=10, command=main_screen).grid(row=0, column=1, sticky='ne')
    Label(topframe, text="Settings", font=("Arial", 40), padx=10).grid(row=1, column=0)

    topic_button = Button(leftframe, text='Topics', command=lambda: set_topics(rightframe), pady=10)
    format_button = Button(leftframe, text='Format', command=lambda: set_formatting(rightframe), pady=10)
    topic_button.grid(row=0, column=0, sticky='nsew')
    format_button.grid(row=1, column=0, sticky='nsew')


def set_topics(frame):
    reset(frame, True)

    frames = []
    entries = []
    options = []
    labels = []

    frame.grid_columnconfigure(1, weight=1)

    radio_var = IntVar()
    for i in range(num_topics):
        Radiobutton(frame, variable=radio_var, value=i).grid(row=i, column=0, sticky='n', pady=5)

        f = Frame(frame, highlightbackground=colors[1], highlightthickness="2")
        f.grid(row=i, column=1, sticky='nsew', columnspan=3)
        frames.append(f)

        frame.grid_rowconfigure(i, weight=1)
        f.grid_columnconfigure(1, weight=1)

        entry_var = StringVar()
        entry_var.set(topicsnames[i])
        Entry(f, textvariable=entry_var).grid(row=0, column=0, sticky='w')
        entries.append(entry_var)
        option_var = StringVar()
        option_var.set(topictypes[i])
        OptionMenu(f, option_var, *topic_choices).grid(row=0, column=1, padx=10, sticky='e')
        options.append(option_var)

    Button(frame, text="edit", command=lambda: edit_topics(frame, frames[radio_var.get()], radio_var.get(), options,
                                                           labels)).grid(row=num_topics, column=0, padx=10, sticky='w')
    Button(frame, text='Delete', command=lambda: deletetopic(radio_var.get(), frame)).grid(row=num_topics, column=1, sticky='w', pady=5, columnspan=2)
    Button(frame, text='Apply', command=lambda: applytopics(entries, options, frame)).grid(row=num_topics, column=2, pady=5)
    Button(frame, text='Cancel', command=settings).grid(row=num_topics, column=3, pady=5)


def edit_topics(frame, oneframe, num, options, labels):
    if len(labels) > 0:
        for a in labels:
            a.destroy()

    for i in range(num_topics):
        frame.grid_rowconfigure(i, weight=1)
    frame.grid_rowconfigure(num, weight=5)
    oneframe.grid_columnconfigure(1, weight=1)

    smallframe = Frame(oneframe)
    smallframe.grid(row=2, column=0, padx=10)
    labels.append(smallframe)

    type = options[num].get()
    newtopics = [0, 0, 0, 0, 0]
    if type == topic_choices[0]:  # choices
        evs = []
        ovs = []
        for i in range(5):
            l = Label(smallframe, text='_')
            l.grid(row=i, column=0)
            ev = StringVar()
            ov = StringVar()
            e = Entry(smallframe, textvariable=ev)
            e.grid(row=i, column=1)
            o = OptionMenu(smallframe, ov, *emojis)
            o.grid(row=i, column=2)
            labels.append(e)
            labels.append(o)
            evs.append(ev)
            ovs.append(ov)
            apply_but_in_sf(smallframe, num, labels, newtopics)
            try:
                ev.set(topicinfo[num][i])
                ov.set(topicinfo[num][i+5])
            except IndexError:
                ev.set("")
                ov.set("")

        newtopics[num] = (type, ovs, evs)
    elif type == topic_choices[1]:  # text
        ov = in_smallframe(smallframe, colors, 'choose a color: ', labels, num, newtopics)
        newtopics[num] = (type, ov)
    elif type == topic_choices[2]:  # num
        ov = in_smallframe(smallframe, emojis, 'choose an icon: ', labels, num, newtopics)
        newtopics[num] = (type, ov)
    elif type == topic_choices[3]:  # y/n
        ov = in_smallframe(smallframe, emojis, 'choose an icon: ', labels, num, newtopics)
        newtopics[num] = (type, ov)
    else:
        l = Label(oneframe, text="choose a type")
        l.grid(row=2, column=0, columnspan=2)
        labels.append(l)


def in_smallframe(smallframe, list, text, labels, num, newtopics):
    l = Label(smallframe, text=text)
    l.grid(row=0, column=0)
    ov = StringVar()
    o = OptionMenu(smallframe, ov, *list)
    o.grid(row=0, column=1)
    labels.append(l)
    labels.append(o)
    apply_but_in_sf(smallframe, num, labels, newtopics)

    try:
        ov.set(topicinfo[num][0])
    except IndexError:
        ov.set("")

    return ov


def apply_but_in_sf(smallframe, num, labels, newtopics):
    applybut = Button(smallframe, text="apply", command=lambda: apply_smallframe(num, newtopics))
    applybut.grid(row=8, column=1, sticky='se')
    labels.append(applybut)


# TODO: save the parts about each topic
def apply_smallframe(framenum, newtopics):
    if newtopics[framenum][0] == topic_choices[0]:
        os = []
        es = []
        newline = []
        for o in newtopics[framenum][1]:
            os.append(o.get())
        for e in newtopics[framenum][2]:
            es.append(e.get())
        newline += es
        newline += os
        topicinfo[framenum] = newline
    else:
        type, ov = newtopics[framenum]
        change = ov.get()
        topicinfo[framenum][0] = change
    update_topics()


# TODO: clear the topic
def deletetopic(framenum, frame):
    response = messagebox.askokcancel("WARNING", "Are you sure you want to delete the topic?")
    if response == 1:
        topictypes[framenum] = ""
        topicsnames[framenum] = ""
        topicinfo[framenum] = []
        set_topics(frame)
        update_topics()
    else:
        print("cancelled deletion")


# TODO: save what topicstypes there are
def applytopics(entries, options, frame):
    response = messagebox.askokcancel("WARNING", "Are you sure you want to apply new topics? "
                                                 "Changed data will be deleted")
    if response == 1:
        changed = []
        for e in range(len(entries)):
            if entries[e].get() != topicsnames[e] or options[e].get() != topictypes[e]:
                changed.append(e)
                topictypes[e] = options[e].get()
                topicsnames[e] = entries[e].get()
                topicinfo[e] = [""]
                for d in range(len(datas)):
                    datas[d][fieldnames[e]] = ""
                set_topics(frame)

        update_data()
        update_topics()
    else:
        print("cancelled applying")


def set_formatting(frame):
    reset(frame, True)

    frame.grid_rowconfigure(2, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    l = Label(frame, text='Theme: ')
    l.grid(row=0, column=0, padx=10, pady=20)
    ov = StringVar()
    ov.set(theme)
    OptionMenu(frame, ov, *themes).grid(row=0, column=1)
    Button(frame, text='apply', command= lambda: apply_theme(ov, frame)).grid(row=0, column=2)
    l2 = Label(frame, text='Format of calendar: ')
    l2.grid(row=1, column=0, padx=10, pady=20)

    window = Frame(frame, highlightbackground=colors[0], highlightthickness="2")
    window.grid(row=2, column=1, columnspan=2, sticky='nsew', padx=30, pady=(0, 30))

    window.grid_rowconfigure(0, weight=2)

    Label(window, text='1', font=("Arial", 20)).grid(row=0, column=0, columnspan=4)
    eightlabels = []
    i = -1
    for r in range(2):
        window.grid_rowconfigure(r + 1, weight=1)
        for c in range(4):
            i += 1
            window.grid_columnconfigure(c, weight=1)
            f = Frame(window, highlightbackground=colors[0], highlightthickness="1")
            f.grid(row=r + 1, column=c, sticky='nsew')
            f.grid_columnconfigure(0, weight=1)
            f.grid_rowconfigure(0, weight=1)
            label = Label(f, text=topicformat[i], font=("Arial", 30))
            label.grid(sticky='nsew')
            eightlabels.append(label)

    spaces = [0,0,0,0,0]
    cvs = []
    spaces_frame = Frame(frame)
    spaces_frame.grid(row=9, column=1)
    for i in range(num_topics):
        if topictypes[i] == topic_choices[0] or topictypes[i] == topic_choices[3]:
            spaces[i] = 1
        elif topictypes[i] == topic_choices[1]:
            spaces[i] = 8
        elif topictypes[i] == topic_choices[2]:
            spaces[i] = 2
        cv = IntVar()
        for t in topicformat:
            if t == str(i):
                cv.set(1)
        Checkbutton(frame, text='{}, {} spaces'.format(topicsnames[i], spaces[i]), variable=cv, command=
                    lambda: update_spaces(spaces_frame, cvs, spaces, eightlabels)).grid(row=3 + i, column=1)
        cvs.append(cv)


def update_spaces(frame, checklist, spaces, eightlabels):
    reset(frame, True)
    space = 0
    checkedcs = []
    for c in range(len(checklist)):
        if checklist[c].get() == 1:
            checkedcs.append(c)

    for check in checkedcs:
        space += spaces[check]

    spaceleft = 8 - space
    if spaceleft >= 0:
        l = Label(frame, text="Spaces left: {}".format(spaceleft))
        update_picture(checkedcs, spaces, eightlabels)
    else:
        l = Label(frame, text="Using too much space")
    l.grid(row=9, column=1)


def update_picture(checked, spaces, labels):
    global topicformat

    topicformat = ["","","","",
                   "","","",""]

    for c in range(len(topicformat)):
        if topicformat[c] == "":
            labels[c]['text'] = ""

    for check in checked:
        w = spaces[check]
        done = False
        if w == 1:
            for c in reversed(range(len(topicformat))):
                if topicformat[c] == "" and not done:
                    labels[c]['text'] = str(check)
                    topicformat[c] = str(check)
                    done = True
        elif w == 2:
            for c in reversed(range(len(topicformat))):
                if topicformat[c] == "" and topicformat[c-1] == "" and not done:
                    if c == 4:
                        c = 3
                    labels[c-1]['text'] = str(check)
                    labels[c]['text'] = "{}b".format(check)
                    topicformat[c-1] = str(check)
                    topicformat[c] = "{}b".format(check)
                    done = True
        elif w == 8:
            for l in labels:
                l['text'] = str(check)
                topicformat = ["T", str(check), str(check), str(check), str(check), str(check), str(check), str(check)]

    update_topics()


def apply_theme(ov, frame):
    global colors
    global theme
    theme = ov.get()
    if theme == themes[0]:
        colors = ["lightgrey", "lightblue", "white"]
    elif theme == themes[1]:
        colors = ["deeppink", "pink", "mistyrose"]
    elif theme == themes[2]:
        colors = ["darkseagreen", "seagreen", "DarkSeaGreen1"]
    else:
        colors = ["lightgrey", "lightblue", "white"]

    set_formatting(frame)


def daily_log(now_month, now_day, monthlength):
    reset(root, True)
    vars = []

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    frame = Frame(root)
    frame.grid(sticky='nsew')

    for r in range(3):
        frame.grid_columnconfigure(r, weight=1)

    Button(frame, text="Home", padx=10, pady=10, command=main_screen).grid(row=0, column=2, sticky='ne')
    dateframe = Frame(frame)
    dateframe.grid(row=0, column=0, columnspan=2)
    Label(dateframe, text='Log of').grid(row=0, column=0, pady=10)

    months = list(range(1, 13))
    days = list(range(1, monthlength + 1))
    month = StringVar()
    day = StringVar()
    month.set(now_month)
    day.set(now_day)
    OptionMenu(dateframe, month, *months).grid(row=0, column=1)
    OptionMenu(dateframe, day, *days).grid(row=0, column=3)
    Label(dateframe, text="-").grid(row=0, column=2)
    vars.append((month, day))

    for i in range(len(topicsnames)):
        Label(frame, text=topicsnames[i] + ":").grid(row=i + 1, column=0)
        if topictypes[i] == topic_choices[0]:
            choice = StringVar()
            listofchoices = topicinfo[i][-5:]
            OptionMenu(frame, choice, *listofchoices).grid(row=i + 1, column=1, columnspan=2)
            vars.append(choice)
        elif topictypes[i] == topic_choices[1]:
            text = StringVar()
            Entry(frame, textvariable=text).grid(row=i + 1, column=1, columnspan=2)
            vars.append(text)
        elif topictypes[i] == topic_choices[2]:
            num = StringVar()
            Entry(frame, textvariable=num).grid(row=i + 1, column=1, columnspan=2)
            vars.append(num)
        elif topictypes[i] == topic_choices[3]:
            yesno = IntVar()
            Checkbutton(frame, variable=yesno).grid(row=i + 1, column=1, columnspan=2)
            vars.append(yesno)
        else:
            print("empty one")

    Button(frame, text='Enter', command=lambda: entered(vars)).grid(column=1, pady=20)
    Button(frame, text='Cancel', command=main_screen).grid(column=1)


# TODO: enters data into data.txt
def entered(vars):
    date_enter = "{}-{}".format(vars[0][0].get(), vars[0][1].get())
    leftover = 6 - len(vars)
    for _ in range(leftover):
        a = StringVar()
        vars.append(a)

    ts = []
    for t in range(len(topictypes)):
        if topictypes[t] == "number":
            ts.append(t)

    numbergood = True
    if len(ts) > 0:
        for s in ts:
            if not is_int(vars[s+1].get()):
                numbergood = False

    if numbergood:
        row = {'date': date_enter, 't1': vars[1].get(), 't2': vars[2].get(), 't3': vars[3].get(),
               't4': vars[4].get(), 't5': vars[5].get()}
        found = False
        if len(datas) > 0:
            for d in range(len(datas)):
                if datas[d]['date'] == date_enter:
                    datas[d] = row
                    found = True
            if not found:
                datas.append(row)
        else:
            datas.append(row)
        update_data()
    else:
        print("int type is a string")

    main_screen()


def main_screen():
    reset(root, True)

    top_main_frame = Frame(root)
    main_frame = Frame(root)
    top_main_frame.grid(row=0, column=0, sticky='nsew')
    main_frame.grid(row=1, column=0, stick='nsew')

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=5)

    boxwid = root.winfo_screenwidth()/7/1.92
    for c in range(7):
        if c != 6:
            main_frame.grid_rowconfigure(c, minsize=100, weight=1)
        main_frame.grid_columnconfigure(c, minsize=boxwid, weight=1)

    now_month, now_day, now_year = get_today()
    create_top_header(top_main_frame, now_month)
    first_day_of_month, totdays = get_first_and_total_days(now_year, now_month)  # mon is 0
    create_days(main_frame, first_day_of_month, totdays, now_day, boxwid)

    Button(main_frame, text="Log", command=lambda: daily_log(now_month, now_day, totdays)).grid(column=6)

    # do last: make sure you can move to diff months

get_emojis()
read_data()
main_screen()
root.mainloop()
