# TecnoParking Colmena - Sistema Automático de Parqueo

Hola, bienvenido al repositorio de TecnoParking Colmena. Este es un proyecto que desarrollé pensando en una solución real al caos de movilidad y la falta de espacio en nuestras ciudades. 

Me di cuenta de que los parqueaderos tradicionales desperdician demasiado espacio en rampas y pasillos de maniobra. Por eso, diseñé conceptualmente un sistema basado en una estructura hexagonal (como un panal de abejas), que permite apilar los vehículos y aprovechar el terreno al máximo.

---

## ¿De qué se trata el proyecto?

Más allá del código, TecnoParking es un modelo de negocio y una solución urbana. Al usar un diseño de colmena automatizado, logro varias cosas importantes:

* Aprovechar mejor el espacio: Triplica la cantidad de carros o motos que caben en un lote normal. Ese espacio que se ahorra se le puede devolver a la ciudad en forma de parques o zonas peatonales.
* Ayudar al medio ambiente: Como los vehículos se apagan en la recepción y un elevador eléctrico los acomoda, se reduce hasta en un 80% las emisiones de gases dentro del parqueadero.
* Es un modelo rentable: Se reducen costos porque no se necesita personal acomodando carros ni vigilando cada piso, y el sistema factura automáticamente el tiempo exacto de uso ($4,000 la hora para carros y $2,000 para motos).

---

## ¿Cómo funciona el software?

El cerebro de este sistema lo programé en Python, usando Tkinter para la interfaz gráfica. Quería mantenerlo ligero y funcional, así que las características principales son:

* Dos tipos de usuario: Una terminal rápida y amigable para los clientes, y un panel de control oculto (protegido por la clave "admin") para el administrador.
* Seguridad en los datos: El programa valida estrictamente que las cédulas ingresadas solo contengan números y no superen los 10 dígitos.
* Persistencia en archivos de texto: No depende de bases de datos externas. Todo el registro de vehículos activos y el historial completo de ingresos y salidas del día se guardan y actualizan en tiempo real en archivos .txt.
* Arquitectura a medida: Como requisito técnico para mi clase, no usé el clásico mainloop() de Tkinter. En su lugar, construí mi propio ciclo infinito (while True) controlando el refresco de la pantalla de forma manual con root.update().

---

## ¿Cómo probar el programa?
 Abre tu terminal o consola y ejecuta el archivo principal:
   python "TECNOPARKING VERSION 3.py"

Puedes probar ingresando un vehículo en el modo usuario, o entrar al modo administrador para descargar el reporte del día.

---

## Autor

Este proyecto fue desarrollado exclusivamente por Juan Fernando Rios, estudiante de ingeniería de la Universidad Autónoma de Occidente, como una propuesta que une la programación con la infraestructura urbana.
