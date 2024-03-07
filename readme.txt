Esto no es una documentacion, pero se especificaran algunas cosas utiles para entender el desarrollo

*********  estatus licencia  ***********

1 --->  Activa
2 --->  Vencida
3 --->  Bloqueada
4 --->  Ilimitada (para admins, etc)

**** estatus de transacciones *********************************

    #Status del transaction
    # 1 --> no_pago
    # 2 --> pagada y por entregar 
    # 3 --> finalizado 


******** explciacion de custom social media *********************

Debido que los modelos fueron mal diseñados anteriormente, para evitar editarlos lo menos posible
y no crear campos inecesarios y ante la necesidad de poner img y files se opto por la siguiente metodologia 
al crear un custom social media de type = image o file recibira el archivo en el request y lo guardara 
en el servidor, luego pondra la direccino del mismo en la url del custom social media
de manera que al obtener un custom social media de tipo image o file quiere decir que 
la url apunta al servidor django.

******** explicacion modelo de productos *************

Debido al poco tiempo que se tiene para sacar la pasarela de pagos,
implementar los metodos adecuados para hacer un crud de productos tomara tiempo que no tenemos,
por ello se opto por poner una tabla falsa de prodcutos, dicha tabla tendra los datos predefenidos,
de esta manera podremos realizar transacciones y llenar la tabla de detalle transaccion (donde se 
guardara la relacion de productos comprados y pagos(transaccion) realizados) 
la tabla falsa actuara como si fuera real, con los metodos adecuados para que el dia que se implemente 
los metodos crud de productos no choque con las otras tablas de transacciones y de detalles


*************** borrado de datos ****************

debido a que el codigo fue pasando de mano en mano, hubieron muchos archivos y modelos planteados
que, a mi pareces, no tienen ningun sentido, intente reacrealos en un diagrama uml pero 
realmente no parecen tener utilidad, estos modelos y metodos jamas de usaron y estan en el olvido
pero darse la tarea de borrar todo es tiempo que no hay, y la verdad, ¿vale la pena? 

********* pay y mercado pago **********************
Debido a que el proyecto se esta lanzando en muchos paises, y que la pasarela de pagos implementada 
con ScrumPay no es apta para aplicarse a otros, se implementara otras pasarelas de pago dentro
del proyecto, como seran mercado pago y etc 
por ahora quieren mantener los usuarios en diferentes servidores (por alguna razon que desconozco)
por lo que el poryecto se estara ramificando, pero la idea es unificar todo en algun momento
esa es la razon por la que mantendre los metodos de mercado pago en otro modulos a los ya creados, y 
lo mismo para todas las otras pasarelas de pago
Sin embargo la primera creada es "pay"



