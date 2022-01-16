# Required Modules for DAS Implementation
from pyzbar.pyzbar import decode
import gspread
import time
import streamlit as st
from PIL import Image

# Required Credentials for Google Sheets API Connection
gc = gspread.service_account(filename="dastest_cred.json")
sh = gc.open_by_key("1nW4f8seohxA24AS7vWTsrvCawztF7HXe6dFHMt-T0v8")


# Searching for target in sheets using Binary Search
def search(low, mid, high, data_set, name, ID, c):
    while low <= high:
        # print("Low:", low, "\nMid:", mid, "\nHigh:", high)
        mid = (high + low) // 2
        # print("We are checking for:", int(data_set[mid][1][2:]), int(ID[2:]))
        if int(data_set[mid][1][2:]) < int(ID[2:]):
            low = mid + 1
        
        elif int(data_set[mid][1][2:]) > int(ID[2:]):
            high = mid - 1
        
        elif int(data_set[mid][1][2:]) == int(ID[2:]):
            if data_set[mid][c] == "FALSE" and name == data_set[mid][2]:
                return True, 1, int(data_set[mid][0]) + 1
            elif data_set[mid][c] == "TRUE" and name == data_set[mid][2]:
                return True, 0, None
            elif name != data_set[mid][2]: # if some one cheats
                return False, 2, None
    else: # Failed to find that element
        return False, None, None

# Checks fletched data

def status(sheet, data_1, data_2, data_3, c): # Searching using Linear Search
    wks = sh.get_worksheet(sheet)
    data_set = wks.get_all_values()
    print(len(data_set))
    low, mid = 0, 0
    high = len(data_set) - 1
    uqn_ID = data_1
    name = data_2
    required, sta, row = search(low, mid, high, data_set, name, uqn_ID, c)
    if required and sta == 1:
        wks.update_cell(row, c + 1, "TRUE")
        # print(f"send: {data_2} with ID: {data_1}")
        output = data_2 + ' attendance set to ' + str(data_set[row][c + 1])
        print(output)
        st.success(output)
        st.balloons()
        time.sleep(2)
        
    elif required and sta == 0:
        output = data_2 + ' is already present!'
        print(output)
        st.error(output)
        time.sleep(2)

    elif sta == 2 or sta == None:
        output = 'QR Not Matching with Database' + str(data_1) + " " + str(data_2) + " " + str(data_3)
        print(output)
        print(data_1, data_2, data_3)
        st.error(output)
        time.sleep(2)
    else:
        output = "Program is dead..."
        print(output)
        st.error(output)
        time.sleep(2)

def decoder(image):
    barcode = decode(image)
    for obj in barcode:
        barcodeData = obj.data.decode("utf-8")
        data_1, data_2, data_3 = map(str, barcodeData.split('\n'))
        if int(data_3[:5]) == 20951:
            status(1, data_1, data_2, data_3, 7)
        elif int(data_3[:5]) == 21955:
            status(2, data_1, data_2, data_3, 6)
        elif int(data_3[:5]) == 21951:
            status(0, data_1, data_2, data_3, 7)
        else:
            output = "Provided QR code is Invalid"
            print(output)
            st.error(output)  ## replace cam with st
            time.sleep(2)
    else:
        st.error("No QR code has been detected; Take a new pic")


# Page Configuration details for Streamlit
st.set_page_config(page_title='DigiAuth System', page_icon="🧊", initial_sidebar_state = 'auto')
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown("""<title> DigiAuth System </title>""", unsafe_allow_html=True)
st.title("Digital Authentication System")

# Declaring empty variable for printing output messages
message = st.empty()

# Camera Input Setup
startcam = st.camera_input('Scan QR Code')

##### FROM HERE 

if startcam:
    img = Image.open(startcam)
    decoder(img)






##### DONT CROSS THIS

# Hiding Streamlit Components which are not necessary
hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown("""<title> DigiAuth System </title>""", unsafe_allow_html=True)