# coding:utf-8
import time, argparse, atexit, multiprocessing
from cracker import *
from utils import *

def display_name():
    duree = time.time() - debut
    if duree >= 60:
        duree = duree/60
        if duree >= 60:
            duree = duree/60
    print(Color.ORANGE + "Durée: "+str(duree) + " secondes" + Color.FIN)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Password Cracker")
    parser.add_argument("-f", "--file", dest="file", help="Path of the dictionary file", required=False)
    parser.add_argument("-g", "--gen", dest="gen", help="Generate MD5 hash of password", required=False)
    parser.add_argument("-md5", dest="md5", help="Hashed password (MD5)", required=False)
    parser.add_argument("-l", "--length", dest="plength", help="Length of password", required=False, type=int)
    parser.add_argument("-o", "--online", dest="online", help="Search online", required=False, action="store_true")
    args = parser.parse_args()
    processes = []
    work_queue = multiprocessing.Queue()
    done_queue = multiprocessing.Queue()
    cracker = Cracker()
    debut = time.time()
    atexit.register(display_name)

    if args.md5:
        print(Color.ORANGE + "[CRACKING HASH " + args.md5 +"]" + Color.FIN)
        if args.file:
            print(Color.ORANGE + "[USING DICTIONARY FILE " + args.file+"]" + Color.FIN)
            p1 = multiprocessing.Process(target=Cracker.work, args=(work_queue, done_queue, args.md5, args.file, False))
            processes.append(p1)
            work_queue.put(cracker)
            p1.start()

            p2 = multiprocessing.Process(target=Cracker.work, args=(work_queue, done_queue, args.md5, args.file, True))
            processes.append(p2)
            work_queue.put(cracker)
            p2.start()
            while True:
                nontrouve = 1
                data = done_queue.get()
                if data == "TROUVE :)":
                    p1.kill()
                    p2.kill()
                    break
                elif data == "NON TROUVE :(":
                    nontrouve = nontrouve +1
                    print(nontrouve)
                    if nontrouve == len(processes):
                        print("AUCUN PROCESSUS N'A TROUVE DE MDP")
                        break
            #Cracker.crack_dict(args.md5, args.file)
        elif args.plength:
            print(Color.ORANGE + "[USING INCREMENTAL MODE FOR " + str(args.plength) + "letter(s)]" + Color.FIN)
            Cracker.crack_incr(args.md5, args.plength)
        elif args.online:
            print(Color.ORANGE + "[USING ONLINE MODE]" + Color.FIN)
            Cracker.crack_online(args.md5)
        else:
            print(Color.ORANGE + "Please choose either -f or -l argument" + Color.FIN)
    else:
        print(Color.ORANGE + "MD5 hash not provided" + Color.FIN)

    if args.gen:
        print(Color.VERT + "[MD5 HASH OF "+ args.gen+ " : " + hashlib.md5(args.gen.encode("utf8")).hexdigest() + "]" + Color.FIN)
