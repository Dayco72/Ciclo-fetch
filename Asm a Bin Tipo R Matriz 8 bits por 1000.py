import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os

# Diccionario de opcodes modificado según la nueva convención:
opcode_map = {
    "ADD": "000000",
    "SUB": "010000",
    "TERN": "100000",
    "SW":   "110000"
}

def reg_to_bin(reg):
    """Convierte un registro del tipo '$4' a una cadena binaria de 5 bits."""
    try:
        # Remueve el signo '$' y convierte a entero
        num = int(reg.replace("$", ""))
        return format(num, '05b')
    except:
        return None

def convert_line(line):
    """Convierte una línea de ASM a una instrucción binaria y agrega '00000100000' al final."""
    tokens = line.strip().split()
    if not tokens:
        return ""
    mnemonic = tokens[0].upper()
    if mnemonic not in opcode_map:
        return f"Error: Instrucción desconocida '{mnemonic}'"
    
    opcode = opcode_map[mnemonic]
    
    # Para ADD, SUB y TERN esperamos 4 tokens: mnemonic, $dest, $src1, $src2
    if mnemonic in ["ADD", "SUB", "TERN"]:
        if len(tokens) != 4:
            return f"Error: Número incorrecto de operandos en '{line.strip()}'"
        dest = reg_to_bin(tokens[1])
        src1 = reg_to_bin(tokens[2])
        src2 = reg_to_bin(tokens[3])
        if None in (dest, src1, src2):
            return f"Error: Formato de registro incorrecto en '{line.strip()}'"
        # Formato: 6 bits (opcode) + 5 bits dest + 5 bits src1 + 5 bits src2
        binary_instruction = opcode + dest + src1 + src2
        return binary_instruction + "00000100000"  # Agrega el sufijo fijo de 11 bits

    # Para SW esperamos 3 tokens: mnemonic, $memoria, $registro
    elif mnemonic == "SW":
        if len(tokens) != 3:
            return f"Error: Número incorrecto de operandos en '{line.strip()}'"
        # En este caso se usa un campo fijo "11111" para el segundo campo
        fixed_field = "11111"
        mem_addr = reg_to_bin(tokens[1])
        reg_field = reg_to_bin(tokens[2])
        if None in (mem_addr, reg_field):
            return f"Error: Formato de registro incorrecto en '{line.strip()}'"
        binary_instruction = opcode + fixed_field + mem_addr + reg_field
        return binary_instruction + "00000100000"
    else:
        return f"Error: Instrucción no soportada '{mnemonic}'"

def load_asm():
    filepath = filedialog.askopenfilename(title="Selecciona el archivo ASM", filetypes=[("ASM Files", "*.ASM"), ("All Files", "*.*")])
    if filepath:
        try:
            with open(filepath, "r") as f:
                content = f.read()
            asm_text.delete(1.0, tk.END)
            asm_text.insert(tk.END, content)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")

def convert_asm_to_bin():
    asm_content = asm_text.get(1.0, tk.END)
    lines = asm_content.strip().splitlines()
    bin_lines = []
    errors = []
    
    # Procesar cada línea y separar errores de instrucciones válidas
    for line in lines:
        # Saltear líneas vacías o comentarios (si comienzan con ; o //)
        if line.strip() == "" or line.strip().startswith(("//", ";")):
            continue
        converted = convert_line(line)
        if converted.startswith("Error:"):
            errors.append(converted)
        else:
            bin_lines.append(converted)
    
    # Mostrar errores si los hay
    if errors:
        messagebox.showerror("Errores en la conversión", "\n".join(errors))
    
    # Concatenar todos los bits de instrucciones válidas
    valid_bits = "".join(bin_lines)
    
    # Si la cantidad de bits no es múltiplo de 8, se rellenan con ceros al final
    if len(valid_bits) % 8 != 0:
        valid_bits = valid_bits.ljust(((len(valid_bits) // 8) + 1) * 8, '0')
    
    # Crear la matriz: dividir los bits en bloques de 8
    rows = [valid_bits[i:i+8] for i in range(0, len(valid_bits), 8)]
    
    # Ajustar la matriz a 1000 filas: si faltan filas, rellenar con "00000000"
    total_rows = 1000
    if len(rows) < total_rows:
        rows.extend(["00000000"] * (total_rows - len(rows)))
    else:
        rows = rows[:total_rows]
    
    # Combinar la matriz en un string para mostrar: cada fila en una línea
    matrix_result = "\n".join(rows)
    bin_text.delete(1.0, tk.END)
    bin_text.insert(tk.END, matrix_result)
    messagebox.showinfo("Conversión", "Conversión a binario completada.")

def save_bin():
    bin_result = bin_text.get(1.0, tk.END)
    if not bin_result.strip():
        messagebox.showwarning("Aviso", "No hay contenido binario para guardar.")
        return
    filepath = filedialog.asksaveasfilename(title="Guardar archivo binario", defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if filepath:
        try:
            with open(filepath, "w") as f:
                f.write(bin_result)
            messagebox.showinfo("Guardado", "Archivo guardado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

# Creación de la ventana principal de la GUI
root = tk.Tk()
root.title("Conversor ASM a Binario")

# Botones y áreas de texto
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=5)

btn_load = tk.Button(frame_buttons, text="Cargar ASM", command=load_asm)
btn_load.grid(row=0, column=0, padx=5)

btn_convert = tk.Button(frame_buttons, text="Convertir a Binario", command=convert_asm_to_bin)
btn_convert.grid(row=0, column=1, padx=5)

btn_save = tk.Button(frame_buttons, text="Guardar Binario", command=save_bin)
btn_save.grid(row=0, column=2, padx=5)

# Área de texto para mostrar el contenido ASM
lbl_asm = tk.Label(root, text="Contenido ASM:")
lbl_asm.pack()
asm_text = scrolledtext.ScrolledText(root, width=70, height=10)
asm_text.pack(padx=10, pady=5)

# Área de texto para mostrar el contenido binario resultante (la matriz)
lbl_bin = tk.Label(root, text="Contenido Binario (Matriz 8x1000):")
lbl_bin.pack()
bin_text = scrolledtext.ScrolledText(root, width=70, height=20)
bin_text.pack(padx=10, pady=5)

root.mainloop()
