import tkinter as tk
from functions import *
from pokemon import *
from moves import *

root = tk.Tk()
root.title("Pokémon Damage Calculator")
root.geometry("1050x750")

pokemon_list = list(pokemon_objects.keys())
move_list = list(moves_by_name.keys())

# update search bar
def update_listbox_attacker(*args):
    search_term = search_var.get().lower()
    listbox.delete(0, tk.END)
    for pokemon in pokemon_list:
        if search_term in pokemon.lower():
            listbox.insert(tk.END, pokemon)

def update_listbox_defender(*args):
    search_term = search_var1.get().lower()
    listbox1.delete(0, tk.END)
    for pokemon in pokemon_list:
        if search_term in pokemon.lower():
            listbox1.insert(tk.END, pokemon)

def update_listbox_move(*args):
    search_term = search_var_move.get().lower()
    listbox_move.delete(0, tk.END)
    for move in move_list:
        if search_term in move.lower():
            listbox_move.insert(tk.END, move)

def reset_all():
    # Clear all attacker fields
    for entry in [level_entry, attack_entry, defense_entry, spatk_entry, spdef_entry, speed_entry, hp_entry]:
        entry.delete(0, tk.END)

    # Clear all defender fields
    for entry in [level_entry1, attack_entry1, defense_entry1, spatk_entry1, spdef_entry1, speed_entry1, hp_entry1]:
        entry.delete(0, tk.END)

    # Clear base power and result
    base_power_entry.delete(0, tk.END)
    result_label.config(text="Damage: ")

    # Clear selected move, attacker, defender
    global selected_move, attacker_hp, defender_hp, defender_type1, defender_type2
    selected_move = None
    attacker_hp = 0
    defender_hp = 0
    defender_type1 = "Normal"
    defender_type2 = None

    # Clear labels
    attacker_label.config(text="Selected Attacker: None", fg="gray")
    defender_label.config(text="Selected Defender: None", fg="gray")
    move_label.config(text="Selected Move: None", fg="gray")

    # Clear search entries and listboxes
    search_var.set("")
    search_var1.set("")
    search_var_move.set("")
    listbox.delete(0, tk.END)
    listbox1.delete(0, tk.END)
    listbox_move.delete(0, tk.END)

attacker_hp = 0
defender_hp = 0
selected_move = None
defender_type1 = "Normal"
defender_type2 = None

def on_attacker_select(event):
    global attacker_hp

    try:
        selected = listbox.get(listbox.curselection())
        poke = pokemon_objects[selected]

        level = 50
        stats = poke.get_stats(level)
        attacker_hp = stats["HP"]

        level_entry.insert(0, str(level))
        attack_entry.insert(0, str(stats["Attack"]))
        defense_entry.insert(0, str(stats["Defense"]))
        spatk_entry.insert(0, str(stats["Sp. Atk"]))
        spdef_entry.insert(0, str(stats["Sp. Def"]))
        speed_entry.insert(0, str(stats["Speed"]))
        hp_entry.insert(0, str(stats["HP"]))

        attacker_label.config(text=f"Selected Attacker: {selected}", fg="green")
    except Exception:
        pass

def on_defender_select(event):
    global defender_hp, defender_type1, defender_type2
    try:
        selected = listbox1.get(listbox1.curselection())
        poke = pokemon_objects[selected]
        level = int(level_entry1.get()) if level_entry1.get() else 50
        stats = poke.get_stats(level)

        defender_hp = stats["HP"]
        defender_type1 = poke.type
        defender_type2 = poke.type1 if poke.type1 != "" else None


        level_entry1.insert(0, str(level))
        attack_entry1.insert(0, str(stats["Attack"]))
        defense_entry1.insert(0, str(stats["Defense"]))
        spatk_entry1.insert(0, str(stats["Sp. Atk"]))
        spdef_entry1.insert(0, str(stats["Sp. Def"]))
        speed_entry1.insert(0, str(stats["Speed"]))
        hp_entry1.insert(0, str(stats["HP"]))

        defender_label.config(text=f"Selected Defender: {selected}", fg="blue")
    except Exception:
        pass

def on_move_select(event):
    global selected_move
    try:
        selected = listbox_move.get(listbox_move.curselection())
        selected_move = moves_by_name[selected]
        base_power_entry.delete(0, tk.END)
        base_power_entry.insert(0, str(selected_move.power))
        move_label.config(text=f"Selected Move: {selected_move.name} ({selected_move.type}, {selected_move.kind})", fg="purple")
    except Exception:
        pass

