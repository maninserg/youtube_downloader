from pytube import YouTube, exceptions

try:
    f = open("urls_youtube.txt", "r")
except FileNotFoundError:
    print("")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("\033[31m\033[5mThere isn't urls_youtube.txt "
          "in the current directory.\033[0m")
    print("\033[31m\033[5mCreate it!!!\033[0m")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("")
    f = []

TP = "video/mp4"
RES = "720"
FPS = "30fps"
AUD = "mp4a"


def print_ok(title):
    status_tx = title + " ==> DONE DOWNLOAD"
    ok = True
    print_form(status_tx, ok)


def print_error(title):
    status_tx = title + " ==> ERROR DOWNLOAD"
    err = False
    print_form(status_tx, err)


def print_form(status_tx, status):
    if status:
        sn = "\033[32m"
        se = "\033[0m"
    else:
        sn = "\033[31m\033[5m"
        se = "\033[0m"
    status = sn + status_tx + se
    print("+" * len(status_tx))
    print(status)
    print("+" * len(status_tx))
    print("")


def print_num_url(n):
    print("")
    print("#" + str(n+1) + " url in urls_youtube.txt")


for n, url in enumerate(f):
    try:
        yt = YouTube(url)
    except exceptions.RegexMatchError:
        print("dkfjadkljfdkl")
        break

    title = yt.title
    err_list = []
    print_num_url(n)
    for i, stream in enumerate(yt.streams):
        str_stream = str(stream)
        cond1 = str_stream.find(TP) >= 0
        cond2 = str_stream.find(RES) >= 0
        cond3 = str_stream.find(FPS) >= 0
        cond4 = str_stream.find(AUD) >= 0
        if cond1 and cond2 and cond3 and cond4:
            err_list.append(True)
            stream = yt.streams[i]
            try:
                stream.download()
            except VideoUnavailable:
                continue
        else:
            err_list.append(False)
    if True in err_list:
        print_ok(title)
    else:
        print_error(title)
