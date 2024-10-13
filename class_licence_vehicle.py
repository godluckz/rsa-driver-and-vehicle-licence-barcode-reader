from class_shared_utils import SharedUtils
from dbr import BarcodeReader
import json

class LicenceVehicle:
    def __init__(self, p_images_location: str, p_debug_on: bool = False) -> None:
        self.images_location = p_images_location
        self.debug_on        = p_debug_on
        self.image_full_path = None
        self.output_file      = "output/vehicle_licence.json"
        self.shared_utils     = SharedUtils(self.images_location,self.output_file,p_debug_on)
               

            
    def _extract_licence_details(self, p_data: bytearray) -> dict:

        """Extract licence details

        Args:
            data (bytearray)
            
        Returns: 
            list: licence details
        """
        w_byte_data = bytes(p_data)

        w_new_data = ""
        w_disc_extract = []

        for i , chr_byte in enumerate(w_byte_data):
            w_data = w_byte_data[chr_byte]
            self.shared_utils._debug_log(f"bytes: {chr_byte} - index: {w_data}")
            w_chr = chr(chr_byte)
            self.shared_utils._debug_log(f"chr: {w_chr}")
            if chr_byte == 37:
                w_new_data = w_new_data.strip()
                if w_new_data:       
                    w_disc_extract.append(w_new_data)   
                w_new_data = ""
            else:
                if w_chr:
                    w_new_data += w_chr                     
        

        self.shared_utils._debug_log(w_disc_extract)
        # w_licence_details = list(zip(self.shared_utils.driver_data_names ,w_disc_extract))
        w_licence_details = [(key, value) for i, (key, value) in enumerate(zip(self.shared_utils.driver_data_names , w_disc_extract))]        
        w_licence_details_dict = dict(w_licence_details)
        return w_licence_details_dict

    


    def read_vehicle_licence_barcode(self, p_image_name: str, p_image_text: str, p_debug : bool = False) -> None:
        """read licence barcode

        Args:
            p_file (str): file name (full path)
            
        Returns: 
            None
        """    
        self.debug_on = p_debug


        self.image_full_path = f"{self.images_location}/{p_image_name}"
        self.shared_utils._debug_log("=================VEHICLE LICENCE=================")
        self.shared_utils._debug_log(f"**Processing: {self.image_full_path}**")
        self.shared_utils._debug_log("++++++++++++++++++++++")
        self.shared_utils._debug_log(f"text: {p_image_text}")    
        
        BarcodeReader.init_license(self.shared_utils.barcode_licence_key) # logic from (credits to) : https://www.dynamsoft.com/codepool/decode-south-africa-driving-license.html
        reader = BarcodeReader()    
        w_results = reader.decode_file(self.image_full_path)
        w_licence_details = None

        if w_results != None and len(w_results) > 0:
            data = w_results[0].barcode_bytes
            self.shared_utils._debug_log(f"len result: {len(w_results)} - len data: {len(data)}")
            if w_results != None and len(w_results) > 0:
                data = w_results[0].barcode_bytes
                self.shared_utils._debug_log("****************")
                self.shared_utils._debug_log(data)        

                w_licence_details = self._extract_licence_details(data)
        self.shared_utils._write_to_file(p_image_name, w_licence_details)
        

if __name__ == "__main__":
    w_debug      = False    
    W_IMAGES_DIR = "images"      
  

    from os import listdir, remove
    from class_image_processing import ImageProcessing
    image_process   = ImageProcessing()

    vehicle_licence = LicenceVehicle(p_images_location = W_IMAGES_DIR, p_debug_on = w_debug) 

    w_images = listdir(W_IMAGES_DIR)    
    for image_item in w_images:          
        w_image_full_path : str = f"{W_IMAGES_DIR}/{image_item}"
        w_image_text = image_process.get_image_text(p_image_with_path = w_image_full_path)
        if "DRIVING LICENCE" in w_image_text or "DRIVER RESTRICTIONS" in w_image_text or len(w_image_text) < 2:
            continue
        else:
            vehicle_licence.read_vehicle_licence_barcode(p_image_name = image_item,
                                                         p_image_text = w_image_text, 
                                                         p_debug      = w_debug)
                