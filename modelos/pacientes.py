import csv   # Importacion para leer el CSV
import os # 
import requests
csv_pacientes = "modelos//pacientes.csv"

id_paciente = 1 
pacientes = []



url = "https://randomuser.me/api/?inc=name,id,phone,email,location&nat=us"



def import_csv():
    global pacientes # La declaramos con global para un uso global
    global id_paciente
    libros = []

    with open(csv_pacientes, newline='') as csvfile:  
        reader = csv.DictReader(csvfile) # DictReader permite la lectura de datos por columna
        for row in reader:
            #Convertimos el ID de cadena a entero
            row['id'] = int(row['id'])
            libros.append(row)

    if len(libros) > 0:
        id_paciente = libros[-1]["id"] + 1
    else:
        id_paciente = 1

def export_paciente_csv():
     with open(csv_pacientes, 'w', newline='') as csvfile:
        
        campo_nombres = ['id','dni','nombre','apellido','telefono','email','direccion_calle','direccion_numero']
        writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
        writer.writeheader()
        for paciente in pacientes:
            writer.writerow(paciente)

def crear_pacientes_api():
    global id_paciente
    global pacientes

    for _ in range(3):
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            paciente_dni = data['results'][0]['id']['value']
            paciente_nombre = data['results'][0]['name']['first']
            paciente_apellido = data['results'][0]['name']['last']
            paciente_telefono = data['results'][0]['phone']
            paciente_email = data['results'][0]['email']
            paciente_direccion = data['results'][0]['location']['street']['name']
            paciente_numero_direccion = data['results'][0]['location']['street']['number']

            paciente = {
                "id": id_paciente,
                "dni": paciente_dni,
                "nombre": paciente_nombre,
                "apellido": paciente_apellido,
                "telefono": paciente_telefono,
                "email": paciente_email,
                "direccion_calle": paciente_direccion,
                "direccion_numero": paciente_numero_direccion
            }
            id_paciente += 1
            pacientes.append(paciente)

    export_paciente_csv()

def obtener_lista_pacientes():
    if os.path.exists(csv_pacientes):
        import_csv()
        return pacientes
    None

def obtener_paciente_id(id_search):
    global pacientes
    

    for i in pacientes:
        if i['id'] == int(id_search):
            return i
    return None


def agregar_paciente(data):
    global pacientes
    global id_paciente

    pacientes.append({
        'id': id_paciente,
        'dni': data['dni'],
        'nombre': data['nombre'],
        'apellido': data['apellido'],
        'telefono': data['telefono'],
        'email': data['email'],
        'direccion_calle': data['direccion_calle'],
        'direccion_numero': data['direccion_numero']
    })

    id_paciente += 1
    export_paciente_csv()

    return pacientes

def modificar_paciente(search_id,data):
    global pacientes

    for paciente in pacientes:
        if paciente['id'] == search_id:
            paciente['dni'] = data['dni']
            paciente['nombre'] = data['nombre']
            paciente['apellido'] = data['apellido']
            paciente['telefono'] = data['telefono']
            paciente['email'] = data['email']
            paciente['direccion_calle'] = data['direccion_calle']
            paciente['direccion_numero'] = data['direccion_numero']

            export_paciente_csv()
          
            return paciente

    return None
