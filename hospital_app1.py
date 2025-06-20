
import streamlit as st
import pandas as pd

# Setup Page
st.set_page_config(page_title="Hospital Management System", layout="wide")

# Background Styling
def set_bg():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("assets/background.jpg");
            background-size: cover;
            background-attachment: fixed;
        }}
        .title-style {{
            font-size:40px;
            color:#004080;
            font-weight:bold;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg()

st.markdown('<p class="title-style">🏥 Hospital Management System</p>', unsafe_allow_html=True)

# Session State Initialization
if "patients" not in st.session_state:
    st.session_state.patients = []

if "doctors" not in st.session_state:
    st.session_state.doctors = pd.DataFrame(columns=["Name", "Specialization"])

if "appointments" not in st.session_state:
    st.session_state.appointments = pd.DataFrame(columns=["Patient", "Doctor", "Date"])

# Sidebar Main Menu
main_menu = st.sidebar.radio("Main Menu", ["Patients", "Doctors", "Appointments", "Billing"])

# -----------------------------------------------
# PATIENTS SECTION
# -----------------------------------------------
if main_menu == "Patients":
    sub_menu = st.sidebar.radio("Patient Options", ["Add Patient", "View Patients", "Search Patient", "Delete Patient"])

    if sub_menu == "Add Patient":
        st.subheader("➕ Add New Patient")
        name = st.text_input("Enter Patient Name")
        if st.button("Add Patient"):
            if name:
                st.session_state.patients.append(name)
                st.success(f"✅ Patient '{name}' added.")
            else:
                st.warning("⚠️ Name cannot be empty.")

    elif sub_menu == "View Patients":
        st.subheader("📋 List of Patients")
        if st.session_state.patients:
            st.write(pd.DataFrame(st.session_state.patients, columns=["Patient Name"]))
        else:
            st.info("No patients added yet.")

    elif sub_menu == "Search Patient":
        st.subheader("🔍 Search Patient")
        search_name = st.text_input("Enter name to search")
        if st.button("Search"):
            results = [p for p in st.session_state.patients if search_name.lower() in p.lower()]
            if results:
                st.success(f"Found: {results}")
            else:
                st.error("❌ No matching patient found.")

    elif sub_menu == "Delete Patient":
        st.subheader("❌ Delete Patient")
        if st.session_state.patients:
            patient_to_delete = st.selectbox("Select Patient to Delete", st.session_state.patients)
            if st.button("Delete Patient"):
                st.session_state.patients.remove(patient_to_delete)
                st.success(f"🗑️ Patient '{patient_to_delete}' deleted.")
        else:
            st.warning("⚠️ No patients to delete.")

# -----------------------------------------------
# DOCTORS SECTION
# -----------------------------------------------
elif main_menu == "Doctors":
    sub_menu = st.sidebar.radio("Doctor Options", ["Add Doctor", "View Doctors", "Delete Doctor"])

    if sub_menu == "Add Doctor":
        st.subheader("➕ Add Doctor")
        doc_name = st.text_input("Doctor Name")
        spec = st.text_input("Specialization")
        if st.button("Add Doctor"):
            if doc_name and spec:
                st.session_state.doctors.loc[len(st.session_state.doctors)] = [doc_name, spec]
                st.success(f"✅ Doctor '{doc_name}' added.")
            else:
                st.warning("⚠️ Please enter all details.")

    elif sub_menu == "View Doctors":
        st.subheader("👨‍⚕️ Doctors List")
        st.dataframe(st.session_state.doctors)

    elif sub_menu == "Delete Doctor":
        st.subheader("❌ Delete Doctor")
        doc_list = st.session_state.doctors["Name"].tolist()
        if doc_list:
            doctor_to_delete = st.selectbox("Select Doctor to Delete", doc_list)
            if st.button("Delete Doctor"):
                st.session_state.doctors = st.session_state.doctors[st.session_state.doctors["Name"] != doctor_to_delete]
                st.success(f"🗑️ Doctor '{doctor_to_delete}' deleted.")
        else:
            st.info("No doctors available.")

# -----------------------------------------------
# APPOINTMENTS SECTION
# -----------------------------------------------
elif main_menu == "Appointments":
    sub_menu = st.sidebar.radio("Appointment Options", ["Book Appointment", "View Appointments", "Delete Appointment"])

    if sub_menu == "Book Appointment":
        st.subheader("📅 Book Appointment")
        if not st.session_state.patients or st.session_state.doctors.empty:
            st.warning("⚠️ Please ensure patients and doctors exist before booking.")
        else:
            patient = st.selectbox("Select Patient", st.session_state.patients)
            doctor = st.selectbox("Select Doctor", st.session_state.doctors["Name"])
            date = st.date_input("Appointment Date")
            if st.button("Book"):
                new_appointment = {"Patient": patient, "Doctor": doctor, "Date": str(date)}
                st.session_state.appointments = pd.concat(
                    [st.session_state.appointments, pd.DataFrame([new_appointment])],
                    ignore_index=True
                )
                st.success("✅ Appointment booked.")

    elif sub_menu == "View Appointments":
        st.subheader("📖 Appointments")
        st.dataframe(st.session_state.appointments)

    elif sub_menu == "Delete Appointment":
        st.subheader("🗑️ Delete Appointment")
        if not st.session_state.appointments.empty:
            index = st.selectbox("Select Appointment to Delete", st.session_state.appointments.index)
            if st.button("Delete Appointment"):
                st.session_state.appointments.drop(index, inplace=True)
                st.session_state.appointments.reset_index(drop=True, inplace=True)
                st.success("✅ Appointment deleted.")
        else:
            st.warning("❌ No appointments to delete.")

# -----------------------------------------------
# BILLING SECTION
# -----------------------------------------------
elif main_menu == "Billing":
    st.header("💳 Patient Billing System")

    if st.session_state.patients:
        selected_patient = st.selectbox("Select Patient", st.session_state.patients)
        room_charge = st.number_input("Room Charge (₹ per day)", min_value=0)
        num_days = st.number_input("Number of Days", min_value=0)
        consultation_fee = st.number_input("Consultation Fee (₹)", min_value=0)
        lab_tests_fee = st.number_input("Lab Test Charges (₹)", min_value=0)
        medicines_fee = st.number_input("Medicines Charges (₹)", min_value=0)

        discount_percent = st.slider("Discount (%)", 0, 50, 0)

        if st.button("Generate Bill"):
            total = (room_charge * num_days) + consultation_fee + lab_tests_fee + medicines_fee
            discount = (discount_percent / 100) * total
            net_total = total - discount

            st.success("💰 Bill Generated Successfully!")
            st.subheader("🧾 Bill Summary")
            st.write(f"**Patient:** {selected_patient}")
            st.write(f"Room Charges: ₹{room_charge} x {num_days} = ₹{room_charge * num_days}")
            st.write(f"Consultation Fee: ₹{consultation_fee}")
            st.write(f"Lab Tests: ₹{lab_tests_fee}")
            st.write(f"Medicines: ₹{medicines_fee}")
            st.write(f"Subtotal: ₹{total}")
            st.write(f"Discount ({discount_percent}%): -₹{discount:.2f}")
            st.markdown(f"### 🧾 Final Payable Amount: ₹{net_total:.2f}")
    else:
        st.warning("⚠️ No patients found. Please add patients first.")
