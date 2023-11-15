# FbToCSV

## Introducción

La base de datos interna utiliza el sistema de base de datos _Firebird 2.5.9_, y podemos utilizar una herramienta llamada _FBExport_ para obtener esta información en formato de texto separado por comas (CSV), el cual es compatible con la mayoría de otros software, incluyendo Microsoft Excel.

Las bases de datos incluyen en formato binario las facturas XML y PDF, lo cual complica el proceso de exportación, ya que el tamaño de la base de datos aumenta exponencialmente (problema acentuado por el hecho de que la empresa factura individualmente cada venta, en otras palabras, no hace una factura global para público en general al final del día). Además, esto crea archivos CSV demasiado grandes para herramientas como Excel y manejadores de base de datos haciendo innecesariamente tardados los tiempos de espera al trabajar con esta información.

Por los motivos mencionados, omitiremos los blob, ya que estas se encuentran de manera redundante como archivos individuales en el servidor de archivos y, en caso de no contar con acceso a este servidor, también se encuentran en las bases de datos del SAT.

## Requisitos

- Firebird 2.5.9 superserver con ISQL y las librerías cliente
- FBExport

## Descripción del script

El script consiste en:

1. Obtener una lista de los nombres de cada tabla.
2. Obtener una lista de los nombres de columna de cada tabla.
3. Filtrar y omitir las columnas con tipos de datos BLOB.
4. Filtrar y omitir las tablas cuya cantidad de datos es cero.
5. Generar las sentencias SELECT para cada tabla.
6. Utilizar estas sentencias para crear un archivo CSV de cada tabla.

## Descripción del Dockerfile

Para facilitar la futura ejecución del script, se creó un entorno en docker que:

1. Descarga e instala un servidor local de Firebird y hace enlaces simbólicos a los archivos necesarios.
2. Descarga e instala una copia de FBexport.
3. Ejecuta el script.

## Uso del script

Para utilizar el script, hay que copiar la base de datos (sin comprimir) a la carpeta app y ejecutar la imagen de docker.

`docker build -t fbtocsv:latest .`

`docker run -v ./app:/app fbtocsv`

Eliminar la imagen:

`docker image rm -f fbtocsv`

Acceder al contenedor:

`docker run --rm -it -v ./app:/app --entrypoint /bin/bash fbtocsv`

## Notas

Se puede encontrar más información de este software en la dirección electrónica: [https://fbexport.sourceforge.net/fbexport.html](https://fbexport.sourceforge.net/fbexport.html)