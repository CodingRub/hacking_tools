import random, string, time, hashlib, sys, argparse, atexit, urllib.request, urllib.response, urllib.error, multiprocessing
from bs4 import BeautifulSoup
from utils import *

class Cracker:

    @staticmethod
    def crack_dict(md5, files, order, done_queue):
        try:
            trouve = False
            ofile = open(files, "r")
            if Order.ASCEND == order:
                contenu = reversed(list(ofile.readlines()))
            else:
                contenu = ofile.readlines()
            for mot in contenu:
                mot = mot.strip("\n")
                mot_md5 = hashlib.md5(mot.encode("utf8")).hexdigest()
                if md5 == mot_md5:
                    print(Color.VERT + "Mot de passe trouvé: " + str(mot) + Color.FIN)
                    trouve = True
                    done_queue.put("TROUVE :)")
            if trouve == False:
                print(Color.ROUGE + "Mot de passe introuvable :(" + Color.FIN)
                done_queue.put("NON TROUVE :(")
            ofile.close()
        except FileNotFoundError:
            print(Color.ROUGE + "Error: Fichier introuvable !" + Color.FIN)
            sys.exit(1)
        except Exception as err:
            print(Color.ROUGE + "Error: " + str(err) + Color.FIN)

    @staticmethod
    def crack_incr(md5, length, currpass=[]):
        lettres = string.ascii_letters
        if length >= 1:
            if len(currpass) == 0:
                currpass = ['a' for _ in range(length)]
                Cracker.crack_incr(md5, length, currpass)
            else: 
                for c in lettres:
                    currpass[length - 1] = c
                    print("Test: " + "".join(currpass))
                    if hashlib.md5("".join(currpass).encode("utf8")).hexdigest() == md5:
                        print(Color.VERT + "MDP trouvé :D " + "".join(currpass) + Color.FIN)
                        sys.exit(1)
                    else:
                        Cracker.crack_incr(md5, length-1, currpass)

    @staticmethod
    def crack_online(md5):
        try:
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"
            headers = {'User-Agent': user_agent}
            url = "https://md5.gromweb.com/?md5="+md5
            request = urllib.request.Request(url, None, headers)
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            print(Color.ROUGE + "Error HTTP: " + e.code + Color.FIN)
        except urllib.error.URLError as e:
            print(Color.ROUGE + "URL Error: " + e.reason + Color.FIN)

        text = response.read().decode('utf8')
        soup = BeautifulSoup(text, "lxml")
        if soup.find('input', {'id': 'form_string_to_hash_string'}).get('value'):
            print(Color.VERT + "HASH HAS BEEN FOUND FROM INTERNET : " + soup.find('input', {'id': 'form_string_to_hash_string'}).get('value') + Color.FIN)
        else:
            print(Color.ROUGE + "HASH WASN'T FOUND :(" + Color.FIN)

    @staticmethod
    def work(work_queue, done_queue, md5, file, order):
        o = work_queue.get()
        o.crack_dict(md5, file, order, done_queue)
