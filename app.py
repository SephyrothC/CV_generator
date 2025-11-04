"""
Application Streamlit pour le générateur de CV personnalisés
"""
import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv

from src.profile_manager import ProfileManager
from src.analyzer import JobOfferAnalyzer
from src.ai_adapter import CVPersonalizer
from src.pdf_generator import PDFGenerator
from src.color_matcher import ColorMatcher

# Charger les variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="CV Generator AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1e293b;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d1fae5;
        border-left: 4px solid #10b981;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #dbeafe;
        border-left: 4px solid #3b82f6;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialise les variables de session"""
    if 'job_offer' not in st.session_state:
        st.session_state.job_offer = None
    if 'customized_cv' not in st.session_state:
        st.session_state.customized_cv = None
    if 'profile' not in st.session_state:
        st.session_state.profile = None


def main():
    """Application principale"""
    initialize_session_state()

    # Header
    st.markdown('<h1 class="main-header">📄 CV Generator AI</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Générez des CV personnalisés automatiquement grâce à l\'IA</p>',
        unsafe_allow_html=True
    )

    # Vérifier la clé API
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("⚠️ ANTHROPIC_API_KEY non trouvée. Créez un fichier .env avec votre clé API.")
        st.info("Copiez le fichier .env.example en .env et ajoutez votre clé API Anthropic.")
        st.stop()

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Charger le profil
        profile_path = st.text_input("Chemin du profil", "data/profile.json")

        if st.button("📂 Charger le profil"):
            try:
                manager = ProfileManager(profile_path)
                st.session_state.profile = manager.load_profile()
                st.success(f"✅ Profil chargé : {st.session_state.profile.personal_info.first_name} {st.session_state.profile.personal_info.last_name}")
            except Exception as e:
                st.error(f"❌ Erreur lors du chargement : {e}")

        st.divider()

        # Template selection
        st.subheader("🎨 Template")
        template_choice = st.selectbox(
            "Choisir un template",
            ["modern", "professional"],
            index=0
        )

        st.divider()

        # Informations
        st.subheader("ℹ️ À propos")
        st.info("""
        **Comment utiliser :**
        1. Chargez votre profil
        2. Collez l'offre d'emploi
        3. Analysez avec l'IA
        4. Ajustez si nécessaire
        5. Générez le PDF
        """)

    # Main content
    if st.session_state.profile is None:
        st.warning("👈 Commencez par charger votre profil dans la barre latérale")
        st.stop()

    # Étape 1 : Saisir l'offre d'emploi
    st.header("1️⃣ Offre d'emploi")

    job_text = st.text_area(
        "Collez le texte de l'offre d'emploi LinkedIn",
        height=200,
        placeholder="Copiez-collez ici le texte complet de l'offre d'emploi...",
        help="Incluez le titre du poste, l'entreprise, la description et les compétences requises"
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        analyze_button = st.button("🔍 Analyser l'offre", type="primary", use_container_width=True)

    if analyze_button and job_text:
        with st.spinner("🤖 Analyse de l'offre en cours..."):
            try:
                analyzer = JobOfferAnalyzer()
                st.session_state.job_offer = analyzer.analyze_job_offer(job_text)
                st.success("✅ Offre analysée avec succès !")
            except Exception as e:
                st.error(f"❌ Erreur lors de l'analyse : {e}")

    # Afficher l'offre analysée
    if st.session_state.job_offer:
        st.divider()
        st.subheader("📊 Résultat de l'analyse")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Entreprise", st.session_state.job_offer.company)
            st.metric("Poste", st.session_state.job_offer.position)

        with col2:
            st.write("**Description :**")
            st.write(st.session_state.job_offer.description)

        col1, col2 = st.columns(2)
        with col1:
            st.write("**Compétences requises :**")
            for skill in st.session_state.job_offer.required_skills:
                st.markdown(f"- {skill}")

        with col2:
            st.write("**Technologies :**")
            for tech in st.session_state.job_offer.technologies:
                st.markdown(f"- {tech}")

    # Étape 2 : Personnaliser le CV
    if st.session_state.job_offer:
        st.divider()
        st.header("2️⃣ Personnalisation du CV")

        if st.button("✨ Personnaliser avec l'IA", type="primary"):
            with st.spinner("🤖 Personnalisation en cours..."):
                try:
                    personalizer = CVPersonalizer()
                    st.session_state.customized_cv = personalizer.personalize_cv(
                        st.session_state.profile,
                        st.session_state.job_offer
                    )
                    # Définir le template choisi
                    st.session_state.customized_cv.template = template_choice

                    # Suggérer des couleurs
                    color_matcher = ColorMatcher()
                    suggested_colors = color_matcher.suggest_colors(
                        st.session_state.job_offer.company,
                        st.session_state.job_offer.keywords
                    )
                    # Utiliser les couleurs suggérées si non définies par l'IA
                    if not st.session_state.customized_cv.colors.get("primary"):
                        st.session_state.customized_cv.colors = suggested_colors

                    st.success("✅ CV personnalisé avec succès !")
                except Exception as e:
                    st.error(f"❌ Erreur lors de la personnalisation : {e}")

    # Afficher la personnalisation
    if st.session_state.customized_cv:
        st.divider()
        st.subheader("📝 Aperçu de la personnalisation")

        # Résumé personnalisé
        st.write("**Résumé personnalisé :**")
        custom_summary = st.text_area(
            "Résumé",
            value=st.session_state.customized_cv.custom_summary,
            height=100,
            key="summary_edit"
        )
        st.session_state.customized_cv.custom_summary = custom_summary

        # Points forts
        st.write("**Points forts :**")
        strengths = []
        for i, strength in enumerate(st.session_state.customized_cv.strengths):
            edited_strength = st.text_input(
                f"Point fort {i+1}",
                value=strength,
                key=f"strength_{i}"
            )
            strengths.append(edited_strength)
        st.session_state.customized_cv.strengths = strengths

        # Compétences sélectionnées
        st.write("**Compétences sélectionnées :**")
        st.write(", ".join(st.session_state.customized_cv.selected_skills))

        col1, col2 = st.columns(2)
        with col1:
            st.write("**Expériences sélectionnées :**")
            for exp_id in st.session_state.customized_cv.selected_experiences:
                exp = next((e for e in st.session_state.profile.experiences if e.id == exp_id), None)
                if exp:
                    st.markdown(f"- {exp.position} @ {exp.company}")

        with col2:
            st.write("**Projets sélectionnés :**")
            for proj_id in st.session_state.customized_cv.selected_projects:
                proj = next((p for p in st.session_state.profile.projects if p.id == proj_id), None)
                if proj:
                    st.markdown(f"- {proj.name}")

        # Couleurs
        st.write("**Couleurs du CV :**")
        col1, col2 = st.columns(2)
        with col1:
            primary_color = st.color_picker(
                "Couleur primaire",
                value=st.session_state.customized_cv.colors.get("primary", "#1e293b")
            )
        with col2:
            secondary_color = st.color_picker(
                "Couleur secondaire",
                value=st.session_state.customized_cv.colors.get("secondary", "#475569")
            )

        st.session_state.customized_cv.colors = {
            "primary": primary_color,
            "secondary": secondary_color
        }

    # Étape 3 : Générer le PDF
    if st.session_state.customized_cv:
        st.divider()
        st.header("3️⃣ Génération du CV")

        col1, col2, col3 = st.columns([2, 2, 3])

        with col1:
            if st.button("📄 Générer PDF", type="primary", use_container_width=True):
                with st.spinner("📄 Génération du PDF en cours..."):
                    try:
                        generator = PDFGenerator()
                        pdf_path = generator.generate_cv(
                            st.session_state.profile,
                            st.session_state.customized_cv
                        )
                        st.success(f"✅ PDF généré : {pdf_path}")

                        # Télécharger le PDF
                        with open(pdf_path, "rb") as f:
                            st.download_button(
                                label="⬇️ Télécharger le PDF",
                                data=f,
                                file_name=Path(pdf_path).name,
                                mime="application/pdf",
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la génération : {e}")

        with col2:
            if st.button("👁️ Aperçu HTML", use_container_width=True):
                with st.spinner("📄 Génération de l'aperçu..."):
                    try:
                        generator = PDFGenerator()
                        html_path = generator.generate_html_preview(
                            st.session_state.profile,
                            st.session_state.customized_cv
                        )
                        st.success(f"✅ Aperçu généré : {html_path}")

                        # Lire et afficher le HTML
                        with open(html_path, "r", encoding="utf-8") as f:
                            html_content = f.read()

                        st.components.v1.html(html_content, height=800, scrolling=True)
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la génération : {e}")


if __name__ == "__main__":
    main()
