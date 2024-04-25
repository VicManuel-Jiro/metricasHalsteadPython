#Victor Manuel Jimenez Rosas
#Importacion de modulos
import tempfile
import math
import sys
import os.path as path
import sqlite3 as dbapi
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import ttk
#Definicion de funciones
def main():
    bdProg=dbapi.connect('bdMetricas.db')
    cursor=bdProg.cursor()
    cursor.execute('''create table if not exists tprog(
                                                Operadores integer,
                                                NumOperadores integer,
                                                Operandos integer,
                                                NumOperandos integer,
                                                Longitud integer,
                                                vocabulario integer,
                                                volumen real,
                                                dificultad real,
                                                Nivel real,
                                                Esfuerzo real,
                                                Tiempo real,
                                                Bugs real,
                                                nombre char(700),
                                                Codigo char(7000) PRIMARY KEY);''')
    bdProg.commit()
    cursor.close()
    bdProg.close()
    mi_app = Aplicacion()
    return 0
def abrir():
    try:
        filename = askopenfilename()
        archivo = open(filename, 'r')
        codigo=archivo.read()
        code=str(codigo)
        temp=tempfile.TemporaryFile(mode='w+t')
        codigo=codigo.replace('#', ' #').replace('+=', ' $masigual ').replace('!=', ' $diferente ').replace('**', ' $potencia ').replace('>=', ' $mayorigual ').replace('<=', ' $menorigual ').replace('==', ' $igualigual ').replace('{', ' $llave ').replace('}', ' ').replace('[', ' $corchete ').replace(']', ' ').replace('(', ' $parentesis ').replace(')', ' ').replace(',', ' $coma ').replace('//', ' $entreentera ')
        codigo=codigo.replace('>', ' $mayor ').replace('<', ' $menor ').replace('=', ' $igual ').replace('+', ' $mas ').replace('-', ' $menos ').replace('*', ' $por ').replace('/', ' $entre ').replace('%', ' $modulo ').replace(':', ' $dospuntos ')
        temp.write(codigo)
        temp.seek(0)
        codigo=[token.replace('\n','')for token in temp.readlines()]
        temp.close()    
        diccionario=['None','raise','assert','and', 'as', 'askopenfilename', 'class', 'def', 'elif', 'else', 'except', 'False', 'for', 'from', 'if', 'IOError', 'import', 'input', 'int', 'in', 'is', 'list', 'math', 'open', 'or', 'print', 'range', 'sys', 'str', 'tempfile', 'tkinter', 'True', 'try', 'ttk', 'while', 'float', 'integer', 'from']
        return ope(codigo,diccionario,code,filename)
    except IOError:
        sys.exit()
def ope(codigo,diccionario,code,filename):
    try:
        o=0
        p=0
        op=[]
        pa=[]
        ca=[]
        ban=False
        cadena=False
        for renglon in codigo:
            if (renglon.startswith(' #') == False):
                comment=False
                for palabra in renglon.split():
                    if (palabra.startswith('#') == False and comment==False):
                        if palabra.startswith('"') or palabra.startswith("'") or palabra.startswith('" ') or palabra.startswith("' "):
                            cadena=True
                        if cadena!=True:
                            if (palabra=='def'):
                                o=o+1
                                ban=True
                                if (palabra not in op):
                                    op.append(palabra)
                            elif (palabra=='return' and ban==False):
                                o=o+1
                                if (palabra not in op):
                                    op.append(palabra)
                            elif (palabra=='return' and ban==True):
                                ban=0
                            elif (palabra.startswith('$') or palabra in diccionario):
                                o=o+1
                                if(palabra not in op):
                                    op.append(palabra)
                            elif(palabra.find('.')!= -1 ):
                                o=o+1
                                if(palabra not in op):
                                    op.append(palabra)
                            else:
                                p=p+1
                                if(palabra not in pa):
                                    pa.append(palabra)
                        if (palabra.endswith('"') or palabra.endswith("'") or palabra.endswith(' "') or palabra.endswith(" '")):
                            p=p+1
                            ca.append(palabra)
                            if (ca not in pa):
                                pa.append(ca)
                            cadena=False
                            ca=[]
                        elif cadena==True:
                            ca.append(palabra)
                    else:
                        comment=True
        return len(op),o,len(pa),p,code,filename
    except IOError:
        sys.exit()
