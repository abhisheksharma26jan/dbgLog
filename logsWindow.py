import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import subprocess
import os
from tkinter import filedialog as fd

home_dir = os.path.expanduser('~')
awsProfilePath = home_dir+"/.aws_profile"


ROOT_DIR=os.path.dirname(os.path.abspath(__file__))
def selectHost(event):
    host = hostcbox.get()
    instancecbox.set("")
    filescbox.set("")

    if host in hostsInstanceMap:
        instancecbox['values'] = list(hostsInstanceMap[host])

        instancecbox.delete(0, "end")


def selectInstance(event):
    instance = instancecbox.get().replace("'","")
    filescbox.set("")
    filePath = "NA"
    awsProfile = "bigdentest"
    searchKey="NA"

    grepText.delete('1.0', tk.END)
    grepText.insert(tk.END, "Loading Files...")
    grepText.update()


    instanceFilesFiles = open(ROOT_DIR+"/instanceFiles.csv","r")

    #print(instanceFilesFiles.readlines())

    foundInFile = False
    for line in instanceFilesFiles.readlines():
        if line.split("$")[0] == instance:
            files = line.split("$")[-1].split(",")
            foundInFile = True
            break

    instanceFilesFiles.close()

    if not foundInFile:
        files = []
        grepProcess = subprocess.Popen(
            [ROOT_DIR + "/scripts/getLogFilesHelper.sh", awsProfile, awsProfilePath, instance, filePath, searchKey],
            cwd=ROOT_DIR, stdout=subprocess.PIPE)

        instanceFilesFiles = open(ROOT_DIR + "/instanceFiles.csv", "a")
        instanceFilesFiles.write(instance+"$")
        for line in grepProcess.stdout:
            line = line.decode('utf-8').strip()
            if "logs" in line and len(line)>6:
                files.append(line)
                instanceFilesFiles.write(line + ",")

        instanceFilesFiles.write("\n")
        instanceFilesFiles.close()

    files.sort(key=str.casefold)
    filescbox['values'] = files

    filescbox.configure(height=32)

    grepText.insert(tk.END, "Done!\n","complete")


