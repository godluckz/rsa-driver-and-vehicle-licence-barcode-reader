
from class_shared_utils import SharedUtils
from dbr import BarcodeReader
import rsa

class LicenceDriver:
    def __init__(self, p_images_location: str, p_debug_on: bool = False) -> None:
        self.images_location = p_images_location
        self.debug_on        = p_debug_on
        self.image_full_path = None
        self.output_file     = "output/driver_licence.json"
        self.shared_utils    = SharedUtils(self.images_location,self.output_file,p_debug_on)

               

    def _decrypt_data(self, data) -> bytearray:
        # logic from (credits to) : https://www.dynamsoft.com/codepool/decode-south-africa-driving-license.html
        """Decrypt data

        Args:
            data (bytes): Raw data
            
        Returns: 
            bytes: decrypted data
        """

        v1 = self.shared_utils.v1
        v2 = self.shared_utils.v2

        pk_v1_128 = self.shared_utils.pk_v1_128
        pk_v1_74  = self.shared_utils.pk_v1_74

        pk_v2_128 = self.shared_utils.pk_v2_128
        pk_v2_74  = self.shared_utils.pk_v1_74

        
        header = data[0: 6]
        pk128 = pk_v1_128
        pk74 = pk_v1_74
        
        if header[0] == v1[0] and header[1] == v1[1] and header[2] == v1[2] and header[3] == v1[3]:
            pk128 = pk_v1_128
            pk74 = pk_v1_74
        elif header[0] == v2[0] and header[1] == v2[1] and header[2] == v2[2] and header[3] == v2[3]:
            pk128 = pk_v2_128
            pk74 = pk_v2_74
        
        all = bytearray()
        
        pubKey = rsa.PublicKey.load_pkcs1(pk128)
        start = 6
        for i in range(5):
            block = data[start: start + 128]
            input = int.from_bytes(block, byteorder='big', signed=False)
            output = pow(input, pubKey.e, mod=pubKey.n)
            
            decrypted_bytes = output.to_bytes(128, byteorder='big', signed=False)
            all += decrypted_bytes
            
            start = start + 128
        
        pubKey = rsa.PublicKey.load_pkcs1(pk74)
        block = data[start: start + 74]
        input = int.from_bytes(block, byteorder='big', signed=False)
        output = pow(input, pubKey.e, mod=pubKey.n)
        
        decrypted_bytes = output.to_bytes(74, byteorder='big', signed=False)
        all += decrypted_bytes
        
        return all


            
    def _extract_licence_details(self, p_data: bytearray) -> dict:

        """Extract licence details

        Args:
            data (bytearray)
            
        Returns: 
            list: licence details
        """
        w_byte_data = bytes(p_data)

        w_new_data = ""
        w_invalid_chr = ["\x01","\x02","x11&ª¡"]
        w_skip = 0
        w_can_start = False        
        w_disc_extract = []

        for i , chr_byte in enumerate(w_byte_data):
            if not w_can_start and chr_byte == 130: #data start from 130
                w_can_start = True        

            if w_can_start:
                w_skip +=1    # move 2 positions befero starting    
                if w_skip > 2:
                    w_data = w_byte_data[chr_byte]
                    self.shared_utils._debug_log(f"bytes: {chr_byte} - index: {w_data}")
                    w_chr = chr(chr_byte)
                    self.shared_utils._debug_log(f"chr: {w_chr}")

                    if chr_byte == 225 or chr_byte == 224:
                        w_new_data = w_new_data.strip()
                        if w_new_data:       
                            w_disc_extract.append(w_new_data)   
                        w_new_data = ""
                    else:
                        if w_chr and w_chr not in w_invalid_chr:
                            w_new_data += w_chr                     

            if i >= 66:
                self.shared_utils._debug_log("********Done extracting************")   
                w_new_data = w_new_data.strip()    
                if w_new_data:
                    w_disc_extract.append(w_new_data)                                 
                break           

        # w_licence_details = list(zip(self.shared_utils.driver_data_names,w_disc_extract))
        w_licence_details = [(key, value) for i, (key,value) in enumerate(zip(self.shared_utils.driver_data_names,w_disc_extract))]
        w_licence_details_dict = dict(w_licence_details)
        return w_licence_details_dict

    


    def read_driver_licence_barcode(self, p_image_name: str,  p_image_text: str, p_debug : bool = False) -> None:
        """read licence barcode

        Args:
            p_file (str): file name (full path)
            
        Returns: 
            None
        """    
        self.debug_on = p_debug


        self.image_full_path = f"{self.images_location}/{p_image_name}"
        self.shared_utils._debug_log("=================DRIVER LICENCE=================")        
        self.shared_utils._debug_log(f"**Processing: {self.image_full_path }**")
        self.shared_utils._debug_log("++++++++++++++++++++++")
        self.shared_utils._debug_log(f"text: {p_image_text}")                

        BarcodeReader.init_license(self.shared_utils.barcode_licence_key)
        reader = BarcodeReader()    
        w_results = reader.decode_file(self.image_full_path )
        w_licence_details = None

        if w_results != None and len(w_results) > 0:
            data = w_results[0].barcode_bytes
            if w_results != None and len(w_results) > 0:
                data = w_results[0].barcode_bytes
                self.shared_utils._debug_log("****************")
                if data == None or len(data) != 720:
                    w_licence_details = None
                else:    
                    w_decrypted = self._decrypt_data(data)

                    w_licence_details = self._extract_licence_details(w_decrypted)
        # print(f"Licence:: {w_licence_details}")
        self.shared_utils._write_to_file(p_image_name, w_licence_details)       
       
    

if __name__ == "__main__":
    w_debug      = False    
    W_IMAGES_DIR = "images"      
  
    from os import listdir, remove
    from os import listdir
    from class_image_processing import ImageProcessing
    image_process   = ImageProcessing()
    
    driver_licence = LicenceDriver(p_images_location = W_IMAGES_DIR, p_debug_on = w_debug)

    w_dir_items = listdir(W_IMAGES_DIR)    
    for image_item in w_dir_items:        
        w_image_full_path : str = f"{W_IMAGES_DIR}/{image_item}"
        w_image_text = image_process.get_image_text(p_image_with_path = w_image_full_path)

        if "DRIVING LICENCE" in w_image_text or "DRIVER RESTRICTIONS" in w_image_text or len(w_image_text) < 2:
            driver_licence.read_driver_licence_barcode(p_image_name = image_item,
                                                       p_image_text = w_image_text, 
                                                       p_debug      = w_debug)    
        