#Definicion de clases
class Aplicacion():
    def __init__(self):
        self.raiz = Tk()
        self.raiz.geometry()
        self.raiz.configure(bg = 'beige',bd=15)
        self.raiz.resizable(width=False,height=False)
        self.raiz.title('Proyecto 1')
        self.titulo=ttk.Label(self.raiz, text="Metricas de Sorftware").grid(row=0,column=1,sticky=N)
        self.tinfo = Text(self.raiz, width=135, height=20)
        self.tinfo.grid(row=1,column=1,sticky=N)
        texto_info = "\n\t\tMetricas de Software\n\n"
        texto_info += "\tElaboro:\n"
        texto_info += "\tVictor Manuel Jimenez Rosas"
        self.tinfo.insert("1.0", texto_info)
        self.tinfo.configure(state="disabled")
        self.bsalir = ttk.Button(self.raiz, text='Salir',command=self.raiz.destroy)
        self.bsalir.grid(row=3,column=2,sticky=S+E)
        self.babrir = ttk.Button(self.raiz, text='Abrir archivo', command=self.info)
        self.babrir.grid(row=3,column=0,sticky=W+S)
        self.bAbrirBase = ttk.Button(self.raiz, text='Consultar', command=self.consult)
        self.bAbrirBase.grid(row=3,column=1,sticky=S+W+E)
        self.bguardar = ttk.Button(self.raiz, text='Guardar metricas', command=self.save)
        self.bguardar.grid(row=4,column=1,sticky=S+W+E)
        self.bguardar.configure(state="disabled")
        self.raiz.mainloop()
    def save(self):
        bdProg=dbapi.connect('bdMetricas.db')
        cursor1=bdProg.cursor()
        cursor2=bdProg.cursor()
        cursor1.execute("""Select * from tprog where Codigo =?""",(self.code,))
        self.tinfo.configure(state="normal")
        self.tinfo.delete("1.0", END)
        if (not cursor1.fetchone()):
            cursor2.execute("""insert into tprog values
            (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(self.n1,self.N1,self.n2,self.N2,self.N,self.n,self.V,self.D,self.L,self.E,self.T,self.B,self.nombre,self.code))
            bdProg.commit()
            texto_info ="Registro agregado"
        else:
            texto_info ="Ya existe el registro "
        self.tinfo.insert("1.0", texto_info)
        self.tinfo.configure(state="disabled")
        self.bguardar.configure(state="disabled")
    def consult(self):
        bdProg=dbapi.connect('bdMetricas.db')
        cursor1=bdProg.cursor()
        cursor1.execute("""Select * from tprog""")
        self.tinfo.configure(state="normal")
        self.tinfo.delete("1.0", END)
        texto_info ="\t\t\t\t\t\t\t\tEN BASE\n"
        for tupla in cursor1.fetchall():
            texto_info += str(tupla[12])  + "\n"
            texto_info +="|n1\t|N1\t|n2\t|N2\t|N\t|n\t|V\t\t|D\t\t|L\t\t|E\t\t|T\t\t|B\n"
            
            texto_info += "|"+str(tupla[0])+"\t|"+str(tupla[1])+"\t|"+str(tupla[2])+"\t|"+str(tupla[3])+"\t|"+str(tupla[4])+"\t|"+str(tupla[5])+"\t|"+str("{0:.3f}".format(tupla[6]))+"\t\t|"+str("{0:.3f}".format(tupla[7]))+"\t\t|"+str("{0:.3f}".format(tupla[8]))+"\t\t|"+str("{0:.3f}".format(tupla[9]))+"\t\t|"+str("{0:.3f}".format(tupla[10]))+"\t\t|"+str("{0:.3f}".format(tupla[11]))
            texto_info += "\n_______________________________________________________________________________________________________________________________________\n"
        self.tinfo.insert("1.0", texto_info)
        self.tinfo.configure(state="disabled")
        self.bguardar.configure(state="disabled")
    def info(self):
        self.n1,self.N1,self.n2,self.N2,self.code,self.nombre=abrir()
        self.tinfo.configure(state="normal")
        self.tinfo.delete("1.0", END)
        self.N=self.N1+self.N2
        self.n=self.n1+self.n2
        self.V=self.N*math.log(self.n,2)
        self.D=(self.n1/2)*(self.N2/self.n2)
        self.L=1/self.D
        self.E=self.D*self.V
        self.T=self.E/18
        self.B=(self.E**(2/3))/3000
        texto_info = str(self.nombre)  + "\n"
        texto_info += "\n\t\tMetricas Basicas\n\n"
        texto_info += "Operadores (n1): " + str(self.n1) + "\n"
        texto_info += "Ocurrencias de operadores (N1): " + str(self.N1) + "\n"
        texto_info += "\nOperandos (n2): " + str(self.n2) + "\n"
        texto_info += "Ocurrencias de operandos (N2): " + str(self.N2) + "\n"
        texto_info += "\n\t\tMetricas Derivadas\n\n"
        texto_info += "Longitud (N): " + str(self.N) + "\n"
        texto_info += "Vocabulario (n): " + str(self.n) + "\n"
        texto_info += "Volumen (V): " + str("{0:.4f}".format(self.V)) + "\n"
        texto_info += "Dificultad(D): " + str("{0:.4f}".format(self.D)) + "\n" 
        texto_info += "Nivel (L): " + str("{0:.4f}".format(self.L)) + "\n"
        texto_info += "Esfuerzo de implementacion (E): " + str("{0:.4f}".format(self.E)) + "\n"
        texto_info += "Tiempo de Implementacion (T): " + str("{0:.4f}".format(self.T)) + "\n"
        texto_info += "Numero de Bugs liberados (B): " + str("{0:.4f}".format(self.B)) + "\n"
        texto_info += "\n\n\t\t Codigo\n" + self.code
        self.tinfo.insert("1.0", texto_info)
        self.tinfo.configure(state="disabled")
        self.bguardar.configure(state="normal")
#Programa principal
if __name__ == '__main__':
    main()
