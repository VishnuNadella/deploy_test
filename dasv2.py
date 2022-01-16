# Required Modules for DAS Implementation
from pyzbar.pyzbar import decode
import gspread
import time
import streamlit as st
from PIL import Image

# Required Credentials for Google Sheets API Connection
gc = gspread.service_account(filename="dastest_cred.json")
sh = gc.open_by_key("1nW4f8seohxA24AS7vWTsrvCawztF7HXe6dFHMt-T0v8")
wks = sh.worksheet('DAS-TEST')

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


if startcam:
    # Fetching Image from Camera
    img = Image.open(startcam)
    for i in decode(img):
        
        # Using Pyzbar Decode to decode QR Image
        text = i.data.decode('utf-8')

        # Scanned QR Code Values
        qr_id, qr_name, qr_roll = map(str, text.split('\n'))
        print(qr_id, qr_name, qr_roll)

        # Extracting details from Database using Unique ID from QR Code        
        if wks.find(qr_id):
            dbrow = str(wks.find(qr_id).row)
            db_id = wks.acell('B' + dbrow).value
            db_name = wks.acell('C' + dbrow).value
            db_roll = wks.acell('E' + dbrow).value

            # Checking if scanned QR Code details are matching with Database
            if qr_id == db_id and qr_name == db_name and qr_roll == db_roll:
                attendance_cell = 'H' + dbrow
                attendance = wks.acell(attendance_cell).value

                if attendance == 'FALSE':
                    wks.update(attendance_cell, 'TRUE', raw=False)
                    output = db_name + ' attendance set to ' + \
                        wks.acell(attendance_cell).value
                    print(output)
                    st.success(output)
                    st.balloons()
                    time.sleep(2)

                else:
                    output = db_name + ' is already present!'
                    print(output)
                    st.error(output)
                    time.sleep(2)

            # Error if QR Code doesn't match with the Database
            else:
                output = 'QR Not Matching with Database'
                print(output)
                print(db_id, db_name, db_roll)
                st.error(output)
                time.sleep(2)

        else:
            output = 'QR Not Matching with Database'
            st.error(output)
            time.sleep(2)

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
