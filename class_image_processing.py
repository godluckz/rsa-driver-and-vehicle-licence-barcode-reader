from PIL import Image
from pytesseract import pytesseract

class ImageProcessing:
    def __init__(self) -> None:
        pass


    def get_image_text(self, p_image_with_path) -> list:
        if p_image_with_path:
            w_img = Image.open(p_image_with_path)
                
            w_text = pytesseract.image_to_string(w_img) 
            
            if w_text:
                w_text_list = w_text[:-1].split("\n")

            w_image_text = [text.strip("") for text in w_text_list if text]#clean up to remove empty items
        
        return w_image_text
        

if __name__ == "__main__":    
    pass