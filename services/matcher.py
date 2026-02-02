import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def semantic_match(
    sentencesA,
    sentencesB,
    embA,
    embB,
    threshold_low=0.65,
    threshold_high=0.85
):
    results_match = []
    results_no_match = []

    similarity_matrix = cosine_similarity(embA, embB)

    for idx_a, sims in enumerate(similarity_matrix):
        best_idx = int(np.argmax(sims))
        best_score = float(sims[best_idx])

        if best_score >= threshold_high:
            results_match.append({
                "pdfA": sentencesA[idx_a],
                "pdfB": sentencesB[best_idx],
                "similarity": round(best_score, 3),
                "type": "strong_match"
            })

        elif best_score >= threshold_low:
            results_match.append({
                "pdfA": sentencesA[idx_a],
                "pdfB": sentencesB[best_idx],
                "similarity": round(best_score, 3),
                "type": "paraphrase_or_related"
            })

        else:
            results_no_match.append({
                "pdfA": sentencesA[idx_a],
                "reason": "No semantic equivalent found in PDF B"
            })

    return {
        "match": results_match,
        "no_match": results_no_match
    }
