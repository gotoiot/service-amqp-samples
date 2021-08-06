<a href="https://www.gotoiot.com/">
    <img src="_doc/gotoiot-logo.png" alt="logo" title="Goto IoT" align="right" width="60" height="60" />
</a>

Service AMQP Samples
====================

*Ayudaría mucho si apoyaras este proyecto con una ⭐ en Github!*

Este proyecto contiene distintos ejemplos para conectarse a un broker RabbitMQ - basado en el protocolo AMQP 0-9-1 - usando distintos ejemplos en lenguaje Python.

> Para que este servicio funcione deberías contar con un broker RabbitMQ corriendo previo a la ejecución del servicio. Si no sabés como hacerlo, el proyecto [Service AMQP Broker](https://github.com/gotoiot/service-amqp-broker) de nuestra organización de Github tiene toda la información necesaria para correrlo dentro del ecosistema Docker.
 
> Para que entiendas el alcance de este proyecto, es recomendable que leas la [Introducción a AMQP](https://www.gotoiot.com/pages/articles/amqp_intro/index.html) y la [Introducción a RabbitMQ](https://www.gotoiot.com/pages/articles/rabbitmq_intro/index.html) que se encuentran publicadas en nuestra web.


## Instalar las dependencias 🔩

Para correr este proyecto es necesario que instales `Docker` y `Docker Compose`. 

<details><summary><b>Mira cómo instalar las dependencias</b></summary><br>

En [este artículo](https://www.gotoiot.com/pages/articles/docker_installation_linux/) publicado en nuestra web están los detalles para instalar Docker y Docker Compose en una máquina Linux. Si querés instalar ambas herramientas en una Raspberry Pi podés seguir [este artículo](https://www.gotoiot.com/pages/articles/rpi_docker_installation) de nuestra web que te muestra todos los pasos necesarios.

En caso que quieras instalar las herramientas en otra plataforma o tengas algún incoveniente, podes leer la documentación oficial de [Docker](https://docs.docker.com/get-docker/) y también la de [Docker Compose](https://docs.docker.com/compose/install/).

Continua con la descarga del código cuando tengas las dependencias instaladas y funcionando.

</details>

## Descargar el código 💾

Para descargar el código, lo más conveniente es que realices un `fork` de este proyecto a tu cuenta personal haciendo click en [este link](https://github.com/gotoiot/service-amqp-samples/fork). Una vez que ya tengas el fork a tu cuenta, descargalo con este comando (acordate de poner tu usuario en el link):

```
git clone https://github.com/USER/service-amqp-samples.git
```

> En caso que no tengas una cuenta en Github podes clonar directamente este repo.

## Ejecutar la aplicación 🚀

Cuando tengas el código descargado, desde una terminal en la raíz del proyecto ejecuta el comando `docker-compose build amqp-samples` que se va encargar de compilar la imagen con los ejemplos en tu máquina (este proceso puede durar unos minutos dependiento tu conexión a internet). 

Una vez que haya compilado, ejecuta el comando `docker-compose up` que va a correr el comando por defecto del servicio y te va a mostrar una lista con las muestras disponibles para que ejecutes. Deberías ver una salida similar a la siguiente:

```
Starting to run Service AMQP Samples

          /$$$$$$            /$$                    /$$$$$$      /$$$$$$$$
         /$$__  $$          | $$                   |_  $$_/     |__  $$__/
        | $$  \__/ /$$$$$$ /$$$$$$   /$$$$$$         | $$   /$$$$$$| $$   
        | $$ /$$$$/$$__  $|_  $$_/  /$$__  $$        | $$  /$$__  $| $$   
        | $$|_  $| $$  \ $$ | $$   | $$  \ $$        | $$ | $$  \ $| $$   
        | $$  \ $| $$  | $$ | $$ /$| $$  | $$        | $$ | $$  | $| $$   
        |  $$$$$$|  $$$$$$/ |  $$$$|  $$$$$$/       /$$$$$|  $$$$$$| $$   
         \______/ \______/   \___/  \______/       |______/\______/|__/   

                            SERVICE AMQP SAMPLES
                            --------------------

################################################################################

    In this repo there are many samples to connect to RabbitMQ broker.
    Each sample includes help message invoking it with -h flag.

    Default exchange:
        Producer: 
            - docker-compose run amqp-samples python samples/default_exchange/producer.py
        Consumer:
            - docker-compose run amqp-samples python samples/default_exchange/consumer.py

    Direct exchange:
        Producer: 
            - docker-compose run amqp-samples python samples/direct_exchange/producer.py
        Consumer:
            - docker-compose run amqp-samples python samples/direct_exchange/consumer.py

    Fanout exchange:
        Producer: 
            - docker-compose run amqp-samples python samples/fanout_exchange/producer.py
        Consumer:
            - docker-compose run amqp-samples python samples/fanout_exchange/consumer.py

    Topic exchange:
        Producer: 
            - docker-compose run amqp-samples python samples/topic_exchange/producer.py
        Consumer:
            - docker-compose run amqp-samples python samples/topic_exchange/consumer.py

    HTTP integration:
        Entities declaration: 
            - docker-compose run amqp-samples python samples/http_integration/create_exchange.py
            - docker-compose run amqp-samples python samples/http_integration/create_queue.py
            - docker-compose run amqp-samples python samples/http_integration/create_binding.py
        Producer: 
            - docker-compose run amqp-samples python samples/http_integration/send_message.py
        Consumer:
            - docker-compose run amqp-samples python samples/http_integration/get_messages.py

################################################################################
```

Si ves esta salida significa que el servicio se encuentra corriendo adecuadamente. Podés leer la información útil para tener un mejor entendimiento de la aplicación.

## Información útil 🔍

En esta sección vas a encontrar información que te va a servir para tener un mayor contexto.

<details><summary><b>Mira todos los detalles</b></summary>

### Funcionamiento de la aplicación

En la carpeta samples se encuentran todos los ejemplos disponibles. Cada uno de los ejemplos de muestra dispone de un HELP accediendo al script con el flah `-h` o `--help` que te van a mostrar como debes invocarlo para correr adecuadamente.

### Configuración de la aplicación

La configuración para conectarse al broker AMQP está alojada en el archivo `env`. Podés cambiarla escribiendo en este archivo directamente. Si por casualidad llegás a borrar la configuración, podés copiar y modificar esta:

```
RABBITMQ_HOSTNAME=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=gotoiot
RABBITMQ_PASS=gotoiot
RABBITMQ_VHOST=/
```

Así mismo, todos los script de ejemplo están preparados para funcionar con valores por defecto que están definidos de la siguiente manera:

```python
rabbitmq_hostname = os.getenv("RABBITMQ_HOSTNAME", "localhost")
rabbitmq_port = int(os.getenv('RABBITMQ_PORT', 5672))
rabbitmq_user = os.getenv("RABBITMQ_USER", "gotoiot")
rabbitmq_pass = os.getenv("RABBITMQ_PASS", "gotoiot")
rabbitmq_vhost = os.getenv("RABBITMQ_VHOST", "/")
```

### Realizar pruebas

La mejor forma de probar los ejemplos es iniciar un consumidor de cualquier tipo de exchange en una terminal y en otra iniciar un productor del mismo tipo de exchange. Los mensajes enviados desde el productor deberían aparecer en el consumidor. Si bien es posible parametrizar cada uno de los scripts, con utilizar los valores por defecto se pueden realizar todas las pruebas necesarias.

Para este ejemplo vamos a crear un consumidor del exchange `gotoiot.direct` utilizando la routing key `event.maintenance`. Abri una terminal y ejecuta el siguiente comando:

```
docker-compose run amqp-samples \
python samples/direct_exchange/consumer.py gotoiot.direct event.maintenance
```

Por otro lado, en otra terminal, vamos a lanzar un productor de datos hacia el exchange `gotoiot.direct` utilizando la routing key `event.maintenance` con el mensaje `'{"sensor_disconected":true}'`. Abri una terminal y ejecuta el siguiente comando:

```
docker-compose run amqp-samples \
python samples/direct_exchange/producer.py gotoiot.direct event.maintenance '{"sensor_disconected":true}'
```

Luego de enviar el mensaje, en la terminal del consumidor deberías ver un mensaje similar al siguiente:

```
Connecting to RabbitMQ: amqp://gotoiot:gotoiot@rabbitmq:5672
Binding exchange 'gotoiot.direct' to queue 'amq.gen-jcY' with routing key 'event.maintenance'
Starting to consume from 'amq.gen-jcYv3-wzHJmbsKhETSWtNA' with 'event.maintenance' routing_key...To exit press CTRL+C
Received message: b'{"sensor_disconected":true}'
```

</details>

## Tecnologías utilizadas 🛠️

<details><summary><b>Mira la lista de tecnologías usadas en el proyecto</b></summary><br>

* [Docker](https://www.docker.com/) - Ecosistema que permite la ejecución de contenedores de software.
* [Docker Compose](https://docs.docker.com/compose/) - Herramienta que permite administrar múltiples contenedores de Docker.
* [Python](https://www.python.org/) - Lenguaje en el que están realizados los servicios.
* [Pika](https://pypi.org/project/pika/) - Biblioteca de Python para interactuar con RabbitMQ.

</details>

## Contribuir 🖇️

Si estás interesado en el proyecto y te gustaría sumar fuerzas para que siga creciendo y mejorando, podés abrir un hilo de discusión para charlar tus propuestas en [este link](https://github.com/gotoiot/service-amqp-samples/issues/new). Así mismo podés leer el archivo [Contribuir.md](https://github.com/gotoiot/gotoiot-doc/wiki/Contribuir) de nuestra Wiki donde están bien explicados los pasos para que puedas enviarnos pull requests.

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

También podés mirar todas las personas que han participado en la [lista completa de contribuyentes](https://github.com/gotoiot/service-amqp-samples/contributors).

## Licencia 📄

Este proyecto está bajo Licencia ([MIT](https://choosealicense.com/licenses/mit/)). Podés ver el archivo [LICENSE.md](LICENSE.md) para más detalles sobre el uso de este material.

---

**Copyright © Goto IoT 2021** - [**Website**](https://www.gotoiot.com) - [**Group**](https://groups.google.com/g/gotoiot) - [**Github**](https://www.github.com/gotoiot) - [**Twitter**](https://www.twitter.com/gotoiot) - [**Wiki**](https://github.com/gotoiot/doc/wiki)
