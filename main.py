from class_licence_driver import LicenceDriver
from class_licence_vehicle import LicenceVehicle
from class_image_processing import ImageProcessing
from os import listdir, remove


if __name__ == "__main__":
    w_debug  = False

    W_IMAGES_DIR  = "images"   
    W_OUTPUT_DIR  = "output"
     

    driver_licence  = LicenceDriver(p_images_location = W_IMAGES_DIR, p_debug_on = w_debug)
    vehicle_licence = LicenceVehicle(p_images_location = W_IMAGES_DIR, p_debug_on = w_debug) 
    image_process   = ImageProcessing()

    # w_output_files = listdir(W_OUTPUT_DIR)   
    # for file in w_output_files:    
    #     remove(f"{W_OUTPUT_DIR}/{file}")   


    w_images = listdir(W_IMAGES_DIR)    
    for image_item in w_images:        
        w_image_full_path : str = f"{W_IMAGES_DIR}/{image_item}"

        w_image_text = image_process.get_image_text(p_image_with_path = w_image_full_path)
        # print(len(w_image_text))

        if "DRIVING LICENCE" in w_image_text or "DRIVER RESTRICTIONS" in w_image_text or len(w_image_text) < 2:
            driver_licence.read_driver_licence_barcode(p_image_name = image_item,
                                                       p_image_text = w_image_text, 
                                                       p_debug      = w_debug)    
        else:
            vehicle_licence.read_vehicle_licence_barcode(p_image_name = image_item,
                                                         p_image_text = w_image_text, 
                                                         p_debug      = w_debug)
    print("+++++++++++++++++++++++++++++++++++")
    print("===================================")
    print("===>>>>>Processing Complete<<<<<===")
    print("===================================")    
    print("+++++++++++++++++++++++++++++++++++")
