from rest_framework.views import APIView
def create_user_task(email, password, errors, lock, corrects, licencia_id):
    try:
        # Intentamos crear el usuario en Firebase
        user = auth.create_user(
            email=email,
            password=password
        )
    except Exception as e:
        print("Error con Firebase")
        with lock:
            errors.append({"email": email, "error": str(e)})
        return
def create_users_in_threads(cant, correo, licencia_id, user_id=None):
    if not licencia_id and user_id:
        try:
            user = CustomerUser.objects.get(id=user_id)
        except Exception as e:
            user = get_object_or_404(CustomerUser, username=user_id)
        licencia_id = user.licencia_id

    if not correo:
        correo = "soyyo"
    correo = correo.lower()
    User = get_user_model()
    users = User.objects.filter(email__startswith=correo, email__endswith=f'@{DOMINIO_NAME}')

    numbers = [int(re.search(re.escape(correo) + r'-(\d+)@', user.email).group(1)) for user in users if re.search(re.escape(correo) + r'-(\d+)@', user.email)]
    max_number = max(numbers) if numbers else 0

    threads = []
    errors = []
    corrects = []
    lock = Lock()

    # Usamos ThreadPoolExecutor para manejar los hilos
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for i in range(1, cant + 1):
            email = f"{correo}-{max_number + i}@{DOMINIO_NAME}"
            password = DOMINIO_NAME

            # Ejecutamos la creación del usuario en un nuevo hilo
            future = executor.submit(create_user_task, email, password, errors, lock, corrects, licencia_id)
            futures.append(future)

        # Esperamos que todos los hilos terminen
        for future in futures:
            try:
                future.result()  # Esto asegura que cualquier excepción en los hilos sea capturada
            except Exception as e:
                errors.append(f"Error creando usuario: {str(e)}")

    return errors, corrects

class CreateALotOfUsers(APIView):
    def post(self, request):
        if not request.user.is_superuser:
            raise TokenNotFound()

        email = request.data.get("email")
        password = request.data.get("password")
        licencia_id = request.data.get("licencia_id")
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            return Response({"mensaje": "El email ya está registrado."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(
            email=email,
            username=email.split('@')[0],
            password=make_password(password),
            licencia_id_id=licencia_id if licencia_id else None
        )
        return Response({"mensaje": "Usuario registrado exitosamente", "user_id": user.id}, status=status.HTTP_201_CREATED)

        if not cant or (not licencia_id and not user_id):
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)
        
        if cant > 50:
            cant = 50

        errors, corrects = create_users_in_threads(cant, correo, licencia_id, user_id)

        if errors:
            return Response({"success": True, "errors": errors, "corrects": corrects}, status=status.HTTP_200_OK)

        return Response({"success": True, "corrects": corrects}, status=status.HTTP_200_OK)
