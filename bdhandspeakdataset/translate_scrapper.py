import pyautogui
import time
import pyperclip as pc
import pandas as pd
from os import listdir
from os.path import isfile, join

exit(0)

class GoogleTranslateWebScrapper: 
    def __init__(self) -> None:
        self.text_input_position_x = 86
        self.text_input_position_y = 360
        self.clipboard_button_max_row = 950
        self.clipboard_button_min_row = 450
        self.clipboard_button_column = 707
        self.max_length_of_sentence = 120

    def clipboard_button_position_learning_module(self):
        learning_text = 'This is me. '
        pc.copy('dummy test')
        sample_clicking_points = []
        for sample_index in range(1, int(self.max_length_of_sentence/len(learning_text))):
            sample_text_to_be_translated = learning_text * sample_index
            # pyautogui.click(86,360)
            pyautogui.click(self.text_input_position_x,self.text_input_position_y)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.typewrite(sample_text_to_be_translated)
            time.sleep(2)
            for i in range(self.clipboard_button_max_row,self.clipboard_button_min_row,-10):   
                pyautogui.click(self.clipboard_button_column, i)
                clipboard_sample = pc.paste()
                if not clipboard_sample == 'dummy test':
                    sample_clicking_points.append(pyautogui.position())
                    pc.copy('dummy test')
                    break
        for sample_clicking_point in sample_clicking_points:
            print(f"x = {sample_clicking_point.x}, y = {sample_clicking_point.y}")
        exit(0)

    def mouse_position_learning_module(self):
        while True:
            print(pyautogui.position())
            time.sleep(1)

    def translate(self, text):
        pyautogui.click(self.text_input_position_x,self.text_input_position_y)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.typewrite(text)
        pc.copy('dummy test')
        time.sleep(len(text)//50 + 1)
        current_translation = 'scrapping error'
        for i in range(self.clipboard_button_max_row,self.clipboard_button_min_row,-10):
            pyautogui.click(self.clipboard_button_column,i)
            current_translation = pc.paste()
            if not current_translation ==  'dummy test':
                return current_translation
        
        return current_translation


path_to_csv_files = '../extractedbdhandspeakskeletons/csv_files.v2'
csv_files = [f for f in listdir(path_to_csv_files) if isfile(join(path_to_csv_files, f))]

scrapper = GoogleTranslateWebScrapper()

for csv_file in csv_files:
    if isfile('translated_csv_files/'+csv_file):
        print('skipping '+csv_file)
        continue

    print('processing csv_file: '+csv_file)
    ocr_dataframe = pd.read_csv(path_to_csv_files+'/'+csv_file)
    ocr_dataframe['translation'] = ''
    for index in ocr_dataframe.index:
        if pd.isnull(ocr_dataframe.loc[index,'text']):
            ocr_dataframe.loc[index,'translation'] = ''
            continue
        # row['translation'] = scrapper.translate(row['text'])
        ocr_dataframe.loc[index,'translation'] = scrapper.translate(ocr_dataframe.loc[index,'text'])
        # print(f"text: {ocr_dataframe.loc[index,'text']}, translation: {ocr_dataframe.loc[index,'translation']}")
    
    ocr_dataframe.to_csv('translated_csv_files/'+csv_file)
