class AffinityScorerAgent:
    """
    Calcula un score sencillo a partir de las features procesadas.
    """

    def score(self, features: dict) -> tuple[float, str]:
        overlap_ratio = features.get("skill_overlap_ratio", 0.0)
        years = features.get("years_experience", 0)

        # Fórmula muy simple para el sprint 2
        score = overlap_ratio * 70 + min(years, 10) * 3

        reason = (
            f"Coincidencia de habilidades: {overlap_ratio:.2f}. "
            f"Años de experiencia considerados: {years}."
        )
        return float(score), reason
