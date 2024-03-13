import datetime
import os
import fitz  # fitz就是pip install PyMuPDF
import os
import cv2
from paddleocr import PPStructure,save_structure_res
from paddleocr.ppstructure.recovery.recovery_to_doc import sorted_layout_boxes, convert_info_docx
from copy import deepcopy
import patch_ng

def pdf2png(pdfPath, baseImagePath):
    imagePath=os.path.join(baseImagePath,os.path.basename(pdfPath).split('.')[0])
    startTime_pdf2img = datetime.datetime.now()  # 开始时间
    print("imagePath=" + imagePath)
    if not os.path.exists(imagePath):
        os.makedirs(imagePath)
    pdfDoc = fitz.open(pdfPath)
    totalPage=pdfDoc.pageCount
    for pg in range(totalPage):
        page = pdfDoc[pg]
        rotate = int(0)
        zoom_x = 2
        zoom_y = 2
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        print(f'正在保存{pdfPath}的第{pg+1}页，共{totalPage}页')
        pix.save(imagePath + '/' + f'images_{pg+1}.png')
    endTime_pdf2img = datetime.datetime.now()
    print(f'{pdfDoc}-pdf2img-花费时间={(endTime_pdf2img - startTime_pdf2img).seconds}秒')


# 中文测试图
table_engine = PPStructure(recovery=True,lang='ch')

image_path = './imgs/demo-scan'
save_folder = './txt'
def img2docx(img_path):
    text=[]
    imgs=os.listdir(img_path)
    for img_name in imgs:
        print(os.path.join(img_path,img_name))
        img = cv2.imread(os.path.join(img_path,img_name))
        result = table_engine(img)

        save_structure_res(result, save_folder, os.path.basename(img_path).split('.')[0])

        h, w, _ = img.shape
        res = sorted_layout_boxes(result, w)
        convert_info_docx(img, res, save_folder, os.path.basename(img_path).split('.')[0])

        for line in res:
            line.pop('img')
            print(line)
            for pra in line['res']:
                text.append(pra['text'])
            text.append('\n')
        with open('txt/res.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(text))


if __name__ == "__main__":
    pdfPath = r'./demo-scan.pdf'
    baseImagePath = './imgs'
    pdf2png(pdfPath, baseImagePath)
    img2docx(image_path)
