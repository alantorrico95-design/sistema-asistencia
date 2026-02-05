from werkzeug.security import check_password_hash

stored_hash = 'scrypt:32768:8:1$rOcGSG4tgOD1JfWS$da265ed1854b88d87892878b92dd4d941967320116c2d73f9c71781695ff93d56b'
password_to_check = '12345'

if check_password_hash(stored_hash, password_to_check):
    print(f"La contraseña '{password_to_check}' ES CORRECTA para el hash.")
else:
    print(f"La contraseña '{password_to_check}' ES INCORRECTA para el hash.")
