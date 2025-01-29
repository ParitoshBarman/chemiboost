from chemiboostapp.models import Purchase
import time
from datetime import datetime, timedelta
import os

deletExtraImagesRUNNINGstatus = True

def deletExtraImages():
    print("Deleting.......")
    global deletExtraImagesRUNNINGstatus
    if deletExtraImagesRUNNINGstatus:
        deletExtraImagesRUNNINGstatus = False
        print("Permition On......")
        time.sleep(15)
        mainDir = "./media/FileDBFolder"
        allfiles = os.listdir(mainDir)
        for file in allfiles:
            created = os.path.getctime(f"{mainDir}/{file}")
            if((datetime.fromtimestamp(created)+timedelta(minutes=1)) < datetime.now()):
                os.remove(f"{mainDir}/{file}")
        deletExtraImagesRUNNINGstatus = True
