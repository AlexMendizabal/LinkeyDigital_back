def GetHtmlForEmail(user,monto, corrects = None, region="bob"):
        
        if region=="br":
            body =f""" 
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Bem-vindo a uma nova era de networking eco-consciente!</h1>
                    </div>
                    <div class="content">
                        <p>Estamos muito felizes em tê-lo como parte da nossa comunidade no Soy Yo Digital. Sabemos que você tem um mundo de possibilidades esperando por você conosco, e estamos aqui para guiá-lo em cada passo.</p>
                        <p> nossa plataforma oferece uma maneira simples e poderosa de unir seu conteúdo em um único link e gerar um QR dinâmico. Imagine como será fácil para seu público se conectar com você!</p>

                        {getCorrects(corrects)}

                        <p>Não se esqueça de que estamos aqui para você em cada etapa do caminho. Se em algum momento você tiver dúvidas ou precisar de ajuda, não hesite em entrar em contato conosco. Seu sucesso é o nosso sucesso, e estamos comprometidos em tornar sua experiência com o Soy Yo Digital excepcional.</p>
                        <p>Estamos empolgados com tudo o que você realizará e compartilhará em nossa plataforma. Bem-vindo ao futuro da inovação!</p>
                        <p>Atenciosamente,</p>
                        <p>A equipe do Soy Yo Digital</p>
                        <p>P.S. Se tiver qualquer dúvida ou preocupação, estamos a apenas uma mensagem de distância. Não hesite em nos contatar a qualquer momento. Estamos aqui para você!</p>
                        <div class="centered-link"><a href="https://www.soueu.com.br/u/#/soueu.digital">Clique aqui</a></div>
                        <div class="QR"><img src="https://api.soueu.com.br/media/SouEuDigital-QRCode.png" alt=""></div>
                    </div>
                </div>
            </body>
            """
        else:
            body = f"""         
            <body>
            <div class="container">
                <div class="header">
                    <h1>¡Bienvenido a una nueva era de networking eco-consciente!</h1>
                </div>
                <div class="content">
                    <p>Nos llena de alegría tenerte como parte de nuestra comunidad en Soy Yo Digital. Sabemos que tienes un mundo de posibilidades esperándote con nosotros, y estamos aquí para guiarte en cada paso.</p>
                    <p>Nuestra plataforma te brinda una forma sencilla y poderosa de unir tu contenido en un solo enlace y generar un Qr dinámico. ¡Imagina lo fácil que será para tu audiencia conectarse contigo!</p>
                    
                    {getCorrects(corrects)}

                    <p>No olvides que estamos aquí para ti en cada paso del camino. Si en algún momento tienes preguntas o necesitas ayuda, no dudes en ponerte en contacto con nosotros. Tu éxito es nuestro éxito, y estamos comprometidos en hacer que tu experiencia con Soy Yo Digital sea excepcional.</p>
                    <p>Estamos emocionados por todo lo que lograrás y compartas en nuestra plataforma. ¡Bienvenido al futuro de la innovación!</p>
                    <p>Un cordial saludo,</p>
                    <p>El equipo de Soy Yo Digital</p>
                    <p>P.D. Si tienes cualquier pregunta o inquietud, estamos a solo un mensaje de distancia. No dudes en contactarnos en cualquier momento. ¡Estamos aquí para ti!</p>
                    <div class="centered-link"><a href="https://linkey.digital/soyyodigital">Click aquí</a></div>
                    <div class="QR"><img src="https://api.linkey.digital/media/SoyYo%20Digital-QRCode.png" alt=""></div>
                </div>
            </div>
        </body> """
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #ffffff;
                    border-radius: 10px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    background-color: #000000;
                    color: #ffffff;
                    padding: 10px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .header img {{
                    width: 100px;
                }}
                .header h1 {{
                    margin: 10px 0;
                }}
                .content {{
                    padding: 20px;
                }}
                p {{
                    color: #333333;
                    margin-bottom: 15px;
                }}
                ol {{
                    padding-left: 20px;
                    margin-bottom: 20px;
                }}
                li {{
                    color: #555555;
                    margin-bottom: 10px;
                }}
                a {{
                    color: #007bff;
                    text-decoration: none;
                }}
                table {{
                    font-family: Arial, sans-serif;
                    border-collapse: collapse;
                    width: 100%;
                    margin-bottom: 20px;
                }}
                th, td {{
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
                .footer {{
                    padding-top: 20px;
                    text-align: center;
                    color: #777777;
                }}
                .QR {{
                    text-align: center;
                    margin-top: 20px;
                }}
                .centered-link {{
                    text-align: center;
                    margin-top: -10px;
                }}
            </style>
        </head>



        {body}


        </html>
        """

        return html

def getCorrects(corrects, region="bob"):
    msg = ''
    if corrects:
        table = ''
        for email in corrects:
            table = table + getTD(email["email"])
        if region == "br":
            msg = f'''<p>Queremos que sua experiência seja inesquecível, por isso apresentamos estes passos simples para você começar com o pé direito:</p>
                        <ol>
                            <li>Vá até o nosso painel de administração em <a href="www.soueu.com.br/admin">www.linkey.digital/admin</a></li>
                            <li>Faça login em cada conta usando os seguintes e-mails:
                                <ul>
                                    <table>
                                        <tr>
                                            <th>Contas criadas</th>
                                            <th>Senha</th>
                                        </tr>
                                        {table}
                                    </table>
                                </ul>
                            </li>
                            <li>Uma vez dentro, atualize seu endereço de e-mail para associar sua conta. Você receberá uma confirmação e poderá escolher uma nova senha para maior segurança.</li>
                            <li>Faça login novamente, desta vez com seu novo e-mail e a senha que escolher. Pronto para dar seu toque pessoal ao seu perfil e compartilhar suas maravilhosas criações!</li>
                        </ol>'''

        else : 
            msg = f'''<p>Queremos que tu experiencia sea inolvidable, por eso te presentamos estos simples pasos para que empieces con el pie derecho:</p>
                        <ol>
                            <li>Dirígete a nuestro panel de administración en <a href="www.linkey.digital/admin">www.linkey.digital/admin</a></li>
                            <li>Ingresa a cada cuenta utilizando los siguientes correos:
                                <ul>
                                    <table>
                                        <tr>
                                        <th>Cuestas creadas</th>
                                        <th>contraseña</th>
                                        </tr>
                                        {table}
                                    </table>
                                </ul>
                            </li>
                            <li>Una vez dentro, actualiza tu dirección de correo electrónico para asociar tu cuenta. Recibirás una confirmación y podrás elegir una nueva contraseña para mayor seguridad.</li>
                            <li>Vuelve a iniciar sesión, esta vez con tu nuevo correo y la contraseña que elijas. ¡Listo para darle tu toque personal a tu perfil y compartir tus maravillosas creaciones!</li>
                        </ol>'''
    return msg

def getTD(email, region="bob"):
    if region == "br":
        msg = f'''  <tr>
                        <td>{email}</td>
                        <td>soueu.com.br</td>
                    </tr>'''
    else: 
        msg = f'''  <tr>
                        <td>{email}</td>
                        <td>linkey.digital</td>
                    </tr>'''
    return msg
