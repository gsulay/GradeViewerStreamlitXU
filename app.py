import streamlit as st
import pandas as pd
import json
import requests


UPDATE_PATH = 'https://raw.githubusercontent.com/gsulay/GradeViewerStreamlitXU/refs/heads/main/data/update.json'


def load_file(file_path, sheet_name):
    print(file_path)
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df

def main():
    st.title("Grade Viewer (Classes under Engr. Sulay)")
    #Add the update date
    resp = requests.get(UPDATE_PATH)
    st.markdown(f'''
    <div style="position: fixed; bottom: 10px; right: 10px; font-size: 14px; color: #555; background-color: rgba(255, 255, 255, 0.8); padding: 5px 10px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);">
        {json.loads(resp.text)['update']}
    </div>
    ''', unsafe_allow_html=True)

    DIRECTORY = json.loads(resp.text)['directory']
    
    # Section Selection
    st.subheader("Select Section:")
    sections = DIRECTORY.keys()
    selected_section = st.radio("", sections)

    if selected_section != None:
        cur_dct = DIRECTORY[selected_section]
        # Block Selection
        st.subheader("Select Block:")
        blocks = cur_dct['blocks']
        selected_block = st.radio("", blocks)

        # SLMIS ID Input
        st.subheader("Enter SLMIS ID:")
        slmis_id = st.text_input("", placeholder="Enter your SLMIS ID")


        submit_button = st.button("Submit")

        #Only shows if submit button is pressed
        if submit_button:
            st.html('<hr>')
            try:
                st.subheader("Grade:")

                df = load_file(cur_dct['file'], sheet_name=selected_block)
                isolated_df = df.loc[df['ID'] == int(slmis_id), :]
                
                if isolated_df.empty: raise ValueError  #Raises Value Error if SLMIS ID is invalid
                
                st.dataframe(isolated_df)
            
            #Error Handling
            except FileNotFoundError :
                st.write("Currently Uploading Data...")
            except ValueError:  
                st.write("Invalid SLMIS ID.")
            except requests.exceptions.HTTPError:
                st.write("Currently Uploading Data...")
            except Exception as e:
                st.write('Something went wrong. Please Contact the Engr. Gifrey John M. Sulay', e)
            
            


    else:
        st.write("Please select a section.")

    
if __name__ == "__main__":
    main()