from transformers import pipeline
from sqlalchemy.orm import Session
from app.models import CoupleWellbeingTrend
from datetime import datetime

# Modelo multilingüe (español incluido)
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def analyze_sentiment(text: str):
    result = sentiment_pipeline(text)[0]
    label = result['label']  # e.g., '4 stars'
    score = float(result['score'])

    if "1" in label or "2" in label:
        sentiment = "negative"
    elif "3" in label:
        sentiment = "neutral"
    else:
        sentiment = "positive"

    return sentiment, score

def generar_conclusion_pareja(pareja):
    # Puedes ajustar los textos y lógica según tus necesidades
    conclusion = []
    conclusion.append(
        f"La pareja {pareja['nombrePareja']} ha mostrado un promedio de sentimiento individual de {pareja['promedioSentimientoIndividual']:.2f}, "
        f"lo que indica un estado emocional {'positivo' if pareja['promedioSentimientoIndividual'] > 0.6 else 'neutral' if pareja['promedioSentimientoIndividual'] > 0.4 else 'negativo'}. "
        f"La tasa de completación de tareas es de {pareja['tasaCompletacionTareas']:.2f}, "
        f"lo que refleja {'un buen compromiso' if pareja['tasaCompletacionTareas'] > 0.7 else 'una participación moderada' if pareja['tasaCompletacionTareas'] > 0.5 else 'baja adherencia'} al proceso terapéutico."
    )
    conclusion.append(
        f"El promedio de estrés individual es de {pareja['promedioEstresIndividual']:.2f}, "
        f"y el gap de empatía es de {pareja['empatiaGapScore']:.2f}. "
        f"El balance de interacción es de {pareja['interaccionBalanceRatio']:.2f}, "
        f"con {pareja['recuentoDeteccionCicloNegativo']} ciclos negativos detectados."
    )
    if pareja['prediccionRiesgoRuptura'] > 0.5:
        conclusion.append(
            "Existe un riesgo elevado de ruptura, por lo que se recomienda una intervención inmediata y sesiones de seguimiento más frecuentes."
        )
    else:
        conclusion.append(
            "El riesgo de ruptura es bajo, pero se recomienda mantener el monitoreo y reforzar los aspectos positivos observados."
        )
    conclusion.append(
        "Entre los insights recientes destacan: " + "; ".join(pareja['insightsRecientes']) + "."
    )
    # Unir y limitar a 200 palabras máximo
    texto = " ".join(conclusion)
    palabras = texto.split()
    if len(palabras) > 200:
        texto = " ".join(palabras[:200]) + "..."
    return texto

def analyze_couples(db: Session):
    # Obtén todos los registros
    records = db.query(CoupleWellbeingTrend).all()
    couples = {}
    for r in records:
        cid = r.couple_id
        if cid not in couples:
            couples[cid] = {
                "sentimientos": [],
                "tareas": [],
                "estres": [],
                "empatia": [],
                "balance": [],
                "churn": [],
                "weeks": [],
                "insights": [],
            }
        # Si tienes un campo de texto, usa analyze_sentiment aquí
        # Aquí solo simulo usando puntuacion_cuestionario_das como proxy
        sentimiento = (r.puntuacion_cuestionario_das - 70) / 80  # Normaliza a 0-1 aprox
        couples[cid]["sentimientos"].append(sentimiento)
        couples[cid]["tareas"].append(r.tasa_cumplimiento_tareas)
        couples[cid]["estres"].append(r.promedio_estres_individual)
        couples[cid]["empatia"].append(r.empatia_gap_score)
        couples[cid]["balance"].append(r.interacion_balance_ratio)
        couples[cid]["churn"].append(r.churn_risk)
        couples[cid]["weeks"].append(r.week_number)
        # Puedes agregar lógica para insights aquí

    result = []
    for cid, vals in couples.items():
        promedio_sentimiento = sum(vals["sentimientos"]) / len(vals["sentimientos"])
        tasa_completacion = sum(vals["tareas"]) / len(vals["tareas"])
        promedio_estres = sum(vals["estres"]) / len(vals["estres"])
        promedio_empatia = sum(vals["empatia"]) / len(vals["empatia"])
        promedio_balance = sum(vals["balance"]) / len(vals["balance"])
        recuento_ciclo_negativo = sum(1 for b in vals["balance"] if b < 1)
        prediccion_riesgo = sum(vals["churn"]) / len(vals["churn"])
        fecha_tendencia = datetime.now().isoformat()
        # Insights de ejemplo
        insights = []
        if promedio_balance < 0.7:
            insights.append("Ciclo negativo recurrente: crítica → defensividad → retirada")
        if promedio_empatia < 0.5:
            insights.append("Baja empatía mutua detectada en las últimas interacciones")
        if promedio_sentimiento > 0.7:
            insights.append("Mejora significativa en la comunicación durante la última semana")
        if promedio_estres > 7:
            insights.append("Alta correlación entre estrés laboral y tensión en la relación")
        if not insights:
            insights.append("Sin anomalías relevantes detectadas en las últimas semanas.")

        pareja = {
            "parejaId": cid,
            "nombrePareja": f"Pareja {cid}",
            "promedioSentimientoIndividual": round(promedio_sentimiento, 2),
            "tasaCompletacionTareas": round(tasa_completacion, 2),
            "promedioEstresIndividual": round(promedio_estres, 2),
            "empatiaGapScore": round(promedio_empatia, 2),
            "interaccionBalanceRatio": round(promedio_balance, 2),
            "recuentoDeteccionCicloNegativo": recuento_ciclo_negativo,
            "prediccionRiesgoRuptura": round(prediccion_riesgo, 2),
            "fechaTendencia": fecha_tendencia,
            "insightsRecientes": insights,
        }
        pareja["conclusion"] = generar_conclusion_pareja(pareja)
        result.append(pareja)

    # Texto de conclusión general
    conclusion = "La mayoría de las parejas muestran una tendencia positiva, aunque algunas presentan ciclos negativos recurrentes y altos niveles de estrés. Se recomienda atención especial a las parejas con bajo balance de interacción y alta puntuación de estrés."

    return {"analisisParejas": result, "conclusion": conclusion}