def readLog4J():
    grepText.delete('1.0', tk.END)



    awsProfile = "bigdentest"
    instance = instancecbox.get().replace("'", "")
    host = hostcbox.get()

    if len(instance) <1:
        grepText.insert(tk.END, "Select a valid instance!\n" ,"error")
        grepText.update()
        return



    if "STLS" in host:
        logFilePath = "/ngs/app/dsservd/IDMSQA2/DS/IdmsCoreServiceClassic/noacmpods/runtime/apple/log4j2.xml"
    elif "I3RW" in host:
         logFilePath = "/ngs/app/dsservd/IDMSQA2/DS/i3Write/defaultInstance/runtime/apple/log4j2.xml"
    elif "DSPF" in host:
        logFilePath = "/ngs/app/dsservd/IDMSQA2/DS/IdMSPublishing/defaultInstance/runtime/apple/log4j2.xml"
    elif "eDSAS" in host:
        logFilePath = "/ngs/app/dsservd/IDMSQA2/DS/IdMSPublishing/defaultInstance/runtime/apple/log4j2.xml"

    grepText.insert(tk.END, "Reading "+logFilePath+"\n")
    grepText.update()

    grepProcess = subprocess.Popen(
        [ROOT_DIR + "/scripts/readLog4JHelper.sh", awsProfile, awsProfilePath, instance, logFilePath ],
        cwd=ROOT_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    count = 0
    for line in grepProcess.stdout:
        line = line.decode('utf-8').strip()

        if "DEBUG" in line:
            grepText.insert(tk.END, line.split("DEBUG", 1)[0], )
            grepText.insert(tk.END, "DEBUG", "searchKey")
            grepText.insert(tk.END, line.split("DEBUG", 1)[1])
        else:
            grepText.insert(tk.END, line+"\n")


        if count % 10 == 0:
            grepText.update()
            grepText.see("end")

        count = count +1


def doGrep():
    instance = instancecbox.get().replace("'", "")
    filePath = filescbox.get()

    if "selected" in SuffixCB.state():
        filePath =filePath + "*"

    awsProfile = "bigdentest"
    searchKey = searchKeyEntry.get()
    A = ACB.get()
    B = BCB.get()

    grepText.delete('1.0', tk.END)
    grepText.insert(tk.END, "grep instance: "+instance+ " searchKey: "+searchKey+" filePath: "+filePath+"\n")
    grepText.update()

    grepProcess = subprocess.Popen(
        [ROOT_DIR + "/scripts/grepLogHelper.sh", awsProfile, awsProfilePath, instance, filePath, searchKey,A,B],
        cwd=ROOT_DIR, stdout=subprocess.PIPE ,stderr=subprocess.PIPE)

    count = 0
    for line in grepProcess.stdout:
        line = line.decode('utf-8').strip()
        if searchKey in line:
            grepText.insert(tk.END, line.split(searchKey, 1)[0], )
            grepText.insert(tk.END, searchKey, "searchKey")
            grepText.insert(tk.END, line.split(searchKey, 1)[1])
        else:
            grepText.insert(tk.END, line)
        grepText.insert(tk.END, "\n")
        count = count + 1
        if count%15==0:
            grepText.update()
            grepText.see("end")

    # error_output = grepProcess.stderr.read()
    # print(error_output)
    # for line in error_output:
    #     grepText.insert(tk.END, line + "\n", "error")


    for line in grepProcess.stderr:
        grepText.insert(tk.END, str(line)+"\n", "error")

    grepText.insert(tk.END,"END\n","complete")
    grepText.see("end")
    grepText.update()


def parseHealthcheck(event):
    hostcbox.set("")
    instancecbox.set("")
    filescbox.set("")

    grepText.delete('1.0', tk.END)
    grepText.insert(tk.END, "Loading Hosts & Instances...\n")
    grepText.update()


    global hostsInstanceMap

    env =envcbox.get()
    if env=="scv2":
        url = "http://scv21-loadb-193gwsgbbthoj-b2c1fd2c2268448c.elb.us-west-2.amazonaws.com:8080/SS/IStatusServlet?type=main"
    elif env=="scv1":
        url = "http://scv1-loadb-1g2yfj9ilyscp-3ab4c0d904a93a78.elb.us-west-2.amazonaws.com:8080/SS/IStatusServlet?type=main"
    elif env=="aws":
        url = "http://qecer-loadb-2lz2zjy7mhe6-7e02068740d57b2a.elb.us-west-2.amazonaws.com:8080/SS/IStatusServlet?type=main"


    
    payload={}
    headers = {
      'Accept': '*/*',
      'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
      'Connection': 'keep-alive',
      'Cookie': 'JSESSIONID=ABEB8E44026D597CE282E72F48E885EA',
      'Referer': 'http://scv21-loadb-193gwsgbbthoj-b2c1fd2c2268448c.elb.us-west-2.amazonaws.com:8080/SS/',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
      'X-Requested-With': 'XMLHttpRequest'
    }

    for attemp in range(5):
        try:
            response = requests.request("GET", url, headers=headers, data=payload,timeout=7)
            break
        except:
            grepText.insert(tk.END, "Retry: Not able to get healthcheck data from "+url+"\n","error" )
            grepText.update()

            pass


    s = response.text


    soup = BeautifulSoup(s, 'html.parser')
    tables = [
    [
        [td.get_text(strip=True) for td in tr.find_all('td')] 
        for tr in table.find_all('tr')
    ] 
    for table in soup.find_all('table')
    ]
    
    hostsInstanceMap = {}
    for row in tables[0]:
        if len(row) > 0 :
            if row[0] in hostsInstanceMap:
                hostsInstanceMap[row[0]].add(row[1])
            else:
                hostsInstanceMap[row[0]] = set()
                hostsInstanceMap[row[0]].add(row[1])

    hostslist = list(hostsInstanceMap.keys())
    hostslist.sort(key=str.casefold)
    hostcbox['values'] = hostslist

    hostcbox.configure(height=len(hostsInstanceMap.keys()) + 2)

    grepText.insert(tk.END, "Done!\n","complete")


def updateCommandText(event=""):
    filePath = filescbox.get()
    if "selected" in SuffixCB.state():
        filePath =filePath + "*"

    executeButton.configure(text="grep -A "+ACB.get()+" -B "+BCB.get()+" "+searchKeyEntry.get()+" "+filePath)


curr = 0
prevS = ""
def search(event):
    global prevS,curr

    grepText.tag_remove('found', '1.0', tk.END)
    grepText.tag_remove('foundHighlight', '1.0', tk.END)

    find_idx = "1.0"
    s = event.widget.get()  # Grabs the text from the entry box

    if len(s) == 0:
        searchResultLabel["text"] = ""
        return
    elif len(s)<3:
        searchResultLabel["text"] = "Search string too short!"
        return

    finds = []

    while 1:
        find_idx = grepText.search(s, find_idx, nocase=1, stopindex=tk.END)
        if not find_idx: break
        lastidx = '%s+%dc' % (find_idx, len(s))
        finds.append((find_idx, lastidx))
        grepText.tag_add('found', find_idx, lastidx)
        find_idx = lastidx

    if s == prevS and len(finds) > 0:
        curr = curr + 1
        if curr == len(finds):
            curr = 0
        grepText.tag_add('foundHighlight', finds[curr][0], finds[curr][1])
        grepText.see(finds[curr][0])
    elif len(finds) > 0:
        prevS = s
        curr = 0
        grepText.tag_add('foundHighlight', finds[0][0], finds[0][1])
        grepText.see(finds[0][0])


    if len(finds) > 0:
        searchResultLabel["text"]=str(curr)+"/"+str(len(finds))
    else:
        searchResultLabel["text"]="0/0"


def save():

    filetypes = (
        ('log files', '*.log'),
    )
    filename = fd.asksaveasfile(
        title='Open a file',
        initialdir='/Users/abhishek/Documents/',
        filetypes=filetypes,
        mode="w")

    # writer = csv.writer(filename)
    # writer.writerows(L)
    filename.close()


def logsWindow():
    global ACB,BCB,tabControl,quickViewText,ignoreServicesText,envText,envFrame,envcbox,hostcbox,instancecbox,grepText,filescbox,searchKeyEntry,searchResultLabel,SuffixCB,executeButton
    newWindow = tk.Tk()

    newWindow.title("Debug Logs")

    w= 1600
    h = 700
    ws = newWindow.winfo_screenwidth() # width of the screen
    hs = newWindow.winfo_screenheight() # height of the screen
    x = (ws/2) - (w/2)
    y = (hs/3) - (h/3)
    newWindow.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    
    #env
    envFrame = tk.Frame(newWindow, background="white",name="envFrame")
    envFrame.configure(background='black')

    envFrame.pack(side="top", fill="both")

    envLabel = tk.Label(envFrame, text="Environment", font=("Monospaced", "13", "bold"), width=15, relief="raised",background="#c1e3f7",fg="black")
    envLabel.pack(side="left")

    envcbox = ttk.Combobox(envFrame,font=("Monospaced"),width=10)
    envcbox['values'] = ["aws","scv1","scv2","scvpch"]
    envcbox['state'] = 'readonly'
    envcbox.pack(side="left",expand=True,fill="both")
    envcbox.bind("<<ComboboxSelected>>", parseHealthcheck)


    hostLabel = tk.Label(envFrame, text="Host", font=("Monospaced", "13", "bold"), width=15, relief="raised",background="#c1e3f7",fg="black")
    hostLabel.pack(side="left")
    
    hostcbox = ttk.Combobox(envFrame,font=("Monospaced"),width=35)
    hostcbox.pack(side="left",expand=True,fill="both")
    hostcbox['state'] = 'readonly'
    hostcbox.bind("<<ComboboxSelected>>", selectHost)

    instanceLabel = tk.Label(envFrame, text="Instance", font=("Monospaced", "13", "bold"), width=15, relief="raised",background="#c1e3f7",fg="black")
    instanceLabel.pack(side="left")

    instancecbox = ttk.Combobox(envFrame,font=("Monospaced"),width=35)
    instancecbox.pack(side="left",expand=True,fill="both")
    instancecbox['state'] = 'readonly'
    instancecbox.bind("<<ComboboxSelected>>", selectInstance)

    
    tabControl = ttk.Notebook(newWindow)

    grepTab = ttk.Frame(tabControl)
    dbgTab = ttk.Frame(tabControl)


    tabControl.add(grepTab, text='GREP Logs')
    tabControl.add(dbgTab, text ='DBG ON/OFF')


    grepControlsFrame = tk.Frame(grepTab, background="black",name="grepControlsFrame")
    grepControlsFrame.pack(side="top", fill="x")

    filesLabel = tk.Label(grepControlsFrame, text="File", font=("Monospaced", "13", "bold"), width=15, relief="raised",background="#f7e3d5",fg="black" )
    filesLabel.grid(row=0,column=0)
    filescbox = ttk.Combobox(grepControlsFrame, font=("Monospaced"), width=35)
    filescbox.grid(row=0,column=1)
    filescbox['state'] = 'readonly'
    filescbox.bind("<<ComboboxSelected>>", updateCommandText)

    #checkbox
    s = ttk.Style()
    s.configure('Red.TCheckbutton', background='black')
    SuffixCB = ttk.Checkbutton(grepControlsFrame, text="*Suffix", width=15,style="Red.TCheckbutton",command=updateCommandText)
    SuffixCB.state(['selected', '!alternate'])
    SuffixCB.grid(row=0,column=2)


    searchKeyLabel = tk.Label(grepControlsFrame, text="Search Key", font=("Monospaced", "13", "bold"), width=15,
                          relief="raised",background="#f7e3d5",fg="black" )
    searchKeyLabel.grid(row=1,column=0)

    searchKeyEntry = tk.Entry(grepControlsFrame, font=("Monospaced"), width=37)
    searchKeyEntry.grid(row=1,column=1)
    searchKeyEntry.bind("<KeyRelease>", updateCommandText)

    #
    ALabel = tk.Label(grepControlsFrame, text="-A", font=("Monospaced", "13", "bold"), width=15,
                              relief="raised", background="#f7e3d5",fg="black")
    ALabel.grid(row=2, column=0)
    ACB = ttk.Combobox(grepControlsFrame, font=("Monospaced"), width=35)
    ACB.grid(row=2, column=1)
    ACB.bind("<<ComboboxSelected>>", updateCommandText)

    L = []
    for i in range(21):
        L.append(i*10)
    ACB['values'] = L
    ACB.current(5)


    BLabel = tk.Label(grepControlsFrame, text="-B", font=("Monospaced", "13", "bold"), width=15,
                              relief="raised",background="#f7e3d5",fg="black" )
    BLabel.grid(row=3, column=0)
    BCB = ttk.Combobox(grepControlsFrame, font=("Monospaced"), width=35)
    BCB.grid(row=3, column=1)
    BCB.bind("<<ComboboxSelected>>", updateCommandText)
    BCB['values'] = L
    BCB.current(5)


    tabControl.pack(expand = 0, fill ="both")


    textFrame = tk.Frame(newWindow, background="black",name="textFrame",height=600)
    textFrame.pack(side="top", fill="both",expand=True)


    # Add a Scrollbar(vertical)
    v = tk.Scrollbar(textFrame, orient='vertical')
    grepText = tk.Text(textFrame,wrap="none", height=1, borderwidth=0, background="white", fg="black",   yscrollcommand = v.set)
    v.config(command=grepText.yview)
    v.pack(side=tk.RIGHT, fill='y')
    grepText.pack(side="top", pady=1, ipady=3 , ipadx=3,expand=True,fill="both")

    # TAGS
    grepText.tag_config('complete', font=("", 13, "bold"), foreground="#1ecafa", justify='left')
    grepText.tag_config('searchKey', font=("", 13,), foreground="red", justify='left')
    grepText.tag_config('error', font=("", 13,), foreground="#b36336", justify='left')


    grepText.tag_configure('found', background='#ffff73')
    grepText.tag_configure('foundHighlight', background='#ffff73', font=("Monospaced", 14, "bold"))


    commandTextFrame = tk.Frame(grepTab, background="white",name="commandTextFrame")
    commandTextFrame.pack(side="top", fill="x")


    executeButton = tk.Button(commandTextFrame, text ="Execute", command = doGrep,activebackground="blue",padx=10,pady=10,cursor="hand")
    executeButton.pack(side="right",expand=True,fill="x")

    # Serach & save
    serachFrame = tk.Frame(newWindow,  name="serachFrame")
    serachFrame.pack(side="top", fill="both", expand=False)
    searchLabel = tk.Label(serachFrame, text="Search", font=("Monospaced", "13", "bold"),)
    searchLabel.pack(side="left",pady=3,padx=2)

    searchEntry = tk.Entry(serachFrame, font=("Monospaced"), width=35)
    searchEntry.pack(side="left",pady=3,padx=0)
    searchEntry.bind('<Return>', search)

    searchResultLabel = tk.Label(serachFrame, text="", font=("Monospaced", "13"), )
    searchResultLabel.pack(side="left", pady=3, padx=2)

    saveButton = tk.Button(serachFrame, text="Save As", command=save, activebackground="blue", padx=10, pady=10,cursor="hand")
    saveButton.pack(side="right", pady=3, padx=19)

    # DBG TAB

    dbgTab
    readLog4JButton = tk.Button(dbgTab, text ="Read Log4J", command = readLog4J,activebackground="blue",padx=10,pady=10,cursor="hand")
    readLog4JButton.pack(side="left",expand=True,fill="x")

    dbgONButton = tk.Button(dbgTab, text ="DBG ON", command = doGrep,activebackground="blue",padx=10,pady=10,cursor="hand")
    dbgONButton.pack(side="left",expand=True,fill="x")
    dbgOFFButton = tk.Button(dbgTab, text ="DBG OFF", command = doGrep,activebackground="blue",padx=10,pady=10,cursor="hand")
    dbgOFFButton.pack(side="left",expand=True,fill="x")


    newWindow.mainloop()

if __name__ == '__main__':
    logsWindow()


