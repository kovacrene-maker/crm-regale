import streamlit as st
import pandas as pd
import datetime

# 1. Konfigurácia stránky
st.set_page_config(
    page_title="CRM Regálové Systémy",
    page_icon="📦",
    layout="wide"
)

st.title("📦 CRM Systém pre Predaj Regálových Systémov")
st.markdown("Interaktívna sieťová databáza pre 500 kontaktov a obchodných prípadov.")

# 2. Bočný panel (Sidebar) - Výber aktívneho kolegu
st.sidebar.header("👤 Tímový prístup")
aktivny_kolega = st.sidebar.selectbox(
    "Vyberte svoje iniciály:", 
    ["SK", "DT", "RK", "XY"]
)
st.sidebar.success(f"Aktuálne pracujete ako: **{aktivny_kolega}**")

st.sidebar.markdown("---")
st.sidebar.info("Tento systém slúži na sledovanie ponúk, stavov a plnenia obchodných cieľov v reálnom čase.")

# 3. Inicializácia databázy pre 500 ID (Session State)
@st.cache_data
def init_database():
    # Zoznam možností pre rolovacie menu
    kolegovia = ["SK", "DT", "RK", "XY"]
    kategorie = ["Opakovaný zákazník", "Nový zákazník", "Dodávateľ", "Spolupracovník"]
    stavy = ["Koncept / V príprave", "Odoslaná", "V vyjednávaní", "Schválená", "Zamietnutá"]
    typy_ponuk = [
        "Paletové regále", "Policové regále", "Konzolové regále", 
        "Plošiny/konštrukcie", "Prepravky", "Dielenský nábytok", 
        "Revízie", "Servis", "Iné"
    ]
    
    # Generovanie 500 prázdnych / predpripravených riadkov s ID 1 až 500
    data = []
    import random
    random.seed(42)
    
    for i in range(1, 501):
        # Pre ukážku naplníme prvých pár riadkov vzorovými dátami, ostatné budú prázdne pripravené
        if i <= 5:
            collab = random.choice(kolegovia)
            stat = random.choice(stavy)
            t_pon = random.choice(typy_ponuk)
            val = random.randint(5, 50) * 1000
        else:
            collab = ""
            stat = ""
            t_pon = ""
            val = 0.0

        data.append({
            "ID": i,
            "Ktorý kolega": collab,
            "Meno": f"Meno {i}" if i <= 5 else "",
            "Priezvisko": f"Priezvisko {i}" if i <= 5 else "",
            "Firma": f"Firma s.r.o. {i}" if i <= 5 else "",
            "Pozícia": "Manažér skladu" if i <= 5 else "",
            "E-mail": f"kontakt{i}@firma.sk" if i <= 5 else "",
            "Telefón": "+421 900 123 456" if i <= 5 else "",
            "Adresa / Mesto": "Bratislava" if i <= 5 else "",
            "Kategória zákazníka": random.choice(kategorie) if i <= 5 else "",
            "Cenová ponuka číslo": f"CP-2026/{i:03d}" if i <= 5 else "",
            "Stav Ponuky": stat,
            "Cenová ponuka": t_pon,
            "Predmet ponuky": "Dodávka a montáž regálového systému" if i <= 5 else "",
            "Hodnota Ponuky (€)": float(val),
            "Dátum Odoslania": str(datetime.date.today()) if i <= 5 else "",
            "Dátum dodania": str(datetime.date.today() + datetime.timedelta(days=30)) if i <= 5 else "",
            "Nasledujúci Krok": "Odoslať follow-up e-mail" if i <= 5 else "",
            "Poznámky": ""
        })
    return pd.DataFrame(data)

# Načítanie dát do pamäte aplikácie
if "df" not in st.session_state:
    st.session_state.df = init_database()

df = st.session_state.df

# 4. Horné KPI Metriky
st.markdown("### 📊 Súhrnné ukazovatele (KPI)")
total_contacts = len(df[df["Meno"] != ""])
total_value = df["Hodnota Ponuky (€)"].sum()
open_value = df[df["Stav Ponuky"] != "Schválená"]["Hodnota Ponuky (€)"].sum()
won_value = df[df["Stav Ponuky"] == "Schválená"]["Hodnota Ponuky (€)"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Aktívne kontakty", f"{total_contacts} / 500")
col2.metric("Celková hodnota ponúk", f"{total_value:,.0f} €".replace(",", " "))
col3.metric("Otvorené ponuky", f"{open_value:,.0f} €".replace(",", " "))
col4.metric("Získané (Schválené)", f"{won_value:,.0f} €".replace(",", " "))

st.markdown("---")

# 5. Interaktívna tabuľka (Data Editor)
st.subheader("📋 Databáza kontaktov a ponúk (500 ID)")
st.markdown("Údaje môžete priamo upravovať v tabuľke nižšie. Zmeny sa okamžite prepočítajú v grafoch.")

# Zobrazenie editovateľnej tabuľky
edited_df = st.data_editor(
    df,
    num_rows="fixed",
    use_container_width=True,
    height=450,
    column_config={
        "ID": st.column_config.NumberColumn("ID", disabled=True),
        "Ktorý kolega": st.column_config.SelectboxColumn(
            "Kolega",
            options=["SK", "DT", "RK", "XY"],
            required=False
        ),
        "Kategória zákazníka": st.column_config.SelectboxColumn(
            "Kategória",
            options=["Opakovaný zákazník", "Nový zákazník", "Dodávateľ", "Spolupracovník"]
        ),
        "Stav Ponuky": st.column_config.SelectboxColumn(
            "Stav Ponuky",
            options=["Koncept / V príprave", "Odoslaná", "V vyjednávaní", "Schválená", "Zamietnutá"]
        ),
        "Cenová ponuka": st.column_config.SelectboxColumn(
            "Typ Ponuky",
            options=[
                "Paletové regále", "Policové regále", "Konzolové regále", 
                "Plošiny/konštrukcie", "Prepravky", "Dielenský nábytok", 
                "Revízie", "Servis", "Iné"
            ]
        ),
        "Hodnota Ponuky (€)": st.column_config.NumberColumn("Hodnota (€)", format="€ %.2f")
    }
)

# Uloženie zmien do session state
st.session_state.df = edited_df

st.markdown("---")

# 6. Štatistické grafy a prehľady
st.subheader("📈 Štatistiky a analýza portfólia")

col_g1, col_g2 = st.columns(2)

with col_g1:
    st.markdown("#### Objem ponúk podľa stavu (€)")
    status_chart_data = edited_df.groupby("Stav Ponuky")["Hodnota Ponuky (€)"].sum()
    if "" in status_chart_data:
        status_chart_data = status_chart_data.drop("")
    st.bar_chart(status_chart_data)

with col_g2:
    st.markdown("#### Hodnota ponúk podľa kolegov (SK, DT, RK, XY)")
    collab_chart_data = edited_df.groupby("Ktorý kolega")["Hodnota Ponuky (€)"].sum()
    if "" in collab_chart_data:
        collab_chart_data = collab_chart_data.drop("")
    st.bar_chart(collab_chart_data)

# Tlačidlo na export údajov
st.markdown("---")
st.download_button(
    label="📥 Stiahnuť aktuálnu databázu ako CSV",
    data=edited_df.to_csv(index=False).encode('utf-8-sig'),
    file_name="crm_regale_data.csv",
    mime="text/csv",
)
