import random
import streamlit as st

st.set_page_config(page_title="Jeu de Guerre - Combat", page_icon="⚔️")

st.title("⚔️ Arène de Combat : Guerrier vs Monstre")
st.caption("Survis et bats le monstre pour remporter la victoire !")

# Initialisation des états du jeu (santé, potions, score)
if "game_started" not in st.session_state:
    st.session_state.player_hp = 100
    st.session_state.monster_hp = 100
    st.session_state.potions = 3
    st.session_state.turn = "player"
    st.session_state.log = "Le combat commence ! Prépare-toi à attaquer."
    st.session_state.game_started = True

# Affichage des barres de vie
col1, col2 = st.columns(2)

with col1:
    st.subheader("🛡️ Ton Héros")
    st.progress(max(0, st.session_state.player_hp) / 100)
    st.write(f"Points de vie : **{st.session_state.player_hp} / 100**")
    st.write(f"Potions restantes : **{st.session_state.potions} 🧪**")

with col2:
    st.subheader("👹 Le Monstre")
    st.progress(max(0, st.session_state.monster_hp) / 100)
    st.write(f"Points de vie : **{st.session_state.monster_hp} / 100**")

st.markdown("---")

# Zone de log des actions
st.info(f"📜 **Journal de combat :**\n\n{st.session_state.log}")

# Fin de partie (Victoire ou Défaite)
if st.session_state.player_hp <= 0:
    st.error("💀 Tu as perdu le combat... Le monstre t'a vaincu !")
    if st.button("🔄 Recommencer une partie"):
        st.session_state.player_hp = 100
        st.session_state.monster_hp = 100
        st.session_state.potions = 3
        st.session_state.log = "Une nouvelle bataille commence !"
        st.rerun()

elif st.session_state.monster_hp <= 0:
    st.success("🎉 VICTOIRE ! Tu as terrassé le monstre avec brio !")
    if st.button("🔄 Relancer une nouvelle partie"):
        st.session_state.player_hp = 100
        st.session_state.monster_hp = 100
        st.session_state.potions = 3
        st.session_state.log = "Une nouvelle bataille commence !"
        st.rerun()

else:
    # Boutons d'action du joueur
    st.subheader("Fais ton choix, guerrier :")
    c1, c2, c3 = st.columns(3)

    # 1. Attaque normale
    if c1.button("⚔️ Attaque rapide"):
        player_damage = random.randint(8, 15)
        st.session_state.monster_hp -= player_damage
        log_msg = f"Tu infliges **{player_damage} dégâts** au monstre !"
        
        # Riposte du monstre si toujours vivant
        if st.session_state.monster_hp > 0:
            monster_damage = random.randint(5, 12)
            st.session_state.player_hp -= monster_damage
            log_msg += f"\n Le monstre riposte et t'inflige **{monster_damage} dégâts**."
            
        st.session_state.log = log_msg
        st.rerun()

    # 2. Coup critique (gros dégâts mais risque d'échec)
    if c2.button("🔥 Coup Spécial (Puissant)"):
        if random.random() > 0.4:  # 60% de chance de réussie
            player_damage = random.randint(18, 28)
            st.session_state.monster_hp -= player_damage
            log_msg = f"Coup critique réussi ! Tu infliges **{player_damage} dégâts** massifs !"
        else:
            log_msg = "❌ Ton attaque spéciale a échoué, tu as raté ta cible !"

        # Riposte du monstre
        if st.session_state.monster_hp > 0:
            monster_damage = random.randint(8, 16)
            st.session_state.player_hp -= monster_damage
            log_msg += f"\n En profitant de ton échec, le monstre t'inflige **{monster_damage} dégâts**."

        st.session_state.log = log_msg
        st.rerun()

    # 3. Utiliser une potion
    if c3.button("🧪 Boire une Potion"):
        if st.session_state.potions > 0:
            heal = random.randint(20, 35)
            st.session_state.player_hp = min(100, st.session_state.player_hp + heal)
            st.session_state.potions -= 1
            log_msg = f"Tu bois une potion et récupères **{heal} PV**."
            
            # Le monstre attaque quand même pendant que tu bois
            monster_damage = random.randint(5, 10)
            st.session_state.player_hp -= monster_damage
            log_msg += f"\n Pendant que tu buvais, le monstre t'a attaqué pour **{monster_damage} dégâts**."
            
            st.session_state.log = log_msg
            st.rerun()
        else:
            st.warning("Tu n'as plus de potions en réserve !")
