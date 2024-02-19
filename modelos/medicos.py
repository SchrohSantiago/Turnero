import csv   # Importacion para leer el CSV
import os # 
import requests
from flask import request
csv_medicos = "modelos//medicos.csv"

id_medico = 1 
medicos = []



url = "https://randomuser.me/api/?password=number,6&inc=name,id,phone,email,login&nat=us" # Url modificada para que el password sea de 6 caracteres y de tipo numerica

def import_csv():
    global medicos # La declaramos con global para un uso global
    global id_medico
    medico = []

    with open(csv_medicos, newline='') as csvfile:  
        reader = csv.DictReader(csvfile) # DictReader permite la lectura de datos por columna
        for row in reader:
            #Convertimos el ID de cadena a entero
            row['id'] = int(row['id'])
            medico.append(row)

    if len(medico) > 0:
        id_medico = medico[-1]["id"] + 1
    else:
        id_medico = 1

def export_medico_csv():
     with open(csv_medicos, 'w', newline='') as csvfile:
        
        campo_nombres = ['id','dni','nombre','apellido','matricula','telefono','email','habilitado']
        writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
        writer.writeheader()
        for medic in medicos:
            writer.writerow(medic)

def crear_medico_api():
    global id_medico
    global medicos

    for _ in range(3):
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            medico_dni = data['results'][0]['id']['value']
            medico_nombre = data['results'][0]['name']['first']
            medico_apellido = data['results'][0]['name']['last']
            medico_matricula = data['results'][0]['login']['password']
            medico_telefono = data['results'][0]['phone']
            medico_email = data['results'][0]['email']
           
            
            

            paciente = {
                "id": id_medico,
                "dni": medico_dni,
                "nombre": medico_nombre,
                "apellido": medico_apellido,
                "matricula": medico_matricula,
                "telefono": medico_telefono,
                "email": medico_email,
                "habilitado": 1
            }
            id_medico += 1
            medicos.append(paciente)
    export_medico_csv()

def obtener_lista_medicos():
    if os.path.exists(csv_medicos):
        import_csv()
        return medicos
    None

def obtener_medico_id(id_search):
    global medicos
    

    for i in medicos:
        if i['id'] == int(id_search):
            return i
    return None


def agregar_medico(data):
    global medicos
    global id_medico

    medicos.append({
        'id': id_medico,
        'dni': data['dni'],
        'nombre': data['nombre'],
        'apellido': data['apellido'],
        'matricula': data['matricula'],
        'telefono': data['telefono'],
        'email': data['email'],
        'habilitado': 1
    })

    id_medico += 1
    export_medico_csv()

    return medicos

def modificar_medico(search_id,data):
    global medicos

    for medico in medicos:
        if medico['id'] == search_id:
            medico['dni'] = data['dni']
            medico['nombre'] = data['nombre']
            medico['apellido'] = data['apellido']
            medico['matricula'] = data['matricula']
            medico['telefono'] = data['telefono']
            medico['email'] = data['email']
            medico['habilitado'] = 1
            print(medico)
            export_medico_csv()
            print('datos exportados')
            return medico

    return None

def desabilitar_medico(search_id):
    global medicos

    for medico in medicos:
        if medico['id'] == search_id:
            medico['habilitado'] = 0
            export_medico_csv()
            return medico
    return None

def verificar_habilitacion_medico(id_medico):
    global medicos
    medico_habilitado = obtener_medico_id(id_medico)
    

    print(medico_habilitado['habilitado'])

    medic_busqueda = int(medico_habilitado['habilitado'])
    print(type(medic_busqueda))

    if medic_busqueda == 1:
        return True
    else: 
        return False
    
