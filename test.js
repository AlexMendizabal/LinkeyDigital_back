// DELETEME: 
// WAITING: JS para hcer la parte de users
const registerNewUser = async () => {
    try {
      setMessage("");
      if (validatePassword()) {
        const res = await createUserWithEmailAndPassword(auth, email, password);

        const user = res.user;
        let idToken = await user.getIdToken(true);

        const response = await fetch(DOMAIN + ENDPOINT_LOGIN_REGISTER, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `JWT ${idToken}`,
          },
        });
        await response.json().then((data) => {
          setMessage("Perfil creado correctamente.");
          history(ROUTER_INITIAL);
        });
      }
    } catch (e) {
      window.alert(e.code);
    }
  };