import argparse
import re
import mysql.connector
import time
import sys
import os
from datetime import datetime

try:
    sys.path.append(".")
    from config import config
except:
    sys.path.append("..")
    from config import config

def init_db():
    db = mysql.connector.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PWD,
        database=config.DB_NAME,
        auth_plugin="mysql_native_password"
    )
    return db

def get_list_data(ocr_type):
    conn = init_db()
    
    if ocr_type=="paddle":
        col = "content_1"
    elif ocr_type=="mmocr":
        col = "content_2"
    elif ocr_type=="textract":
        col = "content_3"
    
    query = "SELECT pcid, file_path FROM printed_content WHERE "+col+" IS NULL"
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    
    return result

def insert_extracted_content(content, ocr_type, pcid):
    conn = init_db()
    now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    
    if ocr_type=="paddle":
        col = "content_1"
    elif ocr_type=="mmocr":
        col = "content_2"
    elif ocr_type=="textract":
        col = "content_3"
    
    query = "UPDATE printed_content SET "+col+"=%s WHERE pcid=%s"
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, (content, pcid))
        conn.commit()
        print(f"{now} | {cursor.rowcount} record inserted.")
    except:
        print(f"{now} | {cursor.rowcount} record failed to insert.")


def retrieve_file(filename, uploaded_file):
    print("retrieving file")
    import requests

    img_file_format = ['jpg', 'jpeg', 'png']
    doc_file_format = ['pdf', 'doc', 'docx', 'txt', 'odt']

    file_format = uploaded_file.split(".")[-1]
    retrieve_content = os.path.join(config.HOST_URL, uploaded_file)
    
    if not os.path.exists("temp"):
        os.mkdir("temp")
    filepath = os.path.join("temp", filename)
    
    if file_format.lower() in img_file_format:
        from PIL import Image
        img = Image.open(requests.get(retrieve_content, stream = True).raw)
        img.save(filepath)

    elif file_format.lower() in doc_file_format:
        # print(retrieve_content)
        with open(filepath, 'wb') as f:
            f.write(requests.get(retrieve_content, stream = True).content)
    print(filepath)
    return filepath


class TextExtractor:
    def __init__(self):
        pass
    
    def paddleocr(self, filepath):
        print("extracting: paddle")
        from paddleocr import PaddleOCR
        ocr = PaddleOCR(use_angle_cls=True, lang='id') # need to run only once to download and load model into memory
        try:
            ocr_detect = ocr.ocr(filepath, cls=True)
            
            collect_text = []
            for idx in range(len(ocr_detect)):
                res = ocr_detect[idx]
                for line in res:
                    collect_text.append(line[1][0])
            result = " ".join(collect_text).replace("- ", "")
            result = result.encode('utf-8', 'ignore').decode(encoding="utf-8")
        except Exception as e:
            print("paddle failed: ", e)
            return False
        
        return result
    
    def mmocr(self, filename):
        print("extracting: mmocr")
        from mmocr.apis import MMOCRInferencer
        # Load models into memory
        ocr = MMOCRInferencer(det='dbnet_resnet18_fpnc_1200e_totaltext', rec='SAR')
        # ocr = MMOCRInferencer(det='DBNet', rec='CRNN')
        
        try:
            # Perform inference
            ocr = ocr(filename, print_result=True)
            ocr = ocr['predictions'][0]['rec_texts']
            ocr.reverse()
            result = " ".join(ocr)
            result = result.encode('utf-8', 'ignore').decode(encoding="utf-8")
        except Exception as e:
            print("mmocr failed: ", e)
            return False
        
        return result
    
    def textract(self, filename):
        print("extracting: textract")
        import textract
        
        try:
            extract = textract.process(filename)
            extract = extract.decode('utf-8', "ignore")
            extract = re.sub("[^A-Z]", " ",extract, 0, re.IGNORECASE)
            extract = re.sub(" +", " ", extract)
            result = extract.encode('utf-8', 'ignore').decode(encoding="utf-8")
        except Exception as e:
            print("txtract failed: ", e)
            return False
        
        return result

if __name__ == "__main__":
    dev = True
    parser = argparse.ArgumentParser(description="Text Extractor-Part of Bhinneka Project")
    parser.add_argument("--pocr", dest="paddle", action='store_true')
    parser.add_argument("--mmocr", dest="mmo", action='store_true')
    parser.add_argument("--txtract", dest="textract", action='store_true')
    
    args = parser.parse_args()
    
    if not (args.paddle or args.mmo or args.textract):
        parser.error('No action requested, add --pocr or --mocr or --txtract')
    
    textractor = TextExtractor()
    if args.paddle:
        permitted_ext = ['jpg', 'jpeg', 'png']
        print("Starting...")
        while True:
            list_data = get_list_data("paddle")
            print("found data: ", len(list_data))
            for gld in list_data:
                ext = gld['file_path'].split(".")[-1]
                if ext not in permitted_ext:
                    continue

                process = textractor.paddleocr(gld['file_path'])
                if not process:
                    filepath = retrieve_file(filename=gld['file_path'].split("/")[-1], uploaded_file=gld['file_path'])
                    process = textractor.paddleocr(filepath)
                    os.remove(filepath)
                
                insert_extracted_content(content=process, ocr_type="paddle", pcid=gld['pcid'])
                
            print("Listening...")
            if not dev:
                time.sleep(60*15)
            else:
                time.sleep(15)
            
    elif args.mmo:
        permitted_ext = ['jpg', 'jpeg', 'png']
        print("Starting...")
        while True:
            list_data = get_list_data("mmocr")
            for gld in list_data:
                ext = gld['file_path'].split(".")[-1]
                if ext not in permitted_ext:
                    continue

                try:
                    process = textractor.mmocr(gld['file_path'])
                except:
                    filepath = retrieve_file(filename=gld['file_path'].split("/")[-1], uploaded_file=gld['file_path'])
                    process = textractor.mmocr(filepath)
                    os.remove(filepath)

                insert_extracted_content(content=process, ocr_type="mmocr", pcid=gld['pcid'])
            
            print("Listening...")
            if not dev:
                time.sleep(60*15)
            else:
                time.sleep(15)

    elif args.textract:
        permitted_ext = ['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx', 'txt', 'odt']
        print("Starting...")
        while True:
            list_data = get_list_data("textract")
            for gld in list_data:
                ext = gld['file_path'].split(".")[-1]
                if ext not in permitted_ext:
                    continue

                process = textractor.textract(gld['file_path'])
                if not process:
                    filepath = retrieve_file(filename=gld['file_path'].split("/")[-1], uploaded_file=gld['file_path'])
                    process = textractor.textract(filepath)
                    os.remove(filepath)

                insert_extracted_content(content=process, ocr_type="textract", pcid=gld['pcid'])
            
            print("Listening...")
            if not dev:
                time.sleep(60*15)
            else:
                time.sleep(15)
