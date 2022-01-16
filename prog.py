# Required Modules for DAS Implementation
import cv2
from pyzbar.pyzbar import decode
import gspread
import time
import streamlit as st

# Required Credentials for Google Sheets API Connection
gc = gspread.service_account(filename="dastest_cred.json")
sh = gc.open_by_key("1nW4f8seohxA24AS7vWTsrvCawztF7HXe6dFHMt-T0v8")
# wks = sh.worksheet('DAS-TEST')

st.set_page_config(page_title='DigiAuth System', page_icon="🧊",layout = 'wide', initial_sidebar_state = 'auto')
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

camcheck = st.checkbox('Start Camera')
cam = st.image([])

message = st.empty()

cap = cv2.VideoCapture(0)



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



## data_1 -> Unique ID
## data_2 -> Name
## data_3 -> Roll number


def status(sheet, data_1, data_2, data_3, c): # Searching using Linear Search
    wks = sh.get_worksheet(sheet)
    data_set = wks.get_all_values()
    print(len(data_set))
    low, mid = 0, 0
    high = len(data_set) - 1
    uqn_ID = data_1
    name = data_2
    required, st, row = search(low, mid, high, data_set, name, uqn_ID, c)
    if required and st == 1:
        wks.update_cell(row, c + 1, "TRUE")
        # print(f"send: {data_2} with ID: {data_1}")
        output = data_2 + ' attendance set to ' + str(data_set[row][c + 1])
        print(output)
        cam.success(output)
        time.sleep(2)
        
    elif required and st == 0:
        output = data_2 + ' is already present!'
        print(output)
        cam.error(output)
        time.sleep(2)

    elif st == 2 or st == None:
        output = 'QR Not Matching with Database' + str(data_1) + " " + str(data_2) + " " + str(data_3)
        print(output)
        print(data_1, data_2, data_3)
        cam.error(output)
        time.sleep(2)
    else:
        output = "Program is dead..."
        print(output)
        cam.error(output)
        time.sleep(2)


def decoder(image):
    gray_img = cv2.cvtColor(image,0)
    barcode = decode(gray_img)
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
            cam.error(output)
            time.sleep(2)


while camcheck:
    success, img = cap.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cam.image(img)
    decoder(img)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown("""<title> DigiAuth System </title>""", unsafe_allow_html=True)