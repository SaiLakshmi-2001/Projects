import streamlit as st
import pandas as pd

# Initialize session states
if "patients" not in st.session_state:
    st.session_state.patients = pd.DataFrame(columns=["Name", "Phone", "Address", "Date", "Disease"])

if "doctors" not in st.session_state:
    st.session_state.doctors = pd.DataFrame(columns=["Name", "Specialization"])

if "appointments" not in st.session_state:
    st.session_state.appointments = pd.DataFrame(columns=["Patient Name", "Doctor", "Date"])

st.title("🏥 Hospital Management System")

menu = st.sidebar.selectbox("Menu", [
    "Add Patient", "View Patients", "Search Patient", "Delete Patient",
    "Add Doctor", "View Doctors", "Search Doctor", "Delete Doctor",
    "Book Appointment", "View Appointments", "Cancel Appointment",
    "Billing"
])

# ---------------- Patient Section ----------------
if menu == "Add Patient":
    st.header("➕ Add Patient Details")
    name = st.text_input("Enter Name")
    phone = st.text_input("Enter Phone Number")
    address = st.text_area("Enter Address")
    date = st.date_input("Date of Visit")
    disease = st.text_input("Disease / Symptoms")

    if st.button("Add Patient"):
        if name and phone and address and disease:
            new_patient = {
                "Name": name,
                "Phone": phone,
                "Address": address,
                "Date": str(date),
                "Disease": disease
            }
            st.session_state.patients = pd.concat(
                [st.session_state.patients, pd.DataFrame([new_patient])],
                ignore_index=True
            )
            st.success("Patient details added successfully!")
        else:
            st.error("Please fill in all fields.")

elif menu == "View Patients":
    st.header("📋 List of Patients")
    if not st.session_state.patients.empty:
        st.dataframe(st.session_state.patients)
    else:
        st.info("No patients found.")

elif menu == "Search Patient":
    st.header("🔍 Search Patient")
    query = st.text_input("Enter name/phone to search:")
    if query:
        df = st.session_state.patients.copy()
        df["Phone"] = df["Phone"].astype(str)
        results = df[
            df["Name"].str.lower().str.contains(query.lower()) |
            df["Phone"].str.contains(query)
        ]
        st.dataframe(results if not results.empty else pd.DataFrame(columns=df.columns))

elif menu == "Delete Patient":
    st.header("❌ Delete Patient")
    if not st.session_state.patients.empty:
        patient_names = st.session_state.patients["Name"].tolist()
        selected = st.selectbox("Select patient to delete", patient_names)
        if st.button("Delete Patient"):
            st.session_state.patients = st.session_state.patients[
                st.session_state.patients["Name"] != selected
            ].reset_index(drop=True)
            st.success(f"Deleted patient: {selected}")
    else:
        st.info("No patients to delete.")

# ---------------- Doctor Section ----------------
elif menu == "Add Doctor":
    st.header("➕ Add Doctor")
    name = st.text_input("Doctor's Name")
    specialization = st.text_input("Specialization")
    if st.button("Add Doctor"):
        if name and specialization:
            new_doc = {"Name": name, "Specialization": specialization}
            st.session_state.doctors = pd.concat(
                [st.session_state.doctors, pd.DataFrame([new_doc])],
                ignore_index=True
            )
            st.success("Doctor added successfully!")
        else:
            st.error("Please fill in all fields.")

elif menu == "View Doctors":
    st.header("👨‍⚕️ List of Doctors")
    if not st.session_state.doctors.empty:
        st.dataframe(st.session_state.doctors)
    else:
        st.info("No doctors added yet.")

elif menu == "Search Doctor":
    st.header("🔍 Search Doctor")
    query = st.text_input("Enter doctor's name or specialization:")
    if query:
        df = st.session_state.doctors
        results = df[df.apply(lambda row: query.lower() in row["Name"].lower() or query.lower() in row["Specialization"].lower(), axis=1)]
        st.dataframe(results if not results.empty else pd.DataFrame(columns=["Name", "Specialization"]))

elif menu == "Delete Doctor":
    st.header("❌ Delete Doctor")
    if not st.session_state.doctors.empty:
        doc_to_delete = st.selectbox("Select doctor to delete", st.session_state.doctors["Name"])
        if st.button("Delete Doctor"):
            st.session_state.doctors = st.session_state.doctors[
                st.session_state.doctors["Name"] != doc_to_delete
            ].reset_index(drop=True)
            st.success(f"Deleted doctor: {doc_to_delete}")
    else:
        st.info("No doctors to delete.")

# ---------------- Appointment Section ----------------
elif menu == "Book Appointment":
    st.header("📅 Book Appointment")
    if st.session_state.patients.empty:
        st.warning("Please add at least one patient.")
    elif st.session_state.doctors.empty:
        st.warning("Please add at least one doctor.")
    else:
        patient = st.selectbox("Select Patient", st.session_state.patients["Name"])
        doctor = st.selectbox("Select Doctor", st.session_state.doctors["Name"])
        date = st.date_input("Appointment Date")
        if st.button("Book Appointment"):
            new_app = {"Patient Name": patient, "Doctor": doctor, "Date": str(date)}
            st.session_state.appointments = pd.concat(
                [st.session_state.appointments, pd.DataFrame([new_app])],
                ignore_index=True
            )
            st.success("Appointment booked successfully!")

elif menu == "View Appointments":
    st.header("📋 All Appointments")
    if not st.session_state.appointments.empty:
        st.dataframe(st.session_state.appointments)
    else:
        st.info("No appointments found.")

elif menu == "Cancel Appointment":
    st.header("❌ Cancel Appointment")
    if not st.session_state.appointments.empty:
        appointment_list = st.session_state.appointments.apply(
            lambda row: f"{row['Patient Name']} with {row['Doctor']} on {row['Date']}", axis=1
        ).tolist()
        selected = st.selectbox("Select appointment to cancel", appointment_list)
        if st.button("Cancel Appointment"):
            st.session_state.appointments = st.session_state.appointments.drop(
                appointment_list.index(selected)
            ).reset_index(drop=True)
            st.success("Appointment cancelled successfully.")
    else:
        st.info("No appointments to cancel.")

# ---------------- Billing Section ----------------
elif menu == "Billing":
    st.header("💳 Patient Billing System")
    if st.session_state.patients.empty:
        st.warning("⚠️ No patients found. Please add patients first.")
    else:
        selected_patient = st.selectbox("Select Patient", st.session_state.patients["Name"])
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
            st.markdown(f"**Patient:** {selected_patient}")
            st.markdown(f"Room Charges: ₹{room_charge} x {num_days} = ₹{room_charge * num_days}")
            st.markdown(f"Consultation Fee: ₹{consultation_fee}")
            st.markdown(f"Lab Tests: ₹{lab_tests_fee}")
            st.markdown(f"Medicines: ₹{medicines_fee}")
            st.markdown(f"Subtotal: ₹{total}")
            st.markdown(f"Discount ({discount_percent}%): -₹{discount:.2f}")
            st.markdown(f"### 🧾 Final Payable Amount: ₹{net_total:.2f}") 


