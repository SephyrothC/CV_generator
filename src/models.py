"""
Modèles de données pour le générateur de CV
"""
from typing import List, Optional, Dict, Any
from datetime import date
from pydantic import BaseModel, EmailStr, Field, validator


class PersonalInfo(BaseModel):
    """Informations personnelles"""
    first_name: str
    last_name: str
    title: str
    email: EmailStr
    phone: str
    location: str
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    summary: str


class Experience(BaseModel):
    """Expérience professionnelle"""
    id: str
    company: str
    position: str
    location: str
    start_date: str
    end_date: Optional[str] = None
    current: bool = False
    description: str
    achievements: List[str]
    technologies: List[str]


class Skill(BaseModel):
    """Compétence technique"""
    name: str
    level: str  # beginner, intermediate, advanced, expert
    years: int


class Project(BaseModel):
    """Projet personnel ou professionnel"""
    id: str
    name: str
    description: str
    role: str
    technologies: List[str]
    achievements: List[str]
    url: Optional[str] = None
    highlights: bool = False


class Education(BaseModel):
    """Formation"""
    degree: str
    field: str
    institution: str
    location: str
    start_date: str
    end_date: str
    description: Optional[str] = None


class Language(BaseModel):
    """Langue"""
    name: str
    level: str


class Certification(BaseModel):
    """Certification"""
    name: str
    issuer: str
    date: str
    credential_id: Optional[str] = None


class Profile(BaseModel):
    """Profil complet de l'utilisateur"""
    personal_info: PersonalInfo
    experiences: List[Experience]
    skills: Dict[str, List[Skill]]  # Catégories de compétences
    projects: List[Project]
    education: List[Education]
    languages: List[Language]
    certifications: Optional[List[Certification]] = []
    interests: Optional[List[str]] = []


class JobOffer(BaseModel):
    """Offre d'emploi analysée"""
    company: str
    position: str
    description: str
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    technologies: List[str] = []
    keywords: List[str] = []
    url: Optional[str] = None


class CustomizedCV(BaseModel):
    """CV personnalisé pour une offre"""
    job_offer: JobOffer
    selected_experiences: List[str]  # IDs des expériences
    selected_projects: List[str]  # IDs des projets
    selected_skills: List[str]  # Noms des compétences
    strengths: List[str]  # 3-4 points forts adaptés
    custom_summary: str  # Résumé personnalisé
    colors: Dict[str, str]  # Couleurs de marque
    template: str = "modern"  # Nom du template à utiliser
