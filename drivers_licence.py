from dbr import BarcodeReader
import base64

import rsa

DEBUG_ON = False


def debug_log(p_msg) -> None:
    global DEBUG_ON
    if DEBUG_ON:
        print(p_msg)


def decrypt_data(data) -> bytearray:

    """Decrypt data

    Args:
        data (bytes): Raw data
        
    Returns: 
        bytes: decrypted data
    """

    v1 = [0x01, 0xe1, 0x02, 0x45]
    v2 = [0x01, 0x9b, 0x09, 0x45]

    pk_v1_128 = '''
    -----BEGIN RSA PUBLIC KEY-----
    MIGXAoGBAP7S4cJ+M2MxbncxenpSxUmBOVGGvkl0dgxyUY1j4FRKSNCIszLFsMNwx2XWXZg8H53gpCsxDMwHrncL0rYdak3M6sdXaJvcv2CEePrzEvYIfMSWw3Ys9cRlHK7No0mfrn7bfrQOPhjrMEFw6R7VsVaqzm9DLW7KbMNYUd6MZ49nAhEAu3l//ex/nkLJ1vebE3BZ2w==
    -----END RSA PUBLIC KEY-----
    '''

    pk_v1_74 = '''
    -----BEGIN RSA PUBLIC KEY-----
    MGACSwD/POxrX0Djw2YUUbn8+u866wbcIynA5vTczJJ5cmcWzhW74F7tLFcRvPj1tsj3J221xDv6owQNwBqxS5xNFvccDOXqlT8MdUxrFwIRANsFuoItmswz+rfY9Cf5zmU=
    -----END RSA PUBLIC KEY-----
    '''

    pk_v2_128 = '''
    -----BEGIN RSA PUBLIC KEY-----
    MIGWAoGBAMqfGO9sPz+kxaRh/qVKsZQGul7NdG1gonSS3KPXTjtcHTFfexA4MkGAmwKeu9XeTRFgMMxX99WmyaFvNzuxSlCFI/foCkx0TZCFZjpKFHLXryxWrkG1Bl9++gKTvTJ4rWk1RvnxYhm3n/Rxo2NoJM/822Oo7YBZ5rmk8NuJU4HLAhAYcJLaZFTOsYU+aRX4RmoF
    -----END RSA PUBLIC KEY-----
    '''

    pk_v2_74 = '''
    -----BEGIN RSA PUBLIC KEY-----
    MF8CSwC0BKDfEdHKz/GhoEjU1XP5U6YsWD10klknVhpteh4rFAQlJq9wtVBUc5DqbsdI0w/bga20kODDahmGtASy9fae9dobZj5ZUJEw5wIQMJz+2XGf4qXiDJu0R2U4Kw==
    -----END RSA PUBLIC KEY-----
    '''

    
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
    w_data_names   = ["LICENCE_CODE","SURNAME","INITIALS","ID_ISSUE_COUNTRY_CODE","LICENCE_ISSUE_COUNTRY_CODE","RESTRICTIONS","LICENCE_NUMBER","CIVIL_REG_CODE"]

    for i , chr_byte in enumerate(w_byte_data):
        if not can_start and chr_byte == 130: #data start from 130
            can_start = True        

        if can_start:
            w_skip +=1    # move 2 positions befero starting    
            if w_skip > 2:
                w_data = w_byte_data[chr_byte]
                debug_log(f"bytes: {chr_byte} - index: {w_data}")
                w_chr = chr(chr_byte)
                debug_log(f"chr: {w_chr}")
                w_count +=1
                if chr_byte == 225 or chr_byte == 224:
                    w_new_data = w_new_data.strip()
                    if w_new_data:       
                        w_disc_extract.append(w_new_data)   
                    w_new_data = ""
                else:
                    if w_chr and w_chr not in invalid_chr:
                        w_new_data += w_chr                     

        if i >= 66:
            debug_log("********Done extracting************")   
            w_new_data = w_new_data.strip()    
            if w_new_data:
                w_disc_extract.append(w_new_data)                                 
            break            

    w_licence_details = list(zip(w_data_names,w_disc_extract))
    return w_licence_details

 


def read_driver_licence_barcode(p_file: str, p_debug : bool = False) -> None:
    """read licence barcode

    Args:
        p_file (str): file name (full path)
        
    Returns: 
        None
    """    
    DEBUG_ON = p_debug

    BARCODE_LICENCE_KEY = "DLS2eyJoYW5kc2hha2VDb2RlIjoiMjAwMDAxLTE2NDk4Mjk3OTI2MzUiLCJvcmdhbml6YXRpb25JRCI6IjIwMDAwMSIsInNlc3Npb25QYXNzd29yZCI6IndTcGR6Vm05WDJrcEQ5YUoifQ=="

    BarcodeReader.init_license(BARCODE_LICENCE_KEY)
    reader = BarcodeReader()    
    results = reader.decode_file(p_file)
    w_licence_details = None

    if results != None and len(results) > 0:
        data = results[0].barcode_bytes
        if results != None and len(results) > 0:
            data = results[0].barcode_bytes
            debug_log("****************")
            if data == None or len(data) != 720:
                w_licence_details = None
            else:    
                w_decrypted = decrypt_data(data)

                w_licence_details = extract_licence_details(w_decrypted)
    print(w_licence_details)
        
       
    

if __name__ == "__main__":
    pass
