<a href="https://www.gotoiot.com/">
    <img src="_doc/gotoiot-logo.png" alt="logo" title="Goto IoT" align="right" width="60" height="60" />
</a>

Service Worker IoT Core
=======================

*Ayudaría mucho si apoyaras este proyecto con una ⭐ en Github!*

Este proyecto es el worker de la plataforma [Edge IoT Core]() que procesa de manera asincrónica eventos y comandos que provienen de una cola. Utiliza una comunicación con un broker RabbitMQ para obtener de una cola los eventos y comandos a procesar, los ejecuta de manera asincrónica y segura a medida que tiene disponibilidad, y termina impactando los datos en una base de datos o bien realizando una comunicación con distintos servicios.

Es capaz de crear las tablas de la base de datos que necesita para correr, y también es capaz de comunicarse con la base de datos y el broker RabbitMQ tomando las configuraciones de variables de entorno, así como también del archivo de configuración general del servicio.

Debido a que utiliza una cola - que se utiliza de buffer - para porcesar los eventos y comandos, y además realiza un ACK de cada dato tomado de la cola, puede realizar las transacciones de manera segura, garantizando que no se pierda ningun dato.

> Para que este servicio funcione deberías contar con un broker RabbitMQ corriendo previo a la ejecución del servicio.

> Si bien este proyecto está adaptado a funcionar con el proyecto Edge IoT Core, que involucra toda una serie de servicios de Goto IoT, es perfectamente adaptable a la comunicación con otros sistemas,lo que lo convierte en una pieza fundamental de trabajo y comunicación entre procesos de manera desacoplada.

## Instalar las dependencias 🔩

Para correr este proyecto es necesario que instales `Docker` y `Docker Compose`. 

<details><summary><b>Mira cómo instalar las dependencias</b></summary><br>

