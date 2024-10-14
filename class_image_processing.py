from PIL import Image
from pytesseract import pytesseract

class ImageProcessing:
    def __init__(self) -> None:
        pass


    def get_image_text(self, p_image_with_path, p_licence_keywords):        
        w_is_driver_licence = False
        if p_image_with_path:
            w_img = Image.open(p_image_with_path)
                
            w_text = pytesseract.image_to_string(w_img) 
                        
            if w_text:
                w_content = w_text[:-1]
                if not w_is_driver_licence:
                    for keyword in p_licence_keywords:
                        if keyword in w_content:
                            w_is_driver_licence = True
            
                w_content_list = w_content.split("\n")

            w_image_text = [text.strip("") for text in w_content_list if text]#clean up to remove empty items
        
        return w_is_driver_licence, w_image_text
        

if __name__ == "__main__":    
    pass