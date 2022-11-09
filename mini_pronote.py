# Author :  Romain MELLAZA

import sqlite3
import time

#Connexion
connexion = sqlite3.connect('pronote.db')

#Récupération d'un curseur
c = connexion.cursor()

## Fonctions ##

# ---- début des instructions SQL

#Création de la table
c.execute("""
    CREATE TABLE IF NOT EXISTS releve(
    Prénom TEXT,
    Nom TEXT,
    Matière TEXT,
    Note INT);
    """)


print("--------- Service Pronote ---------")
print("---- Veuillez vous indentifier ----")
prenom = str(input('Votre Prénom :\n'))
nom = str(input('Votre Nom :\n'))


looping_home = 0

while looping_home != 4 :
    print("\n---------- Menu d'accueil ---------")
    print("    1. Saisir des notes.")
    print("    2. Consulter vos notes.")
    print("    3. Calculer une moyenne.")
    print("    4. Se déconnecter.")
    choice = int(input("Saisisez le numéro correspondant à l'action voulue :\n"))
    

    if choice == 1 :
        choice = 0
        print("\n---- Saisie des notes ----")
        looping_note = 0
        ans = 2
        while looping_note == 0 :
            matiere = str(input('La Matière :\n'))
            note = float(input('Votre Note :\n'))
            data = (prenom, nom, matiere, note)
            c.execute('''INSERT INTO releve VALUES (?,?,?,?)''', data)
            while ans != 0 and ans != 1 :
                looping_note = int(input("Saisir une autre note ?  0 = OUI / 1 = NON\n"))
                ans = looping_note
            ans = 2
        connexion.commit()
    
    if choice == 2 :
        choice = 0
        print("\n---- Consulter vos notes ----")
        task = str('SELECT Matière, Note FROM releve WHERE (Prénom =' + "'" + prenom + "'" + ') AND (Nom =' + "'" + nom + "'" +');')
        res = c.execute(task)
        result = res.fetchall()
        if len(result) == 0 :
            print("Vous n'avez pas de notes dans la base de donnée...")
            time.sleep(4)
        else :
            print(result)
            time.sleep(12)

    if choice == 3 :
        choice = 0
        ans = 2
        looping_avg = 0
        print("\n---- Calculer une moyenne ----")
        while looping_avg == 0 :
            while ans != 0 and ans != 1 :
                avg_type = int(input("Type de moyenne ?  0 = Générale / 1 = D'une Matière\n"))
                ans = avg_type
            if avg_type == 0 :
                looping_avg = 1
                task = str('SELECT AVG(Note) FROM releve WHERE (Prénom =' + "'" + prenom + "'" + ') AND (Nom =' + "'" + nom + "'" +');')
                res = c.execute(task)
                moy_g = res.fetchall()
                print("\nVotre Moyenne Générale est de :",moy_g[0][0])
                time.sleep(6)
            if avg_type == 1 :
                looping_avg = 1
                print("\nLes matières disponibles sont :")
                list_mat = c.execute("SELECT DISTINCT Matière FROM releve")
                print(list_mat.fetchall())
                choice_mat = str(input("\nChoisissez-en une :\n"))
                task = str('SELECT AVG(Note) FROM releve WHERE (Prénom =' + "'" + prenom + "'" + ') AND (Nom =' + "'" + nom + "'" + ') AND (Matière ='+ "'" + choice_mat + "');")
                res = c.execute(task)
                moy_mat = res.fetchall()
                print("Votre Moyenne en",choice_mat,"est de :",moy_mat[0][0])

    if choice == 4 :
        break

#Validation
connexion.commit()

#Déconnexion
connexion.close()