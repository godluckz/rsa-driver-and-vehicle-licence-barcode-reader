from drivers_licence import read_driver_licence_barcode
from vehicle_licence_disc import read_vehicle_licence_barcode

if __name__ == "__main__":
    _DEBUG_ON  = False
    print("=======================================================")
    read_driver_licence_barcode("images/gz_dl_back.jpeg",_DEBUG_ON)    
    print("=======================================================")
    read_vehicle_licence_barcode("images/licence_disc.jpeg",_DEBUG_ON)
