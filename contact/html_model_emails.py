def GetHtmlForEmail(user,monto, corrects = None):
        
        body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    ffont-family: Arial, sans-serif;
                    color: #fff;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #fff;
                }}
                .header {{
                    background-color: #000;
                    color: #fff;
                    padding: 10px;
                    text-align: center;
                    display: flex;
                    align-items: center;

                    border-radius: 50px;
                }}
                .content {{
                    padding: 20px;
                    background-color: #fff;
                }}
                p {{
                    color: #000;
                }}
                img {{
                    width: 100px;
                    margin: 0 50px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <img src="https://www.soyyo.digital/assets/images/soyyo-brand/soyyo-name.png" alt="">
                    <h1>Confirmación de Pago Exitosa</h1>
                </div>
                <div class="content">
                    <p>Estimado/a {user.username},</p>
                    <p>Es un placer informarle que hemos recibido con éxito el pago correspondiente de su pedido. El importe total de {monto} ha sido recibido y registrado en nuestro sistema.</p>
                    <p>Queremos agradecerle por su confianza en Soy Yo Digital.</p>
                    <p>Si tiene alguna pregunta o necesita más información sobre su transacción o cualquier otro asunto, no dude en ponerse en contacto con nuestro equipo de atención al cliente al correo <a href="mailto:soporte@soyyo.digital">soporte@soyyo.digital</a>.</p>
                    <p>Gracias nuevamente por elegir nuestros servicios. Esperamos seguir brindándole la mejor calidad y atención en el futuro.</p>

                    {getCorrects(corrects)}
                    
                </div>
            </div>
        </body>
        </html>
        """

        return body

def getCorrects(corrects):
    if corrects:
        formatted_users = "\n".join([f"'{user['email']}'" for user in corrects])
        correct = f"""<p>Le compartimos los usuarios respectivos a las cuentas que acaba de adquirir:</p>
                    <pre>{formatted_users}</pre>"""
    else :
         correct = ""
    return correct
