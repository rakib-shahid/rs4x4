import hid

vendor_id     = 0xFEDD
product_id    = 0x0753

usage_page    = 0xFF60
usage         = 0x61
report_length = 32

def get_raw_hid_interface():
    device_interfaces = hid.enumerate(vendor_id, product_id)
    raw_hid_interfaces = [i for i in device_interfaces if i['usage_page'] == usage_page and i['usage'] == usage]

    if len(raw_hid_interfaces) == 0:
        return None

    interface = hid.Device(path=raw_hid_interfaces[0]['path'])

    # print(f"Manufacturer: {interface.manufacturer}")
    # print(f"Product: {interface.product}")

    return interface

def send_raw_report(op,data,is_playing=None):
    interface = get_raw_hid_interface()

    if interface is None:
        print("No device found")
        raise FileNotFoundError

    request_data = [0x00] * (report_length - 3) # First byte is Report ID
    request_data[1] = op                        # code for operation (0xFF for text, 0xFC to 0xFE for image)
    request_data[3:len(data)] = data
    if (is_playing):
        request_data[2] = 1
    else:
        request_data[2] = 0
    # print(f"len(request_data) = {len(request_data)}")
    # print(f"request_data = {request_data}")
    request_report = bytes(request_data)

    try:
        interface.write(request_report)
        response_report = interface.read(report_length, timeout=1000)
    except Exception as e:
        print(e)
        
def send_image_data(data,first = None,last=None):
    print(data)
    interface = get_raw_hid_interface()

    if interface is None:
        print("No device found")
        raise FileNotFoundError

    request_data = [0x00] * (report_length - 4) # First byte is Report ID
    if (first == True):
        request_data[1] = 0xFD
    elif (last == True):
        request_data[1] = 0xFC
    else:
        request_data[1] = 0xFE
    request_data[2:len(data)] = data
    print(f"len(request_data) = {len(request_data)}")
    print(f"image_data = {request_data}")

    try:
        interface.write(bytes(request_data))
    except Exception as e:
        print(e)
    
