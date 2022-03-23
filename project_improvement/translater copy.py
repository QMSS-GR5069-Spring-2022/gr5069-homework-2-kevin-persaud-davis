import os
from pathlib import Path
import time

import requests
# from translate import Translator
import googletrans
import pdftotext


def translate_pdf(pdf):

    f_name = Path('news.pdf')
    r = requests.get(pdf)
    f_name.write_bytes(r.content)

    
    # print(r.content)
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # data_dir_path = dir_path + '\\data\\tmp.pdf'
    # with open(data_dir_path, 'wb') as f:
    #     f.write(response.content)


def get_pdf_text(pdf_file):
    print(f'\nget_pdf_text for file : {pdf_file}')

    with open(pdf_file, 'rb') as f:
        pages_text = pdftotext.PDF(f)

    return pages_text

def translate_text(pages, language, out_file):
    print(f'translate text to into: {language}')

    
    total = 0
    index = 1
    with open(out_file, 'w') as f:

        translator = googletrans.Translator()
        lines = []
        for text in pages:
            line = []
            print(f'Page {index}')
            chars = len(text)
            total += chars
            for char in text:
                if char != '\n':
                    line.append(char)
                else:
                    
                    res_line = ''.join(line)
                    #print(res_line)
                    lines.append(res_line)

        
            index += 1

        print(len(lines))
        
        test_text = lines[len(lines)-2]
        print(len(test_text))
        print(test_text)
        tt = test_text.replace(' ', '')
        print((tt))

        # print(lines[1])

        
            # translation = translator.translate(l, dest='en')
            # print(translation)
            
                    
            # for char in text:
            #     if char == '\n':
            #         print("NEWLINE")
            #     else:
            #         print(char)

            # print(text)
            
        # raw_dict = translator.translate(text, target_language=language, format_='text')
        # print(u'{}'.format(raw_dict['translatedText']))
        # print('\n\n')

        # result_file.write(f'Page {index}')
        # result_file.write('\n-----------\n')
        # result_file.write(u'{}'.format(raw_dict['translatedText']))

            

def main():
    
    # translator = Translator(from_lang='german', to_lang='english')

    translator = googletrans.Translator()
    g_text = u'Erinnerung – DAX Equity Index Upgrade – Einführung neuer Reports für lizensierte Third-Party Data gültig ab 21. Februar 2022'

    result = translator.translate(g_text)
    
    print(result)
    # translation = translator.translate(g_text)
    

    # pdf_link = 'https://www.dax-indices.com/document/News/2022/February/Unscheduled_Component_Change_GEX_Index_DE_20220214.pdf'

    # translate_pdf(pdf_link)

    


if __name__ == '__main__':
    main()