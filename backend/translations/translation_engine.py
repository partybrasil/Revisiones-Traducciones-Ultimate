"""
Translation Engine - Sugerencias Multidioma con Fuzzy Matching

Proporciona traducción automática basada en:
- Translation memory (JSON) con traducciones previas
- Glossaries (YAML) con términos específicos por familia
- Fuzzy matching para sugerencias similares
"""

import json
import difflib
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import yaml
from datetime import datetime


class TranslationEngine:
    """
    Motor de traducción con memory y glossaries.
    
    Funcionalidades:
    - suggest_translation(): Sugerencias basadas en memory + glossary + fuzzy matching
    - save_translation(): Guardar nueva traducción en memory
    - get_glossary(): Obtener glosario para familia y idioma
    - export_memory_to_csv(): Exportar memory a CSV
    """
    
    def __init__(self, 
                 memory_path: str = "backend/translations/translation_memory.json",
                 glossaries_dir: str = "backend/translations/glossaries"):
        """
        Inicializar TranslationEngine.
        
        Args:
            memory_path: Ruta al archivo translation_memory.json
            glossaries_dir: Directorio con archivos glossary_*.yaml
        """
        self.memory_path = Path(memory_path)
        self.glossaries_dir = Path(glossaries_dir)
        self.memory = self._load_translation_memory()
        self.glossaries = self._load_glossaries()
    
    def _load_translation_memory(self) -> Dict:
        """Cargar translation memory desde JSON."""
        if not self.memory_path.exists():
            return {}
        
        try:
            with open(self.memory_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading translation memory: {e}")
            return {}
    
    def _load_glossaries(self) -> Dict:
        """
        Cargar todos los glossaries desde YAML.
        
        Returns:
            Dict con estructura: {family: {lang: {term: translation}}}
        """
        glossaries = {}
        
        if not self.glossaries_dir.exists():
            return glossaries
        
        # Buscar todos los archivos glossary_*.yaml
        for yaml_file in self.glossaries_dir.glob("glossary_*.yaml"):
            try:
                # Parse filename: glossary_cosmetics_pt.yaml -> family=cosmetics, lang=pt
                parts = yaml_file.stem.replace("glossary_", "").split("_")
                if len(parts) >= 2:
                    family = "_".join(parts[:-1])  # cosmetics, food, etc.
                    lang = parts[-1]  # pt, it, en, etc.
                    
                    with open(yaml_file, 'r', encoding='utf-8') as f:
                        glossary_data = yaml.safe_load(f)
                    
                    # Organizar por familia
                    if family not in glossaries:
                        glossaries[family] = {}
                    glossaries[family][lang] = glossary_data
            
            except Exception as e:
                print(f"Error loading glossary {yaml_file}: {e}")
        
        return glossaries
    
    def suggest_translation(self, 
                           source_text: str, 
                           source_lang: str, 
                           target_lang: str,
                           threshold: float = 0.75,
                           max_suggestions: int = 5,
                           family: Optional[str] = None) -> List[Dict]:
        """
        Sugerir traducciones basadas en memory, glossary y fuzzy matching.
        
        Args:
            source_text: Texto a traducir
            source_lang: Idioma origen (es, pt, it, en)
            target_lang: Idioma destino (es, pt, it, en)
            threshold: Umbral mínimo de similitud (0.0-1.0) para fuzzy matching
            max_suggestions: Número máximo de sugerencias a retornar
            family: Familia de producto para buscar en glossary (opcional)
        
        Returns:
            Lista de sugerencias ordenadas por confidence:
            [
                {
                    "text": "Creme Hidratante",
                    "confidence": 0.98,
                    "source": "exact_match" | "fuzzy_match" | "glossary"
                },
                ...
            ]
        """
        suggestions = []
        key = f"{source_lang}-{target_lang}"
        
        # 1. Buscar exact match en memory
        if key in self.memory and source_text in self.memory[key]:
            entry = self.memory[key][source_text]
            for translation in entry["translations"]:
                suggestions.append({
                    "text": translation,
                    "confidence": entry.get("confidence", 0.95),
                    "source": "exact_match",
                    "count": entry.get("count", 0)
                })
        
        # 2. Buscar en glossary si se especifica familia
        if family:
            glossary_terms = self._search_in_glossary(source_text, family, target_lang)
            for term in glossary_terms:
                suggestions.append({
                    "text": term,
                    "confidence": 0.99,  # Glossary tiene alta confianza
                    "source": "glossary",
                    "count": 0
                })
        
        # 3. Fuzzy matching en memory
        if key in self.memory:
            fuzzy_matches = self._fuzzy_search(source_text, self.memory[key], threshold)
            for match_text, match_data, ratio in fuzzy_matches:
                for translation in match_data["translations"]:
                    # Ajustar confidence según ratio de similitud
                    adjusted_confidence = match_data.get("confidence", 0.8) * ratio
                    suggestions.append({
                        "text": translation,
                        "confidence": adjusted_confidence,
                        "source": "fuzzy_match",
                        "count": match_data.get("count", 0),
                        "original_match": match_text,
                        "similarity": ratio
                    })
        
        # Eliminar duplicados manteniendo el de mayor confidence
        unique_suggestions = {}
        for sugg in suggestions:
            text = sugg["text"]
            if text not in unique_suggestions or sugg["confidence"] > unique_suggestions[text]["confidence"]:
                unique_suggestions[text] = sugg
        
        # Ordenar por confidence DESC y limitar
        final_suggestions = sorted(unique_suggestions.values(), 
                                   key=lambda x: x["confidence"], 
                                   reverse=True)
        
        return final_suggestions[:max_suggestions]
    
    def _search_in_glossary(self, source_text: str, family: str, target_lang: str) -> List[str]:
        """
        Buscar traducción en glossary para familia y idioma específico.
        
        Args:
            source_text: Texto a buscar
            family: Familia de producto (cosmetics, food, etc.)
            target_lang: Idioma destino (pt, it, en)
        
        Returns:
            Lista de traducciones encontradas en glossary
        """
        translations = []
        
        # Normalizar family name (COSMETICS_FACIAL -> cosmetics)
        family_normalized = family.lower().split("_")[0] if "_" in family else family.lower()
        
        if family_normalized not in self.glossaries:
            return translations
        
        if target_lang not in self.glossaries[family_normalized]:
            return translations
        
        glossary = self.glossaries[family_normalized][target_lang]
        
        # Buscar en todas las subfamilias del glossary
        for subfamily, terms in glossary.items():
            if isinstance(terms, dict) and source_text in terms:
                translations.append(terms[source_text])
        
        return translations
    
    def _fuzzy_search(self, 
                     text: str, 
                     memory_dict: Dict, 
                     threshold: float) -> List[Tuple[str, Dict, float]]:
        """
        Búsqueda fuzzy en memory dict.
        
        Args:
            text: Texto a buscar
            memory_dict: Dict de translation memory para idioma específico
            threshold: Umbral mínimo de similitud
        
        Returns:
            Lista de tuplas (texto_original, data, ratio_similitud)
        """
        matches = []
        
        for stored_text, data in memory_dict.items():
            # Calcular similitud usando SequenceMatcher
            ratio = difflib.SequenceMatcher(None, 
                                           text.lower(), 
                                           stored_text.lower()).ratio()
            
            if ratio >= threshold:
                matches.append((stored_text, data, ratio))
        
        # Ordenar por ratio DESC
        matches.sort(key=lambda x: x[2], reverse=True)
        
        return matches
    
    def save_translation(self, 
                        source_text: str, 
                        target_text: str, 
                        source_lang: str, 
                        target_lang: str,
                        confidence: float = 0.95):
        """
        Guardar nueva traducción en memory y persistir a JSON.
        
        Args:
            source_text: Texto origen
            target_text: Texto traducido
            source_lang: Idioma origen
            target_lang: Idioma destino
            confidence: Nivel de confianza (0.0-1.0)
        """
        key = f"{source_lang}-{target_lang}"
        
        if key not in self.memory:
            self.memory[key] = {}
        
        if source_text not in self.memory[key]:
            # Nueva entrada
            self.memory[key][source_text] = {
                "translations": [target_text],
                "count": 1,
                "confidence": confidence,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
        else:
            # Actualizar entrada existente
            entry = self.memory[key][source_text]
            
            # Añadir traducción si no existe
            if target_text not in entry["translations"]:
                entry["translations"].append(target_text)
            
            entry["count"] = entry.get("count", 0) + 1
            entry["updated_at"] = datetime.utcnow().isoformat()
            
            # Actualizar confidence (promedio ponderado)
            old_confidence = entry.get("confidence", 0.8)
            entry["confidence"] = (old_confidence + confidence) / 2
        
        # Persistir a archivo
        self._persist_memory()
    
    def _persist_memory(self):
        """Guardar translation memory a archivo JSON."""
        try:
            # Crear directorio si no existe
            self.memory_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.memory_path, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, ensure_ascii=False, indent=2)
        
        except Exception as e:
            print(f"Error persisting translation memory: {e}")
    
    def get_glossary(self, family: str, target_lang: str) -> Dict:
        """
        Obtener glosario completo para familia y idioma.
        
        Args:
            family: Familia de producto (COSMETICS_FACIAL, FOOD_PACKAGED, etc.)
            target_lang: Idioma destino (pt, it, en)
        
        Returns:
            Dict con términos y traducciones
        """
        family_normalized = family.lower().split("_")[0] if "_" in family else family.lower()
        
        if family_normalized not in self.glossaries:
            return {}
        
        if target_lang not in self.glossaries[family_normalized]:
            return {}
        
        return self.glossaries[family_normalized][target_lang]
    
    def export_memory_to_csv(self, output_path: str):
        """
        Exportar translation memory a CSV.
        
        Args:
            output_path: Ruta del archivo CSV de salida
        """
        import csv
        
        rows = []
        
        for lang_pair, translations in self.memory.items():
            source_lang, target_lang = lang_pair.split("-")
            
            for source_text, data in translations.items():
                for target_text in data["translations"]:
                    rows.append({
                        "source_lang": source_lang,
                        "target_lang": target_lang,
                        "source_text": source_text,
                        "target_text": target_text,
                        "count": data.get("count", 0),
                        "confidence": data.get("confidence", 0.0),
                        "created_at": data.get("created_at", ""),
                        "updated_at": data.get("updated_at", "")
                    })
        
        # Escribir CSV
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            if rows:
                fieldnames = rows[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
    
    def get_stats(self) -> Dict:
        """
        Obtener estadísticas del translation engine.
        
        Returns:
            Dict con estadísticas: total_pairs, total_translations, languages, etc.
        """
        total_pairs = len(self.memory)
        total_translations = sum(len(translations) for translations in self.memory.values())
        
        languages = set()
        for lang_pair in self.memory.keys():
            source, target = lang_pair.split("-")
            languages.add(source)
            languages.add(target)
        
        glossary_count = sum(
            len(langs) for langs in self.glossaries.values()
        )
        
        return {
            "total_language_pairs": total_pairs,
            "total_source_texts": total_translations,
            "languages_supported": sorted(list(languages)),
            "glossaries_loaded": glossary_count,
            "families_with_glossaries": list(self.glossaries.keys())
        }
