import json
import random
import requests
import time

def generate_patient_data(patient_name, critical_counter):
    heart_rate = random.randint(60, 130)
    blood_pressure_numerator = random.randint(60, 200)
    blood_pressure_denominator = random.randint(60, blood_pressure_numerator)
    
    blood_pressure = f"{blood_pressure_numerator}/{blood_pressure_denominator}"

    # Determine if the patient is critical
    is_critical = False
    if critical_counter < 4 and random.choice([True, False]):
        is_critical = True
        critical_counter += 1
    
    return {
        'patient_name': patient_name,
        'heart_rate': heart_rate,
        'blood_pressure': blood_pressure,
        'is_critical': is_critical
    }

def assign_ranks(all_patient_data):
    sorted_patients = sorted(all_patient_data, key=lambda x: x['heart_rate'], reverse=True)
    for rank, patient in enumerate(sorted_patients, start=1):
        patient['rank'] = rank
    return sorted_patients

def send_to_firebase(patient_data):
    firebase_url = "https://hci-project-b0b77-default-rtdb.firebaseio.com/patients.json"
    response = requests.post(firebase_url, json=patient_data)
    if response.status_code == 200:
        print('Patient data added to Firebase successfully')
    else:
        print('Failed to add patient data to Firebase')
        print(response.text)

patients = ["Abheek", "Aadhi", "Pranav", "Jai", "Jans"]
critical_counter = 0

while True:
    all_patient_data = [generate_patient_data(patient, critical_counter) for patient in patients]

    ranked_patients = assign_ranks(all_patient_data)
    json_data = json.dumps(ranked_patients)

    print(json_data)

    for patient_data in ranked_patients:
        print(f"Patient Name: {patient_data['patient_name']}")
        print(f"Heart Rate: {patient_data['heart_rate']}")
        print(f"Blood Pressure: {patient_data['blood_pressure']}")
        print(f"Critical: {patient_data['is_critical']}")
        print(f"Rank: {patient_data['rank']}")
        print(patient_data)
        send_to_firebase(patient_data)
    time.sleep(5)
