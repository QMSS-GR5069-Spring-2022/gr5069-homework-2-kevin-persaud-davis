import os
from pathlib import Path
import time

import requests
import googletrans
import pdftotext


def translate_pdf(pdf):
    f_name = Path('news.pdf')
    r = requests.get(pdf)
    f_name.write_bytes(r.content)


def get_pdf_text(pdf_file):
    """
    Get text of PDF file

    Parameters:
        
        pdf_file : str

    Returns
        get_pdf_text : pdftotext.PDF

    """
    print(f'\nget_pdf_text for file : {pdf_file}')

    with open(pdf_file, 'rb') as f:
        pages_text = pdftotext.PDF(f)
    return pages_text


def translate_text(pages, language, out_file):
    """
    Translate text to new language and save to disk.
    
    Parameters:
        
        pages: 
        
        language: 
        
        out_file:
        
    Returns:
        translate_text: 
    
    """
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
           

def main():
    translator = googletrans.Translator()
    g_text = u'Erinnerung – DAX Equity Index Upgrade – Einführung neuer Reports für lizensierte Third-Party Data gültig ab 21. Februar 2022'
    result = translator.translate(g_text)   
    print(result)


if __name__ == '__main__':
    main()