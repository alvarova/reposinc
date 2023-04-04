import re

with open('test.txt', 'r') as f:
    lines = f.readlines()

# Crear archivo de salida
with open('output.txt', 'w') as outfile:
    for line in lines:
        
        if 'Nmap scan report for' in line:
            # Extraer la direccion IP
            ip = line.split('for ')[1]

            ip_address = cadena_filtrada = re.sub(r"[^0-9\.]", "", ip).lstrip(".")
            # Buscar la linea con la direccion MAC
            mac_line = lines[lines.index(line) + 2]

            if "Nmap done" in mac_line:
                print "Finalizado"
                break
            else:
                # Extraer la direccion MAC
                mac_address = mac_line.split('MAC Address: ')[1].split(' ')[0]

                # Escribir el par IP/MAC en el archivo de salida
                #outfile.write(ip_address + '|' + mac_address + '\n')
                print (ip_address + '|' + mac_address + '\n')