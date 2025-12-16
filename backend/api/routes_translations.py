"""
API Routes - Translation Engine

Endpoints para sugerencias de traducción y gestión de translation memory.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
from pathlib import Path

# Añadir backend al path
sys.path.append(str(Path(__file__).parent.parent))

from translations.translation_engine import TranslationEngine


router = APIRouter(prefix="/api/translations", tags=["translations"])

# Inicializar TranslationEngine
translation_engine = TranslationEngine()


# --- Pydantic Models ---

class TranslationSuggestionRequest(BaseModel):
    """Request para obtener sugerencias de traducción."""
    source_text: str
    source_lang: str
    target_lang: str
    threshold: float = 0.75
    max_suggestions: int = 5
    family: Optional[str] = None


class TranslationSuggestion(BaseModel):
    """Sugerencia de traducción."""
    text: str
    confidence: float
    source: str  # exact_match, fuzzy_match, glossary
    count: int = 0


class SaveTranslationRequest(BaseModel):
    """Request para guardar traducción."""
    source_text: str
    target_text: str
    source_lang: str
    target_lang: str
    confidence: float = 0.95


class GlossaryResponse(BaseModel):
    """Respuesta con glosario."""
    family: str
    target_lang: str
    terms: Dict[str, str]


class TranslationStatsResponse(BaseModel):
    """Estadísticas del translation engine."""
    total_language_pairs: int
    total_source_texts: int
    languages_supported: List[str]
    glossaries_loaded: int
    families_with_glossaries: List[str]


# --- Routes ---

@router.post("/suggest", response_model=List[TranslationSuggestion])
async def suggest_translation(request: TranslationSuggestionRequest):
    """
    Obtener sugerencias de traducción.
    
    Busca en translation memory, glossaries y fuzzy matching.
    """
    try:
        suggestions = translation_engine.suggest_translation(
            source_text=request.source_text,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            threshold=request.threshold,
            max_suggestions=request.max_suggestions,
            family=request.family
        )
        
        return suggestions
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/save")
async def save_translation(request: SaveTranslationRequest):
    """
    Guardar nueva traducción en memory.
    
    Actualiza translation_memory.json automáticamente.
    """
    try:
        translation_engine.save_translation(
            source_text=request.source_text,
            target_text=request.target_text,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            confidence=request.confidence
        )
        
        return {
            "status": "success",
            "message": "Translation saved successfully",
            "source_text": request.source_text,
            "target_text": request.target_text,
            "lang_pair": f"{request.source_lang}-{request.target_lang}"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/glossary/{family}/{target_lang}", response_model=GlossaryResponse)
async def get_glossary(family: str, target_lang: str):
    """
    Obtener glosario completo para familia y idioma.
    
    Args:
        family: Familia de producto (COSMETICS_FACIAL, FOOD_PACKAGED, etc.)
        target_lang: Idioma destino (pt, it, en)
    """
    try:
        glossary = translation_engine.get_glossary(family, target_lang)
        
        if not glossary:
            raise HTTPException(
                status_code=404, 
                detail=f"Glossary not found for family={family}, lang={target_lang}"
            )
        
        return {
            "family": family,
            "target_lang": target_lang,
            "terms": glossary
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=TranslationStatsResponse)
async def get_translation_stats():
    """
    Obtener estadísticas del translation engine.
    
    Retorna información sobre language pairs, glossaries, etc.
    """
    try:
        stats = translation_engine.get_stats()
        return stats
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/supported-languages")
async def get_supported_languages():
    """
    Obtener lista de idiomas soportados.
    """
    return {
        "languages": ["es", "pt", "it", "en", "fr"],
        "language_names": {
            "es": "Español",
            "pt": "Português",
            "it": "Italiano",
            "en": "English",
            "fr": "Français"
        }
    }


@router.post("/export-csv")
async def export_memory_to_csv(output_path: str = Query("translations_export.csv")):
    """
    Exportar translation memory a CSV.
    
    Args:
        output_path: Path del archivo CSV de salida
    """
    try:
        translation_engine.export_memory_to_csv(output_path)
        
        return {
            "status": "success",
            "message": f"Translation memory exported to {output_path}",
            "file_path": output_path
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
