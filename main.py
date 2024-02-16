import streamlit as st
import datetime
import math
from employee_class import Employee


st.set_page_config(
    page_title="Self Beauty Space - Laser",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded",
)
col1, col2, col3 = st.columns([1,2,1])

with col2:  # Use the middle column for your image
    st.image("self.png", caption="")

def column_checkbox_maker(col_list, col_length, check_dict):
    print("run")
    item_index = 0
    for col in col_list:
        with col:
            for i in range(col_length):
                if item_index == len(check_dict):
                    break
                else:
                    item = list(check_dict.keys())[item_index]
                    st.session_state[item] = st.checkbox(f"{item} - {check_dict[item]}₼")
                    item_index += 1


if 'office' not in st.session_state:
    st.session_state['office'] = ""

if 'laser' not in st.session_state:
    st.session_state['laser'] = ""

if 'specialist' not in st.session_state:
    st.session_state['specialist'] = ""

if 'client_name' not in st.session_state:
    st.session_state['client_name'] = ""

if 'client_surname' not in st.session_state:
    st.session_state['client_surname'] = ""

if 'client_number' not in st.session_state:
    st.session_state['client_number'] = ""

if 'total_time' not in st.session_state:
    st.session_state['total_time'] = 0

if 'chosen_slot' not in st.session_state:
    st.session_state['chosen_slot'] = ""

if 'chosen_procedures' not in st.session_state:
    st.session_state['chosen_procedures'] = []

if 'date' not in st.session_state:
    st.session_state['date'] = datetime.date(2019, 7, 6)

if "date_selected" not in st.session_state:
    st.session_state["date_selected"] = False

if "time_chosen" not in st.session_state:
    st.session_state["time_chosen"] = False

if "procedure_chosen" not in st.session_state:
    st.session_state["procedure_chosen"] = False

if "total_cost" not in st.session_state:
    st.session_state["total_cost"] = 0

if "times_available" not in st.session_state:
    st.session_state["times_available"] = []

spots = {"Dodaqüstü": 5,"Bakenbard": 5,"Çənə": 5,"Üz": 10,"Boğaz": 5,"Üz+Boğaz":12,"Boyun": 5,"Boyun Forma ilə": 10,"Qolaltı": 8,
         "Barmaqlar": 5,"Qollar": 20,"Qollar Dirsəkə qədər": 15,"Sinə": 10,"Qarın (Göbəkdən aşağı)": 5,
         "Qarın": 10, "Kürək": 15, "Bel": 10, "Bikini (Üstü)": 15, "Dərin Bikini (Bikini + Popo içi)": 20,
         "Ayaqlar (dizə qədər)": 15, "Ayaqlar Tam": 25, "Popo": 10,
         "Standard- ayaqlar, qollar, qolaltı, dərin bikini, üz, boğaz": 45,
         "Full Paket - bədənin hər bir hissəsi, üz": 60, "Korreksiya - 1 nahiyyə": 5,
         "Korreksiya - 2 və ya daha çox nahiyyə": 10, "Tükün qısaldılması (bikini keçirilmir)": 5}


for spot in spots:
    if spot not in st.session_state:
        st.session_state[spot] = False


col1, col2, col3 = st.columns([1,2,1])

with col2:  # Use the middle column for your image
    st.image("combo.jpg", caption="Sahil ---- Əhmədli", use_column_width=True)


st.session_state["office"] = st.selectbox("Hansı filialı tərcih edirsiniz?", ("","Sahil", "Əhmədli - tezlikə"))

if st.session_state["office"] != "":
    st.session_state["laser"] = st.selectbox("Hansı lazer cihazını tərcih edirsiniz?", ("","Aleksandrit", "Diod"))

if st.session_state["laser"] != "" and st.session_state["laser"] == "Aleksandrit":
    st.session_state["specialist"] = st.selectbox("Hansı mütəxəssisi tərcih edirsiniz?", ("","Natavan","Nailə","İlahə",
                                                                                          "Xəyalə","Zümrüd"))
elif st.session_state["laser"] != "" and st.session_state["laser"] == "Diod":
    st.session_state["specialist"] = st.selectbox("Hansı mütəxəssisi tərcih edirsiniz?", ("","Natavan","Nailə"))
    
