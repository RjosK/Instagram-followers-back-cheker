from tkinter import *
import pyperclip
import instaloader
import getpass

root = Tk()
root.geometry("500x500")
pass_details = StringVar()
user_details = StringVar()
myList = []

def copytoclipboard():
    # Obtener el contenido del cuadro de texto de solo lectura
    result_box.config(state=NORMAL)  # Permitir leer el contenido
    content = result_box.get(1.0, END).strip()  # Obtener todo el texto desde el inicio (1.0) hasta el final (END)
    result_box.config(state=DISABLED)  # Volver a poner el cuadro en modo solo lectura
    pyperclip.copy(content)  # Copiar el contenido al portapapeles

def get_in():
    username = user_details.get()  # Obtener el usuario desde la entrada
    password = pass_details.get()  # Obtener la contraseña desde la entrada
    if not username or not password:
        print("Usuario o contraseña no proporcionados.")
        return

    ig = instaloader.Instaloader()
    
    try:
        ig.login(user=username, passwd=password)
    except:
        print("Credenciales inválidas.")
        return

    profile = instaloader.Profile.from_username(ig.context, username)
    
    my_followers = [follower.username for follower in profile.get_followers()]
    my_following = [followee.username for followee in profile.get_followees()]
    
    NoFollowMeBack = [followee for followee in my_following if followee not in my_followers]


    myList.extend(NoFollowMeBack)  # Guardar los resultados en la lista para mostrarlos después

    # Limpiar el cuadro de texto antes de mostrar nuevos resultados
    result_box.config(state=NORMAL)  # Permitir escribir en el cuadro temporalmente
    result_box.delete(1.0, END)  # Borrar el contenido anterior
    result_box.insert(END, "\n".join(NoFollowMeBack))  # Insertar los usuarios que no te siguen
    result_box.config(state=DISABLED)  # Volver a poner el cuadro en modo solo lectura

def show_wifi_pass():
    def listToString(s):
        return "\n".join(s)  # Convertir la lista en una cadena con saltos de línea

    myStr = listToString(myList)
    pass_details.set(myStr)

# Interfaz gráfica
Label(root, text="List", font="calibri 20 bold").place(x=240, y=10)

Label(root, text="ENTER YOUR INSTAGRAM ID: ", font="calibri 20 bold").place(x=60, y=80)
Entry(root, textvariable=user_details).place(width=200, height=25, x=60, y=130)

Label(root, text="Password", font="calibri 20 bold").place(x=60, y=160)
Entry(root, textvariable=pass_details, show="*").place(width=200, height=25, x=60, y=210)

Button(root, text="Get List", command=get_in).place(x=60, y=250)

# Cuadro de texto de solo lectura para mostrar la lista de usuarios que no te siguen
result_box = Text(root, height=10, width=30)
result_box.place(x=60, y=290)
result_box.config(state=DISABLED)  # Establecer el cuadro en modo solo lectura

Button(root, text="Copy to Clipboard", command=copytoclipboard).place(x=60, y=470)

root.mainloop()
