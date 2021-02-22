from pytube import Playlist, YouTube
from pytube import exceptions as ex
from sys import argv

# SETTINGS
TP = "video/mp4"
RES = "720"
FPS = "30fps"
AUD = "mp4a"
DOWNLOAD_CAPTION = "no"  # "yes" or "no"
LANGUAGE_CAPTION = "English"
AUTO_GENERATED = "yes"  # "yes" or "no". "no" means that only original captions
# SETTINGS


def get_captions(yt, DOWNLOAD_CAPTION, LANGUAGE_CAPTION, AUTO_GENERATED):
    if DOWNLOAD_CAPTION == "yes":
        list_capitons = list(yt.captions)
        list_i = []
        list_status = []
        for i, caption in enumerate(list_capitons):
            str_caption = str(caption)
            cond_lang = str_caption.find(LANGUAGE_CAPTION) >= 0
            cond_original = (AUTO_GENERATED == "no" and
                             str_caption.find("(auto-generated)") < 0)
            cond_auto_gen = (AUTO_GENERATED == "yes" and
                             str_caption.find("(auto-generated)") >= 0)
            if cond_lang:
                if cond_original:
                    list_i.append(i)
                    caption = list_capitons[i]
                    status = ("Original captions for selected "
                              "language was found")
                    list_status.append(status)
                elif cond_auto_gen:
                    list_i.append(i)
                    status = ("Auto-generated captions for selected "
                              "language was found")
                    list_status.append(status)
            else:
                status = "Captions for selected language was not found"
        if list_i:
            i = list_i[0]
            caption = list_capitons[i]
            f = open(f"{yt.title}.srt", "w")
            f.write(caption.generate_srt_captions())
            f.close()
        if list_status:
            status = list_status[0]
        else:
            status = "Captions for selected language was not found"
    else:
        status = "Download of captions was not choosed"
    return status


def status_url_not():
    url_not = ("Url is not defined or bad. Insert the right url "
               "after the sript's name")
    print("")
    print("+" * len(url_not))
    print(url_not)
    print("+" * len(url_not))
    print("")


def print_info_playlist(p, url):
    url_yes = f"URL: {p.playlist_url}"
    print("")
    print("+" * len(url_yes))
    print(url_yes)
    print(f"Title: {p.title}")
    print("+" * len(url_yes))
    print("")


def find_good_stream(yt, TP, RES, FPS, AUD):
    for i, stream in enumerate(yt.streams):
        str_steam = str(stream)
        cond1 = str_steam.find(TP) >= 0
        cond2 = str_steam.find(RES) >= 0
        cond3 = str_steam.find(FPS) >= 0
        cond4 = str_steam.find(AUD) >= 0
        if cond1 and cond2 and cond3 and cond4:
            stream = yt.streams[i]
            return stream


def status_down_sucsses(yt, i, r):
    ss = "\033[32m"
    sf = "\033[0m"
    ss_cap_bad = "\033[31m\033[5m"
    ss_cap_dont = "\033[31m"
    status = f"{ss}#{yt.title} ==> SUCSSES{sf}"
    if r == "Captions for selected language was not found":
        status_caption = f"{ss_cap_bad}CAPTION: {r} ==> FAIL{sf}"
    elif r == "Download of captions was not choosed":
        status_caption = f"{ss_cap_dont}CAPTION: {r}{sf}"
    else:
        status_caption = f"{ss}CAPTION: {r} ==> SUCSSES{sf}"
    i += 1
    print("")
    print(f"{ss}+{sf}" * (len(status) - len(ss) - len(sf)))
    print(f"{ss}#{i} in the playlist{sf}")
    print(status)
    print(status_caption)
    print(f"{ss}+{sf}" * (len(status) - len(ss) - len(sf)))
    print("")


def status_down_fail(i):
    ss = "\033[31m\033[5m"
    sf = "\033[0m"
    status = f"{ss}FAIL ==> Video is not Availible{sf}"
    i += 1
    print("")
    print(f"{ss}+{sf}" * (len(status) - len(ss) - len(sf)))
    print(f"{ss}#{i} in the playlist{sf}")
    print(status)
    print(f"{ss}+{sf}" * (len(status) - len(ss) - len(sf)))
    print("")


try:
    url = argv[1]
    print(argv)
    p = Playlist(url)
    print_info_playlist(p, url)
except (ValueError, NameError, KeyError):
    status_url_not()


list_urls = []
for url in p.video_urls:
    list_urls.append(url)

st = 0
fh = len(list_urls)
while st < fh:
    try:
        for i in range(st, fh):
            yt = YouTube(list_urls[i])
            stream = find_good_stream(yt, TP, RES, FPS, AUD)
            stream.download()
            r = get_captions(yt, DOWNLOAD_CAPTION, LANGUAGE_CAPTION,
                             AUTO_GENERATED)
            status_down_sucsses(yt, i, r)
            if i >= fh - 1:
                st = fh
    except ex.VideoUnavailable:
        st = i + 1
        status_down_fail(i)
    except ssl.SSLError:
        st = i + 1
        status_down_fail(i)