if st.session_state["specialist"] != "":
    st.session_state["date"] = st.date_input("Gəlmək istədiyiniz tarixi seçin", datetime.datetime.today())
    st.session_state["date_selected"] = True

if st.session_state["date_selected"]:
    emp = Employee(st.session_state["specialist"])
    emp.load_employee_data()

    st.session_state["time_chosen"] = True

    col1, col2, col3, col4 = st.columns(4)
    more_cols = False
    if len(spots)  > 24 and len(spots) <= 32:
        col1, col2, col3, col4 = st.columns(4)
        col_list = [col1, col2, col3, col4]
        column_checkbox_maker(col_list,8,spots)
    elif len(spots)  > 16 and len(spots) <= 24:
        col1, col2, col3 = st.columns(3)
        col_list = [col1, col2, col3]
        column_checkbox_maker(col_list,8,spots)
    elif len(spots) > 8 and len(spots) <= 16:
        col1, col2 = st.columns(2)
        col_list = [col1, col2]
        column_checkbox_maker(col_list,8,spots)
    else:
        col_list = [col1]
        column_checkbox_maker(col_list,8,spots)

    st.markdown("""*bir neçə nahiyə seçdikdə endirim tətbiq olunur:
                \n2 nahiyyə - 10%
                \n3 nahiyyə - 15%
                \n4 nahiyyə - 20%""")

    st.session_state["procedure_chosen"] = True

    st.session_state["time_chosen"] = True
    for spot in spots.keys():
        if st.session_state[spot]:
            st.session_state["chosen_procedures"].append(spot)
        elif spot in st.session_state["chosen_procedures"] and st.session_state[spot] == False:
            st.session_state["chosen_procedures"].remove(spot)

    st.session_state["chosen_procedures"] = list(dict.fromkeys(st.session_state["chosen_procedures"]))

    st.session_state["total_cost"] = 0
    for spot_chosen in st.session_state["chosen_procedures"]:
        st.session_state["total_cost"] += spots[spot_chosen]

    if len(st.session_state["chosen_procedures"]) == 2:
        st.session_state["total_cost"] = st.session_state["total_cost"]*0.9

    elif len(st.session_state["chosen_procedures"]) == 3:
        st.session_state["total_cost"] = st.session_state["total_cost"]*0.85

    elif len(st.session_state["chosen_procedures"]) > 3:
        st.session_state["total_cost"] = st.session_state["total_cost"]*0.8

    st.session_state["total_cost"] = math.floor(st.session_state["total_cost"])


    st.markdown(f"""**Son qiymət: {st.session_state["total_cost"]}  ₼**""")

st.session_state["total_time"] = 0
for spot in st.session_state["chosen_procedures"]:
    st.session_state["total_time"] += int(emp.get_procedure_time(spot))

if st.session_state["time_chosen"]:
    if not st.session_state["times_available"]:
        st.session_state["times_available"] = emp.find_empty_slots(st.session_state["date"].strftime("%Y-%m-%d"),
                                                                   st.session_state["total_time"])

    if st.session_state["times_available"]:

        st.session_state["chosen_slot"] = st.selectbox("Hansı zamanı tərcih edirsiniz?",
                                                       tuple(emp.find_empty_slots(
                                                           st.session_state["date"].strftime("%Y-%m-%d"),
                                                           st.session_state["total_time"])))
        # Set to True after a slot is chosen, you might want to adjust this logic based on your app's flow

    col1,col2,col3 = st.columns(3)

    with col1:
        st.session_state["client_name"] = st.text_input("Adınız:")

    with col2:
        st.session_state["client_surname"] = st.text_input("Soyadınız:")

    with col3:
        st.session_state['client_number'] = st.text_input("Nömrəniz:")


    if st.button("Qeyd Olun"):
        emp.book(st.session_state["date"].strftime("%Y-%m-%d"), st.session_state["chosen_slot"],
                 st.session_state["total_time"],
                 f"""{st.session_state["client_name"]} {st.session_state["client_surname"]}""",
                 f"""{str(st.session_state["chosen_procedures"])} {str(st.session_state["laser"])}""")
        emp.save_to_json()
        if "times_available" not in st.session_state:
            st.session_state["times_available"] = []
        st.markdown("Qeyd etdik!")