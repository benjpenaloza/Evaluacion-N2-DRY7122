import urllib.parse
import requests

main_api = 'https://www.mapquestapi.com/directions/v2/route?'
key = "jn6sF7hJLBe0b2M3a4GkFWtLIRtmrXEm"

while True:
    orig = input('Ciudad de Origen (o q para salir): ')

    if orig.lower() in ['q', 'quit']:
        print('Saliendo del programa.')
        break

    dest = input('Ciudad de Destino (o q para salir): ')

    if dest.lower() in ['q', 'quit']:
        print('Saliendo del programa.')
        break

    url = main_api + urllib.parse.urlencode({
        'key': key,
        'from': orig,
        'to': dest
    })

    response = requests.get(url)

    # Verifica conexión correcta
    if response.status_code != 200:
        print('Error al conectar con la API.')
        print('Codigo HTTP:', response.status_code)
        continue

    json_data = response.json()
    json_status = json_data['info']['statuscode']

    if json_status == 0:

        print('\n=============================================')
        print('Ruta de ' + orig + ' a ' + dest)
        print('Duracion del viaje: ' + json_data['route']['formattedTime'])

        km = json_data['route']['distance'] * 1.61
        print('Distancia: ' + str('{:.2f}'.format(km)) + ' km')

        # Verificar si existe fuelUsed
        if 'fuelUsed' in json_data['route']:
            fuel = json_data['route']['fuelUsed'] * 3.78
            print('Combustible requerido: ' + str('{:.2f}'.format(fuel)) + ' litros')
        else:
            print('Combustible requerido: Informacion no disponible')

        print('=============================================')
        print('Narrativa del viaje:')

        for each in json_data['route']['legs'][0]['maneuvers']:
            dist_km = '{:.2f}'.format(each['distance'] * 1.61)

            print('  - ' + each['narrative'] + ' (' + dist_km + ' km)')

        print('=============================================\n')

    elif json_status == 402:
        print('** Error: Ubicacion invalida. Intenta de nuevo. **')

    elif json_status == 611:
        print('** Error: Falta ingresar una ubicacion. **')

    else:
        print('** Error codigo: ' + str(json_status))
        print('Ver: https://developer.mapquest.com/documentation/directions-api/status-codes **')