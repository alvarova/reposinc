import re, os
import sys
import subprocess
import json
#import mysql.connector

#Puntero a nul para evitar volcado en pantalla
FNULL = open(os.devnull, 'w')
#nombre del archivo para volcado
dump = "dumpIPs.log"


def stage(msg, level):
    # \033[<style>;<text_color>;<background_color>m
    # Estilo normal

    if level == 1:
        print("\033[0m"+msg)
    elif level == 2:
        # Texto amarillo con fondo verde
        print("\033[93m"+msg)
        print("\033[0m ")
    elif level == 3:    
        # Texto rojo
        print("\033[91m"+msg)
        print("\033[0m ")
    elif level == 4:
        # Texto azul con fondo blanco y subrayado
        print("\033[94m"+msg)
        print("\033[0m ")
    else:
        print("\033[0m"+msg)




stage("::Iniciando::",4)
if len(sys.argv) > 1:
    additional_param = sys.argv[1]
else:
    stage("Ejecutando sin parametro de rango de red genérico",2)
    additional_param = "10.7.6.1-254"

stage("--Scan de red--",4)
command = "nmap -sn -oN "+dump+" --privileged --max-retries 1 --host-timeout 100 --min-hostgroup 256 --min-parallelism 128 " + additional_param
sale=subprocess.call(command, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)

stage("--Apertura de volcado--",4)
with open(dump, 'r') as f:
    lines = f.readlines()


count=0
# Crear archivo de salida
stage("--Procesado de datos--",4)
with open('output.txt', 'w') as outfile:
    for line in lines:
        
        if 'Nmap scan report for' in line:
            # Extraer la direccion IP
            # Evaluar si posee mas de 3 puntos, aparte de IP hay una direccion resuelta
            if line.count(".")>3:
                ip = line.split('(')[1]
                ip = ip.rstrip(")")
            else:
                ip = line.split('for ')[1]

            ip_address = cadena_filtrada = re.sub(r"[^0-9\.]", "", ip).lstrip(".")
            # Buscar la linea con la direccion MAC
            mac_line = lines[lines.index(line) + 2]
            count = count +1

            if "Nmap done" in mac_line:

                stage("::Procesadas "+str(count)+" direcciones IP::",2)
                break
            else:
                # Extraer la direccion MAC
                mac_address = mac_line.split('MAC Address: ')[1].split(' ')[0]

                # Escribir el par IP/MAC en el archivo de salida
                outfile.write(ip_address + '|' + mac_address + '\n')
                print (ip_address + '|' + mac_address + '\n')
                



"""

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="mprod_sifisa_db"
)

mycursor = mydb.cursor()

sql = "INSERT INTO mision ( mision ) VALUES (%s)"
val = (output)
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")    

"""