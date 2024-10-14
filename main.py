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

    w_images = listdir(W_IMAGES_DIR)    
    for image_item in w_images:        
        w_image_full_path : str = f"{W_IMAGES_DIR}/{image_item}"
        
        w_is_driver_licence, w_image_text = image_process.get_image_text(p_image_with_path = w_image_full_path, 
                                                                         p_licence_keywords=driver_licence.shared_utils.driver_licence_keywords)
        if driver_licence.shared_utils.debug_on:
            print(w_is_driver_licence," - ",w_image_text)

        if w_is_driver_licence or len(w_image_text) < 2:
            driver_licence.read_driver_licence_barcode(p_image_name = image_item,
                                                       p_image_text = w_image_text)    
        else:
            vehicle_licence.read_vehicle_licence_barcode(p_image_name = image_item,
                                                         p_image_text = w_image_text)
    print("+++++++++++++++++++++++++++++++++++")
    print("===================================")
    print("===>>>>>Processing Complete<<<<<===")
    print("===================================")    
    print("+++++++++++++++++++++++++++++++++++")