def on_calculate():
    try:
        global selected_move
        if not selected_move:
            result_label.config(text="Please select a move.")
            return

        level = int(level_entry.get()) if level_entry.get() else 100

        def safe_int(entry):
            value = entry.get()
            return int(value) if value.strip().isdigit() else 0

        if selected_move.kind.lower() == "special":
            attack = safe_int(spatk_entry)
            defense = safe_int(spdef_entry1)
        else:
            attack = safe_int(attack_entry)
            defense = safe_int(defense_entry1)

        base_power = int(base_power_entry.get())

        
        print(f"DEBUG: Level: {level}, Attack: {attack}, Defense: {defense}, Base Power: {base_power}")
        print(f"DEBUG: Move type: {selected_move.type}, Kind: {selected_move.kind}")
        print(f"DEBUG: Defender Type1: {defender_type1}, Type2: {defender_type2}")

        if defender_hp <= 0:
            result_label.config(text="Defender HP is invalid or not set.")
            return

        # Get type multiplier
        type_multiplier = get_type_multiplier(selected_move.type, defender_type1, defender_type2)

        # Calculate damage using function from functions.py
        damage = calculate_damage(
            level=level,
            attack=attack,
            defense=defense,
            base_power=base_power,
            effectiveness=1.0,
            move_type=selected_move.type,
            defender_type1=defender_type1,
            defender_type2=defender_type2
        )

        if damage is not None:
            percent = (damage / defender_hp) * 100

            # Build effectiveness message
            if type_multiplier == 0.0:
                effectiveness_msg = "It doesn't affect the target..."
            elif type_multiplier < 1.0:
                effectiveness_msg = "It's not very effective..."
            elif type_multiplier > 1.0:
                effectiveness_msg = "It's super effective!"
            else:
                effectiveness_msg = "It's normally effective."

            result_label.config(
                text=f"Damage: {damage} ({percent:.2f}% of target's HP)\n{effectiveness_msg}"
            )
        else:
            result_label.config(text="Error in calculation.")
    except Exception as e:
        result_label.config(text=f"Invalid input! ({e})")


# Layout --- Pokémon
search_var = tk.StringVar()
search_var.trace("w", update_listbox_attacker)

search_var1 = tk.StringVar()
search_var1.trace("w", update_listbox_defender)

tk.Label(root, text="Pokémon 1 (Attacker)").grid(row=0, column=0)
search_entry = tk.Entry(root, textvariable=search_var)
search_entry.grid(row=1, column=0)
listbox = tk.Listbox(root, height=5)
listbox.grid(row=2, column=0)
listbox.bind('<<ListboxSelect>>', on_attacker_select)
attacker_label = tk.Label(root, text="Selected Attacker: None", fg="gray")
attacker_label.grid(row=3, column=0)

tk.Label(root, text="Pokémon 2 (Defender)").grid(row=0, column=2)
search_entry1 = tk.Entry(root, textvariable=search_var1)
search_entry1.grid(row=1, column=2)
listbox1 = tk.Listbox(root, height=5)
listbox1.grid(row=2, column=2)
listbox1.bind('<<ListboxSelect>>', on_defender_select)
defender_label = tk.Label(root, text="Selected Defender: None", fg="gray")
defender_label.grid(row=3, column=2)

# Layout --- Stats and Move Info
level_entry = tk.Entry(root)
attack_entry = tk.Entry(root)
defense_entry = tk.Entry(root)
spatk_entry = tk.Entry(root)
spdef_entry = tk.Entry(root)
speed_entry = tk.Entry(root)
hp_entry = tk.Entry(root)

level_entry1 = tk.Entry(root)
attack_entry1 = tk.Entry(root)
defense_entry1 = tk.Entry(root)
spatk_entry1 = tk.Entry(root)
spdef_entry1 = tk.Entry(root)
speed_entry1 = tk.Entry(root)
hp_entry1 = tk.Entry(root)

base_power_entry = tk.Entry(root)

# Move search
search_var_move = tk.StringVar()
search_var_move.trace("w", update_listbox_move)
tk.Label(root, text="Move Search").grid(row=0, column=4)
search_entry_move = tk.Entry(root, textvariable=search_var_move)
search_entry_move.grid(row=1, column=4)
listbox_move = tk.Listbox(root, height=5)
listbox_move.grid(row=2, column=4)
listbox_move.bind('<<ListboxSelect>>', on_move_select)
move_label = tk.Label(root, text="Selected Move: None", fg="gray")
move_label.grid(row=3, column=4)

# Place everything else you want on the grid here... (Add Entry Fields, Labels as needed)
tk.Label(root, text="Base Power").grid(row=4, column=4)
base_power_entry.grid(row=5, column=4)

calculate_button = tk.Button(root, text="Calculate Damage", command=on_calculate)
calculate_button.grid(row=6, column=4)

result_label = tk.Label(root, text="Damage: ")
result_label.grid(row=7, column=4)

reset_button = tk.Button(root, text="Reset", command=reset_all)
reset_button.grid(row=8, column=4)


root.mainloop()