En [este artículo](https://www.gotoiot.com/pages/articles/docker_installation_linux/) publicado en nuestra web están los detalles para instalar Docker y Docker Compose en una máquina Linux. Si querés instalar ambas herramientas en una Raspberry Pi podés seguir [este artículo](https://www.gotoiot.com/pages/articles/rpi_docker_installation) de nuestra web que te muestra todos los pasos necesarios.

En caso que quieras instalar las herramientas en otra plataforma o tengas algún incoveniente, podes leer la documentación oficial de [Docker](https://docs.docker.com/get-docker/) y también la de [Docker Compose](https://docs.docker.com/compose/install/).

Continua con la descarga del código cuando tengas las dependencias instaladas y funcionando.

</details>

## Descargar el código 💾

Para descargar el código, lo más conveniente es que realices un `fork` de este proyecto a tu cuenta personal haciendo click en [este link](https://github.com/gotoiot/service-worker-iot-core/fork). Una vez que ya tengas el fork a tu cuenta, descargalo con este comando (acordate de poner tu usuario en el link):

```
git clone https://github.com/USER/service-worker-iot-core.git
```

> En caso que no tengas una cuenta en Github podes clonar directamente este repo.

## Ejecutar la aplicación 🚀

Cuando tengas el código descargado, desde una terminal en la raíz del proyecto ejecuta el comando `docker-compose build worker-iot-core` que se va encargar de compilar la imagen del scanner en tu máquina (este proceso puede durar unos minutos dependiento tu conexión a internet). 

Si estás trabajando de manera local - aislado de los demás servicios - podés crear una base de datos de prueba para testear el funcionamiento. Para ello ejecutá el comando `docker-compose run worker-iot-core python bin/create_db.py`.

Una vez que haya compilado activa, ejecutá el servicio de RabbitMQ antes de correr este servicio; para ello ejecuta el comando `docker-compose up -d rabbitmq`. Luego de unos segundos - cuando ya esté corriendo el servicio de RabbitMQ - ejecutá el comando `docker-compose up worker-iot-core` para poner en funcionamiento el servicio. En la terminal (entre un log inicial y las configuraciones) deberías ver una salida similar a la siguiente:

```
...
...
      /$$$$$$            /$$                    /$$$$$$      /$$$$$$$$
     /$$__  $$          | $$                   |_  $$_/     |__  $$__/
    | $$  \__/ /$$$$$$ /$$$$$$   /$$$$$$         | $$   /$$$$$$| $$   
    | $$ /$$$$/$$__  $|_  $$_/  /$$__  $$        | $$  /$$__  $| $$   
    | $$|_  $| $$  \ $$ | $$   | $$  \ $$        | $$ | $$  \ $| $$   
    | $$  \ $| $$  | $$ | $$ /$| $$  | $$        | $$ | $$  | $| $$   
    |  $$$$$$|  $$$$$$/ |  $$$$|  $$$$$$/       /$$$$$|  $$$$$$| $$   
     \______/ \______/   \___/  \______/       |______/\______/|__/   

                      SERVICE WORKER IOT CORE
                      -----------------------
...
...
```

Si ves esta salida significa que el servicio se encuentra corriendo adecuadamente. Podés leer la información útil para tener un mejor entendimiento de la aplicación.

## Información útil 🔍

En esta sección vas a encontrar información que te va a servir para tener un mayor contexto.

<details><summary><b>Mira todos los detalles</b></summary>

### Funcionamiento de la aplicación

El objetivo de la aplicación es leer eventos y comandos provenientes de una cola de RabbitMQ, procesarlos de manera asincrónica y guardar los datos en una base de datos, o bien ejecutar un comando en particular asociado a un handler. Al iniciar, el servicio carga la configuración leyendo las variables de entorno del archivo `env` y las configuraciones del archivo `_storage/settings.json`. En función de los settings inicializa el servicio y luego se queda esperando que lleguen datos por la cola.

Cuando se recibe un nuevo dato, chequea si es un evento o un comando, comprueba la integridad de los datos, y en función del handler asociado a cada entidad realiza el procesamiento. Una vez que realiza el procesamiento, se queda esperando a que lleguen nuevos datos por la cola.

Dada la naturaleza de las colas de mensajes, puede haber eventos y comandos que tarden demasiado en ejecutarse, o bien que el servicio falle en el procesamiento de los mismos, pero debido a que cada mensaje es confirmado luego que se realiza cada operación, los mensajes no confirmados serán mantenidos en la cola hasta que se puedan procesar adecuadamente. Esto le da una gran fiabilidad al sistema.

### Configuración de la aplicación

La configuración de toda la aplicación está alojada en el archivo `_storage/settings.json`. Podés cambiarla escribiendo en este archivo directamente. Si por casualidad llegás a borrar la configuración, podés copiar y modificar esta:

```json
{
    "RABBITMQ_HOSTNAME": "rabbitmq",
    "RABBITMQ_LOCAL_QUEUE_NAME": "local_iot_core",
    "RABBITMQ_PREFETCH_COUNT": 1,
    "EVENTS_TO_OMIT": ""
}
```

Los parámetros de configuración significan lo siguiente:

* **RABBITMQ_HOSTNAME**: Hostname para comunicarse con la cola de mansajes de RabbitMQ.
* **RABBITMQ_LOCAL_QUEUE_NAME**: El nombre de la cola de mensajes a la que se conectará el servicio.
* **RABBITMQ_PREFETCH_COUNT**: La cantidad máxima de mensajes encolados que puede tener el worker (útil cuando hay más de una instancia).
* **EVENTS_TO_OMIT**: La lista de eventos que no se publicaran en caso que sucedan.

Por razones del buen funcionamiento y seguridad de la aplicación, estas variables solo son configurables mediante el archivo `_storage/settings.json`.

### Variables de entorno

Si querés modificar algúna configuración como variable de entorno podés modificar el archivo `env`. Por lo general la configuración por defecto funciona sin necesidad que la modifiques.

### Handlers de eventos y comandos

Cuando llega un nuevo dato por la cola de mensajes, el servicio intentará analizar de qué tipo es, intentará obtener el handler correspondiente desde el mapping `_events_functions_mapping` del archivo `app.py` y realizará el procesamiento. A continuación están los detalles de cada uno de los handlers.

### Binarios

Puede haber ocasiones donde te sea útil ejecutar parte de la funcionalidad como un binario. Todas las utilidades binarias se encuentran en el directorio `bin`.

El siguiente comando sirve para crear una base de datos con las entidades (Modelos) de SQLAlchemy que necesita este servicio para funcionar.

```
docker-compose run worker-iot-core python bin/create_db.py
```

El siguiente comando sirve para borrar completamente la base de datos.

```
docker-compose run worker-iot-core python bin/delete_db.py
```

### Pruebas

La mejor forma de probar el servicio es a través de un cliente de RabbitMQ que pueda enviar datos a la cola donde lee el servicio y evaluar cómo los procesa. En el directorio `test/exploration` tenés algunos archivos de python que sirven para probar las funcionalidades como enviar un evento, o bien datos inválidos y chequear cómo se comporta el servicio. 

Así mismo, si querés podés entrar a la interfaz de RabbitMQ y poder analizar el estado de los Exchanges, Queues, Channels, y demás. Dentro de la interfaz de administración, en la solapa Queues tenés la posibilidad de enviar un mensaje. 

</details>

## Tecnologías utilizadas 🛠️

<details><summary><b>Mira la lista de tecnologías usadas en el proyecto</b></summary><br>

* [Docker](https://www.docker.com/) - Ecosistema que permite la ejecución de contenedores de software.
* [Docker Compose](https://docs.docker.com/compose/) - Herramienta que permite administrar múltiples contenedores de Docker.
* [Python](https://www.python.org/) - Lenguaje en el que están realizados los servicios.
* [Pika](https://pypi.org/project/pika/) - Biblioteca de Python para interactuar con RabbitMQ.
* [SQLAlchemy](https://pypi.org/project/SQLAlchemy/) - Biblioteca de Python por exelencia para interactuar con distintas bases de datos relacionales.

</details>

## Contribuir 🖇️

Si estás interesado en el proyecto y te gustaría sumar fuerzas para que siga creciendo y mejorando, podés abrir un hilo de discusión para charlar tus propuestas en [este link](https://github.com/gotoiot/service-worker-iot-core/issues/new). Así mismo podés leer el archivo [Contribuir.md](https://github.com/gotoiot/gotoiot-doc/wiki/Contribuir) de nuestra Wiki donde están bien explicados los pasos para que puedas enviarnos pull requests.

## Sobre Goto IoT 📖

Goto IoT es una plataforma que publica material y proyectos de código abierto bien documentados junto a una comunidad libre que colabora y promueve el conocimiento sobre IoT entre sus miembros. Acá podés ver los links más importantes:

* **[Sitio web](https://www.gotoiot.com/):** Donde se publican los artículos y proyectos sobre IoT. 
* **[Github de Goto IoT:](https://github.com/gotoiot)** Donde están alojados los proyectos para descargar y utilizar. 
* **[Comunidad de Goto IoT:](https://groups.google.com/g/gotoiot)** Donde los miembros de la comunidad intercambian información e ideas, realizan consultas, solucionan problemas y comparten novedades.
* **[Twitter de Goto IoT:](https://twitter.com/gotoiot)** Donde se publican las novedades del sitio y temas relacionados con IoT.
* **[Wiki de Goto IoT:](https://github.com/gotoiot/doc/wiki)** Donde hay información de desarrollo complementaria para ampliar el contexto.

## Muestas de agradecimiento 🎁

Si te gustó este proyecto y quisieras apoyarlo, cualquiera de estas acciones estaría más que bien para nosotros:

* Apoyar este proyecto con una ⭐ en Github para llegar a más personas.
* Sumarte a [nuestra comunidad](https://groups.google.com/g/gotoiot) abierta y dejar un feedback sobre qué te pareció el proyecto.
* [Seguirnos en twitter](https://github.com/gotoiot/doc/wiki) y dejar algún comentario o like.
* Compartir este proyecto con otras personas.

## Autores 👥

Las colaboraciones principales fueron realizadas por:

* **[Agustin Bassi](https://github.com/agustinBassi)**: Ideación, puesta en marcha y mantenimiento del proyecto.

También podés mirar todas las personas que han participado en la [lista completa de contribuyentes](https://github.com/gotoiot/service-worker-iot-core/contributors).

## Licencia 📄

Este proyecto está bajo Licencia ([MIT](https://choosealicense.com/licenses/mit/)). Podés ver el archivo [LICENSE.md](LICENSE.md) para más detalles sobre el uso de este material.

---

**Copyright © Goto IoT 2021** - [**Website**](https://www.gotoiot.com) - [**Group**](https://groups.google.com/g/gotoiot) - [**Github**](https://www.github.com/gotoiot) - [**Twitter**](https://www.twitter.com/gotoiot) - [**Wiki**](https://github.com/gotoiot/doc/wiki)
