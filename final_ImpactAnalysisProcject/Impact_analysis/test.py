
from main import Main,Container

obj = Main()
copy,static,move,call,dynamic=False,True,False,False,False
obj.sent_file("inputfiles/Jcl_to_Procs.txt",copy,static,move,call,dynamic,True,True,True)
