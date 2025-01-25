import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

#Função para conectar ao banco de dados
def conectar ():
    return sqlite3.connect('clientes.db')

#Criar tabela se não existir
def criar_tabela():
    conn = conectar()
    c=conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
               id INTEGER PRIMARY KEY  AUTOINCREMENT,
               nome TEXT NOT NULL,
               email TEXT NOT NULL,
               telefone TEXT NOT NULL,
               endereco TEXT NOT NULL)
''')
    conn.commit()
    conn.close()

#Função para inserir cliente
def agregar_cliente():
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()
    endereco = entry_endereco.get()

    if nome and email and telefone and endereco:
        conn = conectar()
        c= conn.cursor()
        c.execute('''
                  INSERT INTO clientes (nome, email,telefone,endereco)
                  VALUES (?,?,?,?)
                  ''', (nome, email,telefone,endereco))
        conn.commit()
        conn.close()

        messagebox.showinfo('Sucesso','Cliente cadastrado com sucesso!')
        mostrar_clientes()
    else:
        messagebox.showerror('Erro', 'Todos os campos são obrigatórios!')

#Função para mostrar clientes
def mostrar_clientes():
     for item in tree.get_children():
          tree.delete(item)
     
     conn = conectar()
     c = conn.cursor ()
     c.execute('SELECT * FROM clientes')
     rows = c.fetchall()
     for row in rows:
        tree.insert("", "end", values=(row[0], row[1], row[2],row[3],row[4]))
        conn.close()

#Fução para deletar cliente
def eliminar_cliente():
    selected = tree.selection()
    if selected:
        cliente_id = tree.item(selected)['values'][0]
        conn = conectar()
        c = conn.cursor()
        c.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo('Sucesso', 'Cliente deletado com sucesso!')
        mostrar_clientes()
    else:
       messagebox.showwarning ('Atenção', 'Selecione um cliente para deletar.')

# Função para atualizar o cliente
def atualizar_cliente ():
    selected = tree.selection()
    if selected:
        cliente_id = tree.item(selected) ['values'][0]
        nome = entry_nome.get()
        email = entry_email.get()
        telefone = entry_telefone.get()
        endereco = entry_endereco.get()

        if nome and email and telefone and endereco:
            conn = conectar()
            c = conn.cursor()
            c.execute('''UPDATE clientes SET nome =?, email =?, telefone =?, endereco = ? WHERE id=? ''',
                    (nome,email,telefone,endereco,cliente_id))
            conn.commit()
            conn.close()

            messagebox.showinfo('Sucesso','Cliente atualizado com sucesso!')
            mostrar_clientes()
        else:
           messagebox.showerror('Erro','Todos os campos são obrigatórios')
    else:
        messagebox.showwarning('Atenção','Selecione um cliente para atualizar.')

    #Interface gráfica
janela = tk.Tk()
janela.title('Cadastro de Clientes - RONNY Comércio')

#Campos de entrada
tk.Label(janela, text = 'Nome').grid(row=0,column=0,padx=10,pady=5)
entry_nome = tk.Entry(janela) 
entry_nome.grid(row=0,column=1, padx=10,pady=5)   

tk.Label(janela,text='E-mail').grid(row=1,column=0,padx=10,pady=5)
entry_email=tk.Entry(janela)
entry_email.grid(row=1,column=1,padx=10,pady=5)

tk.Label(janela,text='Telefone').grid(row=2,column=0,padx=10,pady=5)
entry_telefone=tk.Entry(janela)
entry_telefone.grid(row=2,column=1,padx=10,pady=5)

tk.Label(janela,text='Endereço').grid(row=3,column=0,padx=10,pady=5)
entry_endereco=tk.Entry(janela)
entry_endereco.grid(row=3,column=1,padx=10,pady=5)   

#Botões
btn_agregar = tk.Button(janela, text='Adicionar Cliente', command=agregar_cliente)
btn_agregar.grid(row=4,column=0, columnspan=2, pady=10)

btn_atualizar = tk.Button(janela,text='Atualizar Cliente', command=atualizar_cliente)
btn_atualizar.grid(row=5, column=0, columnspan=2, pady=10)

btn_deletar = tk.Button(janela,text='Deletar Cliente', command=eliminar_cliente)
btn_deletar.grid(row=6, column=0, columnspan=2, pady=10)

#Exibir dados
columns = ('ID', 'Nome', 'E-mail', 'Telefone', 'Endereço')
tree=ttk.Treeview(janela, columns=columns, show='headings')
tree.grid(row=7, column=0,columnspan=2,pady=10,padx=10)

for col in columns:
    tree.heading(col, text=col)


criar_tabela()
mostrar_clientes()

janela.mainloop()

