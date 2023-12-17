import os,sys

workDir = os.path.abspath(os.path.dirname(sys.path[0]))

list=["update.py","clear.py","emoji2dict.py","util.py"]

for file in list:
    os.system(f"python {os.path.join(workDir,"tools",file)}")
