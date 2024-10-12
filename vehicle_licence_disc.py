from dbr import BarcodeReader
import base64

import rsa

DEBUG_ON = False


def debug_log(p_msg) -> None:
    global DEBUG_ON
    if DEBUG_ON:
        print(p_msg)


        
def extract_licence_details(p_data: bytearray) -> list:

    """Extract licence details

    Args:
        data (bytearray)
        
    Returns: 
        list: licence details
    """
    w_byte_data = bytes(p_data)

    w_count : int = 0

    invalid_chr = ["\x01","\x02","x11&ª¡"]
    w_skip = 0
    can_start = False
    w_new_data = ""
    w_disc_extract = []
    w_data_names   = ["BARCODE_NAME","KEY1","KEY2","DISC_NR","LICENCE_NO","REGISTER_NO","LICENCE_NUMBER","DESCRIPTION","MAKE","MODEL","COLOR","VIN_NO","ENGINE_NO","DISC_EXPIRY_DATE"]

    for i , chr_byte in enumerate(w_byte_data):
        # if not can_start and chr_byte == 130: #data start from 130
        can_start = True        

        if can_start:
            w_skip +=1    # move 2 positions befero starting    
            if w_skip > 2:
                w_data = w_byte_data[chr_byte]
                debug_log(f"bytes: {chr_byte} - index: {w_data}")
                w_chr = chr(chr_byte)
                debug_log(f"chr: {w_chr}")
                w_count +=1
                if chr_byte == 37:
                    w_new_data = w_new_data.strip()
                    if w_new_data:       
                        w_disc_extract.append(w_new_data)   
                    w_new_data = ""
                else:
                    if w_chr and w_chr not in invalid_chr:
                        w_new_data += w_chr                     
             

    debug_log(w_disc_extract)
    w_licence_details = list(zip(w_data_names,w_disc_extract))
    return w_licence_details

 


def read_vehicle_licence_barcode(p_file: str, p_debug : bool = False) -> None:
    """read licence barcode

    Args:
        p_file (str): file name (full path)
        
    Returns: 
        None
    """    
    DEBUG_ON = p_debug
    
    BARCODE_LICENCE_KEY = "DLS2eyJoYW5kc2hha2VDb2RlIjoiMjAwMDAxLTE2NDk4Mjk3OTI2MzUiLCJvcmdhbml6YXRpb25JRCI6IjIwMDAwMSIsInNlc3Npb25QYXNzd29yZCI6IndTcGR6Vm05WDJrcEQ5YUoifQ=="

    reader = BarcodeReader()    
    results = reader.decode_file(p_file)
    w_licence_details = None

    if results != None and len(results) > 0:
        data = results[0].barcode_bytes
        debug_log(f"len result: {len(results)} - len data: {len(data)}")
        if results != None and len(results) > 0:
            data = results[0].barcode_bytes
            debug_log("****************")
            debug_log(data)        

            w_licence_details = extract_licence_details(data)
    print(w_licence_details)
    

if __name__ == "__main__":
    pass
