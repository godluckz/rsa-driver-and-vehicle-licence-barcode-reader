import json

class SharedUtils:
    def __init__(self, p_images_location: str, p_output_file: str, p_debug_on: bool = False) -> None:
        self.images_location = p_images_location
        self.output_file     = p_output_file        
        self.debug_on        = p_debug_on
        self.barcode_licence_key = "DLS2eyJoYW5kc2hha2VDb2RlIjoiMjAwMDAxLTE2NDk4Mjk3OTI2MzUiLCJvcmdhbml6YXRpb25JRCI6IjIwMDAwMSIsInNlc3Npb25QYXNzd29yZCI6IndTcGR6Vm05WDJrcEQ5YUoifQ=="
        self.driver_data_names   = ["LICENCE_CODE","SURNAME","INITIALS","ID_ISSUE_COUNTRY_CODE","LICENCE_ISSUE_COUNTRY_CODE","RESTRICTIONS","LICENCE_NUMBER","CIVIL_REG_CODE"]
        self.vehicle_data_names  = ["BARCODE_NAME","KEY1","KEY2","DISC_NR","LICENCE_NO","REGISTER_NO","LICENCE_NUMBER","DESCRIPTION","MAKE","MODEL","COLOR","VIN_NO","ENGINE_NO","DISC_EXPIRY_DATE"]
    

        self.v1 = [0x01, 0xe1, 0x02, 0x45]
        self.v2 = [0x01, 0x9b, 0x09, 0x45]

        self.pk_v1_128 = '''
        -----BEGIN RSA PUBLIC KEY-----
        MIGXAoGBAP7S4cJ+M2MxbncxenpSxUmBOVGGvkl0dgxyUY1j4FRKSNCIszLFsMNwx2XWXZg8H53gpCsxDMwHrncL0rYdak3M6sdXaJvcv2CEePrzEvYIfMSWw3Ys9cRlHK7No0mfrn7bfrQOPhjrMEFw6R7VsVaqzm9DLW7KbMNYUd6MZ49nAhEAu3l//ex/nkLJ1vebE3BZ2w==
        -----END RSA PUBLIC KEY-----
        '''

        self.pk_v1_74 = '''
        -----BEGIN RSA PUBLIC KEY-----
        MGACSwD/POxrX0Djw2YUUbn8+u866wbcIynA5vTczJJ5cmcWzhW74F7tLFcRvPj1tsj3J221xDv6owQNwBqxS5xNFvccDOXqlT8MdUxrFwIRANsFuoItmswz+rfY9Cf5zmU=
        -----END RSA PUBLIC KEY-----
        '''

        self.pk_v2_128 = '''
        -----BEGIN RSA PUBLIC KEY-----
        MIGWAoGBAMqfGO9sPz+kxaRh/qVKsZQGul7NdG1gonSS3KPXTjtcHTFfexA4MkGAmwKeu9XeTRFgMMxX99WmyaFvNzuxSlCFI/foCkx0TZCFZjpKFHLXryxWrkG1Bl9++gKTvTJ4rWk1RvnxYhm3n/Rxo2NoJM/822Oo7YBZ5rmk8NuJU4HLAhAYcJLaZFTOsYU+aRX4RmoF
        -----END RSA PUBLIC KEY-----
        '''

        self.pk_v2_74 = '''
        -----BEGIN RSA PUBLIC KEY-----
        MF8CSwC0BKDfEdHKz/GhoEjU1XP5U6YsWD10klknVhpteh4rFAQlJq9wtVBUc5DqbsdI0w/bga20kODDahmGtASy9fae9dobZj5ZUJEw5wIQMJz+2XGf4qXiDJu0R2U4Kw==
        -----END RSA PUBLIC KEY-----
        '''


           
    def _write_to_file(self, p_image_name, p_new_data):
        if p_new_data: 
            licence_details =  {}
            licence_details[p_image_name] = p_new_data
            try:      
                with open(self.output_file,'r+') as file:
                    file_data = json.load(file)
                    file_data.update(licence_details)
                    file.seek(0)
                    json.dump(file_data, file, indent=4)
            except Exception as e:
                with open(self.output_file, 'w+') as file:
                    json.dump(licence_details,file,indent=4)



    def _debug_log(self, p_msg) -> None:
        if self.debug_on:
            print(p_msg)


if __name__ == "__main__":
   pass
        

